# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'export_view.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QFormLayout,
    QGroupBox, QLabel, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_Export_View(object):
    def setupUi(self, Export_View):
        if not Export_View.objectName():
            Export_View.setObjectName(u"Export_View")
        Export_View.resize(240, 400)
        self.verticalLayout = QVBoxLayout(Export_View)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.label_title = QLabel(Export_View)
        self.label_title.setObjectName(u"label_title")
        font = QFont()
        font.setPointSize(32)
        self.label_title.setFont(font)

        self.verticalLayout.addWidget(self.label_title)

        self.groupBox_3 = QGroupBox(Export_View)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.formLayout_2 = QFormLayout(self.groupBox_3)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setObjectName(u"label_2")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.cb_tandem_shown = QCheckBox(self.groupBox_3)
        self.cb_tandem_shown.setObjectName(u"cb_tandem_shown")
        self.cb_tandem_shown.setLayoutDirection(Qt.RightToLeft)
        self.cb_tandem_shown.setChecked(False)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.cb_tandem_shown)


        self.verticalLayout.addWidget(self.groupBox_3)

        self.groupBox = QGroupBox(Export_View)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_2 = QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.btn_export_mesh = QPushButton(self.groupBox)
        self.btn_export_mesh.setObjectName(u"btn_export_mesh")

        self.verticalLayout_2.addWidget(self.btn_export_mesh)

        self.btn_export_shapes = QPushButton(self.groupBox)
        self.btn_export_shapes.setObjectName(u"btn_export_shapes")

        self.verticalLayout_2.addWidget(self.btn_export_shapes)


        self.verticalLayout.addWidget(self.groupBox)

        self.groupBox_2 = QGroupBox(Export_View)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.formLayout = QFormLayout(self.groupBox_2)
        self.formLayout.setObjectName(u"formLayout")
        self.label = QLabel(self.groupBox_2)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.sb_needle_length = QDoubleSpinBox(self.groupBox_2)
        self.sb_needle_length.setObjectName(u"sb_needle_length")
        self.sb_needle_length.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.sb_needle_length.setMaximum(350.000000000000000)

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.sb_needle_length)

        self.btn_export_template_reference = QPushButton(self.groupBox_2)
        self.btn_export_template_reference.setObjectName(u"btn_export_template_reference")

        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.btn_export_template_reference)


        self.verticalLayout.addWidget(self.groupBox_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.retranslateUi(Export_View)

        QMetaObject.connectSlotsByName(Export_View)
    # setupUi

    def retranslateUi(self, Export_View):
        Export_View.setWindowTitle(QCoreApplication.translate("Export_View", u"Form", None))
        self.label_title.setText(QCoreApplication.translate("Export_View", u"export", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("Export_View", u"Options", None))
        self.label_2.setText(QCoreApplication.translate("Export_View", u"Show Tandem", None))
        self.cb_tandem_shown.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("Export_View", u"Models", None))
        self.btn_export_mesh.setText(QCoreApplication.translate("Export_View", u"export mesh", None))
        self.btn_export_shapes.setText(QCoreApplication.translate("Export_View", u"export shape(s)", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("Export_View", u"Documents", None))
        self.label.setText(QCoreApplication.translate("Export_View", u"needle length", None))
        self.sb_needle_length.setSuffix(QCoreApplication.translate("Export_View", u" mm", None))
        self.btn_export_template_reference.setText(QCoreApplication.translate("Export_View", u"export template reference sheet", None))
    # retranslateUi

