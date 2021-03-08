from PyQt5.QtWidgets import QComboBox, QFormLayout, QSlider, QSpinBox, QTextEdit, QWidget
from PyQt5.QtCore import Qt, QSettings
import blipblop.constants as cnst


class TaskSettings(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.settings = QSettings()
        
        self._trial_spinner = QSpinBox()
        self._trial_spinner.setMinimum(5)
        self._trial_spinner.setMaximum(25)
        self._trial_spinner.setValue(int(self.settings.value("task/trials", 5)))
        self._trial_spinner.setToolTip("Number of consecutive trials (5 - 25)")

        self._min_delay_spinner = QSpinBox()
        self._min_delay_spinner.setMinimum(1)
        self._min_delay_spinner.setMaximum(10)
        self._min_delay_spinner.setValue(int(self.settings.value("task/min_delay", 1)))
        self._min_delay_spinner.setToolTip("Minimum delay between start of trial and stimulus display [s]")

        self._max_delay_spinner = QSpinBox()
        self._max_delay_spinner.setMinimum(1)
        self._max_delay_spinner.setMaximum(10)
        self._max_delay_spinner.setValue(int(self.settings.value("task/max_delay", 5)))
        self._max_delay_spinner.setToolTip("Maximum delay between start of trial and stimulus display [s]")

        self._countdown_spinner = QSpinBox()
        self._countdown_spinner.setMinimum(1)
        self._countdown_spinner.setMaximum(10)
        self._countdown_spinner.setValue(int(self.settings.value("task/pause", 3)))
        self._countdown_spinner.setToolTip("Pause between trials [s]")

        self._saliency_slider = QSlider(Qt.Horizontal)
        self._saliency_slider.setMinimum(0)
        self._saliency_slider.setMaximum(100)
        self._saliency_slider.setSliderPosition(int(self.settings.value("task/saliency", 100)))
        self._saliency_slider.setTickInterval(25)
        self._saliency_slider.setTickPosition(QSlider.TicksBelow)

        self._instructions = QTextEdit()
        self._instructions.setMarkdown("* fixate central cross\n * press start (enter) when ready\n * press space bar as soon as the stimulus occurs")
        self._instructions.setMinimumHeight(200)
        self._instructions.setReadOnly(True)

        self.form_layout = QFormLayout()
        self.form_layout.addRow("Settings", None)
        self.form_layout.addRow("number of trials", self._trial_spinner)
        self.form_layout.addRow("minimum delay [s]", self._min_delay_spinner)
        self.form_layout.addRow("maximum delay [s]", self._max_delay_spinner)
        self.form_layout.addRow("pause [s]", self._countdown_spinner)
        self.form_layout.addRow("stimulus saliency", self._saliency_slider)
        self.form_layout.addRow("instructions", self._instructions)
        self.setLayout(self.form_layout)

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
        return self._min_delay_spinner.value()

    @property
    def max_delay(self):
        return self._max_delay_spinner.value()

    @property
    def countdown(self):
        return self._countdown_spinner.value()

    def set_enabled(self, enabled):
        self._trial_spinner.setEnabled(enabled)
        self._saliency_slider.setEnabled(enabled)
        self._countdown_spinner.setEnabled(enabled)
        self._min_delay_spinner.setEnabled(enabled)
        self._max_delay_spinner.setEnabled(enabled)

    def store_settings(self):
        self.settings.setValue("task/trials", self.trials)
        self.settings.setValue("task/salience", self.saliency)
        self.settings.setValue("task/min_delay", self.min_delay)
        self.settings.setValue("task/max_delay", self.max_delay)
        self.settings.setValue("task/pause", self.countdown)


class AuditoryTaskSettings(TaskSettings):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._saliency_slider.setToolTip("Saliency of the stimulus, i.e. its loudness")

        self._sound_combo = QComboBox()
        for k in cnst.SNDS_DICT.keys():
            self._sound_combo.addItem(k)
        self._sound_combo.setCurrentIndex(int(self.settings.value("auditory_task/sound_index", 0)))
        self.form_layout.insertRow(self.form_layout.rowCount() - 1, "stimulus sound", self._sound_combo)

    def set_enabled(self, enabled):
        super().set_enabled(enabled)
        self._sound_combo.setEnabled(enabled)

    def store_settings(self):
        super().store_settings()
        self.settings.setValue("auditory_task/sound_index", self._sound_combo.currentIndex)

    @property
    def sound(self):
        return self._sound_combo.currentText()


class VisualTaskSettings(TaskSettings):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self._saliency_slider.setToolTip("Saliency of the stimulus, i.e. its opacity")

        self._size_slider = QSlider(Qt.Horizontal)
        self._size_slider.setMinimum(0)
        self._size_slider.setMaximum(200)
        self._size_slider.setSliderPosition(int(self.settings.value("visual_task/stimulus_size", 100)))
        self._size_slider.setTickInterval(25)
        self._size_slider.setTickPosition(QSlider.TicksBelow)
        self._size_slider.setToolTip("Diameter of the stimulus in pixel")

        self.form_layout.insertRow(self.form_layout.rowCount() - 1, "stimulus size", self._size_slider)

    def set_enabled(self, enabled):
        super().set_enabled(enabled)
        self._size_slider.setEnabled(enabled)

    def store_settings(self):
        super().store_settings()
        self.settings.setValue("visual_task/stimulus_size", self.size)

    @property
    def size(self):
        return self._size_slider.sliderPosition()
