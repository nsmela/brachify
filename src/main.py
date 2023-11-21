import os
import sys 

SPLASHSCREEN_IMAGE = "src//Presentation//SplashScreen//brachify_splash.png"


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS2
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


if __name__ == "__main__":
    print("beginning brachify")
    from PySide6.QtWidgets import QApplication, QSplashScreen
    from PySide6.QtGui import QPixmap
    app = QApplication(sys.argv)  # pass console arguements to the app
    pixmap = QPixmap(SPLASHSCREEN_IMAGE)
    splash = QSplashScreen(pixmap)
    splash.show()

    from Presentation.MainWindow.core import MainWindow
    window = MainWindow()

    window.showProperly()

    splash.finish(window)
    sys.exit(app.exec())