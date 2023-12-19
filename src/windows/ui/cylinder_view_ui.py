# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cylinder_view.ui'
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
    QLabel, QPushButton, QSizePolicy, QSpacerItem,
    QSpinBox, QWidget)

class Ui_Cylinder_View(object):
    def setupUi(self, Cylinder_View):
        if not Cylinder_View.objectName():
            Cylinder_View.setObjectName(u"Cylinder_View")
        Cylinder_View.resize(240, 356)
        self.formLayout = QFormLayout(Cylinder_View)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 6, 0)
        self.label_title = QLabel(Cylinder_View)
        self.label_title.setObjectName(u"label_title")
        font = QFont()
        font.setPointSize(32)
        self.label_title.setFont(font)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_title)

        self.label = QLabel(Cylinder_View)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.spinbox_diameter = QDoubleSpinBox(Cylinder_View)
        self.spinbox_diameter.setObjectName(u"spinbox_diameter")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.spinbox_diameter)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.formLayout.setItem(7, QFormLayout.LabelRole, self.verticalSpacer)

        self.btn_apply_settings = QPushButton(Cylinder_View)
        self.btn_apply_settings.setObjectName(u"btn_apply_settings")

        self.formLayout.setWidget(6, QFormLayout.SpanningRole, self.btn_apply_settings)

        self.label_3 = QLabel(Cylinder_View)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_3)

        self.cb_add_base = QCheckBox(Cylinder_View)
        self.cb_add_base.setObjectName(u"cb_add_base")
        self.cb_add_base.setLayoutDirection(Qt.RightToLeft)
        self.cb_add_base.setIconSize(QSize(16, 16))

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.cb_add_base)

        self.label_2 = QLabel(Cylinder_View)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)

        self.spinbox_length = QSpinBox(Cylinder_View)
        self.spinbox_length.setObjectName(u"spinbox_length")
        self.spinbox_length.setMinimumSize(QSize(0, 0))
        self.spinbox_length.setMinimum(60)
        self.spinbox_length.setMaximum(300)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.spinbox_length)

#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.spinbox_diameter)
        self.label_3.setBuddy(self.cb_add_base)
        self.label_2.setBuddy(self.spinbox_length)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(Cylinder_View)

        QMetaObject.connectSlotsByName(Cylinder_View)
    # setupUi

    def retranslateUi(self, Cylinder_View):
        Cylinder_View.setWindowTitle(QCoreApplication.translate("Cylinder_View", u"Form", None))
        self.label_title.setText(QCoreApplication.translate("Cylinder_View", u"cylinder", None))
        self.label.setText(QCoreApplication.translate("Cylinder_View", u"cylinder diameter", None))
        self.btn_apply_settings.setText(QCoreApplication.translate("Cylinder_View", u"apply settings", None))
        self.label_3.setText(QCoreApplication.translate("Cylinder_View", u"add base", None))
        self.cb_add_base.setText("")
        self.label_2.setText(QCoreApplication.translate("Cylinder_View", u"cylinder length", None))
        self.spinbox_length.setSuffix(QCoreApplication.translate("Cylinder_View", u" mm", None))
    # retranslateUi

