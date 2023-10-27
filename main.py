# PyQt5 SplashScreen
# https://youtu.be/TsatZJfzb_Q?si=HZ1nt1eqw0AyuYWo
import os

from Presentation.SplashScreen.core import SplashScreen
from PySide6 import QtWidgets
import sys

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS2
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

app = QtWidgets.QApplication(sys.argv)
splash = SplashScreen()
splash.show()

from Presentation.MainWindow.core import MainWindow
window = MainWindow()

window.showProperly()

splash.finish(window)
sys.exit(app.exec_())
