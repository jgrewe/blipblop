from PyQt5.QtWidgets import QComboBox, QFrame, QGroupBox, QHBoxLayout, QLabel, QSplitter, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QItemSelectionModel, Qt

import blipblop.constants as cnst


class AudioBlop(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        
        vbox = QVBoxLayout()
      
        l = QLabel("Auditory task")
        vbox.addWidget(l)



    def reset(self):
        pass

