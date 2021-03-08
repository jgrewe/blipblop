import io
import csv
from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QKeySequence
from PyQt5.QtWidgets import QAction, QLabel, QStackedLayout, QTableWidget, QTableWidgetItem, QWidget
from PyQt5.QtCore import Qt, pyqtSignal

import blipblop.constants as cnst
from blipblop.util.results import MeasurementResults


class ResultsScreen(QWidget):
    back_signal = pyqtSignal()

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.table = QTableWidget()
        self._stack = QStackedLayout(self)
        label = QLabel("There are no results to show\n(press ESC to go back)")
        label.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setBold(True)
        font.setPointSize(25)
        label.setStyleSheet("color: #2D4B9A")
        label.setFont(font)
        self._stack.addWidget(label)         # 0
        self._stack.addWidget(self.table)    # 1
        self.setLayout(self._stack)

        self._back_action = QAction("back")
        self._back_action.setShortcut(QKeySequence("escape"))
        self._back_action.triggered.connect(self.on_back)

        self._copy_action = QAction("copy")
        self._copy_action.setShortcut(QKeySequence("ctrl+c"))
        self._copy_action.triggered.connect(self.copy_selection)

        self.addAction(self._back_action)
        self.addAction(self._copy_action)

    def set_results(self, measurement_results):
        if len(measurement_results) == 0:
            return

        for mr in measurement_results:
            if not isinstance(mr, MeasurementResults):
                print("Some result entries are no MeasurementResults!")
                return

        row_count = max([len(r.results) for r in measurement_results])
        col_count = len(measurement_results)
        self.table.setRowCount(row_count)
        self.table.setColumnCount(col_count)

        for col, mr in enumerate(measurement_results):
            headerItem = QTableWidgetItem(cnst.get_icon("visual_task") if "visual" in mr.name.lower() else cnst.get_icon("auditory_task"), "")
            headerItem.setToolTip("%s started at\n %s " % (mr.name, mr.starttime))
            self.table.setHorizontalHeaderItem(col, headerItem)
            for row, r in enumerate(mr.results):
                item = QTableWidgetItem(str(r))
                self.table.setItem(row, col, item)

        self._stack.setCurrentIndex(1)

    def copy_selection(self):
        """
        solution stolen from StackOverflow https://stackoverflow.com/a/55204654
        """
        selection = self.table.selectedIndexes()
        if selection:
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            table = [[''] * colcount for _ in range(rowcount)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
            stream = io.StringIO()
            csv.writer(stream, delimiter='\t').writerows(table)
            QtWidgets.qApp.clipboard().setText(stream.getvalue())
        return

    def on_back(self):
        self.back_signal.emit()

    def reset(self):
        self.table.clear()
        self._stack.setCurrentIndex(0)
