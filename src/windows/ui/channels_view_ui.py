# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'channels_view.ui'
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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QFormLayout, QGroupBox,
    QLabel, QListWidget, QListWidgetItem, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_Channels_View(object):
    def setupUi(self, Channels_View):
        if not Channels_View.objectName():
            Channels_View.setObjectName(u"Channels_View")
        Channels_View.resize(240, 356)
        self.formLayout = QFormLayout(Channels_View)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(2, 2, 2, 2)
        self.label_title = QLabel(Channels_View)
        self.label_title.setObjectName(u"label_title")
        font = QFont()
        font.setPointSize(32)
        self.label_title.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_title)

        self.label = QLabel(Channels_View)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.spinbox_diameter = QDoubleSpinBox(Channels_View)
        self.spinbox_diameter.setObjectName(u"spinbox_diameter")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.spinbox_diameter)

        self.label_2 = QLabel(Channels_View)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)

        self.listwidget_channels = QListWidget(Channels_View)
        self.listwidget_channels.setObjectName(u"listwidget_channels")

        self.formLayout.setWidget(3, QFormLayout.SpanningRole, self.listwidget_channels)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.formLayout.setItem(6, QFormLayout.LabelRole, self.verticalSpacer)

        self.groupBox = QGroupBox(Channels_View)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout = QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout.addWidget(self.label_4)

        self.pushButton = QPushButton(self.groupBox)
        self.pushButton.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.groupBox)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.verticalLayout.addWidget(self.pushButton_2)


        self.formLayout.setWidget(4, QFormLayout.SpanningRole, self.groupBox)

#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.spinbox_diameter)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(Channels_View)

        QMetaObject.connectSlotsByName(Channels_View)
    # setupUi

    def retranslateUi(self, Channels_View):
        Channels_View.setWindowTitle(QCoreApplication.translate("Channels_View", u"Form", None))
        self.label_title.setText(QCoreApplication.translate("Channels_View", u"channels", None))
        self.label.setText(QCoreApplication.translate("Channels_View", u"channels diameter", None))
        self.label_2.setText(QCoreApplication.translate("Channels_View", u"Channels", None))
        self.groupBox.setTitle(QCoreApplication.translate("Channels_View", u"Channel Details", None))
        self.label_4.setText(QCoreApplication.translate("Channels_View", u"Points:", None))
        self.pushButton.setText(QCoreApplication.translate("Channels_View", u"Hide", None))
        self.pushButton_2.setText(QCoreApplication.translate("Channels_View", u"Set as Tandem", None))
    # retranslateUi

