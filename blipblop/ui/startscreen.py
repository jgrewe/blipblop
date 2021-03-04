import os
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QFrame, QVBoxLayout, QListWidget, QAbstractItemView, QListWidgetItem
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QSettings, pyqtSignal

import blipblop.constants as cnst


class StartScreen(QWidget):
    keyPressed = pyqtSignal(int)

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        #self.setStyleSheet("background-color: white;")

        layout = QGridLayout()
        layout.setColumnStretch(0, 2)
        layout.setColumnStretch(1, 1)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 1)
        layout.setColumnStretch(4, 2)

        layout.setRowStretch(0, 1)
        layout.setRowStretch(1, 0)
        layout.setRowStretch(2, 1)
        layout.setRowStretch(3, 2)
        self.setLayout(layout)
        
        label = QLabel("Measure your reaction times!\nselect a task!")
        # label.setPixmap(QPixmap(os.path.join(cnst.ICONS_FOLDER, "nixview_transparent.png")))
        # label.setMaximumWidth(300)
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label, 1, 1, 1, 3, Qt.AlignCenter)
        
        frame = QFrame()
        l  = QVBoxLayout()
        l.addWidget(QLabel("Recently opened files:"))
        self._file_list = QListWidget(self)
        self._file_list.setSelectionMode(QAbstractItemView.SingleSelection)
        self._file_list.itemClicked.connect(self._on_file_clicked)
        self._file_list.setFrameShape(QFrame.NoFrame)
        self.keyPressed.connect(self._on_key_pressed)
        l.addWidget(self._file_list)
        frame.setLayout(l)
        layout.addWidget(frame, 3, 1, 1, 3)
        self._file_map = {}
    
    def keyPressEvent(self, event):
        super(StartScreen, self).keyPressEvent(event)
        if event.key() == Qt.Key_Return:
            self.keyPressed.emit(event.key())
    
    def _create_short_filename(self, original, index, max_len=40):
        short = original
        parts = original.split(os.sep)
        if len(parts) == 1:
            short = "%i: %s" % (index, short[:max_len])
        else:
            post = parts[-1]
            if len(post) > max_len - 4:
                post = post[:max_len - 4]
                short = str("%i: " % index) + "... " + post
            else:
                short = str("%i: " % index) + " ... ".join([original[:max_len - len(post) - 4], post])
        return short

    def reset(self):
        pass

    def _on_key_pressed(self, key):
        pass
