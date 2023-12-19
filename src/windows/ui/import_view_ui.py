# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'import_view.ui'
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
from PySide6.QtWidgets import (QApplication, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Import_View(object):
    def setupUi(self, Import_View):
        if not Import_View.objectName():
            Import_View.setObjectName(u"Import_View")
        Import_View.resize(240, 400)
        self.verticalLayout = QVBoxLayout(Import_View)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_title = QLabel(Import_View)
        self.label_title.setObjectName(u"label_title")
        font = QFont()
        font.setPointSize(32)
        self.label_title.setFont(font)

        self.verticalLayout.addWidget(self.label_title)

        self.btn_import_folder = QPushButton(Import_View)
        self.btn_import_folder.setObjectName(u"btn_import_folder")

        self.verticalLayout.addWidget(self.btn_import_folder)

        self.label_file_info = QLabel(Import_View)
        self.label_file_info.setObjectName(u"label_file_info")

        self.verticalLayout.addWidget(self.label_file_info)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Import_View)

        QMetaObject.connectSlotsByName(Import_View)
    # setupUi

    def retranslateUi(self, Import_View):
        Import_View.setWindowTitle(QCoreApplication.translate("Import_View", u"Form", None))
        self.label_title.setText(QCoreApplication.translate("Import_View", u"import files", None))
        self.btn_import_folder.setText(QCoreApplication.translate("Import_View", u"import dicom folder", None))
        self.label_file_info.setText(QCoreApplication.translate("Import_View", u"No model(s) loaded", None))
    # retranslateUi

