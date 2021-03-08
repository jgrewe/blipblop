import os
import glob
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtCore import QDirIterator, QUrl

import resources

SNDS_DICT = {}
it = QDirIterator(":", QDirIterator.Subdirectories);
while it.hasNext():
    name = it.next()
    if "sounds/" in name:
        SNDS_DICT[name.split("/")[-1]] = "qrc" + name
print(SNDS_DICT)
organization_name = "de.uni-tuebingen.neuroetho"
application_name = "BlipBlop"
application_version = 0.1

PACKAGE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
ICONS_FOLDER = os.path.join(PACKAGE_ROOT, "icons")
DOCS_ROOT_FILE = os.path.join(PACKAGE_ROOT, "docs", "index.md")
SNDS_FOLDER = os.path.join(PACKAGE_ROOT, "sounds")

ICONS_PATHS = glob.glob(os.path.join(ICONS_FOLDER, "*.png"))
ICONS_PATHS.extend(glob.glob(os.path.join(ICONS_FOLDER, "*.icns")))
ICONS_PATHS = sorted(ICONS_PATHS)
ICON_DICT = {}

for icon in ICONS_PATHS:
    ICON_DICT[icon.split(os.sep)[-1].split(".")[0]] = icon

def get_sound(name):
    if name in SNDS_DICT.keys():
        url = QUrl(SNDS_DICT[name])
        return QMediaContent(url)
    else:
        print("Sound %s not found!" % name)
        return None


def get_icon(name):
    if name in ICON_DICT.keys():
        return QIcon(ICON_DICT[name])
    else:
        return QIcon("blipblop_logo.png")
