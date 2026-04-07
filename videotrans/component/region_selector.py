import cv2
import numpy as np
from PySide6.QtCore import Qt, QRect, QPoint
from PySide6.QtGui import QPixmap, QImage, QPainter, QColor, QPen
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLabel)

from videotrans.configure.config import defaulelang

MAX_PREVIEW_W = 800
MAX_PREVIEW_H = 600


class FrameLabel(QLabel):
    """QLabel that supports mouse-drag rectangle selection."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.setCursor(Qt.CrossCursor)
        self._start = QPoint()
        self._end = QPoint()
        self._drawing = False

    def get_rect(self):
        """Return the selected QRect (normalized so top-left < bottom-right)."""
        if self._start.isNull() and self._end.isNull():
            return QRect()
        return QRect(self._start, self._end).normalized()

    def clear_selection(self):
        self._start = QPoint()
        self._end = QPoint()
        self._drawing = False
        self.update()

    # -- mouse events --
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self._start = event.pos()
            self._end = event.pos()
            self._drawing = True
            self.update()

    def mouseMoveEvent(self, event):
        if self._drawing:
            self._end = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self._drawing:
            self._end = event.pos()
            self._drawing = False
            self.update()

    # -- paint overlay --
    def paintEvent(self, event):
        super().paintEvent(event)
        rect = self.get_rect()
        if rect.isNull() or not rect.isValid():
            return
        painter = QPainter(self)
        # Semi-transparent red fill
        painter.setBrush(QColor(255, 0, 0, 50))
        painter.setPen(QPen(QColor(255, 0, 0), 2))
        painter.drawRect(rect)
        painter.end()


class RegionSelectorDialog(QDialog):
    """
    Dialog that shows the first frame of a video and lets the user
    drag-select a rectangle. Returns (x, y, w, h) in original resolution.
    """

    def __init__(self, video_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle(
            "框选水印区域" if defaulelang == 'zh' else "Select watermark region"
        )
        self.video_path = video_path
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.result = None  # (x, y, w, h) or None

        layout = QVBoxLayout(self)

        # Frame display
        self.frame_label = FrameLabel()
        layout.addWidget(self.frame_label)

        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_confirm = QPushButton(
            "确认" if defaulelang == 'zh' else "Confirm"
        )
        self.btn_reselect = QPushButton(
            "重选" if defaulelang == 'zh' else "Reselect"
        )
        self.btn_cancel = QPushButton(
            "取消" if defaulelang == 'zh' else "Cancel"
        )
        btn_layout.addWidget(self.btn_reselect)
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_confirm)
        layout.addLayout(btn_layout)

        self.btn_confirm.clicked.connect(self._on_confirm)
        self.btn_reselect.clicked.connect(self.frame_label.clear_selection)
        self.btn_cancel.clicked.connect(self.reject)

        self._load_first_frame()

    def _load_first_frame(self):
        cap = cv2.VideoCapture(self.video_path)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        orig_h, orig_w = frame_rgb.shape[:2]

        # Compute scale to fit MAX_PREVIEW
        scale = min(MAX_PREVIEW_W / orig_w, MAX_PREVIEW_H / orig_h, 1.0)
        disp_w = int(orig_w * scale)
        disp_h = int(orig_h * scale)
        self.scale_x = orig_w / disp_w
        self.scale_y = orig_h / disp_h

        if scale < 1.0:
            frame_rgb = cv2.resize(frame_rgb, (disp_w, disp_h),
                                   interpolation=cv2.INTER_AREA)

        h, w, ch = frame_rgb.shape
        qimg = QImage(frame_rgb.data, w, h, ch * w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimg)
        self.frame_label.setPixmap(pixmap)
        self.frame_label.setFixedSize(pixmap.size())
        self.adjustSize()

    def _on_confirm(self):
        rect = self.frame_label.get_rect()
        if rect.isNull() or not rect.isValid() or rect.width() < 2 or rect.height() < 2:
            return
        # Map back to original resolution
        x = max(0, int(rect.x() * self.scale_x))
        y = max(0, int(rect.y() * self.scale_y))
        w = max(1, int(rect.width() * self.scale_x))
        h = max(1, int(rect.height() * self.scale_y))
        self.result = (x, y, w, h)
        self.accept()
