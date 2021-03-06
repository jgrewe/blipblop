from PyQt5.QtWidgets import QAction, QFormLayout, QGridLayout, QLabel, QLineEdit, QPushButton, QSizePolicy, QSlider, QSpinBox, QSplitter, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import QPoint, QRandomGenerator, QTimer, Qt, pyqtSignal, QSettings
from PyQt5.QtGui import QColor, QFont, QKeySequence, QPainter, QBrush, QPen, QPixmap

import os
import blipblop.constants as cnst
import datetime as dt

class SettingsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self._trial_spinner = QSpinBox()
        self._trial_spinner.setMinimum(5)
        self._trial_spinner.setMaximum(25)
        self._trial_spinner.setValue(3)

        self._min_delay_edit = QLineEdit()
        self._min_delay_edit.setText(str("1"))
        self._min_delay_edit.setToolTip("Minimum delay between start of trial and stimulus display [s]")
        self._min_delay_edit.setEnabled(False)
        
        self._max_delay_edit = QLineEdit()
        self._max_delay_edit.setText(str("5"))
        self._max_delay_edit.setToolTip("Maximum delay between start of trial and stimulus display [s]")
        self._max_delay_edit.setEnabled(False)
        
        self._saliency_slider = QSlider(Qt.Horizontal)
        self._saliency_slider.setMinimum(0)
        self._saliency_slider.setMaximum(100)
        self._saliency_slider.setSliderPosition(100)
        self._saliency_slider.setTickInterval(25)
        self._saliency_slider.setTickPosition(QSlider.TicksBelow)
        self._saliency_slider.setToolTip("Saliency of the stimulus, i.e. its opacity")

        self._size_slider = QSlider(Qt.Horizontal)
        self._size_slider.setMinimum(0)
        self._size_slider.setMaximum(200)
        self._size_slider.setSliderPosition(100)
        self._size_slider.setTickInterval(25)
        self._size_slider.setTickPosition(QSlider.TicksBelow)
        self._size_slider.setToolTip("Diameter of the stimulus in pixel")

        self._instructions = QTextEdit()
        self._instructions.setMarkdown("* fixate central cross\n * press start (enter) when ready\n * press space bar as soon as the stimulus occurs")
        self._instructions.setMinimumHeight(200)
        self._instructions.setReadOnly(True)

        form_layout = QFormLayout()
        form_layout.addRow("Settings", None)
        form_layout.addRow("number of trials", self._trial_spinner)
        form_layout.addRow("minimum delay [s]", self._min_delay_edit)
        form_layout.addRow("maximum delay [s]", self._max_delay_edit)
        form_layout.addRow("stimulus saliency", self._saliency_slider)
        form_layout.addRow("stimulus size", self._size_slider)
        form_layout.addRow("instructions", self._instructions)
        self.setLayout(form_layout)

    @property
    def trials(self):
        return self._trial_spinner.value()
    
    @property
    def saliency(self):
        return self._saliency_slider.sliderPosition()
    
    @property
    def size(self):
        return self._size_slider.sliderPosition()
    
    @property
    def min_delay(self):
        return int(self._min_delay_edit.text())
    
    @property
    def max_delay(self):
        return int(self._max_delay_edit.text())
    
    def set_enabled(self, enabled):
        self._trial_spinner.setEnabled(enabled)
        self._saliency_slider.setEnabled(enabled)


