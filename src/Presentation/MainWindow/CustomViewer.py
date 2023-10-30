import logging
import os
import sys

from OCC.Core.AIS import AIS_Manipulator
from OCC.Core.gp import gp_Trsf
from OCC.Display import OCCViewer

from PySide6 import QtCore, QtGui, QtWidgets, QtOpenGL

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)

class qtBaseViewer(QtWidgets.QWidget):
    """The base Qt Widget for an OCC viewer"""

    def __init__(self, parent=None):
        super(qtBaseViewer, self).__init__(parent)
        self._display = OCCViewer.Viewer3d()
        self._inited = False

        # enable Mouse Tracking
        self.setMouseTracking(True)

        # Strong focus
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.WheelFocus)

        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_NativeWindow)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_PaintOnScreen)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_NoSystemBackground)

        self.setAutoFillBackground(False)

    def resizeEvent(self, event):
        super(qtBaseViewer, self).resizeEvent(event)
        self._display.View.MustBeResized()

    def paintEngine(self):
        return None

class OrbitCameraViewer3d(qtBaseViewer):
    # emit signal when selection is changed
    # is a list of TopoDS_*
    if hasattr(QtCore, "pyqtSignal"):  # PyQt5
        sig_topods_selected = QtCore.pyqtSignal(list)
    elif hasattr(QtCore, "Signal"):  # PySide2
        sig_topods_selected = QtCore.Signal(list)
    else:
        raise IOError("no signal")

    def __init__(self, *kargs):
        qtBaseViewer.__init__(self, *kargs)

        self.setObjectName("qt_viewer_3d")

        self._drawbox = False
        self._zoom_area = False
        self._select_area = False
        self._inited = False
        self._leftisdown = False
        self._middleisdown = False
        self._rightisdown = False
        self._selection = None
        self._drawtext = True
        self._qApp = QtWidgets.QApplication.instance()
        self._key_map = {}
        self._current_cursor = "arrow"
        self._available_cursors = {}

    @property
    def qApp(self):
        # reference to QApplication instance
        return self._qApp

    @qApp.setter
    def qApp(self, value):
        self._qApp = value

    def InitDriver(self):
        self._display.Create(window_handle=int(self.winId()), parent=self)
        # background gradient
        self._display.SetModeShaded()
        self._inited = True
        # dict mapping keys to functions
        self._key_map = {
            ord("W"): self._display.SetModeWireFrame,
            ord("S"): self._display.SetModeShaded,
            ord("A"): self._display.EnableAntiAliasing,
            ord("B"): self._display.DisableAntiAliasing,
            ord("H"): self._display.SetModeHLR,
            ord("F"): self._display.FitAll,
            ord("G"): self._display.SetSelectionMode,
        }
        self.createCursors()

    def createCursors(self):
        module_pth = os.path.abspath(os.path.dirname(__file__))
        icon_pth = os.path.join(module_pth, "icons")

        _CURSOR_PIX_ROT = QtGui.QPixmap(os.path.join(icon_pth, "cursor-rotate.png"))
        _CURSOR_PIX_PAN = QtGui.QPixmap(os.path.join(icon_pth, "cursor-pan.png"))
        _CURSOR_PIX_ZOOM = QtGui.QPixmap(os.path.join(icon_pth, "cursor-magnify.png"))
        _CURSOR_PIX_ZOOM_AREA = QtGui.QPixmap(
            os.path.join(icon_pth, "cursor-magnify-area.png")
        )

        self._available_cursors = {
            "arrow": QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor),  # default
            "pan": QtGui.QCursor(_CURSOR_PIX_PAN),
            "rotate": QtGui.QCursor(_CURSOR_PIX_ROT),
            "zoom": QtGui.QCursor(_CURSOR_PIX_ZOOM),
            "zoom-area": QtGui.QCursor(_CURSOR_PIX_ZOOM_AREA),
        }

        self._current_cursor = "arrow"

    def keyPressEvent(self, event):
        super(OrbitCameraViewer3d, self).keyPressEvent(event)
        code = event.key()
        if code in self._key_map:
            self._key_map[code]()
        elif code in range(256):
            log.info(
                'key: "%s"(code %i) not mapped to any function' % (chr(code), code)
            )
        else:
            log.info("key: code %i not mapped to any function" % code)

    def focusInEvent(self, event):
        if self._inited:
            self._display.Repaint()

    def focusOutEvent(self, event):
        if self._inited:
            self._display.Repaint()

    def paintEvent(self, event):
        if not self._inited:
            self.InitDriver()

        self._display.Context.UpdateCurrentViewer()

        if self._drawbox:
            painter = QtGui.QPainter(self)
            painter.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0), 2))
            rect = QtCore.QRect(*self._drawbox)
            painter.drawRect(rect)

    def wheelEvent(self, event):
        delta = event.angleDelta().y()
        zoom_factor = 2.0 if delta > 0 else 0.5
        self._display.ZoomFactor(zoom_factor)

    @property
    def cursor(self):
        return self._current_cursor

    @cursor.setter
    def cursor(self, value):
        if self._current_cursor != value:
            self._current_cursor = value
            if cursor := self._available_cursors.get(value):
                self.qApp.setOverrideCursor(cursor)
            else:
                self.qApp.restoreOverrideCursor()

    def mousePressEvent(self, event):
        self.setFocus()
        ev = event.pos()
        self.dragStartPosX = ev.x()
        self.dragStartPosY = ev.y()
        self._display.StartRotation(self.dragStartPosX, self.dragStartPosY)

    def mouseReleaseEvent(self, event):
        pt = event.pos()
        modifiers = event.modifiers()

        if event.button() == QtCore.Qt.LeftButton:
            # single select otherwise
            self._display.Select(pt.x(), pt.y())

            if self._display.selected_shapes is not None:
                self.sig_topods_selected.emit(self._display.selected_shapes)

        elif event.button() == QtCore.Qt.RightButton:
            pass

        self.cursor = "arrow"

    def DrawBox(self, event):
        tolerance = 2
        pt = event.pos()
        dx = pt.x() - self.dragStartPosX
        dy = pt.y() - self.dragStartPosY
        if abs(dx) <= tolerance and abs(dy) <= tolerance:
            return
        self._drawbox = [self.dragStartPosX, self.dragStartPosY, dx, dy]

    def mouseMoveEvent(self, evt):
        pt = evt.pos()
        # buttons = int(evt.buttons())
        buttons = evt.buttons()
        modifiers = evt.modifiers()
        # ROTATE
        if buttons == QtCore.Qt.RightButton:
            self.cursor = "rotate"
            self._display.Rotation(pt.x(), pt.y())
            self._drawbox = False
        elif buttons == QtCore.Qt.MiddleButton:
            dx = pt.x() - self.dragStartPosX
            dy = pt.y() - self.dragStartPosY
            self.dragStartPosX = pt.x()
            self.dragStartPosY = pt.y()
            self.cursor = "pan"
            self._display.Pan(dx, -dy)
            self._drawbox = False
        else:
            self._drawbox = False
            self._display.MoveTo(pt.x(), pt.y())
            self.cursor = "arrow"