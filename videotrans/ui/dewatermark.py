from PySide6 import QtWidgets
from PySide6.QtCore import QMetaObject, QSize, Qt
from PySide6.QtGui import QCursor
from PySide6.QtWidgets import (QHBoxLayout, QLabel, QLineEdit, QListWidget,
                               QPushButton, QVBoxLayout, QComboBox)

from videotrans.configure.config import tr, defaulelang


class Ui_dewatermark(object):
    def setupUi(self, dewatermark):
        self.has_done = False
        self.videourls = []
        if not dewatermark.objectName():
            dewatermark.setObjectName("dewatermark")

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dewatermark.sizePolicy().hasHeightForWidth())
        dewatermark.setSizePolicy(sizePolicy)
        dewatermark.setMinimumSize(643, 420)

        self.horizontalLayout_3 = QHBoxLayout(dewatermark)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        # Video selection row
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.videourl = QLineEdit()
        self.videourl.setObjectName("videourl")
        self.videourl.setMinimumSize(QSize(0, 35))
        self.videourl.setReadOnly(True)
        self.horizontalLayout.addWidget(self.videourl)

        self.videobtn = QPushButton()
        self.videobtn.setObjectName("videobtn")
        self.videobtn.setMinimumSize(QSize(180, 35))
        self.videobtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.horizontalLayout.addWidget(self.videobtn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        # Regions list
        self.regions_list = QListWidget()
        self.regions_list.setObjectName("regions_list")
        self.regions_list.setMinimumHeight(100)
        self.verticalLayout.addWidget(self.regions_list)

        # Add / delete region buttons row
        region_btn_layout = QHBoxLayout()
        self.select_region_btn = QPushButton()
        self.select_region_btn.setObjectName("select_region_btn")
        self.select_region_btn.setMinimumSize(QSize(0, 35))
        self.select_region_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.delete_region_btn = QPushButton()
        self.delete_region_btn.setObjectName("delete_region_btn")
        self.delete_region_btn.setMinimumSize(QSize(0, 35))
        self.delete_region_btn.setCursor(QCursor(Qt.PointingHandCursor))

        region_btn_layout.addWidget(self.select_region_btn)
        region_btn_layout.addWidget(self.delete_region_btn)
        self.verticalLayout.addLayout(region_btn_layout)

        # Mode selection row
        mode_layout = QHBoxLayout()
        self.label_mode = QLabel()
        self.combo_mode = QComboBox()
        self.combo_mode.addItems(
            ["基础模式 (FFmpeg delogo)", "标准模式 (LaMa AI 修复)"]
            if defaulelang == 'zh' else
            ["Basic (FFmpeg delogo)", "Standard (LaMa AI inpaint)"]
        )
        mode_layout.addWidget(self.label_mode)
        mode_layout.addWidget(self.combo_mode)
        self.verticalLayout.addLayout(mode_layout)

        # Start button
        self.startbtn = QPushButton()
        self.startbtn.setObjectName("startbtn")
        self.startbtn.setMinimumSize(QSize(0, 35))
        self.startbtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.verticalLayout.addWidget(self.startbtn)

        # Result label
        self.resultlabel = QLabel()
        self.resultlabel.setObjectName("resultlabel")
        self.verticalLayout.addWidget(self.resultlabel)

        # Open result dir button
        self.resultbtn = QPushButton()
        self.resultbtn.setObjectName("resultbtn")
        self.resultbtn.setStyleSheet("background-color:transparent")
        self.resultbtn.setMinimumSize(QSize(0, 30))
        self.resultbtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.verticalLayout.addWidget(self.resultbtn)

        self.horizontalLayout_3.addLayout(self.verticalLayout)

        dewatermark.setWindowTitle(
            "视频去水印" if defaulelang == 'zh' else "Remove watermark from video"
        )
        self.retranslateUi()
        QMetaObject.connectSlotsByName(dewatermark)

    def retranslateUi(self):
        self.videourl.setPlaceholderText(tr("Select  Videos"))
        self.videobtn.setText(tr("Select a Video"))
        self.label_mode.setText(
            "去水印模式" if defaulelang == 'zh' else "Dewatermark mode"
        )
        self.select_region_btn.setText(
            "框选添加水印区域" if defaulelang == 'zh' else "Add watermark region"
        )
        self.delete_region_btn.setText(
            "删除选中区域" if defaulelang == 'zh' else "Delete selected region"
        )
        self.startbtn.setText(tr("Start operating"))
        self.resultlabel.setText("")
        self.resultbtn.setText(tr("Open the save results directory"))
