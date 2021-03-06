from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, pyqtSignal


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
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(6, 1)

        layout.setRowStretch(0, 1)
        layout.setRowStretch(4, 1)
        self.setLayout(layout)

        label = QLabel("Measure your reaction times!\nselect a task")
        font = QFont()
        font.setBold(True)
        font.setPointSize(25)
        label.setStyleSheet("color: #2D4B9A")
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1, 2, 1, 3, Qt.AlignCenter)

        visual_task_label = MyLabel()
        visual_task_label.setStatusTip("Start a new visual measurement (Ctrl+1)")
        visual_task_label.setToolTip("Click to start a new visual task (Ctrl+1)")
        visual_task_label.setPixmap(QPixmap(":/icons/visual_task_large"))
        visual_task_label.setMaximumWidth(256)
        visual_task_label.clicked.connect(self.new_visual_task)

        auditory_task_label = MyLabel()
        auditory_task_label.setStatusTip("Start a new auditory measurement (Ctrl+2)")
        auditory_task_label.setToolTip("click to start a new auditory task (Ctrl+2)")
        auditory_task_label.setPixmap(QPixmap(":/icons/auditory_task_large"))
        auditory_task_label.setMaximumWidth(256)
        auditory_task_label.clicked.connect(self.new_auditory_task)

        layout.addWidget(visual_task_label, 2, 1, 2, 2, Qt.AlignCenter)
        layout.addWidget(auditory_task_label, 2, 4, 2, 2, Qt.AlignCenter)

    def new_auditory_task(self):
        self.auditory_task_signal.emit()

    def new_visual_task(self):
        self.visual_task_signal.emit()
