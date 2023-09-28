################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
################################################################################
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore

## ==> GUI FILE
from Presentation.MainDisplay.core import Display


class UIFunctions(Display):

    def toggleMenu(self, maxWidth, enable):
        if enable:

            # GET WIDTH
            width = self.ui.frame_left_menu.width()
            maxExtend = maxWidth
            standard = 80

            # SET MAX WIDTH
            if width == 80:
                widthExtended = maxExtend
            else:
                widthExtended = standard

            # ANIMATION
            self.animation = QtCore.QPropertyAnimation(self.ui.frame_left_menu, b"minimumWidth")
            self.animation.setDuration(200)
            self.animation.setStartValue(width)
            self.animation.setEndValue(widthExtended)
            self.animation.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.animation.start()

    def setPage(self, index: int):
        stylesheet = "QPushButton{background-color: lightgreen;}"
        self.ui.btn_page_1.setChecked(False)
        self.ui.btn_page_1.setStyleSheet("")

        self.ui.btn_page_2.setChecked(False)
        self.ui.btn_page_2.setStyleSheet("")

        self.ui.btn_page_3.setChecked(False)
        self.ui.btn_page_3.setStyleSheet("")

        if index == 0:
            self.ui.btn_page_1.setChecked(True)
            self.ui.btn_page_1.setStyleSheet(stylesheet)
        elif index == 1:
            self.ui.btn_page_2.setChecked(True)
            self.ui.btn_page_2.setStyleSheet(stylesheet)
        elif index == 2:
            self.ui.btn_page_3.setChecked(True)
            self.ui.btn_page_3.setStyleSheet(stylesheet)

        self.ui.stackedWidget.setCurrentIndex(index)
