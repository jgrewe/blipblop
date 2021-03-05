from PyQt5.QtWidgets import QStackedLayout, QWidget

from blipblop.ui.startscreen import StartScreen
from blipblop.ui.visualblip import VisualBlip
from blipblop.ui.audioblop import AudioBlop
from blipblop.ui.resultsscreen import ResultsScreen

class CentralWidget(QWidget):
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        self._start_screen = StartScreen()
        self._start_screen.visual_task_signal.connect(self.on_new_visual_task)
        self._start_screen.auditory_task_signal.connect(self.on_new_auditory_task)

        self._visual_screen = VisualBlip(self)
        # self._visual_screen.close_signal.connect(self.on_plot_close)

        self._auditory_screen = AudioBlop(self)
        #self._auditory_screen.close_signal.connect(self.on_plot_close)
        
        self._results_screen = ResultsScreen(self)
        #self._results_screen.close_signal.connect(self.on_plot_close)
        
        self._stack = QStackedLayout(self)
        self._stack.addWidget(self._start_screen)     # 0
        self._stack.addWidget(self._visual_screen)    # 1
        self._stack.addWidget(self._auditory_screen)  # 2
        self._stack.addWidget(self._results_screen)   # 3

        self.setLayout(self._stack)
        self._task_results = []
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
        self._stack.setCurrentIndex(0)
        
    def on_new_visual_task(self):
        self._stack.setCurrentIndex(1)
    
    def on_new_auditory_task(self):
        self._stack.setCurrentIndex(2)
