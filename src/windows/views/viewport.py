from OCC.Display import OCCViewer
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB

from PySide6 import QtCore, QtGui, QtWidgets

from classes.app import get_app
from classes.logger import log
from windows.models.shape_model import ShapeModel

class qtBaseViewer(QtWidgets.QWidget):
    """The base Qt Widget for an OCC viewer"""

    def __init__(self, parent=None):
        super(qtBaseViewer, self).__init__(parent)
        self._display = OCCViewer.Viewer3d()

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


# ref   https://github.com/tpaviot/pythonocc-core/blob/master/src/Display/OCCViewer.py
#       https://github.com/tpaviot/pythonocc-core/blob/master/src/Display/qtDisplay.py
class OrbitCameraViewer3d(qtBaseViewer):
    # emit signal when selection is changed
    # is a list of TopoDS_*
    sig_topods_selected = QtCore.Signal(list)

    def update_display(self, shapes: list, resize: bool = True):
        # clear all the shapes
        self._display.Context.RemoveAll(True)

        loggedinfo = "shapes: "
        for shape in shapes:
            loggedinfo += f"\nShape: {shape.label}, rgb: {shape.rgb}"
            colour = Quantity_Color(
                shape.rgb[0], shape.rgb[1], shape.rgb[2], Quantity_TOC_RGB)
            self._display.DisplayShape(shape.shape, color=colour, update=False)

        self._display.Repaint()
        # set the grid model

        # resize
        if resize: self._display.FitAll()
        log.info(loggedinfo)

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
        self._qApp = get_app()
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

    def keyPressEvent(self, event):
        code = event.key()
        if code in self._key_map:
            self._key_map[code]()
        elif code in range(256):
            pass

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
