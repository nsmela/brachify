
from PySide6.QtWidgets import QApplication

from classes.signals import AppSignals


def get_app():
    """ Returns the current QApplication instance """
    return QApplication.instance()


class RadiotherapyApp(QApplication):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.args = super().arguments()
        self.errors = []
        self.signals = AppSignals()

        try:
            from classes.info import APP_NAME, DIR_PATH
            from classes.logger import log
            log.info(f"Starting {APP_NAME}")

        except ImportError as error_message:
            print(f"logging module unable to import! \n{error_message}")
            raise

        except Exception as error_message:
            print(f"Unable to start logging. \n{error_message}")
            raise

        self.path = DIR_PATH

    def gui(self):
        """
        Initialize the GUI and the Main Window
        :return: bool: True if the GUI has no errors, False if initialization fails
        """

        try:
            from windows.main_window import MainWindow
            self.window = MainWindow()

            # TODO process args like autoloading a file or project

            return True
        
        except Exception as error_message:
            from classes.logger import log
            log.critical(f"Main window start failed: {error_message}")
            return False

