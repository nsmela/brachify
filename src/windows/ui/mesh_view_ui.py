# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mesh_view.ui'
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

class Ui_Mesh_View(object):
    def setupUi(self, Mesh_View):
        if not Mesh_View.objectName():
            Mesh_View.setObjectName(u"Mesh_View")
        Mesh_View.resize(240, 400)
        self.verticalLayout = QVBoxLayout(Mesh_View)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_title = QLabel(Mesh_View)
        self.label_title.setObjectName(u"label_title")
        font = QFont()
        font.setPointSize(32)
        self.label_title.setFont(font)

        self.verticalLayout.addWidget(self.label_title)

        self.btn_import_mesh = QPushButton(Mesh_View)
        self.btn_import_mesh.setObjectName(u"btn_import_mesh")

        self.verticalLayout.addWidget(self.btn_import_mesh)

        self.label_mesh_info = QLabel(Mesh_View)
        self.label_mesh_info.setObjectName(u"label_mesh_info")

        self.verticalLayout.addWidget(self.label_mesh_info)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Mesh_View)

        QMetaObject.connectSlotsByName(Mesh_View)
    # setupUi

    def retranslateUi(self, Mesh_View):
        Mesh_View.setWindowTitle(QCoreApplication.translate("Mesh_View", u"Form", None))
        self.label_title.setText(QCoreApplication.translate("Mesh_View", u"mesh", None))
        self.btn_import_mesh.setText(QCoreApplication.translate("Mesh_View", u"import mesh", None))
        self.label_mesh_info.setText(QCoreApplication.translate("Mesh_View", u"No model(s) loaded", None))
    # retranslateUi