class VisualBlip(QWidget):
    task_done = pyqtSignal()
    task_aborted = pyqtSignal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        
        widget = QWidget()
        grid = QGridLayout()
        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(3, 1)
        grid.setRowStretch(1, 1)
        grid.setRowStretch(3, 1)
        widget.setLayout(grid)

        l = QLabel("Visual reaction test")
        l.setPixmap(QPixmap(os.path.join(cnst.ICONS_FOLDER, "visual_task.png")))
        grid.addWidget(l, 0, 0, Qt.AlignLeft)

        l2 =QLabel("Measurement of visual reaction times\npress enter to start")
        font = QFont()
        font.setBold(True)
        font.setPointSize(20)
        l2.setFont(font)
        l2.setStyleSheet("color: #2D4B9A")
        grid.addWidget(l2, 1, 0, 1, 2, Qt.AlignLeft)
        
        settings_btn = QPushButton(cnst.get_icon("settings"), "")
        settings_btn.setToolTip("edit task settings")
        settings_btn.setShortcut(QKeySequence("alt+s"))
        settings_btn.clicked.connect(self.on_toggle_settings)
        grid.addWidget(settings_btn, 0, 3, Qt.AlignRight)
        
        self._status_label = QLabel("Ready to start, press enter ...")
        grid.addWidget(self._status_label, 3, 0, Qt.AlignBaseline)

        self._draw_area = QLabel()
        self._draw_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        grid.addWidget(self._draw_area, 2, 1)
        
        self._settings = SettingsPanel()
        
        self._splitter = QSplitter()
        self._splitter.addWidget(widget)
        self._splitter.addWidget(self._settings)
        self._splitter.setCollapsible(1, True)
        self._splitter.widget(1).hide()
        vbox = QVBoxLayout()
        vbox.addWidget(self._splitter)
        self.setLayout(vbox)
        
        self.reset_canvas()
        self.create_actions()

        self._start_time = None
        self._response_time = None
        self._reaction_times = []
        self._trial_counter = 0
        self._session_running = False
        self._trial_running = False
        self._random_generator = QRandomGenerator()

        self.setFocus()
    
    def create_actions(self):
        self._start_action = QAction("start trial")
        self._start_action.setShortcuts([QKeySequence("enter"), QKeySequence("return")])
        self._start_action.triggered.connect(self.on_trial_start)
        
        self._reaction = QAction("reaction")
        self._reaction.setShortcut(QKeySequence("space"))
        self._reaction.triggered.connect(self.on_reaction)

        self._abort = QAction("abort")
        self._abort.setShortcut(QKeySequence("escape"))
        self._abort.triggered.connect(self.on_abort)
        
        self.addAction(self._start_action)
        self.addAction(self._reaction)
        self.addAction(self._abort)

    def on_reaction(self):
        if not self._session_running or not self._trial_running:
            return
        
        self._response_time = dt.datetime.now()
        if self._trial_counter < self._settings.trials:
            self._status_label.setText("Trial %i of %i, press enter for next trial" % (self._trial_counter, self._settings.trials))
        if self._start_time is None:
            self._reaction_times.append(-1000)
        else:
            reaction_time = self._response_time - self._start_time
            self._reaction_times.append(reaction_time.total_seconds())
        self.reset_canvas()
        self._trial_running = False
        if self._trial_counter >= self._settings.trials:
            self.task_done.emit()

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
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.drawLine(left, right)
        painter.drawLine(top, bottom)
        painter.end()
        self._canvas = QPixmap(400, 400)
        self._canvas_center = QPoint(200, 200)
        self._draw_area.setPixmap(self._canvas)

    def blip(self):
        stim_size = self._settings.size
        painter = QPainter(self._draw_area.pixmap())    
        painter.setPen(QPen(Qt.red,  1, Qt.SolidLine))
        color = QColor(Qt.red)
        color.setAlphaF(self._settings.saliency/100)
        painter.setBrush(QBrush(color, Qt.SolidPattern))      
        painter.drawEllipse(self._canvas_center, stim_size, stim_size)
        painter.end()
        self._start_time = dt.datetime.now()
        self._draw_area.update()
    
    def on_trial_start(self):
        if self._trial_running:
            return
        if not self._session_running:
            self._settings.set_enabled(False)
            self._session_running = True
        self._trial_running = True
        if self._trial_counter >= self._settings.trials:
            self.task_done.emit
            return
        self._trial_counter += 1
        self._status_label.setText("Trial %i of %i running" % (self._trial_counter, self._settings.trials))
        self.setStatusTip("Test")
        min_interval = int(self._settings.min_delay * 10)
        max_interval = int(self._settings.max_delay * 10)
        interval = self._random_generator.bounded(min_interval, max_interval) * 100
        self._start_time = None
        timer = QTimer(self)
        timer.setSingleShot(True)
        timer.setInterval(int(interval))
        timer.timeout.connect(self.blip)
        timer.start()
    
    def on_abort(self):
        self.reset()
        self.task_aborted.emit()
    
    @property
    def results(self):
        return self._reaction_times
        
    def reset(self):
        self.reset_canvas()
        self._trial_counter = 0
        self._session_running = 0
        self._reaction_times = []
        self._trial_running = False
        self._session_running = False
        self._status_label.setText("Ready to start...")
        self._settings.set_enabled(True)
        
    def on_toggle_settings(self):
        if self._splitter.sizes()[1] > 0:
            self._splitter.widget(1).hide()
        else:
            self._splitter.widget(1).show()
