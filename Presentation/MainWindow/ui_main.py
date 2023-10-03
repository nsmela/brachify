# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file './Presentation/MainWindow/ui_main.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 715)
        MainWindow.setMinimumSize(QtCore.QSize(1000, 500))
        MainWindow.setAcceptDrops(False)
        MainWindow.setStyleSheet("background-color: rgb(45, 45, 45);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAcceptDrops(True)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.Top_Bar = QtWidgets.QFrame(self.centralwidget)
        self.Top_Bar.setMaximumSize(QtCore.QSize(16777215, 40))
        self.Top_Bar.setStyleSheet("background-color: rgb(35, 35, 35);")
        self.Top_Bar.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Top_Bar.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Top_Bar.setObjectName("Top_Bar")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.Top_Bar)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_toggle = QtWidgets.QFrame(self.Top_Bar)
        self.frame_toggle.setMaximumSize(QtCore.QSize(78, 40))
        self.frame_toggle.setStyleSheet("background-color: rgb(85, 170, 255);")
        self.frame_toggle.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_toggle.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_toggle.setObjectName("frame_toggle")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame_toggle)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_14 = QtWidgets.QLabel(self.frame_toggle)
        self.label_14.setMinimumSize(QtCore.QSize(78, 48))
        self.label_14.setMaximumSize(QtCore.QSize(78, 48))
        self.label_14.setObjectName("label_14")
        self.verticalLayout_2.addWidget(self.label_14, 0, QtCore.Qt.AlignVCenter)
        self.horizontalLayout.addWidget(self.frame_toggle)
        self.frame_top = QtWidgets.QFrame(self.Top_Bar)
        self.frame_top.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_top.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_top.setObjectName("frame_top")
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout(self.frame_top)
        self.horizontalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.btn_views_imports = QtWidgets.QPushButton(self.frame_top)
        self.btn_views_imports.setMinimumSize(QtCore.QSize(86, 0))
        self.btn_views_imports.setMaximumSize(QtCore.QSize(86, 48))
        self.btn_views_imports.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_views_imports.setObjectName("btn_views_imports")
        self.horizontalLayout_17.addWidget(self.btn_views_imports)
        self.btn_views_cylinder = QtWidgets.QPushButton(self.frame_top)
        self.btn_views_cylinder.setMinimumSize(QtCore.QSize(86, 0))
        self.btn_views_cylinder.setMaximumSize(QtCore.QSize(86, 48))
        self.btn_views_cylinder.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_views_cylinder.setObjectName("btn_views_cylinder")
        self.horizontalLayout_17.addWidget(self.btn_views_cylinder)
        self.btn_views_channels = QtWidgets.QPushButton(self.frame_top)
        self.btn_views_channels.setMinimumSize(QtCore.QSize(86, 0))
        self.btn_views_channels.setMaximumSize(QtCore.QSize(86, 48))
        self.btn_views_channels.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_views_channels.setObjectName("btn_views_channels")
        self.horizontalLayout_17.addWidget(self.btn_views_channels)
        self.btn_views_tandem = QtWidgets.QPushButton(self.frame_top)
        self.btn_views_tandem.setMinimumSize(QtCore.QSize(86, 0))
        self.btn_views_tandem.setMaximumSize(QtCore.QSize(86, 48))
        self.btn_views_tandem.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_views_tandem.setObjectName("btn_views_tandem")
        self.horizontalLayout_17.addWidget(self.btn_views_tandem)
        self.btn_views_exports = QtWidgets.QPushButton(self.frame_top)
        self.btn_views_exports.setMinimumSize(QtCore.QSize(86, 0))
        self.btn_views_exports.setMaximumSize(QtCore.QSize(86, 48))
        self.btn_views_exports.setStyleSheet("QPushButton {\n"
"    color: rgb(255, 255, 255);\n"
"    background-color: rgb(35, 35, 35);\n"
"    border: 0px solid;\n"
"}\n"
"QPushButton:hover {\n"
"    background-color: rgb(85, 170, 255);\n"
"}")
        self.btn_views_exports.setObjectName("btn_views_exports")
        self.horizontalLayout_17.addWidget(self.btn_views_exports)
        self.horizontalLayout.addWidget(self.frame_top, 0, QtCore.Qt.AlignHCenter)
        self.verticalLayout.addWidget(self.Top_Bar)
        self.Content = QtWidgets.QFrame(self.centralwidget)
        self.Content.setAcceptDrops(False)
        self.Content.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.Content.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Content.setObjectName("Content")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.Content)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_pages = QtWidgets.QFrame(self.Content)
        self.frame_pages.setAcceptDrops(False)
        self.frame_pages.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_pages.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_pages.setObjectName("frame_pages")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_pages)
        self.horizontalLayout_3.setContentsMargins(4, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.stackedWidget = QtWidgets.QStackedWidget(self.frame_pages)
        self.stackedWidget.setMaximumSize(QtCore.QSize(240, 16777215))
        self.stackedWidget.setAcceptDrops(False)
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setAcceptDrops(False)
        self.page_1.setObjectName("page_1")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.page_1)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.label_1 = QtWidgets.QLabel(self.page_1)
        font = QtGui.QFont()
        font.setPointSize(40)
        self.label_1.setFont(font)
        self.label_1.setStyleSheet("color: #FFF;")
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1.setObjectName("label_1")
        self.verticalLayout_7.addWidget(self.label_1, 0, QtCore.Qt.AlignTop)
        self.groupBox_2 = QtWidgets.QGroupBox(self.page_1)
        self.groupBox_2.setObjectName("groupBox_2")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.frame_2 = QtWidgets.QFrame(self.groupBox_2)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lineedit_dicom_rs = QtWidgets.QLineEdit(self.frame_2)
        self.lineedit_dicom_rs.setFrame(False)
        self.lineedit_dicom_rs.setReadOnly(True)
        self.lineedit_dicom_rs.setObjectName("lineedit_dicom_rs")
        self.horizontalLayout_5.addWidget(self.lineedit_dicom_rs)
        self.btn_import_dicom_rs = QtWidgets.QPushButton(self.frame_2)
        self.btn_import_dicom_rs.setObjectName("btn_import_dicom_rs")
        self.horizontalLayout_5.addWidget(self.btn_import_dicom_rs)
        self.verticalLayout_10.addWidget(self.frame_2)
        self.verticalLayout_7.addWidget(self.groupBox_2)
        self.groupBox_3 = QtWidgets.QGroupBox(self.page_1)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.frame_3 = QtWidgets.QFrame(self.groupBox_3)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_3)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.lineedit_dicom_rp = QtWidgets.QLineEdit(self.frame_3)
        self.lineedit_dicom_rp.setFrame(False)
        self.lineedit_dicom_rp.setReadOnly(True)
        self.lineedit_dicom_rp.setObjectName("lineedit_dicom_rp")
        self.horizontalLayout_6.addWidget(self.lineedit_dicom_rp)
        self.btn_import_dicom_rp = QtWidgets.QPushButton(self.frame_3)
        self.btn_import_dicom_rp.setObjectName("btn_import_dicom_rp")
        self.horizontalLayout_6.addWidget(self.btn_import_dicom_rp)
        self.horizontalLayout_14.addWidget(self.frame_3)
        self.verticalLayout_7.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(self.page_1)
        self.groupBox_4.setObjectName("groupBox_4")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.frame_4 = QtWidgets.QFrame(self.groupBox_4)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.lineedit_tandem = QtWidgets.QLineEdit(self.frame_4)
        self.lineedit_tandem.setFrame(False)
        self.lineedit_tandem.setReadOnly(True)
        self.lineedit_tandem.setObjectName("lineedit_tandem")
        self.horizontalLayout_7.addWidget(self.lineedit_tandem)
        self.btn_import_tandem = QtWidgets.QPushButton(self.frame_4)
        self.btn_import_tandem.setObjectName("btn_import_tandem")
        self.horizontalLayout_7.addWidget(self.btn_import_tandem)
        self.verticalLayout_11.addWidget(self.frame_4)
        self.verticalLayout_7.addWidget(self.groupBox_4)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem)
        self.frame = QtWidgets.QFrame(self.page_1)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_7.addWidget(self.frame)
        self.stackedWidget.addWidget(self.page_1)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.verticallayout_6 = QtWidgets.QVBoxLayout(self.page_2)
        self.verticallayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticallayout_6.setObjectName("verticallayout_6")
        self.label_2 = QtWidgets.QLabel(self.page_2)
        font = QtGui.QFont()
        font.setPointSize(40)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: #FFF;")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticallayout_6.addWidget(self.label_2, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.frame_5 = QtWidgets.QFrame(self.page_2)
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label = QtWidgets.QLabel(self.frame_5)
        self.label.setObjectName("label")
        self.horizontalLayout_8.addWidget(self.label)
        self.cylinderRadiusSpinBox = QtWidgets.QDoubleSpinBox(self.frame_5)
        self.cylinderRadiusSpinBox.setObjectName("cylinderRadiusSpinBox")
        self.horizontalLayout_8.addWidget(self.cylinderRadiusSpinBox)
        self.verticallayout_6.addWidget(self.frame_5, 0, QtCore.Qt.AlignTop)
        self.frame_6 = QtWidgets.QFrame(self.page_2)
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_6 = QtWidgets.QLabel(self.frame_6)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_9.addWidget(self.label_6)
        self.cylinderLengthSpinBox = QtWidgets.QDoubleSpinBox(self.frame_6)
        self.cylinderLengthSpinBox.setDecimals(1)
        self.cylinderLengthSpinBox.setMinimum(30.0)
        self.cylinderLengthSpinBox.setMaximum(350.0)
        self.cylinderLengthSpinBox.setObjectName("cylinderLengthSpinBox")
        self.horizontalLayout_9.addWidget(self.cylinderLengthSpinBox)
        self.verticallayout_6.addWidget(self.frame_6)
        self.frame_12 = QtWidgets.QFrame(self.page_2)
        self.frame_12.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_12")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.frame_12)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        self.label_15 = QtWidgets.QLabel(self.frame_12)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_16.addWidget(self.label_15)
        self.checkbox_cylinder_base = QtWidgets.QCheckBox(self.frame_12)
        self.checkbox_cylinder_base.setText("")
        self.checkbox_cylinder_base.setIconSize(QtCore.QSize(32, 32))
        self.checkbox_cylinder_base.setChecked(True)
        self.checkbox_cylinder_base.setObjectName("checkbox_cylinder_base")
        self.horizontalLayout_16.addWidget(self.checkbox_cylinder_base, 0, QtCore.Qt.AlignRight)
        self.verticallayout_6.addWidget(self.frame_12)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticallayout_6.addItem(spacerItem1)
        self.stackedWidget.addWidget(self.page_2)
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.page_3)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_3 = QtWidgets.QLabel(self.page_3)
        font = QtGui.QFont()
        font.setPointSize(40)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: #FFF;")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_8.addWidget(self.label_3, 0, QtCore.Qt.AlignTop)
        self.label_7 = QtWidgets.QLabel(self.page_3)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_8.addWidget(self.label_7)
        self.channelsListWidget = QtWidgets.QListWidget(self.page_3)
        self.channelsListWidget.setMinimumSize(QtCore.QSize(200, 0))
        self.channelsListWidget.setFlow(QtWidgets.QListView.TopToBottom)
        self.channelsListWidget.setViewMode(QtWidgets.QListView.IconMode)
        self.channelsListWidget.setUniformItemSizes(True)
        self.channelsListWidget.setObjectName("channelsListWidget")
        self.verticalLayout_8.addWidget(self.channelsListWidget, 0, QtCore.Qt.AlignLeft)
        self.groupBox = QtWidgets.QGroupBox(self.page_3)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 4)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.frame_7 = QtWidgets.QFrame(self.groupBox)
        self.frame_7.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_8 = QtWidgets.QLabel(self.frame_7)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_10.addWidget(self.label_8)
        self.channelRadiusSpinBox = QtWidgets.QDoubleSpinBox(self.frame_7)
        self.channelRadiusSpinBox.setObjectName("channelRadiusSpinBox")
        self.horizontalLayout_10.addWidget(self.channelRadiusSpinBox)
        self.verticalLayout_6.addWidget(self.frame_7)
        self.frame_11 = QtWidgets.QFrame(self.groupBox)
        self.frame_11.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.frame_11)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_13 = QtWidgets.QLabel(self.frame_11)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_15.addWidget(self.label_13)
        self.slider_needle_extension = QtWidgets.QSlider(self.frame_11)
        self.slider_needle_extension.setMaximum(15)
        self.slider_needle_extension.setSliderPosition(0)
        self.slider_needle_extension.setOrientation(QtCore.Qt.Horizontal)
        self.slider_needle_extension.setTickPosition(QtWidgets.QSlider.TicksBothSides)
        self.slider_needle_extension.setTickInterval(1)
        self.slider_needle_extension.setObjectName("slider_needle_extension")
        self.horizontalLayout_15.addWidget(self.slider_needle_extension)
        self.verticalLayout_6.addWidget(self.frame_11)
        self.frame_8 = QtWidgets.QFrame(self.groupBox)
        self.frame_8.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_9 = QtWidgets.QLabel(self.frame_8)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_11.addWidget(self.label_9)
        self.channelExtendCheckBox = QtWidgets.QCheckBox(self.frame_8)
        self.channelExtendCheckBox.setText("")
        self.channelExtendCheckBox.setIconSize(QtCore.QSize(32, 32))
        self.channelExtendCheckBox.setObjectName("channelExtendCheckBox")
        self.horizontalLayout_11.addWidget(self.channelExtendCheckBox)
        self.verticalLayout_6.addWidget(self.frame_8)
        self.btn_channel_disable = QtWidgets.QPushButton(self.groupBox)
        self.btn_channel_disable.setObjectName("btn_channel_disable")
        self.verticalLayout_6.addWidget(self.btn_channel_disable)
        self.verticalLayout_8.addWidget(self.groupBox)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem2)
        self.stackedWidget.addWidget(self.page_3)
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setObjectName("page_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.page_4)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_4 = QtWidgets.QLabel(self.page_4)
        font = QtGui.QFont()
        font.setPointSize(40)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: #FFF;")
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_5.addWidget(self.label_4, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.frame_9 = QtWidgets.QFrame(self.page_4)
        self.frame_9.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.frame_9)
        self.horizontalLayout_12.setContentsMargins(0, -1, 0, 0)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_10 = QtWidgets.QLabel(self.frame_9)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_12.addWidget(self.label_10)
        self.tandemHieghtSpinBox = QtWidgets.QSpinBox(self.frame_9)
        self.tandemHieghtSpinBox.setObjectName("tandemHieghtSpinBox")
        self.horizontalLayout_12.addWidget(self.tandemHieghtSpinBox)
        self.verticalLayout_5.addWidget(self.frame_9, 0, QtCore.Qt.AlignTop)
        self.frame_10 = QtWidgets.QFrame(self.page_4)
        self.frame_10.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_10.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_10.setObjectName("frame_10")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.frame_10)
        self.horizontalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_11 = QtWidgets.QLabel(self.frame_10)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_13.addWidget(self.label_11)
        self.tandemRotationSlider = QtWidgets.QSlider(self.frame_10)
        self.tandemRotationSlider.setOrientation(QtCore.Qt.Horizontal)
        self.tandemRotationSlider.setObjectName("tandemRotationSlider")
        self.horizontalLayout_13.addWidget(self.tandemRotationSlider)
        self.verticalLayout_5.addWidget(self.frame_10)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem3)
        self.stackedWidget.addWidget(self.page_4)
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setObjectName("page_5")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.page_5)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_5 = QtWidgets.QLabel(self.page_5)
        font = QtGui.QFont()
        font.setPointSize(40)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: #FFF;")
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_9.addWidget(self.label_5, 0, QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.label_12 = QtWidgets.QLabel(self.page_5)
        self.label_12.setObjectName("label_12")
        self.verticalLayout_9.addWidget(self.label_12)
        self.label_16 = QtWidgets.QLabel(self.page_5)
        self.label_16.setObjectName("label_16")
        self.verticalLayout_9.addWidget(self.label_16)
        self.btn_export_file = QtWidgets.QPushButton(self.page_5)
        self.btn_export_file.setObjectName("btn_export_file")
        self.verticalLayout_9.addWidget(self.btn_export_file)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_9.addItem(spacerItem4)
        self.stackedWidget.addWidget(self.page_5)
        self.horizontalLayout_3.addWidget(self.stackedWidget)
        self.model_frame = QtWidgets.QFrame(self.frame_pages)
        self.model_frame.setMinimumSize(QtCore.QSize(0, 0))
        self.model_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.model_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.model_frame.setObjectName("model_frame")
        self.gridLayout = QtWidgets.QGridLayout(self.model_frame)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3.addWidget(self.model_frame)
        self.horizontalLayout_2.addWidget(self.frame_pages)
        self.verticalLayout.addWidget(self.Content)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Brachy App"))
        self.label_14.setText(_translate("MainWindow", "<strong> BRACHY</strong>APP"))
        self.btn_views_imports.setText(_translate("MainWindow", "imports"))
        self.btn_views_cylinder.setText(_translate("MainWindow", "cylinder"))
        self.btn_views_channels.setText(_translate("MainWindow", "channels"))
        self.btn_views_tandem.setText(_translate("MainWindow", "tandem"))
        self.btn_views_exports.setText(_translate("MainWindow", "exports"))
        self.label_1.setText(_translate("MainWindow", "imports"))
        self.groupBox_2.setTitle(_translate("MainWindow", "cylinder file"))
        self.btn_import_dicom_rs.setText(_translate("MainWindow", "import dicom rs"))
        self.groupBox_3.setTitle(_translate("MainWindow", "needle channels file"))
        self.btn_import_dicom_rp.setText(_translate("MainWindow", "import dicom rp"))
        self.groupBox_4.setTitle(_translate("MainWindow", "tandem file"))
        self.btn_import_tandem.setText(_translate("MainWindow", "import tandem"))
        self.label_2.setText(_translate("MainWindow", "cylinder"))
        self.label.setText(_translate("MainWindow", "Diameter (mm)"))
        self.label_6.setText(_translate("MainWindow", "Length (mm)"))
        self.label_15.setText(_translate("MainWindow", "Add Base"))
        self.label_3.setText(_translate("MainWindow", "channels"))
        self.label_7.setText(_translate("MainWindow", "Loaded Channels"))
        self.groupBox.setTitle(_translate("MainWindow", "Channel Settings"))
        self.label_8.setText(_translate("MainWindow", "Radius (mm):"))
        self.label_13.setText(_translate("MainWindow", "Interior Extension"))
        self.label_9.setText(_translate("MainWindow", "Entend"))
        self.btn_channel_disable.setText(_translate("MainWindow", "Disable/Remove"))
        self.label_4.setText(_translate("MainWindow", "tandem"))
        self.label_10.setText(_translate("MainWindow", "Height"))
        self.label_11.setText(_translate("MainWindow", "Rotation"))
        self.label_5.setText(_translate("MainWindow", "export"))
        self.label_12.setText(_translate("MainWindow", "Info"))
        self.label_16.setText(_translate("MainWindow", "Data"))
        self.btn_export_file.setText(_translate("MainWindow", "export file"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
