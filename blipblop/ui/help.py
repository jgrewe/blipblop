from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QFrame, QHBoxLayout, QPushButton, QSizePolicy, QTextBrowser, QVBoxLayout, QWidget
from PyQt5.QtCore import QUrl

import blipblop.constants as cnst

class HelpDialog(QDialog):
    
    def __init__(self, parent = None) -> None:
        super().__init__(parent=parent)
        
        self.setModal(True)
        self.setMinimumSize(500, 750)

        self.help = HelpBrowser()

        self.help._edit.historyChanged.connect(self._on_history_changed)
        
        self.back_btn = QPushButton(QIcon(":/icons/docs_back"), "back")
        self.back_btn.setEnabled(False)
        self.back_btn.clicked.connect(self.help._edit.backward)
        self.home_btn = QPushButton(QIcon(":/icons/docs_home"),"home")
        self.home_btn.clicked.connect(self.help._edit.home)
        self.fwd_btn = QPushButton(QIcon(":/icons/docs_fwd"),"forward")
        self.fwd_btn.setEnabled(False)
        self.fwd_btn.clicked.connect(self.help._edit.forward)
        
        empty = QWidget()
        empty.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        hbox = QHBoxLayout()
        hbox.addWidget(self.back_btn)
        hbox.addWidget(self.home_btn)
        hbox.addWidget(self.fwd_btn)
        hbox.addWidget(empty)      
        
        bbox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        bbox.accepted.connect(self.accept)
        layout = QVBoxLayout()

        layout.addLayout(hbox)
        layout.addWidget(self.help)
        layout.addWidget(bbox)
        self.setLayout(layout)
        
    def _on_history_changed(self):
        self.back_btn.setEnabled(self.help._edit.isBackwardAvailable())
        self.fwd_btn.setEnabled(self.help._edit.isForwardAvailable())


class HelpBrowser(QWidget):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setLayout(QVBoxLayout())
        # FIXME https://stackoverflow.com/a/43217828  about loading from esource files
        doc_url = QUrl.fromLocalFile(cnst.DOCS_ROOT_FILE)
        self._edit = QTextBrowser()
        self._edit.setOpenLinks(True)
        self._edit.setOpenExternalLinks(True)
        self._edit.setSource(doc_url)
        self._edit.setEnabled(True)
        self._edit.setFrameShape(QFrame.NoFrame)

        self.layout().addWidget(self._edit)
