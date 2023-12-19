# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tandem_view.ui'
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
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QFormLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_Tandem_View(object):
    def setupUi(self, Tandem_View):
        if not Tandem_View.objectName():
            Tandem_View.setObjectName(u"Tandem_View")
        Tandem_View.resize(230, 356)
        self.verticalLayout = QVBoxLayout(Tandem_View)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label_title = QLabel(Tandem_View)
        self.label_title.setObjectName(u"label_title")
        font = QFont()
        font.setPointSize(32)
        self.label_title.setFont(font)

        self.verticalLayout.addWidget(self.label_title)

        self.tabWidget = QTabWidget(Tandem_View)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tab_import = QWidget()
        self.tab_import.setObjectName(u"tab_import")
        self.formLayout_2 = QFormLayout(self.tab_import)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.label_6 = QLabel(self.tab_import)
        self.label_6.setObjectName(u"label_6")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.label_6)

        self.sb_height_offset = QDoubleSpinBox(self.tab_import)
        self.sb_height_offset.setObjectName(u"sb_height_offset")
        self.sb_height_offset.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.sb_height_offset.setMinimum(-100.000000000000000)
        self.sb_height_offset.setMaximum(100.000000000000000)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.sb_height_offset)

        self.btn_import = QPushButton(self.tab_import)
        self.btn_import.setObjectName(u"btn_import")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.btn_import)

        self.btn_clear_import = QPushButton(self.tab_import)
        self.btn_clear_import.setObjectName(u"btn_clear_import")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.btn_clear_import)

        self.label_5 = QLabel(self.tab_import)
        self.label_5.setObjectName(u"label_5")

        self.formLayout_2.setWidget(2, QFormLayout.SpanningRole, self.label_5)

        self.tabWidget.addTab(self.tab_import, "")
        self.tab_generate = QWidget()
        self.tab_generate.setObjectName(u"tab_generate")
        self.formLayout = QFormLayout(self.tab_generate)
        self.formLayout.setObjectName(u"formLayout")
        self.btn_apply = QPushButton(self.tab_generate)
        self.btn_apply.setObjectName(u"btn_apply")

        self.formLayout.setWidget(9, QFormLayout.SpanningRole, self.btn_apply)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.formLayout.setItem(11, QFormLayout.SpanningRole, self.verticalSpacer)

        self.label = QLabel(self.tab_generate)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.sp_channel_diameter = QDoubleSpinBox(self.tab_generate)
        self.sp_channel_diameter.setObjectName(u"sp_channel_diameter")
        self.sp_channel_diameter.setMaximumSize(QSize(16777215, 16777215))

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.sp_channel_diameter)

        self.label_2 = QLabel(self.tab_generate)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_2)

        self.sp_tip_diameter = QDoubleSpinBox(self.tab_generate)
        self.sp_tip_diameter.setObjectName(u"sp_tip_diameter")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.sp_tip_diameter)

        self.label_3 = QLabel(self.tab_generate)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_3)

        self.sp_tip_thickness = QDoubleSpinBox(self.tab_generate)
        self.sp_tip_thickness.setObjectName(u"sp_tip_thickness")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.sp_tip_thickness)

        self.label_4 = QLabel(self.tab_generate)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_4)

        self.sp_tip_angle = QDoubleSpinBox(self.tab_generate)
        self.sp_tip_angle.setObjectName(u"sp_tip_angle")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.sp_tip_angle)

        self.btn_clear_generate = QPushButton(self.tab_generate)
        self.btn_clear_generate.setObjectName(u"btn_clear_generate")

        self.formLayout.setWidget(10, QFormLayout.SpanningRole, self.btn_clear_generate)

        self.tabWidget.addTab(self.tab_generate, "")

        self.verticalLayout.addWidget(self.tabWidget)

#if QT_CONFIG(shortcut)
        self.label.setBuddy(self.sp_channel_diameter)
        self.label_2.setBuddy(self.sp_tip_diameter)
        self.label_3.setBuddy(self.sp_tip_thickness)
        self.label_4.setBuddy(self.sp_tip_angle)
#endif // QT_CONFIG(shortcut)

        self.retranslateUi(Tandem_View)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Tandem_View)
    # setupUi

    def retranslateUi(self, Tandem_View):
        Tandem_View.setWindowTitle(QCoreApplication.translate("Tandem_View", u"Form", None))
        self.label_title.setText(QCoreApplication.translate("Tandem_View", u"tandem", None))
        self.label_6.setText(QCoreApplication.translate("Tandem_View", u"height offset", None))
        self.sb_height_offset.setSuffix(QCoreApplication.translate("Tandem_View", u" mm", None))
        self.btn_import.setText(QCoreApplication.translate("Tandem_View", u"import", None))
        self.btn_clear_import.setText(QCoreApplication.translate("Tandem_View", u"clear", None))
        self.label_5.setText(QCoreApplication.translate("Tandem_View", u"Model Details", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_import), QCoreApplication.translate("Tandem_View", u"import", None))
        self.btn_apply.setText(QCoreApplication.translate("Tandem_View", u"apply", None))
        self.label.setText(QCoreApplication.translate("Tandem_View", u"channel diameter", None))
        self.sp_channel_diameter.setSuffix(QCoreApplication.translate("Tandem_View", u" mm", None))
        self.label_2.setText(QCoreApplication.translate("Tandem_View", u"tip diameter", None))
        self.sp_tip_diameter.setSuffix(QCoreApplication.translate("Tandem_View", u" mm", None))
        self.label_3.setText(QCoreApplication.translate("Tandem_View", u"tip thickness", None))
        self.sp_tip_thickness.setSuffix(QCoreApplication.translate("Tandem_View", u" mm", None))
        self.label_4.setText(QCoreApplication.translate("Tandem_View", u"tip angle", None))
        self.sp_tip_angle.setSuffix(QCoreApplication.translate("Tandem_View", u" deg", None))
        self.btn_clear_generate.setText(QCoreApplication.translate("Tandem_View", u"clear", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_generate), QCoreApplication.translate("Tandem_View", u"generate", None))
    # retranslateUi

