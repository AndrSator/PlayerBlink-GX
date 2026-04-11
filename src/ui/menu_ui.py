# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'menu.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QComboBox,
    QDoubleSpinBox, QFrame, QGraphicsView, QGroupBox,
    QHBoxLayout, QLabel, QLayout, QPushButton,
    QScrollArea, QSizePolicy, QSpacerItem, QSpinBox,
    QTabWidget, QTextEdit, QVBoxLayout, QWidget)

from superqt import QDoubleRangeSlider

class Ui_menu_view(object):
    def setupUi(self, menu_view):
        if not menu_view.objectName():
            menu_view.setObjectName(u"menu_view")
        menu_view.resize(712, 567)
        self.verticalLayout_3 = QVBoxLayout(menu_view)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.tab_widget = QTabWidget(menu_view)
        self.tab_widget.setObjectName(u"tab_widget")
        self.tab_widget.setMinimumSize(QSize(700, 0))
        self.tab_widget.setTabPosition(QTabWidget.West)
        self.tab_widget.setTabShape(QTabWidget.Rounded)
        self.tab_widget.setElideMode(Qt.ElideNone)
        self.tab_widget.setUsesScrollButtons(False)
        self.tab_widget.setDocumentMode(False)
        self.tab_widget.setTabBarAutoHide(False)
        self.Main = QWidget()
        self.Main.setObjectName(u"Main")
        self.verticalLayout_4 = QVBoxLayout(self.Main)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.lbl_seed_title = QLabel(self.Main)
        self.lbl_seed_title.setObjectName(u"lbl_seed_title")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_seed_title.sizePolicy().hasHeightForWidth())
        self.lbl_seed_title.setSizePolicy(sizePolicy)
        self.lbl_seed_title.setProperty(u"title", True)

        self.verticalLayout.addWidget(self.lbl_seed_title)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.btn_4bytes_s0 = QPushButton(self.Main)
        self.btn_4bytes_s0.setObjectName(u"btn_4bytes_s0")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_4bytes_s0.sizePolicy().hasHeightForWidth())
        self.btn_4bytes_s0.setSizePolicy(sizePolicy1)
        self.btn_4bytes_s0.setMinimumSize(QSize(0, 24))
        self.btn_4bytes_s0.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_4bytes_s0.setAcceptDrops(False)
        self.btn_4bytes_s0.setProperty(u"maxLength", 4)
        self.btn_4bytes_s0.setProperty(u"frame", False)
        self.btn_4bytes_s0.setProperty(u"readOnly", True)
        self.btn_4bytes_s0.setProperty(u"class", u"seedValue")

        self.horizontalLayout_3.addWidget(self.btn_4bytes_s0)

        self.btn_4bytes_s1 = QPushButton(self.Main)
        self.btn_4bytes_s1.setObjectName(u"btn_4bytes_s1")
        sizePolicy1.setHeightForWidth(self.btn_4bytes_s1.sizePolicy().hasHeightForWidth())
        self.btn_4bytes_s1.setSizePolicy(sizePolicy1)
        self.btn_4bytes_s1.setMinimumSize(QSize(0, 24))
        self.btn_4bytes_s1.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_4bytes_s1.setAcceptDrops(False)
        self.btn_4bytes_s1.setProperty(u"maxLength", 4)
        self.btn_4bytes_s1.setProperty(u"frame", False)
        self.btn_4bytes_s1.setProperty(u"readOnly", True)
        self.btn_4bytes_s1.setProperty(u"class", u"seedValue")

        self.horizontalLayout_3.addWidget(self.btn_4bytes_s1)

        self.btn_4bytes_s2 = QPushButton(self.Main)
        self.btn_4bytes_s2.setObjectName(u"btn_4bytes_s2")
        sizePolicy1.setHeightForWidth(self.btn_4bytes_s2.sizePolicy().hasHeightForWidth())
        self.btn_4bytes_s2.setSizePolicy(sizePolicy1)
        self.btn_4bytes_s2.setMinimumSize(QSize(0, 24))
        self.btn_4bytes_s2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_4bytes_s2.setAcceptDrops(False)
        self.btn_4bytes_s2.setProperty(u"maxLength", 4)
        self.btn_4bytes_s2.setProperty(u"frame", False)
        self.btn_4bytes_s2.setProperty(u"readOnly", True)
        self.btn_4bytes_s2.setProperty(u"class", u"seedValue")

        self.horizontalLayout_3.addWidget(self.btn_4bytes_s2)

        self.btn_4bytes_s3 = QPushButton(self.Main)
        self.btn_4bytes_s3.setObjectName(u"btn_4bytes_s3")
        sizePolicy1.setHeightForWidth(self.btn_4bytes_s3.sizePolicy().hasHeightForWidth())
        self.btn_4bytes_s3.setSizePolicy(sizePolicy1)
        self.btn_4bytes_s3.setMinimumSize(QSize(0, 24))
        self.btn_4bytes_s3.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_4bytes_s3.setAcceptDrops(False)
        self.btn_4bytes_s3.setProperty(u"maxLength", 4)
        self.btn_4bytes_s3.setProperty(u"frame", False)
        self.btn_4bytes_s3.setProperty(u"readOnly", True)
        self.btn_4bytes_s3.setProperty(u"class", u"seedValue")

        self.horizontalLayout_3.addWidget(self.btn_4bytes_s3)

        self.btn_8bytes_s0 = QPushButton(self.Main)
        self.btn_8bytes_s0.setObjectName(u"btn_8bytes_s0")
        sizePolicy1.setHeightForWidth(self.btn_8bytes_s0.sizePolicy().hasHeightForWidth())
        self.btn_8bytes_s0.setSizePolicy(sizePolicy1)
        self.btn_8bytes_s0.setMinimumSize(QSize(0, 24))
        self.btn_8bytes_s0.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_8bytes_s0.setAcceptDrops(False)
        self.btn_8bytes_s0.setProperty(u"maxLength", 4)
        self.btn_8bytes_s0.setProperty(u"frame", False)
        self.btn_8bytes_s0.setProperty(u"readOnly", True)
        self.btn_8bytes_s0.setProperty(u"class", u"seedValue")

        self.horizontalLayout_3.addWidget(self.btn_8bytes_s0)

        self.btn_8bytes_s1 = QPushButton(self.Main)
        self.btn_8bytes_s1.setObjectName(u"btn_8bytes_s1")
        sizePolicy1.setHeightForWidth(self.btn_8bytes_s1.sizePolicy().hasHeightForWidth())
        self.btn_8bytes_s1.setSizePolicy(sizePolicy1)
        self.btn_8bytes_s1.setMinimumSize(QSize(0, 24))
        self.btn_8bytes_s1.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_8bytes_s1.setAcceptDrops(False)
        self.btn_8bytes_s1.setProperty(u"maxLength", 4)
        self.btn_8bytes_s1.setProperty(u"frame", False)
        self.btn_8bytes_s1.setProperty(u"readOnly", True)
        self.btn_8bytes_s1.setProperty(u"class", u"seedValue")

        self.horizontalLayout_3.addWidget(self.btn_8bytes_s1)

        self.switch_seed_display = QPushButton(self.Main)
        self.switch_seed_display.setObjectName(u"switch_seed_display")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.switch_seed_display.sizePolicy().hasHeightForWidth())
        self.switch_seed_display.setSizePolicy(sizePolicy2)
        self.switch_seed_display.setMinimumSize(QSize(0, 0))
        self.switch_seed_display.setMaximumSize(QSize(45, 45))
        self.switch_seed_display.setFlat(True)

        self.horizontalLayout_3.addWidget(self.switch_seed_display)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.line_2 = QFrame(self.Main)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout.addWidget(self.line_2)

        self.lbl_reident_title = QLabel(self.Main)
        self.lbl_reident_title.setObjectName(u"lbl_reident_title")
        sizePolicy.setHeightForWidth(self.lbl_reident_title.sizePolicy().hasHeightForWidth())
        self.lbl_reident_title.setSizePolicy(sizePolicy)
        self.lbl_reident_title.setProperty(u"title", True)

        self.verticalLayout.addWidget(self.lbl_reident_title)

        self.rslider_reident_range = QDoubleRangeSlider(self.Main)
        self.rslider_reident_range.setObjectName(u"rslider_reident_range")
        sizePolicy.setHeightForWidth(self.rslider_reident_range.sizePolicy().hasHeightForWidth())
        self.rslider_reident_range.setSizePolicy(sizePolicy)
        self.rslider_reident_range.setMinimumSize(QSize(0, 20))

        self.verticalLayout.addWidget(self.rslider_reident_range)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.lbl_reident_min = QLabel(self.Main)
        self.lbl_reident_min.setObjectName(u"lbl_reident_min")

        self.horizontalLayout_4.addWidget(self.lbl_reident_min)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.lbl_reident_max = QLabel(self.Main)
        self.lbl_reident_max.setObjectName(u"lbl_reident_max")

        self.horizontalLayout_4.addWidget(self.lbl_reident_max)


        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.switch_tracking = QPushButton(self.Main)
        self.switch_tracking.setObjectName(u"switch_tracking")
        self.switch_tracking.setEnabled(False)
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.switch_tracking.sizePolicy().hasHeightForWidth())
        self.switch_tracking.setSizePolicy(sizePolicy3)
        self.switch_tracking.setMinimumSize(QSize(75, 75))
        self.switch_tracking.setStyleSheet(u"")
        self.switch_tracking.setFlat(True)

        self.horizontalLayout_5.addWidget(self.switch_tracking)

        self.switch_tracking_tidsid = QPushButton(self.Main)
        self.switch_tracking_tidsid.setObjectName(u"switch_tracking_tidsid")
        self.switch_tracking_tidsid.setEnabled(False)
        sizePolicy3.setHeightForWidth(self.switch_tracking_tidsid.sizePolicy().hasHeightForWidth())
        self.switch_tracking_tidsid.setSizePolicy(sizePolicy3)
        self.switch_tracking_tidsid.setMinimumSize(QSize(75, 75))
        self.switch_tracking_tidsid.setFlat(True)

        self.horizontalLayout_5.addWidget(self.switch_tracking_tidsid)

        self.btn_reidentify = QPushButton(self.Main)
        self.btn_reidentify.setObjectName(u"btn_reidentify")
        self.btn_reidentify.setEnabled(False)
        sizePolicy3.setHeightForWidth(self.btn_reidentify.sizePolicy().hasHeightForWidth())
        self.btn_reidentify.setSizePolicy(sizePolicy3)
        self.btn_reidentify.setMinimumSize(QSize(75, 75))
        self.btn_reidentify.setFlat(True)

        self.horizontalLayout_5.addWidget(self.btn_reidentify)


        self.verticalLayout.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.btn_start_countdown = QPushButton(self.Main)
        self.btn_start_countdown.setObjectName(u"btn_start_countdown")
        self.btn_start_countdown.setEnabled(False)
        sizePolicy3.setHeightForWidth(self.btn_start_countdown.sizePolicy().hasHeightForWidth())
        self.btn_start_countdown.setSizePolicy(sizePolicy3)
        self.btn_start_countdown.setMinimumSize(QSize(75, 75))
        self.btn_start_countdown.setFlat(True)

        self.horizontalLayout_31.addWidget(self.btn_start_countdown)


        self.verticalLayout.addLayout(self.horizontalLayout_31)

        self.widget = QWidget(self.Main)
        self.widget.setObjectName(u"widget")
        sizePolicy3.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy3)
        self.widget.setMinimumSize(QSize(150, 150))
        self.verticalLayout_14 = QVBoxLayout(self.widget)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.placeholder_countdown_display = QWidget(self.widget)
        self.placeholder_countdown_display.setObjectName(u"placeholder_countdown_display")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.placeholder_countdown_display.sizePolicy().hasHeightForWidth())
        self.placeholder_countdown_display.setSizePolicy(sizePolicy4)
        self.placeholder_countdown_display.setMinimumSize(QSize(150, 150))

        self.verticalLayout_14.addWidget(self.placeholder_countdown_display)


        self.verticalLayout.addWidget(self.widget)

        self.chkb_auto_start_countdown = QCheckBox(self.Main)
        self.chkb_auto_start_countdown.setObjectName(u"chkb_auto_start_countdown")

        self.verticalLayout.addWidget(self.chkb_auto_start_countdown)

        self.verticalSpacer_6 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer_6)


        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.line_5 = QFrame(self.Main)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.VLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_2.addWidget(self.line_5)

        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.lbl_calibration_title = QLabel(self.Main)
        self.lbl_calibration_title.setObjectName(u"lbl_calibration_title")
        sizePolicy.setHeightForWidth(self.lbl_calibration_title.sizePolicy().hasHeightForWidth())
        self.lbl_calibration_title.setSizePolicy(sizePolicy)
        self.lbl_calibration_title.setProperty(u"title", True)

        self.verticalLayout_2.addWidget(self.lbl_calibration_title)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_5 = QLabel(self.Main)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_10.addWidget(self.label_5)

        self.spin_advance_target = QSpinBox(self.Main)
        self.spin_advance_target.setObjectName(u"spin_advance_target")
        self.spin_advance_target.setFrame(False)
        self.spin_advance_target.setAlignment(Qt.AlignCenter)
        self.spin_advance_target.setReadOnly(False)
        self.spin_advance_target.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spin_advance_target.setSpecialValueText(u"")
        self.spin_advance_target.setKeyboardTracking(False)
        self.spin_advance_target.setMinimum(1)
        self.spin_advance_target.setMaximum(1000000)
        self.spin_advance_target.setValue(1000)

        self.horizontalLayout_10.addWidget(self.spin_advance_target)


        self.verticalLayout_2.addLayout(self.horizontalLayout_10)

        self.lbl_adv_trgt_eta = QLabel(self.Main)
        self.lbl_adv_trgt_eta.setObjectName(u"lbl_adv_trgt_eta")
        self.lbl_adv_trgt_eta.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lbl_adv_trgt_eta.setProperty(u"smallText", True)

        self.verticalLayout_2.addWidget(self.lbl_adv_trgt_eta)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.label = QLabel(self.Main)
        self.label.setObjectName(u"label")

        self.horizontalLayout_6.addWidget(self.label)

        self.spin_final_a_press_delay = QSpinBox(self.Main)
        self.spin_final_a_press_delay.setObjectName(u"spin_final_a_press_delay")
        self.spin_final_a_press_delay.setFrame(False)
        self.spin_final_a_press_delay.setAlignment(Qt.AlignCenter)
        self.spin_final_a_press_delay.setReadOnly(False)
        self.spin_final_a_press_delay.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spin_final_a_press_delay.setSpecialValueText(u"")
        self.spin_final_a_press_delay.setKeyboardTracking(False)
        self.spin_final_a_press_delay.setMinimum(0)
        self.spin_final_a_press_delay.setMaximum(1000000)
        self.spin_final_a_press_delay.setValue(0)

        self.horizontalLayout_6.addWidget(self.spin_final_a_press_delay)


        self.verticalLayout_2.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_4 = QLabel(self.Main)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_9.addWidget(self.label_4)

        self.spin_timeline_buffer = QSpinBox(self.Main)
        self.spin_timeline_buffer.setObjectName(u"spin_timeline_buffer")
        self.spin_timeline_buffer.setFrame(False)
        self.spin_timeline_buffer.setAlignment(Qt.AlignCenter)
        self.spin_timeline_buffer.setReadOnly(False)
        self.spin_timeline_buffer.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spin_timeline_buffer.setSpecialValueText(u"")
        self.spin_timeline_buffer.setKeyboardTracking(False)
        self.spin_timeline_buffer.setMinimum(0)
        self.spin_timeline_buffer.setMaximum(1000000)
        self.spin_timeline_buffer.setValue(0)

        self.horizontalLayout_9.addWidget(self.spin_timeline_buffer)


        self.verticalLayout_2.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_6 = QLabel(self.Main)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_11.addWidget(self.label_6)

        self.lbl_timeline_start = QLabel(self.Main)
        self.lbl_timeline_start.setObjectName(u"lbl_timeline_start")
        self.lbl_timeline_start.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_11.addWidget(self.lbl_timeline_start)


        self.verticalLayout_2.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_7 = QLabel(self.Main)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_12.addWidget(self.label_7)

        self.lbl_press_a = QLabel(self.Main)
        self.lbl_press_a.setObjectName(u"lbl_press_a")
        self.lbl_press_a.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_12.addWidget(self.lbl_press_a)


        self.verticalLayout_2.addLayout(self.horizontalLayout_12)

        self.chkb_plus_one_menu_close = QCheckBox(self.Main)
        self.chkb_plus_one_menu_close.setObjectName(u"chkb_plus_one_menu_close")
        self.chkb_plus_one_menu_close.setChecked(True)
        self.chkb_plus_one_menu_close.setTristate(False)

        self.verticalLayout_2.addWidget(self.chkb_plus_one_menu_close)

        self.line_9 = QFrame(self.Main)
        self.line_9.setObjectName(u"line_9")
        self.line_9.setFrameShape(QFrame.Shape.HLine)
        self.line_9.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line_9)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.lbl_time_delay = QLabel(self.Main)
        self.lbl_time_delay.setObjectName(u"lbl_time_delay")

        self.horizontalLayout_13.addWidget(self.lbl_time_delay)

        self.spin_time_delay = QDoubleSpinBox(self.Main)
        self.spin_time_delay.setObjectName(u"spin_time_delay")
        self.spin_time_delay.setFrame(False)
        self.spin_time_delay.setAlignment(Qt.AlignCenter)
        self.spin_time_delay.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spin_time_delay.setDecimals(2)

        self.horizontalLayout_13.addWidget(self.spin_time_delay)


        self.verticalLayout_2.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.lbl_advance_delay = QLabel(self.Main)
        self.lbl_advance_delay.setObjectName(u"lbl_advance_delay")

        self.horizontalLayout_15.addWidget(self.lbl_advance_delay)

        self.spin_advance_delay = QSpinBox(self.Main)
        self.spin_advance_delay.setObjectName(u"spin_advance_delay")
        self.spin_advance_delay.setFrame(False)
        self.spin_advance_delay.setAlignment(Qt.AlignCenter)
        self.spin_advance_delay.setReadOnly(False)
        self.spin_advance_delay.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spin_advance_delay.setSpecialValueText(u"")
        self.spin_advance_delay.setKeyboardTracking(False)
        self.spin_advance_delay.setMinimum(0)
        self.spin_advance_delay.setMaximum(1000)
        self.spin_advance_delay.setValue(0)

        self.horizontalLayout_15.addWidget(self.spin_advance_delay)


        self.verticalLayout_2.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.lbl_advance_delay_2 = QLabel(self.Main)
        self.lbl_advance_delay_2.setObjectName(u"lbl_advance_delay_2")

        self.horizontalLayout_19.addWidget(self.lbl_advance_delay_2)

        self.spin_advance_delay_2 = QSpinBox(self.Main)
        self.spin_advance_delay_2.setObjectName(u"spin_advance_delay_2")
        self.spin_advance_delay_2.setFrame(False)
        self.spin_advance_delay_2.setAlignment(Qt.AlignCenter)
        self.spin_advance_delay_2.setReadOnly(False)
        self.spin_advance_delay_2.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spin_advance_delay_2.setSpecialValueText(u"")
        self.spin_advance_delay_2.setKeyboardTracking(False)
        self.spin_advance_delay_2.setMinimum(0)
        self.spin_advance_delay_2.setMaximum(1000)
        self.spin_advance_delay_2.setValue(0)

        self.horizontalLayout_19.addWidget(self.spin_advance_delay_2)


        self.verticalLayout_2.addLayout(self.horizontalLayout_19)

        self.line_10 = QFrame(self.Main)
        self.line_10.setObjectName(u"line_10")
        self.line_10.setFrameShape(QFrame.Shape.HLine)
        self.line_10.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_2.addWidget(self.line_10)

        self.lbl_noise_title = QLabel(self.Main)
        self.lbl_noise_title.setObjectName(u"lbl_noise_title")
        sizePolicy.setHeightForWidth(self.lbl_noise_title.sizePolicy().hasHeightForWidth())
        self.lbl_noise_title.setSizePolicy(sizePolicy)
        self.lbl_noise_title.setProperty(u"title", True)

        self.verticalLayout_2.addWidget(self.lbl_noise_title)

        self.chkb_reident_pkmn_npc = QCheckBox(self.Main)
        self.chkb_reident_pkmn_npc.setObjectName(u"chkb_reident_pkmn_npc")

        self.verticalLayout_2.addWidget(self.chkb_reident_pkmn_npc)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.lbl_npcs = QLabel(self.Main)
        self.lbl_npcs.setObjectName(u"lbl_npcs")

        self.horizontalLayout_20.addWidget(self.lbl_npcs)

        self.spin_npcs = QSpinBox(self.Main)
        self.spin_npcs.setObjectName(u"spin_npcs")
        self.spin_npcs.setFrame(False)
        self.spin_npcs.setAlignment(Qt.AlignCenter)
        self.spin_npcs.setReadOnly(False)
        self.spin_npcs.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spin_npcs.setSpecialValueText(u"")
        self.spin_npcs.setKeyboardTracking(False)
        self.spin_npcs.setMinimum(0)
        self.spin_npcs.setMaximum(50)
        self.spin_npcs.setValue(0)

        self.horizontalLayout_20.addWidget(self.spin_npcs)


        self.verticalLayout_2.addLayout(self.horizontalLayout_20)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.lbl_npcs_during_countdown = QLabel(self.Main)
        self.lbl_npcs_during_countdown.setObjectName(u"lbl_npcs_during_countdown")

        self.horizontalLayout_21.addWidget(self.lbl_npcs_during_countdown)

        self.spin_npcs_countdown = QSpinBox(self.Main)
        self.spin_npcs_countdown.setObjectName(u"spin_npcs_countdown")
        self.spin_npcs_countdown.setFrame(False)
        self.spin_npcs_countdown.setAlignment(Qt.AlignCenter)
        self.spin_npcs_countdown.setReadOnly(False)
        self.spin_npcs_countdown.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spin_npcs_countdown.setSpecialValueText(u"")
        self.spin_npcs_countdown.setKeyboardTracking(False)
        self.spin_npcs_countdown.setMinimum(0)
        self.spin_npcs_countdown.setMaximum(50)
        self.spin_npcs_countdown.setValue(0)

        self.horizontalLayout_21.addWidget(self.spin_npcs_countdown)


        self.verticalLayout_2.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.lbl_pkmn_npcs = QLabel(self.Main)
        self.lbl_pkmn_npcs.setObjectName(u"lbl_pkmn_npcs")

        self.horizontalLayout_22.addWidget(self.lbl_pkmn_npcs)

        self.spin_pkmn_npcs_countdown = QSpinBox(self.Main)
        self.spin_pkmn_npcs_countdown.setObjectName(u"spin_pkmn_npcs_countdown")
        self.spin_pkmn_npcs_countdown.setFrame(False)
        self.spin_pkmn_npcs_countdown.setAlignment(Qt.AlignCenter)
        self.spin_pkmn_npcs_countdown.setReadOnly(False)
        self.spin_pkmn_npcs_countdown.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spin_pkmn_npcs_countdown.setSpecialValueText(u"")
        self.spin_pkmn_npcs_countdown.setKeyboardTracking(False)
        self.spin_pkmn_npcs_countdown.setMinimum(0)
        self.spin_pkmn_npcs_countdown.setMaximum(50)
        self.spin_pkmn_npcs_countdown.setValue(0)

        self.horizontalLayout_22.addWidget(self.spin_pkmn_npcs_countdown)


        self.verticalLayout_2.addLayout(self.horizontalLayout_22)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label_2 = QLabel(self.Main)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_7.addWidget(self.label_2)

        self.spin_manual_advance = QSpinBox(self.Main)
        self.spin_manual_advance.setObjectName(u"spin_manual_advance")
        self.spin_manual_advance.setFrame(False)
        self.spin_manual_advance.setAlignment(Qt.AlignCenter)
        self.spin_manual_advance.setReadOnly(False)
        self.spin_manual_advance.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spin_manual_advance.setSpecialValueText(u"")
        self.spin_manual_advance.setKeyboardTracking(False)
        self.spin_manual_advance.setMinimum(1)
        self.spin_manual_advance.setMaximum(1000000)
        self.spin_manual_advance.setValue(165)

        self.horizontalLayout_7.addWidget(self.spin_manual_advance)


        self.verticalLayout_2.addLayout(self.horizontalLayout_7)


        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.line_7 = QFrame(self.Main)
        self.line_7.setObjectName(u"line_7")
        self.line_7.setFrameShape(QFrame.Shape.VLine)
        self.line_7.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_2.addWidget(self.line_7)

        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setSizeConstraint(QLayout.SetMinimumSize)
        self.lbl_timeline_title = QLabel(self.Main)
        self.lbl_timeline_title.setObjectName(u"lbl_timeline_title")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.lbl_timeline_title.sizePolicy().hasHeightForWidth())
        self.lbl_timeline_title.setSizePolicy(sizePolicy5)
        self.lbl_timeline_title.setProperty(u"title", True)

        self.verticalLayout_7.addWidget(self.lbl_timeline_title)

        self.groupBox = QGroupBox(self.Main)
        self.groupBox.setObjectName(u"groupBox")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy6)
        self.groupBox.setMinimumSize(QSize(150, 300))
        self.groupBox.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_8 = QVBoxLayout(self.groupBox)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.scrollArea = QScrollArea(self.groupBox)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setMinimumSize(QSize(0, 0))
        self.scrollArea.setMaximumSize(QSize(16777215, 16777215))
        self.scrollArea.setStyleSheet(u"")
        self.scrollArea.setFrameShape(QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QFrame.Plain)
        self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(Qt.AlignCenter)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 148, 412))
        self.verticalLayout_11 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.list_advance_timeline = QVBoxLayout()
        self.list_advance_timeline.setSpacing(0)
        self.list_advance_timeline.setObjectName(u"list_advance_timeline")

        self.verticalLayout_11.addLayout(self.list_advance_timeline)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_8.addWidget(self.scrollArea)


        self.verticalLayout_7.addWidget(self.groupBox)

        self.btn_stop_timeline = QPushButton(self.Main)
        self.btn_stop_timeline.setObjectName(u"btn_stop_timeline")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.btn_stop_timeline.sizePolicy().hasHeightForWidth())
        self.btn_stop_timeline.setSizePolicy(sizePolicy7)
        self.btn_stop_timeline.setStyleSheet(u"")
        self.btn_stop_timeline.setFlat(True)

        self.verticalLayout_7.addWidget(self.btn_stop_timeline)


        self.horizontalLayout_2.addLayout(self.verticalLayout_7)

        self.line_6 = QFrame(self.Main)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_2.addWidget(self.line_6)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.placeholder_tracking_progress = QWidget(self.Main)
        self.placeholder_tracking_progress.setObjectName(u"placeholder_tracking_progress")
        sizePolicy2.setHeightForWidth(self.placeholder_tracking_progress.sizePolicy().hasHeightForWidth())
        self.placeholder_tracking_progress.setSizePolicy(sizePolicy2)
        self.placeholder_tracking_progress.setMinimumSize(QSize(0, 20))
        self.placeholder_tracking_progress.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_4.addWidget(self.placeholder_tracking_progress)

        self.tab_widget.addTab(self.Main, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.Main), u"Main")
        self.EyeManager = QWidget()
        self.EyeManager.setObjectName(u"EyeManager")
        self.verticalLayout_9 = QVBoxLayout(self.EyeManager)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.placeholder_eye_manager = QWidget(self.EyeManager)
        self.placeholder_eye_manager.setObjectName(u"placeholder_eye_manager")
        sizePolicy4.setHeightForWidth(self.placeholder_eye_manager.sizePolicy().hasHeightForWidth())
        self.placeholder_eye_manager.setSizePolicy(sizePolicy4)

        self.horizontalLayout.addWidget(self.placeholder_eye_manager)

        self.line_4 = QFrame(self.EyeManager)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setFrameShape(QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout.addWidget(self.line_4)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.btn_create_resource = QPushButton(self.EyeManager)
        self.btn_create_resource.setObjectName(u"btn_create_resource")
        sizePolicy8 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.btn_create_resource.sizePolicy().hasHeightForWidth())
        self.btn_create_resource.setSizePolicy(sizePolicy8)
        self.btn_create_resource.setMinimumSize(QSize(45, 45))
        self.btn_create_resource.setMaximumSize(QSize(45, 45))
        self.btn_create_resource.setFlat(True)

        self.verticalLayout_10.addWidget(self.btn_create_resource)

        self.btn_delete_resource = QPushButton(self.EyeManager)
        self.btn_delete_resource.setObjectName(u"btn_delete_resource")
        sizePolicy8.setHeightForWidth(self.btn_delete_resource.sizePolicy().hasHeightForWidth())
        self.btn_delete_resource.setSizePolicy(sizePolicy8)
        self.btn_delete_resource.setMinimumSize(QSize(45, 45))
        self.btn_delete_resource.setMaximumSize(QSize(45, 45))
        self.btn_delete_resource.setFlat(True)

        self.verticalLayout_10.addWidget(self.btn_delete_resource)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout_10)


        self.verticalLayout_9.addLayout(self.horizontalLayout)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.switch_preview_tracking = QPushButton(self.EyeManager)
        self.switch_preview_tracking.setObjectName(u"switch_preview_tracking")
        self.switch_preview_tracking.setStyleSheet(u"")
        self.switch_preview_tracking.setFlat(True)

        self.horizontalLayout_14.addWidget(self.switch_preview_tracking)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_2)

        self.label_9 = QLabel(self.EyeManager)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_14.addWidget(self.label_9)

        self.doubleSpinBox = QDoubleSpinBox(self.EyeManager)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        sizePolicy2.setHeightForWidth(self.doubleSpinBox.sizePolicy().hasHeightForWidth())
        self.doubleSpinBox.setSizePolicy(sizePolicy2)
        self.doubleSpinBox.setFrame(False)
        self.doubleSpinBox.setAlignment(Qt.AlignCenter)
        self.doubleSpinBox.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.doubleSpinBox.setKeyboardTracking(False)
        self.doubleSpinBox.setDecimals(1)
        self.doubleSpinBox.setMaximum(1.000000000000000)
        self.doubleSpinBox.setValue(0.900000000000000)

        self.horizontalLayout_14.addWidget(self.doubleSpinBox)


        self.verticalLayout_9.addLayout(self.horizontalLayout_14)

        self.tab_widget.addTab(self.EyeManager, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.EyeManager), u"EyeManager")
        self.Config = QWidget()
        self.Config.setObjectName(u"Config")
        self.verticalLayout_6 = QVBoxLayout(self.Config)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.lbl_config_title = QLabel(self.Config)
        self.lbl_config_title.setObjectName(u"lbl_config_title")
        sizePolicy.setHeightForWidth(self.lbl_config_title.sizePolicy().hasHeightForWidth())
        self.lbl_config_title.setSizePolicy(sizePolicy)
        self.lbl_config_title.setProperty(u"title", True)

        self.verticalLayout_12.addWidget(self.lbl_config_title)

        self.cmb_config = QComboBox(self.Config)
        self.cmb_config.setObjectName(u"cmb_config")

        self.verticalLayout_12.addWidget(self.cmb_config)

        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.textEdit = QTextEdit(self.Config)
        self.textEdit.setObjectName(u"textEdit")
        sizePolicy3.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy3)
        self.textEdit.setMaximumSize(QSize(16777215, 100))

        self.horizontalLayout_30.addWidget(self.textEdit)

        self.gv_img_preview = QGraphicsView(self.Config)
        self.gv_img_preview.setObjectName(u"gv_img_preview")
        sizePolicy8.setHeightForWidth(self.gv_img_preview.sizePolicy().hasHeightForWidth())
        self.gv_img_preview.setSizePolicy(sizePolicy8)
        self.gv_img_preview.setMaximumSize(QSize(100, 100))

        self.horizontalLayout_30.addWidget(self.gv_img_preview)


        self.verticalLayout_12.addLayout(self.horizontalLayout_30)

        self.line_11 = QFrame(self.Config)
        self.line_11.setObjectName(u"line_11")
        self.line_11.setFrameShape(QFrame.Shape.HLine)
        self.line_11.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_12.addWidget(self.line_11)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.lbl_cfg_roi = QLabel(self.Config)
        self.lbl_cfg_roi.setObjectName(u"lbl_cfg_roi")

        self.horizontalLayout_17.addWidget(self.lbl_cfg_roi)

        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_17.addItem(self.horizontalSpacer_3)

        self.lbl_cfg_roi_value = QLabel(self.Config)
        self.lbl_cfg_roi_value.setObjectName(u"lbl_cfg_roi_value")

        self.horizontalLayout_17.addWidget(self.lbl_cfg_roi_value)


        self.verticalLayout_12.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.lbl_cfg_threshold = QLabel(self.Config)
        self.lbl_cfg_threshold.setObjectName(u"lbl_cfg_threshold")

        self.horizontalLayout_23.addWidget(self.lbl_cfg_threshold)

        self.horizontalSpacer_6 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_23.addItem(self.horizontalSpacer_6)

        self.lbl_cfg_threshold_value = QLabel(self.Config)
        self.lbl_cfg_threshold_value.setObjectName(u"lbl_cfg_threshold_value")

        self.horizontalLayout_23.addWidget(self.lbl_cfg_threshold_value)


        self.verticalLayout_12.addLayout(self.horizontalLayout_23)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.lbl_cfg_plus_one_menu_close = QLabel(self.Config)
        self.lbl_cfg_plus_one_menu_close.setObjectName(u"lbl_cfg_plus_one_menu_close")

        self.horizontalLayout_24.addWidget(self.lbl_cfg_plus_one_menu_close)

        self.horizontalSpacer_7 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_24.addItem(self.horizontalSpacer_7)

        self.lbl_cfg_plus_one_menu_close_value = QLabel(self.Config)
        self.lbl_cfg_plus_one_menu_close_value.setObjectName(u"lbl_cfg_plus_one_menu_close_value")

        self.horizontalLayout_24.addWidget(self.lbl_cfg_plus_one_menu_close_value)


        self.verticalLayout_12.addLayout(self.horizontalLayout_24)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.lbl_cfg_final_a_press_delay = QLabel(self.Config)
        self.lbl_cfg_final_a_press_delay.setObjectName(u"lbl_cfg_final_a_press_delay")

        self.horizontalLayout_25.addWidget(self.lbl_cfg_final_a_press_delay)

        self.horizontalSpacer_8 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_25.addItem(self.horizontalSpacer_8)

        self.lbl_cfg_final_a_press_delay_value = QLabel(self.Config)
        self.lbl_cfg_final_a_press_delay_value.setObjectName(u"lbl_cfg_final_a_press_delay_value")

        self.horizontalLayout_25.addWidget(self.lbl_cfg_final_a_press_delay_value)


        self.verticalLayout_12.addLayout(self.horizontalLayout_25)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.lbl_timeline_buffer = QLabel(self.Config)
        self.lbl_timeline_buffer.setObjectName(u"lbl_timeline_buffer")

        self.horizontalLayout_26.addWidget(self.lbl_timeline_buffer)

        self.horizontalSpacer_9 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_26.addItem(self.horizontalSpacer_9)

        self.lbl_timeline_buffer_value = QLabel(self.Config)
        self.lbl_timeline_buffer_value.setObjectName(u"lbl_timeline_buffer_value")

        self.horizontalLayout_26.addWidget(self.lbl_timeline_buffer_value)


        self.verticalLayout_12.addLayout(self.horizontalLayout_26)

        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.lbl_cfg_npcs = QLabel(self.Config)
        self.lbl_cfg_npcs.setObjectName(u"lbl_cfg_npcs")

        self.horizontalLayout_27.addWidget(self.lbl_cfg_npcs)

        self.horizontalSpacer_10 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_27.addItem(self.horizontalSpacer_10)

        self.lbl_cfg_npcs_value = QLabel(self.Config)
        self.lbl_cfg_npcs_value.setObjectName(u"lbl_cfg_npcs_value")

        self.horizontalLayout_27.addWidget(self.lbl_cfg_npcs_value)


        self.verticalLayout_12.addLayout(self.horizontalLayout_27)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.lbl_cfg_npcs_cd = QLabel(self.Config)
        self.lbl_cfg_npcs_cd.setObjectName(u"lbl_cfg_npcs_cd")

        self.horizontalLayout_28.addWidget(self.lbl_cfg_npcs_cd)

        self.horizontalSpacer_11 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_28.addItem(self.horizontalSpacer_11)

        self.lbl_cfg_npcs_cd_value = QLabel(self.Config)
        self.lbl_cfg_npcs_cd_value.setObjectName(u"lbl_cfg_npcs_cd_value")

        self.horizontalLayout_28.addWidget(self.lbl_cfg_npcs_cd_value)


        self.verticalLayout_12.addLayout(self.horizontalLayout_28)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.lbl_cfg_pkmn_npcs = QLabel(self.Config)
        self.lbl_cfg_pkmn_npcs.setObjectName(u"lbl_cfg_pkmn_npcs")

        self.horizontalLayout_29.addWidget(self.lbl_cfg_pkmn_npcs)

        self.horizontalSpacer_12 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_29.addItem(self.horizontalSpacer_12)

        self.lbl_cfg_pkmn_npcs_countdown_value = QLabel(self.Config)
        self.lbl_cfg_pkmn_npcs_countdown_value.setObjectName(u"lbl_cfg_pkmn_npcs_countdown_value")

        self.horizontalLayout_29.addWidget(self.lbl_cfg_pkmn_npcs_countdown_value)


        self.verticalLayout_12.addLayout(self.horizontalLayout_29)

        self.verticalSpacer_5 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_12.addItem(self.verticalSpacer_5)


        self.horizontalLayout_8.addLayout(self.verticalLayout_12)

        self.line_8 = QFrame(self.Config)
        self.line_8.setObjectName(u"line_8")
        self.line_8.setFrameShape(QFrame.Shape.VLine)
        self.line_8.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_8.addWidget(self.line_8)

        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.btn_create_config = QPushButton(self.Config)
        self.btn_create_config.setObjectName(u"btn_create_config")
        sizePolicy8.setHeightForWidth(self.btn_create_config.sizePolicy().hasHeightForWidth())
        self.btn_create_config.setSizePolicy(sizePolicy8)
        self.btn_create_config.setMinimumSize(QSize(45, 45))
        self.btn_create_config.setMaximumSize(QSize(45, 45))
        self.btn_create_config.setFlat(True)

        self.verticalLayout_13.addWidget(self.btn_create_config)

        self.line_3 = QFrame(self.Config)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_13.addWidget(self.line_3)

        self.btn_save_config = QPushButton(self.Config)
        self.btn_save_config.setObjectName(u"btn_save_config")
        sizePolicy8.setHeightForWidth(self.btn_save_config.sizePolicy().hasHeightForWidth())
        self.btn_save_config.setSizePolicy(sizePolicy8)
        self.btn_save_config.setMinimumSize(QSize(45, 45))
        self.btn_save_config.setMaximumSize(QSize(45, 45))
        self.btn_save_config.setFlat(True)

        self.verticalLayout_13.addWidget(self.btn_save_config)

        self.btn_load_config = QPushButton(self.Config)
        self.btn_load_config.setObjectName(u"btn_load_config")
        sizePolicy8.setHeightForWidth(self.btn_load_config.sizePolicy().hasHeightForWidth())
        self.btn_load_config.setSizePolicy(sizePolicy8)
        self.btn_load_config.setMinimumSize(QSize(45, 45))
        self.btn_load_config.setMaximumSize(QSize(45, 45))
        self.btn_load_config.setFlat(True)

        self.verticalLayout_13.addWidget(self.btn_load_config)

        self.verticalSpacer_2 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_13.addItem(self.verticalSpacer_2)


        self.horizontalLayout_8.addLayout(self.verticalLayout_13)


        self.verticalLayout_6.addLayout(self.horizontalLayout_8)

        self.tab_widget.addTab(self.Config, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.Config), u"Config")
        self.Preferences = QWidget()
        self.Preferences.setObjectName(u"Preferences")
        self.tab_widget.addTab(self.Preferences, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.Preferences), u"Preferences")
        self.Debug = QWidget()
        self.Debug.setObjectName(u"Debug")
        self.verticalLayout_5 = QVBoxLayout(self.Debug)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.btn_generate_blinks = QPushButton(self.Debug)
        self.btn_generate_blinks.setObjectName(u"btn_generate_blinks")

        self.verticalLayout_5.addWidget(self.btn_generate_blinks)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_4)

        self.tab_widget.addTab(self.Debug, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.Debug), u"Debug")

        self.verticalLayout_3.addWidget(self.tab_widget)

        self.line = QFrame(menu_view)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalSpacer_4 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_4)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.btn_eye_manager = QPushButton(menu_view)
        self.btn_eye_manager.setObjectName(u"btn_eye_manager")
        sizePolicy3.setHeightForWidth(self.btn_eye_manager.sizePolicy().hasHeightForWidth())
        self.btn_eye_manager.setSizePolicy(sizePolicy3)
        self.btn_eye_manager.setMinimumSize(QSize(45, 45))
        self.btn_eye_manager.setMaximumSize(QSize(45, 45))
        self.btn_eye_manager.setFlat(True)
        self.btn_eye_manager.setProperty(u"menuIcon", True)

        self.horizontalLayout_18.addWidget(self.btn_eye_manager)

        self.btn_configs = QPushButton(menu_view)
        self.btn_configs.setObjectName(u"btn_configs")
        sizePolicy3.setHeightForWidth(self.btn_configs.sizePolicy().hasHeightForWidth())
        self.btn_configs.setSizePolicy(sizePolicy3)
        self.btn_configs.setMinimumSize(QSize(45, 45))
        self.btn_configs.setMaximumSize(QSize(45, 45))
        self.btn_configs.setFlat(True)
        self.btn_configs.setProperty(u"menuIcon", True)

        self.horizontalLayout_18.addWidget(self.btn_configs)

        self.btn_preferences = QPushButton(menu_view)
        self.btn_preferences.setObjectName(u"btn_preferences")
        sizePolicy3.setHeightForWidth(self.btn_preferences.sizePolicy().hasHeightForWidth())
        self.btn_preferences.setSizePolicy(sizePolicy3)
        self.btn_preferences.setMinimumSize(QSize(45, 45))
        self.btn_preferences.setMaximumSize(QSize(45, 45))
        self.btn_preferences.setFlat(True)
        self.btn_preferences.setProperty(u"menuIcon", True)

        self.horizontalLayout_18.addWidget(self.btn_preferences)

        self.btn_debug = QPushButton(menu_view)
        self.btn_debug.setObjectName(u"btn_debug")
        sizePolicy3.setHeightForWidth(self.btn_debug.sizePolicy().hasHeightForWidth())
        self.btn_debug.setSizePolicy(sizePolicy3)
        self.btn_debug.setMinimumSize(QSize(0, 0))
        self.btn_debug.setMaximumSize(QSize(45, 45))
        self.btn_debug.setFlat(True)
        self.btn_debug.setProperty(u"menuIcon", True)

        self.horizontalLayout_18.addWidget(self.btn_debug)


        self.horizontalLayout_16.addLayout(self.horizontalLayout_18)

        self.horizontalSpacer_5 = QSpacerItem(0, 0, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_16.addItem(self.horizontalSpacer_5)


        self.verticalLayout_3.addLayout(self.horizontalLayout_16)


        self.retranslateUi(menu_view)

        self.tab_widget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(menu_view)
    # setupUi

    def retranslateUi(self, menu_view):
        menu_view.setWindowTitle(QCoreApplication.translate("menu_view", u"Menu", None))
        self.lbl_seed_title.setText(QCoreApplication.translate("menu_view", u"Seed", None))
        self.btn_4bytes_s0.setText("")
        self.btn_4bytes_s1.setText("")
        self.btn_4bytes_s2.setText("")
        self.btn_4bytes_s3.setText("")
        self.btn_8bytes_s0.setText("")
        self.btn_8bytes_s1.setText("")
        self.switch_seed_display.setText(QCoreApplication.translate("menu_view", u"32/64", None))
        self.lbl_reident_title.setText(QCoreApplication.translate("menu_view", u"Reidentification", None))
        self.lbl_reident_min.setText(QCoreApplication.translate("menu_view", u"0", None))
        self.lbl_reident_max.setText(QCoreApplication.translate("menu_view", u"1000000", None))
        self.switch_tracking.setText(QCoreApplication.translate("menu_view", u"MONITOR BLINKS", None))
        self.switch_tracking_tidsid.setText(QCoreApplication.translate("menu_view", u"TID/SID", None))
        self.btn_reidentify.setText(QCoreApplication.translate("menu_view", u"REIDENTIFY", None))
        self.btn_start_countdown.setText(QCoreApplication.translate("menu_view", u"TIMELINE", None))
        self.chkb_auto_start_countdown.setText(QCoreApplication.translate("menu_view", u"AUTO START COUNTDOWN", None))
        self.lbl_calibration_title.setText(QCoreApplication.translate("menu_view", u"Advance Calibration", None))
        self.label_5.setText(QCoreApplication.translate("menu_view", u"Target", None))
        self.spin_advance_target.setSuffix("")
        self.spin_advance_target.setPrefix("")
        self.lbl_adv_trgt_eta.setText("")
        self.label.setText(QCoreApplication.translate("menu_view", u"Final \u24b6 Press Delay", None))
        self.spin_final_a_press_delay.setSuffix("")
        self.spin_final_a_press_delay.setPrefix("")
        self.label_4.setText(QCoreApplication.translate("menu_view", u"Timeline Buffer", None))
        self.spin_timeline_buffer.setSuffix("")
        self.spin_timeline_buffer.setPrefix("")
        self.label_6.setText(QCoreApplication.translate("menu_view", u"Countdown Starts at", None))
        self.lbl_timeline_start.setText("")
        self.label_7.setText(QCoreApplication.translate("menu_view", u"Press \u24b6 at", None))
        self.lbl_press_a.setText("")
        self.chkb_plus_one_menu_close.setText(QCoreApplication.translate("menu_view", u"+1 ON MENU CLOSE", None))
        self.lbl_time_delay.setText(QCoreApplication.translate("menu_view", u"Time Delay", None))
        self.lbl_advance_delay.setText(QCoreApplication.translate("menu_view", u"Advance Delay", None))
        self.spin_advance_delay.setSuffix("")
        self.spin_advance_delay.setPrefix("")
        self.lbl_advance_delay_2.setText(QCoreApplication.translate("menu_view", u"Advance Delay 2", None))
        self.spin_advance_delay_2.setSuffix("")
        self.spin_advance_delay_2.setPrefix("")
        self.lbl_noise_title.setText(QCoreApplication.translate("menu_view", u"Noise", None))
        self.chkb_reident_pkmn_npc.setText(QCoreApplication.translate("menu_view", u"Reidentify with NPC Pok\u00e9mon", None))
        self.lbl_npcs.setText(QCoreApplication.translate("menu_view", u"NPCs", None))
        self.spin_npcs.setSuffix("")
        self.spin_npcs.setPrefix("")
        self.lbl_npcs_during_countdown.setText(QCoreApplication.translate("menu_view", u"NPCs during CD", None))
        self.spin_npcs_countdown.setSuffix("")
        self.spin_npcs_countdown.setPrefix("")
        self.lbl_pkmn_npcs.setText(QCoreApplication.translate("menu_view", u"PKMNs NPCs during CD", None))
        self.spin_pkmn_npcs_countdown.setSuffix("")
        self.spin_pkmn_npcs_countdown.setPrefix("")
        self.label_2.setText(QCoreApplication.translate("menu_view", u"X to Advance", None))
        self.spin_manual_advance.setSuffix("")
        self.spin_manual_advance.setPrefix("")
        self.lbl_timeline_title.setText(QCoreApplication.translate("menu_view", u"Advance Timeline", None))
        self.groupBox.setTitle("")
        self.btn_stop_timeline.setText(QCoreApplication.translate("menu_view", u"STOP", None))
        self.btn_create_resource.setText(QCoreApplication.translate("menu_view", u"CREATE", None))
        self.btn_delete_resource.setText(QCoreApplication.translate("menu_view", u"DELETE", None))
        self.switch_preview_tracking.setText(QCoreApplication.translate("menu_view", u"PREVIEW TRACKING", None))
        self.label_9.setText(QCoreApplication.translate("menu_view", u"Threshold", None))
        self.lbl_config_title.setText(QCoreApplication.translate("menu_view", u"Configuration", None))
        self.lbl_cfg_roi.setText(QCoreApplication.translate("menu_view", u"Region of Interest Coords", None))
        self.lbl_cfg_roi_value.setText(QCoreApplication.translate("menu_view", u"[X, Y, W, H]", None))
        self.lbl_cfg_threshold.setText(QCoreApplication.translate("menu_view", u"Image Recognition Threshold", None))
        self.lbl_cfg_threshold_value.setText(QCoreApplication.translate("menu_view", u"0.0", None))
        self.lbl_cfg_plus_one_menu_close.setText(QCoreApplication.translate("menu_view", u"+1 on Menu Close", None))
        self.lbl_cfg_plus_one_menu_close_value.setText(QCoreApplication.translate("menu_view", u"YES", None))
        self.lbl_cfg_final_a_press_delay.setText(QCoreApplication.translate("menu_view", u"Final \u24b6 Press Delay", None))
        self.lbl_cfg_final_a_press_delay_value.setText(QCoreApplication.translate("menu_view", u"0", None))
        self.lbl_timeline_buffer.setText(QCoreApplication.translate("menu_view", u"Timeline Buffer", None))
        self.lbl_timeline_buffer_value.setText(QCoreApplication.translate("menu_view", u"0", None))
        self.lbl_cfg_npcs.setText(QCoreApplication.translate("menu_view", u"NPCs", None))
        self.lbl_cfg_npcs_value.setText(QCoreApplication.translate("menu_view", u"0", None))
        self.lbl_cfg_npcs_cd.setText(QCoreApplication.translate("menu_view", u"NPCs during Countdown", None))
        self.lbl_cfg_npcs_cd_value.setText(QCoreApplication.translate("menu_view", u"0", None))
        self.lbl_cfg_pkmn_npcs.setText(QCoreApplication.translate("menu_view", u"Pok\u00e9mon NPCs during Countdown", None))
        self.lbl_cfg_pkmn_npcs_countdown_value.setText(QCoreApplication.translate("menu_view", u"0", None))
        self.btn_create_config.setText(QCoreApplication.translate("menu_view", u"CREATE", None))
        self.btn_save_config.setText(QCoreApplication.translate("menu_view", u"SAVE", None))
        self.btn_load_config.setText(QCoreApplication.translate("menu_view", u"LOAD", None))
        self.btn_generate_blinks.setText(QCoreApplication.translate("menu_view", u"GENERATE BLINKS", None))
        self.btn_eye_manager.setText(QCoreApplication.translate("menu_view", u"EYE MANAGER", None))
        self.btn_configs.setText(QCoreApplication.translate("menu_view", u"CONFIGS", None))
        self.btn_preferences.setText(QCoreApplication.translate("menu_view", u"PREFERENCES", None))
        self.btn_debug.setText(QCoreApplication.translate("menu_view", u"DEBUG", None))
    # retranslateUi

