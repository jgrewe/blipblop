from PyQt5.QtWidgets import QAction, QGridLayout, QLabel, QPushButton, QSizePolicy, QSplitter, QVBoxLayout, QWidget
from PyQt5.QtCore import QPoint, QRandomGenerator, QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QIcon, QKeySequence, QPainter, QBrush, QPen, QPixmap

from blipblop.ui.countdownlabel import CountdownLabel
from blipblop.ui.settings import VisualTaskSettings
import datetime as dt


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

        icon_label = QLabel("Visual reaction test")
        icon_label.setPixmap(QPixmap(":/icons/visual_task"))
        grid.addWidget(icon_label, 0, 0, Qt.AlignLeft)

        heading_label = QLabel("Measurement of visual reaction times\npress enter to start")
        font = QFont()
        font.setBold(True)
        font.setPointSize(20)
        heading_label.setFont(font)
        heading_label.setStyleSheet("color: #2D4B9A")
        grid.addWidget(heading_label, 1, 0, 1, 2, Qt.AlignLeft)

        settings_btn = QPushButton(QIcon(":/icons/settings"), "")
        settings_btn.setToolTip("edit task settings")
        settings_btn.setShortcut(QKeySequence("alt+s"))
        settings_btn.clicked.connect(self.on_toggle_settings)
        grid.addWidget(settings_btn, 0, 3, Qt.AlignRight)

        self._status_label = QLabel("Ready to start, press enter ...")
        grid.addWidget(self._status_label, 4, 0, Qt.AlignBaseline)

        self._countdown_label = CountdownLabel(text="Next trial in:")
        grid.addWidget(self._countdown_label, 4, 1, Qt.AlignCenter)
        self._countdown_label.countdown_done.connect(self.run_trial)

        self._draw_area = QLabel()
        self._draw_area.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        grid.addWidget(self._draw_area, 2, 1)

        self._settings = VisualTaskSettings()

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
            self._status_label.setText("Trial %i of %i" % (self._trial_counter, self._settings.trials))
        if self._start_time is None:
            self._reaction_times.append(-1000)
        else:
            reaction_time = self._response_time - self._start_time
            self._reaction_times.append(reaction_time.total_seconds())
        self.reset_canvas()
        self._trial_running = False
        if self._timer.isActive():
            self._timer.stop()
        if self._trial_counter >= self._settings.trials:
            self.task_done.emit()
            return
        self._countdown_label.start(self._settings.countdown)

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
        self._countdown_label.start(time=self._settings.countdown)

    def run_trial(self):
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
        self._timer = QTimer(self)
        self._timer.setSingleShot(True)
        self._timer.setInterval(int(interval))
        self._timer.timeout.connect(self.blip)
        self._timer.start()

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
        self._countdown_label.stop()
        self._settings.set_enabled(True)

    def on_toggle_settings(self):
        if self._splitter.sizes()[1] > 0:
            self._splitter.widget(1).hide()
        else:
            self._splitter.widget(1).show()
