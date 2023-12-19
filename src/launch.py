from PySide6.QtWidgets import QApplication

import sys

from classes import info


app = None


def main():
    global app

    # parse command-line arguements
    # process arguements

    print(f"Loaded modules from: {info.DIR_PATH}")

    from classes.app import RadiotherapyApp

    argv = [sys.argv[0]]

    try:
        app = RadiotherapyApp(argv)
    except Exception:
        # TODO show errors from within app
        print("Radiotherapy App failed to load!")
        input("Press enter key to continue...")

    app.setApplicationName(info.APP_NAME)
    app.setApplicationVersion(info.APP_VERSION)

    # launch GUI
    if app.gui():

        # close the splash screen if any
        try:
            import pyi_splash
            pyi_splash.close()
            app.window.activateWindow()
        except:
            pass

        sys.exit(app.exec())


if __name__ == "__main__":
    main()
