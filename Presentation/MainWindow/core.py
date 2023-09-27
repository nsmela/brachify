from PyQt5.QtWidgets import QMainWindow
from Presentation.MainWindow.ui_functions import UIFunctions

from Presentation.MainWindow.ui_main import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ## TOGGLE/BURGUER MENU
        ########################################################################
        self.ui.Btn_Toggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 250, True))
        self.ui.btn_page_1.setCheckable(True)
        self.ui.btn_page_2.setCheckable(True)
        self.ui.btn_page_3.setCheckable(True)

        ## PAGES
        ########################################################################

        # PAGE 1
        self.ui.btn_page_1.clicked.connect(lambda: UIFunctions.setPage(self, 0))

        # PAGE 2
        self.ui.btn_page_2.clicked.connect(lambda: UIFunctions.setPage(self, 1))

        # PAGE 3
        self.ui.btn_page_3.clicked.connect(lambda: UIFunctions.setPage(self, 2))