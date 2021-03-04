import os
import glob
from PyQt5.QtGui import QIcon

organization = "bendalab"
application = "blipblop"
version = 0.1

PACKAGE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
ICONS_FOLDER = os.path.join(PACKAGE_ROOT, "icons")
DOCS_ROOT_FILE = os.path.join(PACKAGE_ROOT, "docs", "index.md")

ICONS_PATHS = glob.glob(os.path.join(ICONS_FOLDER, "*.png"))
ICONS_PATHS.extend(glob.glob(os.path.join(ICONS_FOLDER, "*.icns")))
ICONS_PATHS = sorted(ICONS_PATHS)
ICON_DICT = {}
for icon in ICONS_PATHS:
    ICON_DICT[icon.split(os.sep)[-1].split(".")[0]] = icon

def get_icon(name):
    if name in ICON_DICT.keys():
        return QIcon(ICON_DICT[name])
    else:
        return QIcon("nix_logo.png")

