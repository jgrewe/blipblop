import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QSettings
from blipblop.ui.mainwindow import BlipBlop
import blipblop.constants as cnst

try:
    # Include in try/except block if you're also targeting Mac/Linux
    from PyQt5.QtWinExtras import QtWin
    myappid = "%s.%s" %(cnst.organization_name, cnst.application_version)
    QtWin.setCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

def main():
    print("executing main.main")
    app = QApplication(sys.argv)
    app.setApplicationName(cnst.application_name)
    app.setApplicationVersion(str(cnst.application_version))
    app.setOrganizationDomain(cnst.organization_name)
    app.setWindowIcon(QIcon(":/icons/app_icon_png"))
    settings = QSettings()
    width = int(settings.value("app/width", 1024))
    height = int(settings.value("app/height", 768))
    x = int(settings.value("app/pos_x", 100))
    y = int(settings.value("app/pos_y", 100))
    window = BlipBlop()
    window.setMinimumWidth(800)
    window.setMinimumHeight(600)
    window.resize(width, height)
    window.move(x, y)
    window.show()
    
    code = app.exec_()
    print("Application exit!")
    pos = window.pos()
    settings.setValue("app/width", window.width())
    settings.setValue("app/height", window.height())
    settings.setValue("app/pos_x", pos.x())
    settings.setValue("app/pos_y", pos.y())
    sys.exit(code)
