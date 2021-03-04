import sys
from PyQt5.QtWidgets import QWidget, QFileDialog, QMainWindow, QMenuBar, QToolBar, QAction, QStatusBar, QSizePolicy
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import QSize, QSettings, Qt

import blipblop.constants as cnst
from blipblop.ui.help import HelpDialog
from blipblop.ui.about import AboutDialog
from blipblop.ui.centralwidget import CentralWidget


class BlipBlop(QMainWindow):
    
    def __init__(self, *args, **kwargs):
        super(BlipBlop, self).__init__(*args, **kwargs)
        self._current_item = None
        self.setWindowTitle("BlipBlop")
        
        self.setStatusBar(QStatusBar(self))
        self.setMenuBar(QMenuBar(self))
        self.create_actions()
        self._task_results = []
        self._cw = CentralWidget()
        self.setCentralWidget(self._cw)
        self.show()
    
    def create_actions(self):
        self._quit_action = QAction(cnst.get_icon("nixview_quit"), "Quit", self)
        self._quit_action.setStatusTip("Quit BlipBlop")
        self._quit_action.setShortcut(QKeySequence("Ctrl+q"))
        self._quit_action.triggered.connect(self.on_quit)

        self._new_action = QAction(cnst.get_icon("new_task"), "New session", self)
        self._new_action.setStatusTip("Start a new session discarding previous results")
        self._new_action.setShortcut(QKeySequence("Ctrl+n"))
        self._new_action.triggered.connect(self.on_new)

        """
        self._plot_action = QAction(cnst.get_icon("nix_data_array"), "Plot", self)
        self._plot_action.setStatusTip("Plot currently selected entity")
        self._plot_action.setShortcut(QKeySequence("Ctrl+p"))
        self._plot_action.setEnabled(False)
        self._plot_action.triggered.connect(self.on_item_plot)
        """

        self._results_action = QAction(cnst.get_icon("nix_data_frame"), "Show results", self)
        self._results_action.setStatusTip("Show results as table")
        self._results_action.setShortcut(QKeySequence("Ctrl+t"))
        self._results_action.setEnabled(True)
        #self._table_action.triggered.connect(self.on_file_close)

        self._about_action = QAction("about")
        self._about_action.setStatusTip("Show about dialog")
        self._about_action.setEnabled(True)
        self._about_action.triggered.connect(self.on_about)

        self._help_action = QAction(cnst.get_icon("nixview_help"), "help")
        self._help_action.setStatusTip("Show help dialog")
        self._help_action.setShortcut(QKeySequence("F1"))
        self._help_action.setEnabled(True)
        self._help_action.triggered.connect(self.on_help)

        self._visual_task_action = QAction(cnst.get_icon("visual_task"), "visual")
        self._visual_task_action.setStatusTip("Start measuring visual reaction times")
        self._visual_task_action.setEnabled(True)

        self._auditory_task_action = QAction(cnst.get_icon("auditory_task"), "auditory")
        self._auditory_task_action.setStatusTip("Start measuring auditory reaction times")
        self._auditory_task_action.setEnabled(False)

        self.create_toolbar()
        self.create_menu() 

    def create_toolbar(self):
        self._toolbar = QToolBar("My main toolbar")
        #self._toolbar.setStyleSheet("QToolButton:!hover {background-color:none}")
        self._toolbar.setAllowedAreas(Qt.LeftToolBarArea | Qt.TopToolBarArea)
        self._toolbar.setIconSize(QSize(32, 32))

        # self._toolbar.addAction(self._file_open_action)
        #self._toolbar.addAction(self._file_close_action)
        self._toolbar.addAction(self._new_action)

        self._toolbar.addSeparator()
        self._toolbar.addAction(self._visual_task_action)
        self._toolbar.addAction(self._auditory_task_action)
        self._toolbar.addAction(self._results_action)
        self._toolbar.addAction(self._help_action)
        
        empty = QWidget()
        empty.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self._toolbar.addWidget(empty)
        self._toolbar.addSeparator()
        self._toolbar.addAction(self._quit_action)

        self.addToolBar(Qt.LeftToolBarArea, self._toolbar)

    def create_menu(self):
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        # file_menu.addAction(self._file_open_action)
        # file_menu.addAction(self._file_close_action)
        # file_menu.addSeparator()
        file_menu.addAction(self._quit_action)
        
        task_menu = menu.addMenu("&Tasks")
        task_menu.addAction(self._new_action)
        task_menu.addSeparator()
        task_menu.addAction(self._visual_task_action)
        task_menu.addAction(self._auditory_task_action)
        #plot_menu = menu.addMenu("&Plot")
        #plot_menu.addAction(self._plot_action)
        #plot_menu.addAction(self._table_action)
        
        help_menu = menu.addMenu("&Help")
        help_menu.addAction(self._about_action)
        help_menu.addAction(self._help_action)
        self.setMenuBar(menu)

    def on_quit(self, s):
        sys.exit()

    def on_new(self):
        self._cw.reset()
        

    def on_about(self):
        about = AboutDialog(self)
        about.show()
        pass

    def on_help(self, e):
        help = HelpDialog(self)
        help.show()
        
    def on_visual(self):
        pass# cw.