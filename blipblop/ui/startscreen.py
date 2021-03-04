import os
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal

import blipblop.constants as cnst


class MyLabel(QLabel):
    clicked = pyqtSignal()
    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.clicked.emit()


class StartScreen(QWidget):
    visual_task_signal = pyqtSignal()
    auditory_task_signal = pyqtSignal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        layout = QGridLayout()
        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(6, 1)
       
        layout.setRowStretch(0, 1)
        layout.setRowStretch(4, 2)
        self.setLayout(layout)
        
        label = QLabel("Measure your reaction times!\nselect a task")
        font = QFont()
        font.setPointSize(25)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1, 2, 1, 3, Qt.AlignCenter)
        
        visual_task_label = MyLabel()
        visual_task_label.setToolTip("Click to start a new visual task")
        visual_task_label.setPixmap(QPixmap(os.path.join(cnst.ICONS_FOLDER, "visual_task_large.png")))
        visual_task_label.setMaximumWidth(256)
        visual_task_label.clicked.connect(self.new_visual_task)
        
        auditory_task_label = MyLabel()
        auditory_task_label.setToolTip("Click to start a new auditory task")
        auditory_task_label.setPixmap(QPixmap(os.path.join(cnst.ICONS_FOLDER, "auditory_task_large.png")))
        auditory_task_label.setMaximumWidth(256)
        auditory_task_label.clicked.connect(self.new_auditory_task)
        
        layout.addWidget(visual_task_label, 2, 1, 2, 2, Qt.AlignCenter )
        layout.addWidget(auditory_task_label, 2, 4, 2, 2, Qt.AlignCenter )

    def new_auditory_task(self):
        self.auditory_task_signal.emit()
    
    def new_visual_task(self):
        self.visual_task_signal.emit()
