# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QGridLayout, QHBoxLayout, QMainWindow,
    QPushButton, QSizePolicy, QSpacerItem, QStackedWidget,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(882, 687)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.top_menu_bar = QWidget(self.centralwidget)
        self.top_menu_bar.setObjectName(u"top_menu_bar")
        self.top_menu_bar.setMinimumSize(QSize(0, 64))
        self.top_menu_bar.setMaximumSize(QSize(16777215, 64))
        self.horizontalLayout = QHBoxLayout(self.top_menu_bar)
        self.horizontalLayout.setSpacing(1)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.btn_import_view = QPushButton(self.top_menu_bar)
        self.btn_import_view.setObjectName(u"btn_import_view")
        self.btn_import_view.setMinimumSize(QSize(80, 0))
        self.btn_import_view.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout.addWidget(self.btn_import_view)

        self.btn_cylinder_view = QPushButton(self.top_menu_bar)
        self.btn_cylinder_view.setObjectName(u"btn_cylinder_view")

        self.horizontalLayout.addWidget(self.btn_cylinder_view)

        self.btn_channels_view = QPushButton(self.top_menu_bar)
        self.btn_channels_view.setObjectName(u"btn_channels_view")
        self.btn_channels_view.setMinimumSize(QSize(80, 0))
        self.btn_channels_view.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout.addWidget(self.btn_channels_view)

        self.btn_tandem_view = QPushButton(self.top_menu_bar)
        self.btn_tandem_view.setObjectName(u"btn_tandem_view")

        self.horizontalLayout.addWidget(self.btn_tandem_view)

        self.btn_export_view = QPushButton(self.top_menu_bar)
        self.btn_export_view.setObjectName(u"btn_export_view")

        self.horizontalLayout.addWidget(self.btn_export_view)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer_2)


        self.verticalLayout_5.addWidget(self.top_menu_bar)

        self.bodywidget = QWidget(self.centralwidget)
        self.bodywidget.setObjectName(u"bodywidget")
        self.horizontalLayout_2 = QHBoxLayout(self.bodywidget)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.left_menu_bar = QWidget(self.bodywidget)
        self.left_menu_bar.setObjectName(u"left_menu_bar")
        self.left_menu_bar.setMinimumSize(QSize(240, 0))
        self.left_menu_bar.setMaximumSize(QSize(240, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.left_menu_bar)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.viewswidget = QStackedWidget(self.left_menu_bar)
        self.viewswidget.setObjectName(u"viewswidget")
        self.page_import = QWidget()
        self.page_import.setObjectName(u"page_import")
        self.verticalLayout_7 = QVBoxLayout(self.page_import)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.viewswidget.addWidget(self.page_import)
        self.page_cylinder = QWidget()
        self.page_cylinder.setObjectName(u"page_cylinder")
        self.verticalLayout = QVBoxLayout(self.page_cylinder)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.viewswidget.addWidget(self.page_cylinder)
        self.page_channels = QWidget()
        self.page_channels.setObjectName(u"page_channels")
        self.verticalLayout_3 = QVBoxLayout(self.page_channels)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.viewswidget.addWidget(self.page_channels)
        self.page_tandem = QWidget()
        self.page_tandem.setObjectName(u"page_tandem")
        self.verticalLayout_4 = QVBoxLayout(self.page_tandem)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.viewswidget.addWidget(self.page_tandem)
        self.page_export = QWidget()
        self.page_export.setObjectName(u"page_export")
        self.verticalLayout_8 = QVBoxLayout(self.page_export)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.viewswidget.addWidget(self.page_export)

        self.verticalLayout_2.addWidget(self.viewswidget)


        self.horizontalLayout_2.addWidget(self.left_menu_bar)

        self.display_view_widget = QWidget(self.bodywidget)
        self.display_view_widget.setObjectName(u"display_view_widget")
        self.display_view_widget.setMinimumSize(QSize(600, 540))
        self.gridLayout = QGridLayout(self.display_view_widget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout_2.addWidget(self.display_view_widget)


        self.verticalLayout_5.addWidget(self.bodywidget)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.viewswidget.setCurrentIndex(4)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"brachify", None))
        self.btn_import_view.setText(QCoreApplication.translate("MainWindow", u"import", None))
        self.btn_cylinder_view.setText(QCoreApplication.translate("MainWindow", u"cylinder", None))
        self.btn_channels_view.setText(QCoreApplication.translate("MainWindow", u"channels", None))
        self.btn_tandem_view.setText(QCoreApplication.translate("MainWindow", u"tandem", None))
        self.btn_export_view.setText(QCoreApplication.translate("MainWindow", u"export", None))
    # retranslateUi

