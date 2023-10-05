# PyQt5 SplashScreen
# https://youtu.be/TsatZJfzb_Q?si=HZ1nt1eqw0AyuYWo

from Presentation.SplashScreen.core import SplashScreen
from PyQt5 import QtWidgets
import sys

app = QtWidgets.QApplication(sys.argv)
splash = SplashScreen()
splash.show()

from Presentation.MainWindow.core import MainWindow
window = MainWindow()

window.showProperly()

splash.finish(window)
sys.exit(app.exec_())
