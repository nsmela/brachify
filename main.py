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

# resizing to force the display window to correctly scale
# size = [window.size().width(), window.size().height()]
# window.show()
# window.resize(size[0] + 1, size[1] + 1)
window.showProperly()

splash.finish(window)
sys.exit(app.exec_())
