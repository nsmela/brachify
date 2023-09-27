################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow, QGraphicsDropShadowEffect

# GUI FILE
from Presentation.MainWindow.core import MainWindow

# IMPORT FUNCTIONS
from Presentation.MainWindow.ui_functions import *
from Presentation.SplashScreen.ui_splash_interface import Ui_SplashScreen

counter = 0


class SplashScreen(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_SplashScreen()
        self.ui.setupUi(self)

        # Remove window dressing

        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # drop shadow effect
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        # start
        global counter
        self.ui.progressBar.setValue(counter)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.setInterval(35)
        self.timer.start()

        # load window in advance
        self.main = MainWindow()

        self.show()

    def progress(self):
        global counter
        counter += 1
        print(f"Counter: {counter}")

        # set value to progress bar
        self.ui.progressBar.setValue(counter)
        # if done
        if counter > 100:
            self.timer.stop()

            # show main window
            self.main.show()

            # close splash screen
            self.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec_())
