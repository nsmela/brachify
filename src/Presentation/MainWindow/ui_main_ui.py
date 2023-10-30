# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'ui_main.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QListView, QListWidget, QListWidgetItem,
    QMainWindow, QPushButton, QSizePolicy, QSpacerItem,
    QStackedWidget, QTabWidget, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1000, 727)
        MainWindow.setMinimumSize(QSize(1000, 500))
        MainWindow.setAcceptDrops(False)
        MainWindow.setStyleSheet(u"background-color: rgb(45, 45, 45);")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setAcceptDrops(True)
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.Top_Bar = QFrame(self.centralwidget)
        self.Top_Bar.setObjectName(u"Top_Bar")
        self.Top_Bar.setMaximumSize(QSize(16777215, 40))
        self.Top_Bar.setStyleSheet(u"background-color: rgb(35, 35, 35);")
        self.Top_Bar.setFrameShape(QFrame.NoFrame)
        self.Top_Bar.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.Top_Bar)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.frame_toggle = QFrame(self.Top_Bar)
        self.frame_toggle.setObjectName(u"frame_toggle")
        self.frame_toggle.setMaximumSize(QSize(78, 40))
        self.frame_toggle.setStyleSheet(u"background-color: rgb(85, 170, 255);")
        self.frame_toggle.setFrameShape(QFrame.StyledPanel)
        self.frame_toggle.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.frame_toggle)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.label_14 = QLabel(self.frame_toggle)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setMinimumSize(QSize(78, 48))
        self.label_14.setMaximumSize(QSize(78, 48))

        self.verticalLayout_2.addWidget(self.label_14, 0, Qt.AlignVCenter)


        self.horizontalLayout.addWidget(self.frame_toggle)

        self.frame_top = QFrame(self.Top_Bar)
        self.frame_top.setObjectName(u"frame_top")
        self.frame_top.setFrameShape(QFrame.StyledPanel)
        self.frame_top.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_17 = QHBoxLayout(self.frame_top)
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.btn_views_imports = QPushButton(self.frame_top)
        self.btn_views_imports.setObjectName(u"btn_views_imports")
        self.btn_views_imports.setMinimumSize(QSize(86, 0))
        self.btn_views_imports.setMaximumSize(QSize(86, 48))
        self.btn_views_imports.setStyleSheet(u"QPushButton {\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgb(35, 35, 35);\n"
"	border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(85, 170, 255);\n"
"}")

        self.horizontalLayout_17.addWidget(self.btn_views_imports)

        self.btn_views_cylinder = QPushButton(self.frame_top)
        self.btn_views_cylinder.setObjectName(u"btn_views_cylinder")
        self.btn_views_cylinder.setMinimumSize(QSize(86, 0))
        self.btn_views_cylinder.setMaximumSize(QSize(86, 48))
        self.btn_views_cylinder.setStyleSheet(u"QPushButton {\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgb(35, 35, 35);\n"
"	border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(85, 170, 255);\n"
"}")

        self.horizontalLayout_17.addWidget(self.btn_views_cylinder)

        self.btn_views_channels = QPushButton(self.frame_top)
        self.btn_views_channels.setObjectName(u"btn_views_channels")
        self.btn_views_channels.setMinimumSize(QSize(86, 0))
        self.btn_views_channels.setMaximumSize(QSize(86, 48))
        self.btn_views_channels.setStyleSheet(u"QPushButton {\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgb(35, 35, 35);\n"
"	border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(85, 170, 255);\n"
"}")

        self.horizontalLayout_17.addWidget(self.btn_views_channels)

        self.btn_views_tandem = QPushButton(self.frame_top)
        self.btn_views_tandem.setObjectName(u"btn_views_tandem")
        self.btn_views_tandem.setMinimumSize(QSize(86, 0))
        self.btn_views_tandem.setMaximumSize(QSize(86, 48))
        self.btn_views_tandem.setStyleSheet(u"QPushButton {\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgb(35, 35, 35);\n"
"	border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(85, 170, 255);\n"
"}")

        self.horizontalLayout_17.addWidget(self.btn_views_tandem)

        self.btn_views_exports = QPushButton(self.frame_top)
        self.btn_views_exports.setObjectName(u"btn_views_exports")
        self.btn_views_exports.setMinimumSize(QSize(86, 0))
        self.btn_views_exports.setMaximumSize(QSize(86, 48))
        self.btn_views_exports.setStyleSheet(u"QPushButton {\n"
"	color: rgb(255, 255, 255);\n"
"	background-color: rgb(35, 35, 35);\n"
"	border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"	background-color: rgb(85, 170, 255);\n"
"}")

        self.horizontalLayout_17.addWidget(self.btn_views_exports)


        self.horizontalLayout.addWidget(self.frame_top, 0, Qt.AlignHCenter)


        self.verticalLayout.addWidget(self.Top_Bar)

        self.Content = QFrame(self.centralwidget)
        self.Content.setObjectName(u"Content")
        self.Content.setAcceptDrops(False)
        self.Content.setFrameShape(QFrame.NoFrame)
        self.Content.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.Content)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.frame_pages = QFrame(self.Content)
        self.frame_pages.setObjectName(u"frame_pages")
        self.frame_pages.setAcceptDrops(False)
        self.frame_pages.setFrameShape(QFrame.StyledPanel)
        self.frame_pages.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.frame_pages)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(4, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.frame_pages)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setMaximumSize(QSize(240, 16777215))
        self.stackedWidget.setAcceptDrops(False)
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        self.page_1.setAcceptDrops(False)
        self.verticalLayout_7 = QVBoxLayout(self.page_1)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_1 = QLabel(self.page_1)
        self.label_1.setObjectName(u"label_1")
        font = QFont()
        font.setPointSize(40)
        self.label_1.setFont(font)
        self.label_1.setStyleSheet(u"color: #FFF;")
        self.label_1.setAlignment(Qt.AlignCenter)

        self.verticalLayout_7.addWidget(self.label_1, 0, Qt.AlignTop)

        self.groupBox_2 = QGroupBox(self.page_1)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.verticalLayout_10 = QVBoxLayout(self.groupBox_2)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.frame_2 = QFrame(self.groupBox_2)
        self.frame_2.setObjectName(u"frame_2")
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.frame_2)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.lineedit_dicom_rs = QLineEdit(self.frame_2)
        self.lineedit_dicom_rs.setObjectName(u"lineedit_dicom_rs")
        self.lineedit_dicom_rs.setFrame(False)
        self.lineedit_dicom_rs.setReadOnly(True)

        self.horizontalLayout_5.addWidget(self.lineedit_dicom_rs)

        self.btn_import_dicom_folder = QPushButton(self.frame_2)
        self.btn_import_dicom_folder.setObjectName(u"btn_import_dicom_folder")

        self.horizontalLayout_5.addWidget(self.btn_import_dicom_folder)


        self.verticalLayout_10.addWidget(self.frame_2)


        self.verticalLayout_7.addWidget(self.groupBox_2)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer_5)

        self.frame = QFrame(self.page_1)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.frame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")

        self.verticalLayout_7.addWidget(self.frame)

        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticallayout_6 = QVBoxLayout(self.page_2)
        self.verticallayout_6.setObjectName(u"verticallayout_6")
        self.verticallayout_6.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.page_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"color: #FFF;")
        self.label_2.setAlignment(Qt.AlignCenter)

        self.verticallayout_6.addWidget(self.label_2, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.frame_5 = QFrame(self.page_2)
        self.frame_5.setObjectName(u"frame_5")
        self.frame_5.setFrameShape(QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.frame_5)
        self.label.setObjectName(u"label")

        self.horizontalLayout_8.addWidget(self.label)

        self.cylinderDiameterSpinBox = QDoubleSpinBox(self.frame_5)
        self.cylinderDiameterSpinBox.setObjectName(u"cylinderDiameterSpinBox")

        self.horizontalLayout_8.addWidget(self.cylinderDiameterSpinBox)


        self.verticallayout_6.addWidget(self.frame_5, 0, Qt.AlignTop)

        self.frame_6 = QFrame(self.page_2)
        self.frame_6.setObjectName(u"frame_6")
        self.frame_6.setFrameShape(QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_9 = QHBoxLayout(self.frame_6)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.label_6 = QLabel(self.frame_6)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_9.addWidget(self.label_6)

        self.cylinderLengthSpinBox = QDoubleSpinBox(self.frame_6)
        self.cylinderLengthSpinBox.setObjectName(u"cylinderLengthSpinBox")
        self.cylinderLengthSpinBox.setDecimals(1)
        self.cylinderLengthSpinBox.setMinimum(30.000000000000000)
        self.cylinderLengthSpinBox.setMaximum(350.000000000000000)

        self.horizontalLayout_9.addWidget(self.cylinderLengthSpinBox)


        self.verticallayout_6.addWidget(self.frame_6)

        self.frame_12 = QFrame(self.page_2)
        self.frame_12.setObjectName(u"frame_12")
        self.frame_12.setFrameShape(QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_16 = QHBoxLayout(self.frame_12)
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.label_15 = QLabel(self.frame_12)
        self.label_15.setObjectName(u"label_15")

        self.horizontalLayout_16.addWidget(self.label_15)

        self.checkbox_cylinder_base = QCheckBox(self.frame_12)
        self.checkbox_cylinder_base.setObjectName(u"checkbox_cylinder_base")
        self.checkbox_cylinder_base.setIconSize(QSize(32, 32))
        self.checkbox_cylinder_base.setChecked(True)

        self.horizontalLayout_16.addWidget(self.checkbox_cylinder_base, 0, Qt.AlignRight)


        self.verticallayout_6.addWidget(self.frame_12)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticallayout_6.addItem(self.verticalSpacer)

        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.verticalLayout_8 = QVBoxLayout(self.page_3)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.label_3 = QLabel(self.page_3)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(u"color: #FFF;")
        self.label_3.setAlignment(Qt.AlignCenter)

        self.verticalLayout_8.addWidget(self.label_3, 0, Qt.AlignTop)

        self.groupBox = QGroupBox(self.page_3)
        self.groupBox.setObjectName(u"groupBox")
        self.verticalLayout_6 = QVBoxLayout(self.groupBox)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 4)
        self.frame_7 = QFrame(self.groupBox)
        self.frame_7.setObjectName(u"frame_7")
        self.frame_7.setFrameShape(QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_10 = QHBoxLayout(self.frame_7)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_8 = QLabel(self.frame_7)
        self.label_8.setObjectName(u"label_8")

        self.horizontalLayout_10.addWidget(self.label_8)

        self.channelDiameterSpinBox = QDoubleSpinBox(self.frame_7)
        self.channelDiameterSpinBox.setObjectName(u"channelDiameterSpinBox")
        self.channelDiameterSpinBox.setMinimum(1.000000000000000)
        self.channelDiameterSpinBox.setMaximum(15.000000000000000)
        self.channelDiameterSpinBox.setSingleStep(0.500000000000000)

        self.horizontalLayout_10.addWidget(self.channelDiameterSpinBox)


        self.verticalLayout_6.addWidget(self.frame_7)

        self.frame_13 = QFrame(self.groupBox)
        self.frame_13.setObjectName(u"frame_13")
        self.frame_13.setFrameShape(QFrame.StyledPanel)
        self.frame_13.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_18 = QHBoxLayout(self.frame_13)
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.label_17 = QLabel(self.frame_13)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_18.addWidget(self.label_17)

        self.checkBox_hide_cylinder = QCheckBox(self.frame_13)
        self.checkBox_hide_cylinder.setObjectName(u"checkBox_hide_cylinder")

        self.horizontalLayout_18.addWidget(self.checkBox_hide_cylinder)


        self.verticalLayout_6.addWidget(self.frame_13)


        self.verticalLayout_8.addWidget(self.groupBox)

        self.label_7 = QLabel(self.page_3)
        self.label_7.setObjectName(u"label_7")

        self.verticalLayout_8.addWidget(self.label_7)

        self.channelsListWidget = QListWidget(self.page_3)
        self.channelsListWidget.setObjectName(u"channelsListWidget")
        self.channelsListWidget.setMinimumSize(QSize(200, 0))
        self.channelsListWidget.setFlow(QListView.TopToBottom)
        self.channelsListWidget.setViewMode(QListView.IconMode)
        self.channelsListWidget.setUniformItemSizes(True)

        self.verticalLayout_8.addWidget(self.channelsListWidget, 0, Qt.AlignLeft)

        self.groupBox_5 = QGroupBox(self.page_3)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setEnabled(True)
        self.horizontalLayout_6 = QHBoxLayout(self.groupBox_5)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.btn_channel_disable = QPushButton(self.groupBox_5)
        self.btn_channel_disable.setObjectName(u"btn_channel_disable")

        self.horizontalLayout_6.addWidget(self.btn_channel_disable)

        self.btn_channel_tandem = QPushButton(self.groupBox_5)
        self.btn_channel_tandem.setObjectName(u"btn_channel_tandem")
        self.btn_channel_tandem.setMinimumSize(QSize(50, 0))
        self.btn_channel_tandem.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_6.addWidget(self.btn_channel_tandem)


        self.verticalLayout_8.addWidget(self.groupBox_5)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_8.addItem(self.verticalSpacer_3)

        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QWidget()
        self.page_4.setObjectName(u"page_4")
        self.verticalLayout_5 = QVBoxLayout(self.page_4)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 3)
        self.label_4 = QLabel(self.page_4)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setFont(font)
        self.label_4.setStyleSheet(u"color: #FFF;")
        self.label_4.setAlignment(Qt.AlignCenter)

        self.verticalLayout_5.addWidget(self.label_4, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.tandem_tabbedWidget = QTabWidget(self.page_4)
        self.tandem_tabbedWidget.setObjectName(u"tandem_tabbedWidget")
        self.tandem_tab_preloaded = QWidget()
        self.tandem_tab_preloaded.setObjectName(u"tandem_tab_preloaded")
        self.verticalLayout_11 = QVBoxLayout(self.tandem_tab_preloaded)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.listWidget_savedTandems = QListWidget(self.tandem_tab_preloaded)
        self.listWidget_savedTandems.setObjectName(u"listWidget_savedTandems")

        self.verticalLayout_11.addWidget(self.listWidget_savedTandems)

        self.groupbox_newTandem = QGroupBox(self.tandem_tab_preloaded)
        self.groupbox_newTandem.setObjectName(u"groupbox_newTandem")
        self.groupbox_newTandem.setMaximumSize(QSize(16777215, 1677215))
        self.verticalLayout_4 = QVBoxLayout(self.groupbox_newTandem)
        self.verticalLayout_4.setSpacing(2)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(2, 0, 0, 2)
        self.frame_15 = QFrame(self.groupbox_newTandem)
        self.frame_15.setObjectName(u"frame_15")
        self.frame_15.setFrameShape(QFrame.StyledPanel)
        self.frame_15.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_20 = QHBoxLayout(self.frame_15)
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.label_19 = QLabel(self.frame_15)
        self.label_19.setObjectName(u"label_19")

        self.horizontalLayout_20.addWidget(self.label_19)

        self.tandem_lineEdit_toolModel = QLineEdit(self.frame_15)
        self.tandem_lineEdit_toolModel.setObjectName(u"tandem_lineEdit_toolModel")

        self.horizontalLayout_20.addWidget(self.tandem_lineEdit_toolModel)

        self.btn_tandem_importToolModel = QPushButton(self.frame_15)
        self.btn_tandem_importToolModel.setObjectName(u"btn_tandem_importToolModel")
        self.btn_tandem_importToolModel.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout_20.addWidget(self.btn_tandem_importToolModel)


        self.verticalLayout_4.addWidget(self.frame_15)

        self.frame_16 = QFrame(self.groupbox_newTandem)
        self.frame_16.setObjectName(u"frame_16")
        self.frame_16.setFrameShape(QFrame.StyledPanel)
        self.frame_16.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_21 = QHBoxLayout(self.frame_16)
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.label_20 = QLabel(self.frame_16)
        self.label_20.setObjectName(u"label_20")

        self.horizontalLayout_21.addWidget(self.label_20)

        self.lineEdit_tandemName = QLineEdit(self.frame_16)
        self.lineEdit_tandemName.setObjectName(u"lineEdit_tandemName")

        self.horizontalLayout_21.addWidget(self.lineEdit_tandemName)


        self.verticalLayout_4.addWidget(self.frame_16)

        self.frame_17 = QFrame(self.groupbox_newTandem)
        self.frame_17.setObjectName(u"frame_17")
        self.frame_17.setFrameShape(QFrame.StyledPanel)
        self.frame_17.setFrameShadow(QFrame.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.frame_17)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.frame_18 = QFrame(self.frame_17)
        self.frame_18.setObjectName(u"frame_18")
        self.frame_18.setFrameShape(QFrame.StyledPanel)
        self.frame_18.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_22 = QHBoxLayout(self.frame_18)
        self.horizontalLayout_22.setSpacing(2)
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.btn_tandem_add_update = QPushButton(self.frame_18)
        self.btn_tandem_add_update.setObjectName(u"btn_tandem_add_update")

        self.horizontalLayout_22.addWidget(self.btn_tandem_add_update)

        self.btn_tandem_clear = QPushButton(self.frame_18)
        self.btn_tandem_clear.setObjectName(u"btn_tandem_clear")

        self.horizontalLayout_22.addWidget(self.btn_tandem_clear)


        self.verticalLayout_12.addWidget(self.frame_18)


        self.verticalLayout_4.addWidget(self.frame_17)


        self.verticalLayout_11.addWidget(self.groupbox_newTandem)

        self.tandem_tabbedWidget.addTab(self.tandem_tab_preloaded, "")
        self.tandem_tab_generated = QWidget()
        self.tandem_tab_generated.setObjectName(u"tandem_tab_generated")
        self.tandem_tab_generated.setFocusPolicy(Qt.NoFocus)
        self.verticalLayout_13 = QVBoxLayout(self.tandem_tab_generated)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.custom_tandem_frame = QFrame(self.tandem_tab_generated)
        self.custom_tandem_frame.setObjectName(u"custom_tandem_frame")
        self.custom_tandem_frame.setFrameShape(QFrame.StyledPanel)
        self.custom_tandem_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.custom_tandem_frame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.channel_diameter_frame = QFrame(self.custom_tandem_frame)
        self.channel_diameter_frame.setObjectName(u"channel_diameter_frame")
        self.channel_diameter_frame.setFrameShape(QFrame.StyledPanel)
        self.channel_diameter_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_7 = QHBoxLayout(self.channel_diameter_frame)
        self.horizontalLayout_7.setSpacing(2)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(2, 0, 0, 0)
        self.label_9 = QLabel(self.channel_diameter_frame)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_7.addWidget(self.label_9)

        self.tandem_spinbox_channel_diameter = QDoubleSpinBox(self.channel_diameter_frame)
        self.tandem_spinbox_channel_diameter.setObjectName(u"tandem_spinbox_channel_diameter")

        self.horizontalLayout_7.addWidget(self.tandem_spinbox_channel_diameter)


        self.verticalLayout_3.addWidget(self.channel_diameter_frame)

        self.frame_3 = QFrame(self.custom_tandem_frame)
        self.frame_3.setObjectName(u"frame_3")
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_13 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.label_10 = QLabel(self.frame_3)
        self.label_10.setObjectName(u"label_10")

        self.horizontalLayout_13.addWidget(self.label_10)

        self.tandem_spinbox_tip_diameter = QDoubleSpinBox(self.frame_3)
        self.tandem_spinbox_tip_diameter.setObjectName(u"tandem_spinbox_tip_diameter")

        self.horizontalLayout_13.addWidget(self.tandem_spinbox_tip_diameter)


        self.verticalLayout_3.addWidget(self.frame_3)

        self.tip_thickness_frame = QFrame(self.custom_tandem_frame)
        self.tip_thickness_frame.setObjectName(u"tip_thickness_frame")
        self.tip_thickness_frame.setFrameShape(QFrame.StyledPanel)
        self.tip_thickness_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.tip_thickness_frame)
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_11 = QLabel(self.tip_thickness_frame)
        self.label_11.setObjectName(u"label_11")

        self.horizontalLayout_11.addWidget(self.label_11)

        self.tandem_spinbox_tip_thickness = QDoubleSpinBox(self.tip_thickness_frame)
        self.tandem_spinbox_tip_thickness.setObjectName(u"tandem_spinbox_tip_thickness")

        self.horizontalLayout_11.addWidget(self.tandem_spinbox_tip_thickness)


        self.verticalLayout_3.addWidget(self.tip_thickness_frame)

        self.tip_angle_frame = QFrame(self.custom_tandem_frame)
        self.tip_angle_frame.setObjectName(u"tip_angle_frame")
        self.tip_angle_frame.setFrameShape(QFrame.StyledPanel)
        self.tip_angle_frame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_12 = QHBoxLayout(self.tip_angle_frame)
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_13 = QLabel(self.tip_angle_frame)
        self.label_13.setObjectName(u"label_13")

        self.horizontalLayout_12.addWidget(self.label_13)

        self.tandem_spinbox_tip_angle = QDoubleSpinBox(self.tip_angle_frame)
        self.tandem_spinbox_tip_angle.setObjectName(u"tandem_spinbox_tip_angle")

        self.horizontalLayout_12.addWidget(self.tandem_spinbox_tip_angle)


        self.verticalLayout_3.addWidget(self.tip_angle_frame)


        self.verticalLayout_13.addWidget(self.custom_tandem_frame)

        self.tandem_tabbedWidget.addTab(self.tandem_tab_generated, "")

        self.verticalLayout_5.addWidget(self.tandem_tabbedWidget, 0, Qt.AlignLeft|Qt.AlignTop)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_2)

        self.stackedWidget.addWidget(self.page_4)
        self.page_5 = QWidget()
        self.page_5.setObjectName(u"page_5")
        self.verticalLayout_9 = QVBoxLayout(self.page_5)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.label_5 = QLabel(self.page_5)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setFont(font)
        self.label_5.setStyleSheet(u"color: #FFF;")
        self.label_5.setAlignment(Qt.AlignCenter)

        self.verticalLayout_9.addWidget(self.label_5, 0, Qt.AlignHCenter|Qt.AlignTop)

        self.label_12 = QLabel(self.page_5)
        self.label_12.setObjectName(u"label_12")

        self.verticalLayout_9.addWidget(self.label_12)

        self.label_16 = QLabel(self.page_5)
        self.label_16.setObjectName(u"label_16")

        self.verticalLayout_9.addWidget(self.label_16)

        self.btn_export_stl = QPushButton(self.page_5)
        self.btn_export_stl.setObjectName(u"btn_export_stl")

        self.verticalLayout_9.addWidget(self.btn_export_stl)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout_9.addItem(self.verticalSpacer_4)

        self.stackedWidget.addWidget(self.page_5)

        self.horizontalLayout_3.addWidget(self.stackedWidget)

        self.model_frame = QFrame(self.frame_pages)
        self.model_frame.setObjectName(u"model_frame")
        self.model_frame.setMinimumSize(QSize(0, 0))
        self.model_frame.setFrameShape(QFrame.StyledPanel)
        self.model_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.model_frame)
        self.gridLayout.setObjectName(u"gridLayout")

        self.horizontalLayout_3.addWidget(self.model_frame)


        self.horizontalLayout_2.addWidget(self.frame_pages)


        self.verticalLayout.addWidget(self.Content)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(3)
        self.tandem_tabbedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"brachify", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"<html><head/><body><p> brach<span style=\" font-weight:600;\">IFY</span></p></body></html>", None))
        self.btn_views_imports.setText(QCoreApplication.translate("MainWindow", u"imports", None))
        self.btn_views_cylinder.setText(QCoreApplication.translate("MainWindow", u"cylinder", None))
        self.btn_views_channels.setText(QCoreApplication.translate("MainWindow", u"channels", None))
        self.btn_views_tandem.setText(QCoreApplication.translate("MainWindow", u"tandem", None))
        self.btn_views_exports.setText(QCoreApplication.translate("MainWindow", u"exports", None))
        self.label_1.setText(QCoreApplication.translate("MainWindow", u"imports", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"import folder", None))
        self.btn_import_dicom_folder.setText(QCoreApplication.translate("MainWindow", u"import", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"cylinder", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Diameter (mm)", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Length (mm)", None))
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Add Base", None))
        self.checkbox_cylinder_base.setText("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"channels", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Universal Channel Settings", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Diameter (mm):", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Hide Cylinder?", None))
        self.checkBox_hide_cylinder.setText("")
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Loaded Channels", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Individual Settings", None))
        self.btn_channel_disable.setText(QCoreApplication.translate("MainWindow", u"Disable/Remove", None))
        self.btn_channel_tandem.setText(QCoreApplication.translate("MainWindow", u"Tandem", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"tandem", None))
        self.groupbox_newTandem.setTitle(QCoreApplication.translate("MainWindow", u"New Tandem", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Tool Model", None))
        self.btn_tandem_importToolModel.setText(QCoreApplication.translate("MainWindow", u"...", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Tandem Name:", None))
        self.btn_tandem_add_update.setText(QCoreApplication.translate("MainWindow", u"Add/Update", None))
        self.btn_tandem_clear.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.tandem_tabbedWidget.setTabText(self.tandem_tabbedWidget.indexOf(self.tandem_tab_preloaded), QCoreApplication.translate("MainWindow", u"PreLoaded Tandems", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"channel diameter", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"tip diameter", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"tip thickness", None))
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"tip angle", None))
        self.tandem_tabbedWidget.setTabText(self.tandem_tabbedWidget.indexOf(self.tandem_tab_generated), QCoreApplication.translate("MainWindow", u"Generated", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"export", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Info", None))
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Data", None))
        self.btn_export_stl.setText(QCoreApplication.translate("MainWindow", u"export STL", None))
    # retranslateUi

