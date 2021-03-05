from PyQt5.QtWidgets import QAction, QComboBox, QFrame, QGroupBox, QGridLayout, QLabel, QPushButton, QShortcut, QSizePolicy, QSplitter, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QItemSelectionModel, QLine, QPoint, Qt
from PyQt5.QtGui import QColor, QKeySequence, QPainter, QBrush, QPen, QPixmap

import blipblop.constants as cnst

class SettingsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        

class VisualBlip(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        
        grid = QGridLayout()
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(2, 1)
        grid.setRowStretch(1, 1)
        grid.setRowStretch(3, 1)
        self.setLayout(grid)

        l = QLabel("Visual task")
        grid.addWidget(l, 0, 0, Qt.AlignLeft)
        instruction_label = QLabel("Instructions:\n -fixate central cross\n -press start (enter) when ready\n -press space bar as soon as the stimulus occurs")
        grid.addWidget(instruction_label, 3, 1, Qt.AlignLeft)
        self._draw_area = QLabel()
        self._draw_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        grid.addWidget(self._draw_area, 2, 1)
        self.reset_canvas()
        self.create_actions()
    
    def create_actions(self):
        self._start_action = QAction("start trial")
        self._start_action.setShortcuts([QKeySequence("enter"), QKeySequence("return")])
        self._start_action.triggered.connect(self.paint_event)
        self._reaction = QAction("reaction")
        self._reaction.setShortcut(QKeySequence("space"))
        self._reaction.triggered.connect(self.on_reaction)
        
        self.addAction(self._start_action)
        self.addAction(self._reaction)

    def on_reaction(self):
        print("reaction")
        self.reset_canvas()

    def reset_canvas(self):
        bkg_color = QColor()
        bkg_color.setAlphaF(0.0)
        canvas = QPixmap(400, 400)
        self._canvas_center = QPoint(200, 200)
        canvas.fill(bkg_color)
        self.draw_fixation(canvas)        
        self._draw_area.setPixmap(canvas)
        self._draw_area.update()

    def draw_fixation(self, pixmap):
        left = QPoint(175, 200)
        right = QPoint(225, 200)
        top = QPoint(200, 175)
        bottom = QPoint(200, 225)
        painter = QPainter(pixmap)    
        painter.setPen(QPen(Qt.red,  1, Qt.SolidLine))
        painter.drawLine(left, right)
        painter.drawLine(top, bottom)
        painter.end()
        self._canvas = QPixmap(400, 400)
        self._canvas_center = QPoint(200, 200)
        self._draw_area.setPixmap(self._canvas)

    def paint_event(self):
        painter = QPainter(self._draw_area.pixmap())    
        painter.setPen(QPen(Qt.red,  1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        
        painter.drawEllipse(self._canvas_center, 100, 100)
        painter.end()
        self._draw_area.update()
         
    def reset(self):
        pass

