from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QTimer, pyqtSignal
from PyQt5.QtGui import QFont

class CountdownLabel(QLabel):
    countdown_done = pyqtSignal()
    
    def __init__(self, parent=None, text=""):
        super().__init__(parent=parent)
        self._text = text
        self._count = 0
        self._timer = QTimer()
        self._timer.timeout.connect(self.on_timeout)
        font = QFont()
        font.setBold(True)
        font.setPointSize(20)
        self.setFont(font)
        self.setStyleSheet("color: #2D4B9A")

    def start(self, time=3):
        if time < 1:
            time = 1
        self._count = time
        self.setText("%s %i" % (self._text, self._count))
        self.update()
        self._timer.start(1000)

    def stop(self):
        if self._timer.isActive():
            self._timer.stop()
            self.setText("")
            
    def on_timeout(self):
        self._count -= 1
        self.setText("%s %i" % (self._text, self._count))
        self.update()
        if self._count <= 0:
            self._timer.stop()
            self.setText("")
            self.update()
            self.countdown_done.emit()
        