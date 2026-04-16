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
    QHBoxLayout, QLabel, QPushButton, QScrollArea,
    QSizePolicy, QSlider, QSpacerItem, QSpinBox,
    QTabWidget, QTextEdit, QVBoxLayout, QWidget)

from superqt import QDoubleRangeSlider

class Ui_menu_view(object):
    def setupUi(self, menu_view):
        if not menu_view.objectName():
            menu_view.setObjectName(u"menu_view")
        menu_view.resize(712, 613)
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
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.gbox_adv_timeline = QGroupBox(self.Main)
        self.gbox_adv_timeline.setObjectName(u"gbox_adv_timeline")
        self.gbox_adv_timeline.setMaximumSize(QSize(150, 16777215))
        self.verticalLayout = QVBoxLayout(self.gbox_adv_timeline)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.lbl_timeline_title = QLabel(self.gbox_adv_timeline)
        self.lbl_timeline_title.setObjectName(u"lbl_timeline_title")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lbl_timeline_title.sizePolicy().hasHeightForWidth())
        self.lbl_timeline_title.setSizePolicy(sizePolicy)
        self.lbl_timeline_title.setMinimumSize(QSize(0, 20))
        self.lbl_timeline_title.setProperty(u"title", True)

        self.verticalLayout.addWidget(self.lbl_timeline_title)

        self.scrollArea = QScrollArea(self.gbox_adv_timeline)
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
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 128, 445))
        self.verticalLayout_11 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.list_advance_timeline = QVBoxLayout()
        self.list_advance_timeline.setSpacing(0)
        self.list_advance_timeline.setObjectName(u"list_advance_timeline")

        self.verticalLayout_11.addLayout(self.list_advance_timeline)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout.addWidget(self.scrollArea)

        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setSpacing(0)
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.horizontalSpacer_13 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_32.addItem(self.horizontalSpacer_13)

        self.btn_stop_timeline = QPushButton(self.gbox_adv_timeline)
        self.btn_stop_timeline.setObjectName(u"btn_stop_timeline")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.btn_stop_timeline.sizePolicy().hasHeightForWidth())
        self.btn_stop_timeline.setSizePolicy(sizePolicy1)
        self.btn_stop_timeline.setMinimumSize(QSize(25, 25))
        self.btn_stop_timeline.setMaximumSize(QSize(25, 25))
        self.btn_stop_timeline.setStyleSheet(u"")
        self.btn_stop_timeline.setFlat(True)

        self.horizontalLayout_32.addWidget(self.btn_stop_timeline)

        self.btn_copy_timeline_adv = QPushButton(self.gbox_adv_timeline)
        self.btn_copy_timeline_adv.setObjectName(u"btn_copy_timeline_adv")
        sizePolicy1.setHeightForWidth(self.btn_copy_timeline_adv.sizePolicy().hasHeightForWidth())
        self.btn_copy_timeline_adv.setSizePolicy(sizePolicy1)
        self.btn_copy_timeline_adv.setMinimumSize(QSize(25, 25))
        self.btn_copy_timeline_adv.setMaximumSize(QSize(25, 25))
        self.btn_copy_timeline_adv.setStyleSheet(u"")
        self.btn_copy_timeline_adv.setFlat(True)

        self.horizontalLayout_32.addWidget(self.btn_copy_timeline_adv)


        self.verticalLayout.addLayout(self.horizontalLayout_32)


        self.horizontalLayout_2.addWidget(self.gbox_adv_timeline)

        self.column1 = QVBoxLayout()
        self.column1.setObjectName(u"column1")
        self.gbox_tracking = QGroupBox(self.Main)
        self.gbox_tracking.setObjectName(u"gbox_tracking")
        self.verticalLayout_14 = QVBoxLayout(self.gbox_tracking)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(10, 10, 10, 10)
        self.lbl_tracking_title = QLabel(self.gbox_tracking)
        self.lbl_tracking_title.setObjectName(u"lbl_tracking_title")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lbl_tracking_title.sizePolicy().hasHeightForWidth())
        self.lbl_tracking_title.setSizePolicy(sizePolicy2)
        self.lbl_tracking_title.setMinimumSize(QSize(0, 20))
        self.lbl_tracking_title.setProperty(u"title", True)

        self.verticalLayout_14.addWidget(self.lbl_tracking_title)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.switch_tracking = QPushButton(self.gbox_tracking)
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

        self.switch_tracking_tidsid = QPushButton(self.gbox_tracking)
        self.switch_tracking_tidsid.setObjectName(u"switch_tracking_tidsid")
        self.switch_tracking_tidsid.setEnabled(False)
        sizePolicy3.setHeightForWidth(self.switch_tracking_tidsid.sizePolicy().hasHeightForWidth())
        self.switch_tracking_tidsid.setSizePolicy(sizePolicy3)
        self.switch_tracking_tidsid.setMinimumSize(QSize(75, 75))
        self.switch_tracking_tidsid.setFlat(True)

        self.horizontalLayout_5.addWidget(self.switch_tracking_tidsid)

        self.btn_reidentify = QPushButton(self.gbox_tracking)
        self.btn_reidentify.setObjectName(u"btn_reidentify")
        self.btn_reidentify.setEnabled(False)
        sizePolicy3.setHeightForWidth(self.btn_reidentify.sizePolicy().hasHeightForWidth())
        self.btn_reidentify.setSizePolicy(sizePolicy3)
        self.btn_reidentify.setMinimumSize(QSize(75, 75))
        self.btn_reidentify.setFlat(True)

        self.horizontalLayout_5.addWidget(self.btn_reidentify)


        self.verticalLayout_14.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.lbl_plus_one_menu_close = QLabel(self.gbox_tracking)
        self.lbl_plus_one_menu_close.setObjectName(u"lbl_plus_one_menu_close")
        sizePolicy2.setHeightForWidth(self.lbl_plus_one_menu_close.sizePolicy().hasHeightForWidth())
        self.lbl_plus_one_menu_close.setSizePolicy(sizePolicy2)

        self.horizontalLayout_20.addWidget(self.lbl_plus_one_menu_close)

        self.chkb_plus_one_menu_close = QCheckBox(self.gbox_tracking)
        self.chkb_plus_one_menu_close.setObjectName(u"chkb_plus_one_menu_close")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.chkb_plus_one_menu_close.sizePolicy().hasHeightForWidth())
        self.chkb_plus_one_menu_close.setSizePolicy(sizePolicy4)
        self.chkb_plus_one_menu_close.setMinimumSize(QSize(0, 25))
        self.chkb_plus_one_menu_close.setChecked(True)
        self.chkb_plus_one_menu_close.setTristate(False)

        self.horizontalLayout_20.addWidget(self.chkb_plus_one_menu_close)


        self.verticalLayout_14.addLayout(self.horizontalLayout_20)

        self.line_6 = QFrame(self.gbox_tracking)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_6.setProperty(u"isLine", True)

        self.verticalLayout_14.addWidget(self.line_6)

        self.lbl_reident_title = QLabel(self.gbox_tracking)
        self.lbl_reident_title.setObjectName(u"lbl_reident_title")
        sizePolicy2.setHeightForWidth(self.lbl_reident_title.sizePolicy().hasHeightForWidth())
        self.lbl_reident_title.setSizePolicy(sizePolicy2)
        self.lbl_reident_title.setProperty(u"title", True)

        self.verticalLayout_14.addWidget(self.lbl_reident_title)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.lbl_reident_min = QLabel(self.gbox_tracking)
        self.lbl_reident_min.setObjectName(u"lbl_reident_min")

        self.horizontalLayout_6.addWidget(self.lbl_reident_min)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_6.addItem(self.horizontalSpacer)

        self.lbl_reident_max = QLabel(self.gbox_tracking)
        self.lbl_reident_max.setObjectName(u"lbl_reident_max")

        self.horizontalLayout_6.addWidget(self.lbl_reident_max)


        self.verticalLayout_14.addLayout(self.horizontalLayout_6)

        self.rslider_reident_range = QDoubleRangeSlider(self.gbox_tracking)
        self.rslider_reident_range.setObjectName(u"rslider_reident_range")
        sizePolicy2.setHeightForWidth(self.rslider_reident_range.sizePolicy().hasHeightForWidth())
        self.rslider_reident_range.setSizePolicy(sizePolicy2)
        self.rslider_reident_range.setMinimumSize(QSize(0, 20))

        self.verticalLayout_14.addWidget(self.rslider_reident_range)


        self.column1.addWidget(self.gbox_tracking)

        self.gbox_countdown = QGroupBox(self.Main)
        self.gbox_countdown.setObjectName(u"gbox_countdown")
        self.verticalLayout_16 = QVBoxLayout(self.gbox_countdown)
        self.verticalLayout_16.setSpacing(0)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(10, 10, 10, 10)
        self.lbl_countdown_title = QLabel(self.gbox_countdown)
        self.lbl_countdown_title.setObjectName(u"lbl_countdown_title")
        sizePolicy2.setHeightForWidth(self.lbl_countdown_title.sizePolicy().hasHeightForWidth())
        self.lbl_countdown_title.setSizePolicy(sizePolicy2)
        self.lbl_countdown_title.setMinimumSize(QSize(0, 20))
        self.lbl_countdown_title.setProperty(u"title", True)

        self.verticalLayout_16.addWidget(self.lbl_countdown_title)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.btn_start_countdown = QPushButton(self.gbox_countdown)
        self.btn_start_countdown.setObjectName(u"btn_start_countdown")
        self.btn_start_countdown.setEnabled(False)
        sizePolicy3.setHeightForWidth(self.btn_start_countdown.sizePolicy().hasHeightForWidth())
        self.btn_start_countdown.setSizePolicy(sizePolicy3)
        self.btn_start_countdown.setMinimumSize(QSize(75, 75))
        self.btn_start_countdown.setFlat(True)

        self.horizontalLayout_31.addWidget(self.btn_start_countdown)


        self.verticalLayout_16.addLayout(self.horizontalLayout_31)

        self.horizontalLayout_36 = QHBoxLayout()
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.lbl_auto_start_countdown = QLabel(self.gbox_countdown)
        self.lbl_auto_start_countdown.setObjectName(u"lbl_auto_start_countdown")
        sizePolicy2.setHeightForWidth(self.lbl_auto_start_countdown.sizePolicy().hasHeightForWidth())
        self.lbl_auto_start_countdown.setSizePolicy(sizePolicy2)

        self.horizontalLayout_36.addWidget(self.lbl_auto_start_countdown)

        self.chkb_auto_start_countdown = QCheckBox(self.gbox_countdown)
        self.chkb_auto_start_countdown.setObjectName(u"chkb_auto_start_countdown")
        self.chkb_auto_start_countdown.setMinimumSize(QSize(0, 25))
        self.chkb_auto_start_countdown.setChecked(True)
        self.chkb_auto_start_countdown.setTristate(False)

        self.horizontalLayout_36.addWidget(self.chkb_auto_start_countdown)


        self.verticalLayout_16.addLayout(self.horizontalLayout_36)

        self.widget = QWidget(self.gbox_countdown)
        self.widget.setObjectName(u"widget")
        sizePolicy5 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy5)
        self.widget.setMinimumSize(QSize(0, 150))
        self.widget.setMaximumSize(QSize(16777215, 16777215))
        self.verticalLayout_17 = QVBoxLayout(self.widget)
        self.verticalLayout_17.setSpacing(0)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.placeholder_countdown_display = QWidget(self.widget)
        self.placeholder_countdown_display.setObjectName(u"placeholder_countdown_display")
        sizePolicy5.setHeightForWidth(self.placeholder_countdown_display.sizePolicy().hasHeightForWidth())
        self.placeholder_countdown_display.setSizePolicy(sizePolicy5)
        self.placeholder_countdown_display.setMinimumSize(QSize(150, 150))

        self.verticalLayout_17.addWidget(self.placeholder_countdown_display)


        self.verticalLayout_16.addWidget(self.widget)


        self.column1.addWidget(self.gbox_countdown)


        self.horizontalLayout_2.addLayout(self.column1)

        self.column2 = QVBoxLayout()
        self.column2.setObjectName(u"column2")
        self.column2.setContentsMargins(0, 0, 0, 0)
        self.gbox_seed = QGroupBox(self.Main)
        self.gbox_seed.setObjectName(u"gbox_seed")
        sizePolicy2.setHeightForWidth(self.gbox_seed.sizePolicy().hasHeightForWidth())
        self.gbox_seed.setSizePolicy(sizePolicy2)
        self.verticalLayout_15 = QVBoxLayout(self.gbox_seed)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(10, 10, 10, 10)
        self.lbl_seed_title = QLabel(self.gbox_seed)
        self.lbl_seed_title.setObjectName(u"lbl_seed_title")
        sizePolicy2.setHeightForWidth(self.lbl_seed_title.sizePolicy().hasHeightForWidth())
        self.lbl_seed_title.setSizePolicy(sizePolicy2)
        self.lbl_seed_title.setMinimumSize(QSize(0, 20))
        self.lbl_seed_title.setProperty(u"title", True)

        self.verticalLayout_15.addWidget(self.lbl_seed_title)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.verticalLayout_7 = QVBoxLayout()
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.btn_8bytes_s0 = QPushButton(self.gbox_seed)
        self.btn_8bytes_s0.setObjectName(u"btn_8bytes_s0")
        sizePolicy6 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(self.btn_8bytes_s0.sizePolicy().hasHeightForWidth())
        self.btn_8bytes_s0.setSizePolicy(sizePolicy6)
        self.btn_8bytes_s0.setMinimumSize(QSize(0, 25))
        self.btn_8bytes_s0.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_8bytes_s0.setAcceptDrops(False)
        self.btn_8bytes_s0.setProperty(u"maxLength", 4)
        self.btn_8bytes_s0.setProperty(u"frame", False)
        self.btn_8bytes_s0.setProperty(u"readOnly", True)
        self.btn_8bytes_s0.setProperty(u"class", u"seedValue")

        self.horizontalLayout_4.addWidget(self.btn_8bytes_s0)

        self.btn_4bytes_s0 = QPushButton(self.gbox_seed)
        self.btn_4bytes_s0.setObjectName(u"btn_4bytes_s0")
        sizePolicy6.setHeightForWidth(self.btn_4bytes_s0.sizePolicy().hasHeightForWidth())
        self.btn_4bytes_s0.setSizePolicy(sizePolicy6)
        self.btn_4bytes_s0.setMinimumSize(QSize(0, 25))
        self.btn_4bytes_s0.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_4bytes_s0.setAcceptDrops(False)
        self.btn_4bytes_s0.setProperty(u"maxLength", 4)
        self.btn_4bytes_s0.setProperty(u"frame", False)
        self.btn_4bytes_s0.setProperty(u"readOnly", True)
        self.btn_4bytes_s0.setProperty(u"class", u"seedValue")

        self.horizontalLayout_4.addWidget(self.btn_4bytes_s0)

        self.btn_4bytes_s1 = QPushButton(self.gbox_seed)
        self.btn_4bytes_s1.setObjectName(u"btn_4bytes_s1")
        sizePolicy6.setHeightForWidth(self.btn_4bytes_s1.sizePolicy().hasHeightForWidth())
        self.btn_4bytes_s1.setSizePolicy(sizePolicy6)
        self.btn_4bytes_s1.setMinimumSize(QSize(0, 25))
        self.btn_4bytes_s1.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_4bytes_s1.setAcceptDrops(False)
        self.btn_4bytes_s1.setProperty(u"maxLength", 4)
        self.btn_4bytes_s1.setProperty(u"frame", False)
        self.btn_4bytes_s1.setProperty(u"readOnly", True)
        self.btn_4bytes_s1.setProperty(u"class", u"seedValue")

        self.horizontalLayout_4.addWidget(self.btn_4bytes_s1)


        self.verticalLayout_7.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_34 = QHBoxLayout()
        self.horizontalLayout_34.setSpacing(0)
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.btn_8bytes_s1 = QPushButton(self.gbox_seed)
        self.btn_8bytes_s1.setObjectName(u"btn_8bytes_s1")
        sizePolicy6.setHeightForWidth(self.btn_8bytes_s1.sizePolicy().hasHeightForWidth())
        self.btn_8bytes_s1.setSizePolicy(sizePolicy6)
        self.btn_8bytes_s1.setMinimumSize(QSize(0, 25))
        self.btn_8bytes_s1.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_8bytes_s1.setAcceptDrops(False)
        self.btn_8bytes_s1.setProperty(u"maxLength", 4)
        self.btn_8bytes_s1.setProperty(u"frame", False)
        self.btn_8bytes_s1.setProperty(u"readOnly", True)
        self.btn_8bytes_s1.setProperty(u"class", u"seedValue")

        self.horizontalLayout_34.addWidget(self.btn_8bytes_s1)

        self.btn_4bytes_s2 = QPushButton(self.gbox_seed)
        self.btn_4bytes_s2.setObjectName(u"btn_4bytes_s2")
        sizePolicy6.setHeightForWidth(self.btn_4bytes_s2.sizePolicy().hasHeightForWidth())
        self.btn_4bytes_s2.setSizePolicy(sizePolicy6)
        self.btn_4bytes_s2.setMinimumSize(QSize(0, 25))
        self.btn_4bytes_s2.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_4bytes_s2.setAcceptDrops(False)
        self.btn_4bytes_s2.setProperty(u"maxLength", 4)
        self.btn_4bytes_s2.setProperty(u"frame", False)
        self.btn_4bytes_s2.setProperty(u"readOnly", True)
        self.btn_4bytes_s2.setProperty(u"class", u"seedValue")

        self.horizontalLayout_34.addWidget(self.btn_4bytes_s2)

        self.btn_4bytes_s3 = QPushButton(self.gbox_seed)
        self.btn_4bytes_s3.setObjectName(u"btn_4bytes_s3")
        sizePolicy6.setHeightForWidth(self.btn_4bytes_s3.sizePolicy().hasHeightForWidth())
        self.btn_4bytes_s3.setSizePolicy(sizePolicy6)
        self.btn_4bytes_s3.setMinimumSize(QSize(0, 25))
        self.btn_4bytes_s3.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_4bytes_s3.setAcceptDrops(False)
        self.btn_4bytes_s3.setProperty(u"maxLength", 4)
        self.btn_4bytes_s3.setProperty(u"frame", False)
        self.btn_4bytes_s3.setProperty(u"readOnly", True)
        self.btn_4bytes_s3.setProperty(u"class", u"seedValue")

        self.horizontalLayout_34.addWidget(self.btn_4bytes_s3)


        self.verticalLayout_7.addLayout(self.horizontalLayout_34)


        self.horizontalLayout_3.addLayout(self.verticalLayout_7)

        self.switch_seed_display = QPushButton(self.gbox_seed)
        self.switch_seed_display.setObjectName(u"switch_seed_display")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(self.switch_seed_display.sizePolicy().hasHeightForWidth())
        self.switch_seed_display.setSizePolicy(sizePolicy7)
        self.switch_seed_display.setMinimumSize(QSize(0, 0))
        self.switch_seed_display.setMaximumSize(QSize(45, 16777215))
        self.switch_seed_display.setFlat(True)

        self.horizontalLayout_3.addWidget(self.switch_seed_display)


        self.verticalLayout_15.addLayout(self.horizontalLayout_3)


        self.column2.addWidget(self.gbox_seed)

        self.gbox_calibration = QGroupBox(self.Main)
        self.gbox_calibration.setObjectName(u"gbox_calibration")
        self.verticalLayout_18 = QVBoxLayout(self.gbox_calibration)
        self.verticalLayout_18.setSpacing(0)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(10, 10, 10, 6)
        self.lbl_calibration_title = QLabel(self.gbox_calibration)
        self.lbl_calibration_title.setObjectName(u"lbl_calibration_title")
        sizePolicy2.setHeightForWidth(self.lbl_calibration_title.sizePolicy().hasHeightForWidth())
        self.lbl_calibration_title.setSizePolicy(sizePolicy2)
        self.lbl_calibration_title.setProperty(u"title", True)

        self.verticalLayout_18.addWidget(self.lbl_calibration_title)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.label_5 = QLabel(self.gbox_calibration)
        self.label_5.setObjectName(u"label_5")

        self.horizontalLayout_10.addWidget(self.label_5)

        self.spin_advance_target = QSpinBox(self.gbox_calibration)
        self.spin_advance_target.setObjectName(u"spin_advance_target")
        self.spin_advance_target.setMinimumSize(QSize(0, 25))
        self.spin_advance_target.setFrame(False)
        self.spin_advance_target.setAlignment(Qt.AlignCenter)
        self.spin_advance_target.setReadOnly(False)
        self.spin_advance_target.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spin_advance_target.setSpecialValueText(u"")
        self.spin_advance_target.setKeyboardTracking(False)
        self.spin_advance_target.setMinimum(1)
        self.spin_advance_target.setMaximum(1000000)
        self.spin_advance_target.setValue(1000)

        self.horizontalLayout_10.addWidget(self.spin_advance_target)


        self.verticalLayout_18.addLayout(self.horizontalLayout_10)

        self.lbl_adv_trgt_eta = QLabel(self.gbox_calibration)
        self.lbl_adv_trgt_eta.setObjectName(u"lbl_adv_trgt_eta")
        self.lbl_adv_trgt_eta.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.lbl_adv_trgt_eta.setProperty(u"smallText", True)

        self.verticalLayout_18.addWidget(self.lbl_adv_trgt_eta)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.label = QLabel(self.gbox_calibration)
        self.label.setObjectName(u"label")

        self.horizontalLayout_7.addWidget(self.label)

        self.spin_final_a_press_delay = QSpinBox(self.gbox_calibration)
        self.spin_final_a_press_delay.setObjectName(u"spin_final_a_press_delay")
        self.spin_final_a_press_delay.setMinimumSize(QSize(0, 25))
        self.spin_final_a_press_delay.setFrame(False)
        self.spin_final_a_press_delay.setAlignment(Qt.AlignCenter)
        self.spin_final_a_press_delay.setReadOnly(False)
        self.spin_final_a_press_delay.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spin_final_a_press_delay.setSpecialValueText(u"")
        self.spin_final_a_press_delay.setKeyboardTracking(False)
        self.spin_final_a_press_delay.setMinimum(0)
        self.spin_final_a_press_delay.setMaximum(1000000)
        self.spin_final_a_press_delay.setValue(0)

        self.horizontalLayout_7.addWidget(self.spin_final_a_press_delay)


        self.verticalLayout_18.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.label_4 = QLabel(self.gbox_calibration)
        self.label_4.setObjectName(u"label_4")

        self.horizontalLayout_9.addWidget(self.label_4)

        self.spin_timeline_buffer = QSpinBox(self.gbox_calibration)
        self.spin_timeline_buffer.setObjectName(u"spin_timeline_buffer")
        self.spin_timeline_buffer.setMinimumSize(QSize(0, 25))
        self.spin_timeline_buffer.setFrame(False)
        self.spin_timeline_buffer.setAlignment(Qt.AlignCenter)
        self.spin_timeline_buffer.setReadOnly(False)
        self.spin_timeline_buffer.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spin_timeline_buffer.setSpecialValueText(u"")
        self.spin_timeline_buffer.setKeyboardTracking(False)
        self.spin_timeline_buffer.setMinimum(0)
        self.spin_timeline_buffer.setMaximum(1000000)
        self.spin_timeline_buffer.setValue(0)

        self.horizontalLayout_9.addWidget(self.spin_timeline_buffer)


        self.verticalLayout_18.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.label_6 = QLabel(self.gbox_calibration)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout_11.addWidget(self.label_6)

        self.lbl_timeline_start = QLabel(self.gbox_calibration)
        self.lbl_timeline_start.setObjectName(u"lbl_timeline_start")
        self.lbl_timeline_start.setMinimumSize(QSize(0, 25))
        self.lbl_timeline_start.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_11.addWidget(self.lbl_timeline_start)


        self.verticalLayout_18.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.label_7 = QLabel(self.gbox_calibration)
        self.label_7.setObjectName(u"label_7")

        self.horizontalLayout_12.addWidget(self.label_7)

        self.lbl_press_a = QLabel(self.gbox_calibration)
        self.lbl_press_a.setObjectName(u"lbl_press_a")
        self.lbl_press_a.setMinimumSize(QSize(0, 25))
        self.lbl_press_a.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_12.addWidget(self.lbl_press_a)


        self.verticalLayout_18.addLayout(self.horizontalLayout_12)

        self.line_2 = QFrame(self.gbox_calibration)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_2.setProperty(u"isLine", True)

        self.verticalLayout_18.addWidget(self.line_2)

        self.lbl_timeline = QLabel(self.gbox_calibration)
        self.lbl_timeline.setObjectName(u"lbl_timeline")
        self.lbl_timeline.setMinimumSize(QSize(0, 20))
        self.lbl_timeline.setMargin(0)
        self.lbl_timeline.setProperty(u"title", True)

        self.verticalLayout_18.addWidget(self.lbl_timeline)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.lbl_time_delay = QLabel(self.gbox_calibration)
        self.lbl_time_delay.setObjectName(u"lbl_time_delay")

        self.horizontalLayout_13.addWidget(self.lbl_time_delay)

        self.spin_time_delay = QDoubleSpinBox(self.gbox_calibration)
        self.spin_time_delay.setObjectName(u"spin_time_delay")
        self.spin_time_delay.setMinimumSize(QSize(0, 25))
        self.spin_time_delay.setFrame(False)
        self.spin_time_delay.setAlignment(Qt.AlignCenter)
        self.spin_time_delay.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spin_time_delay.setDecimals(2)

        self.horizontalLayout_13.addWidget(self.spin_time_delay)


        self.verticalLayout_18.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.lbl_advance_delay = QLabel(self.gbox_calibration)
        self.lbl_advance_delay.setObjectName(u"lbl_advance_delay")

        self.horizontalLayout_15.addWidget(self.lbl_advance_delay)

        self.spin_advance_delay = QSpinBox(self.gbox_calibration)
        self.spin_advance_delay.setObjectName(u"spin_advance_delay")
        self.spin_advance_delay.setMinimumSize(QSize(0, 25))
        self.spin_advance_delay.setFrame(False)
        self.spin_advance_delay.setAlignment(Qt.AlignCenter)
        self.spin_advance_delay.setReadOnly(False)
        self.spin_advance_delay.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spin_advance_delay.setSpecialValueText(u"")
        self.spin_advance_delay.setKeyboardTracking(False)
        self.spin_advance_delay.setMinimum(0)
        self.spin_advance_delay.setMaximum(1000)
        self.spin_advance_delay.setValue(0)

        self.horizontalLayout_15.addWidget(self.spin_advance_delay)


        self.verticalLayout_18.addLayout(self.horizontalLayout_15)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.lbl_advance_delay_2 = QLabel(self.gbox_calibration)
        self.lbl_advance_delay_2.setObjectName(u"lbl_advance_delay_2")

        self.horizontalLayout_19.addWidget(self.lbl_advance_delay_2)

        self.spin_advance_delay_2 = QSpinBox(self.gbox_calibration)
        self.spin_advance_delay_2.setObjectName(u"spin_advance_delay_2")
        self.spin_advance_delay_2.setMinimumSize(QSize(0, 25))
        self.spin_advance_delay_2.setFrame(False)
        self.spin_advance_delay_2.setAlignment(Qt.AlignCenter)
        self.spin_advance_delay_2.setReadOnly(False)
        self.spin_advance_delay_2.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spin_advance_delay_2.setSpecialValueText(u"")
        self.spin_advance_delay_2.setKeyboardTracking(False)
        self.spin_advance_delay_2.setMinimum(0)
        self.spin_advance_delay_2.setMaximum(1000)
        self.spin_advance_delay_2.setValue(0)

        self.horizontalLayout_19.addWidget(self.spin_advance_delay_2)


        self.verticalLayout_18.addLayout(self.horizontalLayout_19)

        self.line_5 = QFrame(self.gbox_calibration)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_5.setProperty(u"isLine", True)

        self.verticalLayout_18.addWidget(self.line_5)

        self.lbl_noise_title = QLabel(self.gbox_calibration)
        self.lbl_noise_title.setObjectName(u"lbl_noise_title")
        sizePolicy2.setHeightForWidth(self.lbl_noise_title.sizePolicy().hasHeightForWidth())
        self.lbl_noise_title.setSizePolicy(sizePolicy2)
        self.lbl_noise_title.setMinimumSize(QSize(0, 20))
        self.lbl_noise_title.setProperty(u"title", True)

        self.verticalLayout_18.addWidget(self.lbl_noise_title)

        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.lbl_pkmn_npcs = QLabel(self.gbox_calibration)
        self.lbl_pkmn_npcs.setObjectName(u"lbl_pkmn_npcs")

        self.horizontalLayout_22.addWidget(self.lbl_pkmn_npcs)

        self.spin_pkmn_npcs_countdown = QSpinBox(self.gbox_calibration)
        self.spin_pkmn_npcs_countdown.setObjectName(u"spin_pkmn_npcs_countdown")
        self.spin_pkmn_npcs_countdown.setMinimumSize(QSize(0, 25))
        self.spin_pkmn_npcs_countdown.setFrame(False)
        self.spin_pkmn_npcs_countdown.setAlignment(Qt.AlignCenter)
        self.spin_pkmn_npcs_countdown.setReadOnly(False)
        self.spin_pkmn_npcs_countdown.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spin_pkmn_npcs_countdown.setSpecialValueText(u"")
        self.spin_pkmn_npcs_countdown.setKeyboardTracking(False)
        self.spin_pkmn_npcs_countdown.setMinimum(0)
        self.spin_pkmn_npcs_countdown.setMaximum(50)
        self.spin_pkmn_npcs_countdown.setValue(0)

        self.horizontalLayout_22.addWidget(self.spin_pkmn_npcs_countdown)


        self.verticalLayout_18.addLayout(self.horizontalLayout_22)

        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.lbl_npcs_during_countdown = QLabel(self.gbox_calibration)
        self.lbl_npcs_during_countdown.setObjectName(u"lbl_npcs_during_countdown")

        self.horizontalLayout_21.addWidget(self.lbl_npcs_during_countdown)

        self.spin_npcs_countdown = QSpinBox(self.gbox_calibration)
        self.spin_npcs_countdown.setObjectName(u"spin_npcs_countdown")
        self.spin_npcs_countdown.setMinimumSize(QSize(0, 25))
        self.spin_npcs_countdown.setFrame(False)
        self.spin_npcs_countdown.setAlignment(Qt.AlignCenter)
        self.spin_npcs_countdown.setReadOnly(False)
        self.spin_npcs_countdown.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spin_npcs_countdown.setSpecialValueText(u"")
        self.spin_npcs_countdown.setKeyboardTracking(False)
        self.spin_npcs_countdown.setMinimum(-1)
        self.spin_npcs_countdown.setMaximum(50)
        self.spin_npcs_countdown.setValue(0)

        self.horizontalLayout_21.addWidget(self.spin_npcs_countdown)


        self.verticalLayout_18.addLayout(self.horizontalLayout_21)

        self.horizontalLayout_35 = QHBoxLayout()
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.lbl_npcs = QLabel(self.gbox_calibration)
        self.lbl_npcs.setObjectName(u"lbl_npcs")

        self.horizontalLayout_35.addWidget(self.lbl_npcs)

        self.spin_npcs = QSpinBox(self.gbox_calibration)
        self.spin_npcs.setObjectName(u"spin_npcs")
        self.spin_npcs.setMinimumSize(QSize(0, 25))
        self.spin_npcs.setFrame(False)
        self.spin_npcs.setAlignment(Qt.AlignCenter)
        self.spin_npcs.setReadOnly(False)
        self.spin_npcs.setButtonSymbols(QAbstractSpinBox.UpDownArrows)
        self.spin_npcs.setSpecialValueText(u"")
        self.spin_npcs.setKeyboardTracking(False)
        self.spin_npcs.setMinimum(-1)
        self.spin_npcs.setMaximum(50)
        self.spin_npcs.setValue(0)

        self.horizontalLayout_35.addWidget(self.spin_npcs)


        self.verticalLayout_18.addLayout(self.horizontalLayout_35)

        self.horizontalLayout_37 = QHBoxLayout()
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.lbl_reident_pkmn_npc = QLabel(self.gbox_calibration)
        self.lbl_reident_pkmn_npc.setObjectName(u"lbl_reident_pkmn_npc")
        sizePolicy2.setHeightForWidth(self.lbl_reident_pkmn_npc.sizePolicy().hasHeightForWidth())
        self.lbl_reident_pkmn_npc.setSizePolicy(sizePolicy2)

        self.horizontalLayout_37.addWidget(self.lbl_reident_pkmn_npc)

        self.chkb_reident_pkmn_npc = QCheckBox(self.gbox_calibration)
        self.chkb_reident_pkmn_npc.setObjectName(u"chkb_reident_pkmn_npc")
        self.chkb_reident_pkmn_npc.setMinimumSize(QSize(0, 25))
        self.chkb_reident_pkmn_npc.setChecked(True)
        self.chkb_reident_pkmn_npc.setTristate(False)

        self.horizontalLayout_37.addWidget(self.chkb_reident_pkmn_npc)


        self.verticalLayout_18.addLayout(self.horizontalLayout_37)

        self.verticalSpacer_3 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_18.addItem(self.verticalSpacer_3)


        self.column2.addWidget(self.gbox_calibration)


        self.horizontalLayout_2.addLayout(self.column2)


        self.verticalLayout_4.addLayout(self.horizontalLayout_2)

        self.placeholder_tracking_progress = QWidget(self.Main)
        self.placeholder_tracking_progress.setObjectName(u"placeholder_tracking_progress")
        sizePolicy4.setHeightForWidth(self.placeholder_tracking_progress.sizePolicy().hasHeightForWidth())
        self.placeholder_tracking_progress.setSizePolicy(sizePolicy4)
        self.placeholder_tracking_progress.setMinimumSize(QSize(0, 20))
        self.placeholder_tracking_progress.setMaximumSize(QSize(16777215, 16777215))

        self.verticalLayout_4.addWidget(self.placeholder_tracking_progress)

        self.tab_widget.addTab(self.Main, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.Main), u"Main")
        self.EyeManager = QWidget()
        self.EyeManager.setObjectName(u"EyeManager")
        self.verticalLayout_9 = QVBoxLayout(self.EyeManager)
        self.verticalLayout_9.setSpacing(6)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.placeholder_eye_manager = QWidget(self.EyeManager)
        self.placeholder_eye_manager.setObjectName(u"placeholder_eye_manager")
        sizePolicy5.setHeightForWidth(self.placeholder_eye_manager.sizePolicy().hasHeightForWidth())
        self.placeholder_eye_manager.setSizePolicy(sizePolicy5)

        self.horizontalLayout.addWidget(self.placeholder_eye_manager)

        self.verticalLayout_10 = QVBoxLayout()
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.btn_create_resource = QPushButton(self.EyeManager)
        self.btn_create_resource.setObjectName(u"btn_create_resource")
        sizePolicy1.setHeightForWidth(self.btn_create_resource.sizePolicy().hasHeightForWidth())
        self.btn_create_resource.setSizePolicy(sizePolicy1)
        self.btn_create_resource.setMinimumSize(QSize(32, 32))
        self.btn_create_resource.setMaximumSize(QSize(32, 32))
        self.btn_create_resource.setFlat(True)

        self.verticalLayout_10.addWidget(self.btn_create_resource)

        self.btn_delete_resource = QPushButton(self.EyeManager)
        self.btn_delete_resource.setObjectName(u"btn_delete_resource")
        sizePolicy1.setHeightForWidth(self.btn_delete_resource.sizePolicy().hasHeightForWidth())
        self.btn_delete_resource.setSizePolicy(sizePolicy1)
        self.btn_delete_resource.setMinimumSize(QSize(32, 32))
        self.btn_delete_resource.setMaximumSize(QSize(32, 32))
        self.btn_delete_resource.setFlat(True)

        self.verticalLayout_10.addWidget(self.btn_delete_resource)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_10.addItem(self.verticalSpacer)

        self.switch_preview_tracking = QPushButton(self.EyeManager)
        self.switch_preview_tracking.setObjectName(u"switch_preview_tracking")
        sizePolicy1.setHeightForWidth(self.switch_preview_tracking.sizePolicy().hasHeightForWidth())
        self.switch_preview_tracking.setSizePolicy(sizePolicy1)
        self.switch_preview_tracking.setMinimumSize(QSize(32, 32))
        self.switch_preview_tracking.setMaximumSize(QSize(32, 32))
        self.switch_preview_tracking.setStyleSheet(u"")
        self.switch_preview_tracking.setFlat(True)

        self.verticalLayout_10.addWidget(self.switch_preview_tracking)


        self.horizontalLayout.addLayout(self.verticalLayout_10)


        self.verticalLayout_9.addLayout(self.horizontalLayout)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.lbl_threshold = QLabel(self.EyeManager)
        self.lbl_threshold.setObjectName(u"lbl_threshold")

        self.horizontalLayout_14.addWidget(self.lbl_threshold)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_14.addItem(self.horizontalSpacer_2)

        self.slider_threshold = QSlider(self.EyeManager)
        self.slider_threshold.setObjectName(u"slider_threshold")
        self.slider_threshold.setMinimumSize(QSize(0, 20))
        self.slider_threshold.setMinimum(10)
        self.slider_threshold.setMaximum(100)
        self.slider_threshold.setSingleStep(10)
        self.slider_threshold.setValue(80)
        self.slider_threshold.setOrientation(Qt.Horizontal)

        self.horizontalLayout_14.addWidget(self.slider_threshold)

        self.lbl_threshold_value = QLabel(self.EyeManager)
        self.lbl_threshold_value.setObjectName(u"lbl_threshold_value")
        self.lbl_threshold_value.setMinimumSize(QSize(30, 0))
        self.lbl_threshold_value.setAlignment(Qt.AlignCenter)

        self.horizontalLayout_14.addWidget(self.lbl_threshold_value)


        self.verticalLayout_9.addLayout(self.horizontalLayout_14)

        self.tab_widget.addTab(self.EyeManager, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.EyeManager), u"EyeManager")
        self.Config = QWidget()
        self.Config.setObjectName(u"Config")
        self.verticalLayout_6 = QVBoxLayout(self.Config)
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.lbl_config_title = QLabel(self.Config)
        self.lbl_config_title.setObjectName(u"lbl_config_title")
        sizePolicy2.setHeightForWidth(self.lbl_config_title.sizePolicy().hasHeightForWidth())
        self.lbl_config_title.setSizePolicy(sizePolicy2)
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
        sizePolicy1.setHeightForWidth(self.gv_img_preview.sizePolicy().hasHeightForWidth())
        self.gv_img_preview.setSizePolicy(sizePolicy1)
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

        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.btn_create_config = QPushButton(self.Config)
        self.btn_create_config.setObjectName(u"btn_create_config")
        sizePolicy1.setHeightForWidth(self.btn_create_config.sizePolicy().hasHeightForWidth())
        self.btn_create_config.setSizePolicy(sizePolicy1)
        self.btn_create_config.setMinimumSize(QSize(32, 32))
        self.btn_create_config.setMaximumSize(QSize(32, 32))
        self.btn_create_config.setFlat(True)

        self.verticalLayout_13.addWidget(self.btn_create_config)

        self.btn_save_config = QPushButton(self.Config)
        self.btn_save_config.setObjectName(u"btn_save_config")
        sizePolicy1.setHeightForWidth(self.btn_save_config.sizePolicy().hasHeightForWidth())
        self.btn_save_config.setSizePolicy(sizePolicy1)
        self.btn_save_config.setMinimumSize(QSize(32, 32))
        self.btn_save_config.setMaximumSize(QSize(32, 32))
        self.btn_save_config.setFlat(True)

        self.verticalLayout_13.addWidget(self.btn_save_config)

        self.btn_load_config = QPushButton(self.Config)
        self.btn_load_config.setObjectName(u"btn_load_config")
        sizePolicy1.setHeightForWidth(self.btn_load_config.sizePolicy().hasHeightForWidth())
        self.btn_load_config.setSizePolicy(sizePolicy1)
        self.btn_load_config.setMinimumSize(QSize(32, 32))
        self.btn_load_config.setMaximumSize(QSize(32, 32))
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
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.btn_generate_blinks = QPushButton(self.Debug)
        self.btn_generate_blinks.setObjectName(u"btn_generate_blinks")

        self.verticalLayout_5.addWidget(self.btn_generate_blinks)

        self.btn_generate_blinks_munchlax = QPushButton(self.Debug)
        self.btn_generate_blinks_munchlax.setObjectName(u"btn_generate_blinks_munchlax")

        self.verticalLayout_5.addWidget(self.btn_generate_blinks_munchlax)

        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.label_2 = QLabel(self.Debug)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_33.addWidget(self.label_2)

        self.spin_manual_advance = QSpinBox(self.Debug)
        self.spin_manual_advance.setObjectName(u"spin_manual_advance")
        self.spin_manual_advance.setMinimumSize(QSize(0, 25))
        self.spin_manual_advance.setFrame(False)
        self.spin_manual_advance.setAlignment(Qt.AlignCenter)
        self.spin_manual_advance.setReadOnly(False)
        self.spin_manual_advance.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.spin_manual_advance.setSpecialValueText(u"")
        self.spin_manual_advance.setKeyboardTracking(False)
        self.spin_manual_advance.setMinimum(1)
        self.spin_manual_advance.setMaximum(1000000)
        self.spin_manual_advance.setValue(165)

        self.horizontalLayout_33.addWidget(self.spin_manual_advance)


        self.verticalLayout_5.addLayout(self.horizontalLayout_33)

        self.verticalSpacer_4 = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout_5.addItem(self.verticalSpacer_4)

        self.tab_widget.addTab(self.Debug, "")
        self.tab_widget.setTabText(self.tab_widget.indexOf(self.Debug), u"Debug")

        self.verticalLayout_3.addWidget(self.tab_widget)

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
        self.gbox_adv_timeline.setTitle("")
        self.lbl_timeline_title.setText(QCoreApplication.translate("menu_view", u"Timeline", None))
        self.btn_stop_timeline.setText(QCoreApplication.translate("menu_view", u"S", None))
        self.btn_copy_timeline_adv.setText(QCoreApplication.translate("menu_view", u"C", None))
        self.gbox_tracking.setTitle("")
        self.lbl_tracking_title.setText(QCoreApplication.translate("menu_view", u"Tracking", None))
        self.switch_tracking.setText(QCoreApplication.translate("menu_view", u"MONITOR BLINKS", None))
        self.switch_tracking_tidsid.setText(QCoreApplication.translate("menu_view", u"TID/SID", None))
        self.btn_reidentify.setText(QCoreApplication.translate("menu_view", u"REIDENTIFY", None))
        self.lbl_plus_one_menu_close.setText(QCoreApplication.translate("menu_view", u"+1 On menu close", None))
        self.chkb_plus_one_menu_close.setText("")
        self.lbl_reident_title.setText(QCoreApplication.translate("menu_view", u"Reidentification", None))
        self.lbl_reident_min.setText(QCoreApplication.translate("menu_view", u"0", None))
        self.lbl_reident_max.setText(QCoreApplication.translate("menu_view", u"1000000", None))
        self.gbox_countdown.setTitle("")
        self.lbl_countdown_title.setText(QCoreApplication.translate("menu_view", u"Countdown", None))
        self.btn_start_countdown.setText(QCoreApplication.translate("menu_view", u"TIMELINE", None))
        self.lbl_auto_start_countdown.setText(QCoreApplication.translate("menu_view", u"Start the countdown automatically", None))
        self.chkb_auto_start_countdown.setText("")
        self.gbox_seed.setTitle("")
        self.lbl_seed_title.setText(QCoreApplication.translate("menu_view", u"Seed", None))
        self.btn_8bytes_s0.setText("")
        self.btn_4bytes_s0.setText("")
        self.btn_4bytes_s1.setText("")
        self.btn_8bytes_s1.setText("")
        self.btn_4bytes_s2.setText("")
        self.btn_4bytes_s3.setText("")
        self.switch_seed_display.setText(QCoreApplication.translate("menu_view", u"32/64", None))
        self.gbox_calibration.setTitle("")
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
        self.lbl_timeline.setText(QCoreApplication.translate("menu_view", u"Timeline Setup", None))
        self.lbl_time_delay.setText(QCoreApplication.translate("menu_view", u"Time Delay", None))
        self.lbl_advance_delay.setText(QCoreApplication.translate("menu_view", u"Advance Delay", None))
        self.spin_advance_delay.setSuffix("")
        self.spin_advance_delay.setPrefix("")
        self.lbl_advance_delay_2.setText(QCoreApplication.translate("menu_view", u"Advance Delay 2", None))
        self.spin_advance_delay_2.setSuffix("")
        self.spin_advance_delay_2.setPrefix("")
        self.lbl_noise_title.setText(QCoreApplication.translate("menu_view", u"Noise", None))
        self.lbl_pkmn_npcs.setText(QCoreApplication.translate("menu_view", u"PKMNs NPCs dur. CD", None))
        self.spin_pkmn_npcs_countdown.setSuffix("")
        self.spin_pkmn_npcs_countdown.setPrefix("")
        self.lbl_npcs_during_countdown.setText(QCoreApplication.translate("menu_view", u"NPCs dur. CD", None))
        self.spin_npcs_countdown.setSuffix("")
        self.spin_npcs_countdown.setPrefix("")
        self.lbl_npcs.setText(QCoreApplication.translate("menu_view", u"NPCs", None))
        self.spin_npcs.setSuffix("")
        self.spin_npcs.setPrefix("")
        self.lbl_reident_pkmn_npc.setText(QCoreApplication.translate("menu_view", u"Reidentify with NPC Pok\u00e9mon", None))
        self.chkb_reident_pkmn_npc.setText("")
        self.btn_create_resource.setText(QCoreApplication.translate("menu_view", u"CREATE", None))
        self.btn_delete_resource.setText(QCoreApplication.translate("menu_view", u"DELETE", None))
        self.switch_preview_tracking.setText(QCoreApplication.translate("menu_view", u"PREVIEW TRACKING", None))
        self.lbl_threshold.setText(QCoreApplication.translate("menu_view", u"Threshold", None))
        self.lbl_threshold_value.setText(QCoreApplication.translate("menu_view", u"0.8", None))
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
        self.btn_generate_blinks_munchlax.setText(QCoreApplication.translate("menu_view", u"GENERATE BLINKS FROM MUNCHLAX", None))
        self.label_2.setText(QCoreApplication.translate("menu_view", u"X to Advance", None))
        self.spin_manual_advance.setSuffix("")
        self.spin_manual_advance.setPrefix("")
        self.btn_eye_manager.setText(QCoreApplication.translate("menu_view", u"EYE MANAGER", None))
        self.btn_configs.setText(QCoreApplication.translate("menu_view", u"CONFIGS", None))
        self.btn_preferences.setText(QCoreApplication.translate("menu_view", u"PREFERENCES", None))
        self.btn_debug.setText(QCoreApplication.translate("menu_view", u"DEBUG", None))
    # retranslateUi

