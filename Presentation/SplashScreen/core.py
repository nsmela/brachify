from PyQt5 import QtWidgets, QtCore
from PyQt5 import QtGui
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect, QSplashScreen

# GUI FILE


# IMPORT FUNCTIONS
from Presentation.SplashScreen.ui_splash import Ui_SplashScreen

counter = 0


class SplashScreen(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__()
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

        # centre screen
        qr = self.frameGeometry()
        centre_point = QtGui.QGuiApplication.primaryScreen().availableGeometry().center()
        qr.moveCenter(centre_point)
        self.move(qr.topLeft())
        
        # start
        global counter
        self.ui.progressBar.setValue(counter)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        self.timer.setInterval(35)
        self.timer.start()

        self.show()

    def progress(self):
        global counter
        counter += 1

        # set value to progress bar
        self.ui.progressBar.setValue(counter)
        # if done
        if counter > 100:
            self.timer.stop()

            # close splash screen
            self.close()