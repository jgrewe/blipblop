#!/usr/bin/python3
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings
from blipblop.ui.mainwindow import BlipBlop
import blipblop.constants as cnst

try:
    # Include in try/except block if you're also targeting Mac/Linux
    from PyQt5.QtWinExtras import QtWin
    myappid = 'neuroetho.uni-tuebingen.de.blipblop.0.1'
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("blipblop")
    app.setApplicationVersion("0.1")
    app.setOrganizationDomain("neuroetho.uni-tuebingen.de")
    app.setWindowIcon(cnst.get_icon("blipblop_logo.png"))
    settings = QSettings()
    width = settings.value("app/width", 1024)
    height = settings.value("app/height", 768)
    x = settings.value("app/pos_x", 100)
    y = settings.value("app/pos_y", 100)
    window = BlipBlop()
    window.setMinimumWidth(800)
    window.setMinimumHeight(600)
    window.resize(width, height)
    window.move(x, y)
    window.show()
    
    code = app.exec_()
    pos = window.pos()
    settings.setValue("app/width", window.width())
    settings.setValue("app/height", window.height())
    settings.setValue("app/pos_x", pos.x())
    settings.setValue("app/pos_y", pos.y())
    sys.exit(code)
    

if __name__ == "__main__":
    main()