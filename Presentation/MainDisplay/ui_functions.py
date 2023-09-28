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
        oldStyle = self.button_style
        stylesheet = "QPushButton{background-color: rgb(85, 170, 255);}"
        self.ui.btn_page_1.setStyleSheet(oldStyle)
        self.ui.btn_page_2.setStyleSheet(oldStyle)
        self.ui.btn_page_3.setStyleSheet(oldStyle)
        self.ui.btn_page_4.setStyleSheet(oldStyle)
        self.ui.btn_page_5.setStyleSheet(oldStyle)
        
        if index == 0:
            self.ui.btn_page_1.setStyleSheet(stylesheet)
        elif index == 1:
            self.ui.btn_page_2.setStyleSheet(stylesheet)
        elif index == 2:
            self.ui.btn_page_3.setStyleSheet(stylesheet)
        elif index == 3:
            self.ui.btn_page_4.setStyleSheet(stylesheet)
        elif index == 4:
            self.ui.btn_page_5.setStyleSheet(stylesheet)

        self.ui.stackedWidget.setCurrentIndex(index)
