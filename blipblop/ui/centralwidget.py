from PyQt5.QtWidgets import QStackedLayout, QWidget

import datetime as dt

from blipblop.ui.startscreen import StartScreen
from blipblop.ui.visualblip import VisualBlip
from blipblop.ui.audioblop import AudioBlop
from blipblop.ui.resultsscreen import ResultsScreen
from blipblop.util.results import MeasurementResults

class CentralWidget(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        self._start_screen = StartScreen()
        self._start_screen.visual_task_signal.connect(self.on_new_visual_task)
        self._start_screen.auditory_task_signal.connect(self.on_new_auditory_task)

        self._visual_screen = VisualBlip(self)
        self._visual_screen.task_done.connect(self.on_visual_task_done)
        self._visual_screen.task_aborted.connect(self.on_task_aborted)

        self._auditory_screen = AudioBlop(self)
        self._auditory_screen.task_done.connect(self.on_auditory_task_done)
        self._auditory_screen.task_aborted.connect(self.on_task_aborted)
        
        self._results_screen = ResultsScreen(self)
        self._results_screen.back_signal.connect(self.on_task_aborted)
        
        self._stack = QStackedLayout(self)
        self._stack.addWidget(self._start_screen)     # 0
        self._stack.addWidget(self._visual_screen)    # 1
        self._stack.addWidget(self._auditory_screen)  # 2
        self._stack.addWidget(self._results_screen)   # 3

        self.setLayout(self._stack)
        self._task_results = []
        self._task_start = None
        self._stack.setCurrentIndex(0)

    def show_file_content(self):
        self._stack.setCurrentIndex(1)
        self._visual_stims_screen.update()

    def plot_item(self, item_descriptor):
        self._stack.setCurrentIndex(2)
        self._auditory_screen.plot(item_descriptor)

    def on_plot_close(self):
        self._stack.setCurrentIndex(1)

    def reset(self):
        self._task_results = []
        self._results_screen.reset()
        self._stack.setCurrentIndex(0)
        
    def on_new_visual_task(self):
        self._task_start = dt.datetime.now()
        self._stack.setCurrentIndex(1)

    def on_visual_task_done(self):
        task_results = MeasurementResults("Visual task")
        task_results.starttime = self._task_start
        task_results.results = self._visual_screen.results
        self._task_results.append(task_results)
        self._visual_screen.reset
        self._stack.setCurrentIndex(0)

    def on_task_aborted(self):
        self._stack.setCurrentIndex(0)

    def on_new_auditory_task(self):
        self._stack.setCurrentIndex(2)
        
    def on_auditory_task_done(self):
        task_results = MeasurementResults("Auditory task")
        task_results.starttime = self._task_start
        task_results.results = self._auditory_screen.results
        self._task_results.append(task_results)
        self._auditory_screen.reset
        self._stack.setCurrentIndex(0)

    def on_show_results(self):
        self._results_screen.set_results(self._task_results)
        self._stack.setCurrentIndex(3)
