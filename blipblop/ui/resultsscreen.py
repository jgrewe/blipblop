from PyQt5.QtWidgets import QComboBox, QFrame, QGroupBox, QHBoxLayout, QLabel, QSplitter, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QItemSelectionModel, Qt

import blipblop.constants as cnst


class ResultsScreen(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        
        main_splitter = QSplitter(Qt.Vertical)
        self.layout().addWidget(main_splitter)       
        

    def reset(self):
        pass
