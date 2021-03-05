#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import QApplication
from blipblop.ui.mainwindow import BlipBlop

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("blipblop")
    app.setApplicationVersion("0.1")
    app.setOrganizationDomain("neuroetho.uni-tuebingen.de")
    window = BlipBlop()
    window.setMinimumWidth(800)
    window.setMinimumHeight(600)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()