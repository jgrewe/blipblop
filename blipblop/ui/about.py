import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

import blipblop.constants as cnst


class AboutDialog(QDialog):
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setModal(True)
        about = About(self)
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(about)
        bbox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        bbox.accepted.connect(self.accept)
        self.layout().addWidget(bbox)


class About(QWidget):
    
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setLayout(QVBoxLayout())
        
        heading = QLabel("BlipBlop")
        font = heading.font()
        font.setPointSize(18)
        font.setBold(True)
        heading.setFont(font)
        heading.setAlignment(Qt.AlignCenter)
        subheading = QLabel("How fast are you?\nmeasure your reaction times to visual and auditory stimuli.\nby Jan Grewe")
        subheading.setAlignment(Qt.AlignCenter)
        nix_link = QLabel("https://github.com/jgrewe/blipblop")
        nix_link.setOpenExternalLinks(True)
        nix_link.setAlignment(Qt.AlignCenter)

        # rtd_link = QLabel("https://nixio.readthedocs.io/en/master/")
        # rtd_link.setOpenExternalLinks(True)
        # rtd_link.setAlignment(Qt.AlignCenter)

        iconlabel = QLabel()
        pixmap = QPixmap(os.path.join(cnst.ICONS_FOLDER, "nix_logo.png"))
        s = pixmap.size()
        new_height = int(s.height() * 300/s.width())
        pixmap = pixmap.scaled(300, new_height, Qt.KeepAspectRatio, Qt.FastTransformation)
        iconlabel.setPixmap(pixmap)
        iconlabel.setMaximumWidth(300)
        iconlabel.setAlignment(Qt.AlignCenter)
        iconlabel.setScaledContents(True)
        
        self.layout().addWidget(heading)
        self.layout().addWidget(subheading)
        self.layout().addWidget(iconlabel)
        self.layout().addWidget(nix_link)
        # self.layout().addWidget(rtd_link)
