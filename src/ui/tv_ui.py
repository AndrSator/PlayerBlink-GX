# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'tv.ui'
##
## Created by: Qt User Interface Compiler version 6.11.0
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
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtWidgets import (QApplication, QComboBox, QFrame, QGridLayout,
    QHBoxLayout, QPushButton, QSizePolicy, QSpacerItem,
    QVBoxLayout, QWidget)

class Ui_tv_view(object):
    def setupUi(self, tv_view):
        if not tv_view.objectName():
            tv_view.setObjectName(u"tv_view")
        tv_view.resize(849, 482)
        self.gridLayout = QGridLayout(tv_view)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.display = QOpenGLWidget(tv_view)
        self.display.setObjectName(u"display")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.display.sizePolicy().hasHeightForWidth())
        self.display.setSizePolicy(sizePolicy)
        self.display.setAutoFillBackground(False)
        self.display.setStyleSheet(u"")

        self.verticalLayout_6.addWidget(self.display)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btn_device_prev = QPushButton(tv_view)
        self.btn_device_prev.setObjectName(u"btn_device_prev")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_device_prev.sizePolicy().hasHeightForWidth())
        self.btn_device_prev.setSizePolicy(sizePolicy1)
        self.btn_device_prev.setMinimumSize(QSize(0, 45))
        self.btn_device_prev.setMaximumSize(QSize(16777215, 16777215))
        self.btn_device_prev.setAutoFillBackground(False)
        self.btn_device_prev.setStyleSheet(u"")
        self.btn_device_prev.setFlat(True)

        self.horizontalLayout_2.addWidget(self.btn_device_prev)

        self.btn_device_refresh = QPushButton(tv_view)
        self.btn_device_refresh.setObjectName(u"btn_device_refresh")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.btn_device_refresh.sizePolicy().hasHeightForWidth())
        self.btn_device_refresh.setSizePolicy(sizePolicy2)
        self.btn_device_refresh.setMinimumSize(QSize(0, 45))
        self.btn_device_refresh.setMaximumSize(QSize(16777215, 16777215))
        self.btn_device_refresh.setAutoFillBackground(False)
        self.btn_device_refresh.setStyleSheet(u"")
        self.btn_device_refresh.setCheckable(False)
        self.btn_device_refresh.setFlat(True)

        self.horizontalLayout_2.addWidget(self.btn_device_refresh)

        self.btn_device_next = QPushButton(tv_view)
        self.btn_device_next.setObjectName(u"btn_device_next")
        self.btn_device_next.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.btn_device_next.sizePolicy().hasHeightForWidth())
        self.btn_device_next.setSizePolicy(sizePolicy1)
        self.btn_device_next.setMinimumSize(QSize(0, 45))
        self.btn_device_next.setMaximumSize(QSize(16777215, 16777215))
        self.btn_device_next.setAutoFillBackground(False)
        self.btn_device_next.setStyleSheet(u"")
        self.btn_device_next.setFlat(True)

        self.horizontalLayout_2.addWidget(self.btn_device_next)

        self.cmb_windows_list = QComboBox(tv_view)
        self.cmb_windows_list.setObjectName(u"cmb_windows_list")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.cmb_windows_list.sizePolicy().hasHeightForWidth())
        self.cmb_windows_list.setSizePolicy(sizePolicy3)
        self.cmb_windows_list.setMinimumSize(QSize(0, 45))
        self.cmb_windows_list.setFrame(False)

        self.horizontalLayout_2.addWidget(self.cmb_windows_list)


        self.verticalLayout_6.addLayout(self.horizontalLayout_2)


        self.horizontalLayout.addLayout(self.verticalLayout_6)


        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.switch_capture = QPushButton(tv_view)
        self.switch_capture.setObjectName(u"switch_capture")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.switch_capture.sizePolicy().hasHeightForWidth())
        self.switch_capture.setSizePolicy(sizePolicy4)
        self.switch_capture.setMinimumSize(QSize(45, 45))
        self.switch_capture.setMaximumSize(QSize(45, 45))
        self.switch_capture.setFlat(True)

        self.verticalLayout_7.addWidget(self.switch_capture)

        self.switch_pause = QPushButton(tv_view)
        self.switch_pause.setObjectName(u"switch_pause")
        sizePolicy4.setHeightForWidth(self.switch_pause.sizePolicy().hasHeightForWidth())
        self.switch_pause.setSizePolicy(sizePolicy4)
        self.switch_pause.setMinimumSize(QSize(45, 45))
        self.switch_pause.setMaximumSize(QSize(45, 45))
        self.switch_pause.setFlat(True)

        self.verticalLayout_7.addWidget(self.switch_pause)

        self.btn_adjust_screen = QPushButton(tv_view)
        self.btn_adjust_screen.setObjectName(u"btn_adjust_screen")
        sizePolicy4.setHeightForWidth(self.btn_adjust_screen.sizePolicy().hasHeightForWidth())
        self.btn_adjust_screen.setSizePolicy(sizePolicy4)
        self.btn_adjust_screen.setMinimumSize(QSize(45, 45))
        self.btn_adjust_screen.setMaximumSize(QSize(45, 45))
        self.btn_adjust_screen.setIconSize(QSize(12, 12))
        self.btn_adjust_screen.setFlat(True)

        self.verticalLayout_7.addWidget(self.btn_adjust_screen)

        self.line = QFrame(tv_view)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_7.addWidget(self.line)

        self.switch_crop_tracking_area = QPushButton(tv_view)
        self.switch_crop_tracking_area.setObjectName(u"switch_crop_tracking_area")
        sizePolicy4.setHeightForWidth(self.switch_crop_tracking_area.sizePolicy().hasHeightForWidth())
        self.switch_crop_tracking_area.setSizePolicy(sizePolicy4)
        self.switch_crop_tracking_area.setMinimumSize(QSize(45, 45))
        self.switch_crop_tracking_area.setMaximumSize(QSize(45, 45))
        self.switch_crop_tracking_area.setFlat(True)

        self.verticalLayout_7.addWidget(self.switch_crop_tracking_area)

        self.switch_crop_eye = QPushButton(tv_view)
        self.switch_crop_eye.setObjectName(u"switch_crop_eye")
        sizePolicy4.setHeightForWidth(self.switch_crop_eye.sizePolicy().hasHeightForWidth())
        self.switch_crop_eye.setSizePolicy(sizePolicy4)
        self.switch_crop_eye.setMinimumSize(QSize(45, 45))
        self.switch_crop_eye.setMaximumSize(QSize(45, 45))
        self.switch_crop_eye.setFlat(True)

        self.verticalLayout_7.addWidget(self.switch_crop_eye)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_7.addItem(self.verticalSpacer)

        self.switch_monitor_mode = QPushButton(tv_view)
        self.switch_monitor_mode.setObjectName(u"switch_monitor_mode")
        self.switch_monitor_mode.setMinimumSize(QSize(45, 45))
        self.switch_monitor_mode.setMaximumSize(QSize(45, 45))
        self.switch_monitor_mode.setFlat(True)

        self.verticalLayout_7.addWidget(self.switch_monitor_mode)


        self.horizontalLayout_3.addLayout(self.verticalLayout_7)


        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 1, 1, 1)


        self.retranslateUi(tv_view)

        QMetaObject.connectSlotsByName(tv_view)
    # setupUi

    def retranslateUi(self, tv_view):
        tv_view.setWindowTitle(QCoreApplication.translate("tv_view", u"TV", None))
        self.btn_device_prev.setText(QCoreApplication.translate("tv_view", u"<", None))
        self.btn_device_refresh.setText(QCoreApplication.translate("tv_view", u"NO INPUT FOUND", None))
        self.btn_device_next.setText(QCoreApplication.translate("tv_view", u">", None))
        self.switch_capture.setText(QCoreApplication.translate("tv_view", u"CAPTURE", None))
        self.switch_pause.setText(QCoreApplication.translate("tv_view", u"PAUSE", None))
        self.btn_adjust_screen.setText(QCoreApplication.translate("tv_view", u"ADJUST", None))
        self.switch_crop_tracking_area.setText(QCoreApplication.translate("tv_view", u"ROI", None))
        self.switch_crop_eye.setText(QCoreApplication.translate("tv_view", u"CROP", None))
        self.switch_monitor_mode.setText(QCoreApplication.translate("tv_view", u"MODE", None))
    # retranslateUi

