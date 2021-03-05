from PyQt5.QtWidgets import QComboBox, QFrame, QGroupBox, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QSplitter, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QItemSelectionModel, Qt
from PyQt5.QtGui import QPainter, QBrush, QPen, QPixmap

import blipblop.constants as cnst

class SettingsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        

class VisualBlip(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        
        l = QLabel("Visual task")
        self._draw_area = QLabel()
        self._draw_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        canvas = QPixmap(400, 300)
        canvas = QPixmap()
        
        self._draw_area.setPixmap(canvas)
        vbox.addWidget(l)
        vbox.addWidget(self._draw_area)
        
        start_btn = QPushButton("start")
        start_btn.clicked.connect(self.paint_event)
        vbox.addWidget(start_btn)
       
    def paint_event(self):
        painter = QPainter(self._draw_area.pixmap())    
        painter.setPen(QPen(Qt.red,  1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        painter.drawEllipse(40, 40, 80, 100)
        painter.end()
        self._draw_area.update()
        
        
    def reset(self):
        pass

