# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'cwindow.ui'
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
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_CustomWindow(object):
    def setupUi(self, CustomWindow):
        if not CustomWindow.objectName():
            CustomWindow.setObjectName(u"CustomWindow")
        CustomWindow.resize(400, 300)
        CustomWindow.setMinimumSize(QSize(400, 300))
        self.verticalLayout_2 = QVBoxLayout(CustomWindow)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.topbar = QFrame(CustomWindow)
        self.topbar.setObjectName(u"topbar")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.topbar.sizePolicy().hasHeightForWidth())
        self.topbar.setSizePolicy(sizePolicy)
        self.topbar.setMinimumSize(QSize(0, 30))
        self.topbar.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.topbar.setStyleSheet(u"")
        self.topbar.setFrameShape(QFrame.NoFrame)
        self.topbar.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.topbar)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_3.addItem(self.horizontalSpacer)

        self.switch_always_on_top = QPushButton(self.topbar)
        self.switch_always_on_top.setObjectName(u"switch_always_on_top")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.switch_always_on_top.sizePolicy().hasHeightForWidth())
        self.switch_always_on_top.setSizePolicy(sizePolicy1)
        self.switch_always_on_top.setMinimumSize(QSize(30, 30))
        self.switch_always_on_top.setMaximumSize(QSize(30, 30))
        self.switch_always_on_top.setFlat(True)

        self.horizontalLayout_3.addWidget(self.switch_always_on_top)

        self.btn_minimize = QPushButton(self.topbar)
        self.btn_minimize.setObjectName(u"btn_minimize")
        sizePolicy1.setHeightForWidth(self.btn_minimize.sizePolicy().hasHeightForWidth())
        self.btn_minimize.setSizePolicy(sizePolicy1)
        self.btn_minimize.setMinimumSize(QSize(30, 30))
        self.btn_minimize.setMaximumSize(QSize(30, 30))
        self.btn_minimize.setFlat(True)

        self.horizontalLayout_3.addWidget(self.btn_minimize)

        self.btn_close = QPushButton(self.topbar)
        self.btn_close.setObjectName(u"btn_close")
        sizePolicy1.setHeightForWidth(self.btn_close.sizePolicy().hasHeightForWidth())
        self.btn_close.setSizePolicy(sizePolicy1)
        self.btn_close.setMinimumSize(QSize(30, 30))
        self.btn_close.setMaximumSize(QSize(30, 30))
        self.btn_close.setFlat(True)

        self.horizontalLayout_3.addWidget(self.btn_close)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)


        self.verticalLayout.addWidget(self.topbar)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.placeholder_content = QWidget(CustomWindow)
        self.placeholder_content.setObjectName(u"placeholder_content")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.placeholder_content.sizePolicy().hasHeightForWidth())
        self.placeholder_content.setSizePolicy(sizePolicy2)

        self.verticalLayout_2.addWidget(self.placeholder_content)


        self.retranslateUi(CustomWindow)

        QMetaObject.connectSlotsByName(CustomWindow)
    # setupUi

    def retranslateUi(self, CustomWindow):
        CustomWindow.setWindowTitle(QCoreApplication.translate("CustomWindow", u"PlayerBlink GX", None))
        self.switch_always_on_top.setText(QCoreApplication.translate("CustomWindow", u"*", None))
        self.btn_minimize.setText(QCoreApplication.translate("CustomWindow", u"_", None))
        self.btn_close.setText(QCoreApplication.translate("CustomWindow", u"X", None))
    # retranslateUi

