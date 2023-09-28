from PyQt5.QtWidgets import QMainWindow
from Presentation.MainDisplay.ui_main import Ui_MainWindow

class Display(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        ## TOGGLE/BURGUER MENU
        ########################################################################
        self.ui.Btn_Toggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 250, True))
        self.button_style = self.ui.btn_page_1.styleSheet()
        
        ## PAGES
        ########################################################################
        from Presentation.MainDisplay.ui_functions import UIFunctions
        # PAGE 1
        self.ui.btn_page_1.clicked.connect(lambda: UIFunctions.setPage(self, 0))

        # PAGE 2
        self.ui.btn_page_2.clicked.connect(lambda: UIFunctions.setPage(self, 1))

        # PAGE 3
        self.ui.btn_page_3.clicked.connect(lambda: UIFunctions.setPage(self, 2))
        
        # PAGE 4
        self.ui.btn_page_4.clicked.connect(lambda: UIFunctions.setPage(self, 3))
        
        # PAGE 5
        self.ui.btn_page_5.clicked.connect(lambda: UIFunctions.setPage(self, 4))