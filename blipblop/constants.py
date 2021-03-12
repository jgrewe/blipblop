import os
import glob
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QMediaContent
from PyQt5.QtCore import QUrl

import resources  # needs to be imported somewhere in the project to be picked up by qt

organization_name = "de.uni-tuebingen.neuroetho"
application_name = "BlipBlop"
application_version = 0.1

PACKAGE_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
ICONS_FOLDER = os.path.join(PACKAGE_ROOT, "icons")
DOCS_ROOT_FILE = os.path.join(PACKAGE_ROOT, "docs", "index.md")
SNDS_FOLDER = os.path.join(PACKAGE_ROOT, "sounds")

# Find and list sounds
SNDS_PATHS = glob.glob(os.path.join(SNDS_FOLDER, "*.wav"))
SNDS_PATHS = sorted(SNDS_PATHS)
SNDS_DICT = {}

for snd in SNDS_PATHS:
    SNDS_DICT[snd.split(os.sep)[-1].split(".")[0]] = snd

""" This snippet is kept because it shows how to iterate the qt resources.py file
it = QDirIterator(":", QDirIterator.Subdirectories);
while it.hasNext():
    name = it.next()
    if "sounds/" in name:
        SNDS_DICT[name.split("/")[-1]] = "qrc" + name
"""

# Find and list icons and images
ICONS_PATHS = glob.glob(os.path.join(ICONS_FOLDER, "*.png"))
ICONS_PATHS.extend(glob.glob(os.path.join(ICONS_FOLDER, "*.icns")))
ICONS_PATHS = sorted(ICONS_PATHS)
ICON_DICT = {}

for icon in ICONS_PATHS:
    ICON_DICT[icon.split(os.sep)[-1].split(".")[0]] = icon


def get_sound(name):
    if name in SNDS_DICT.keys():
        url = QUrl.fromLocalFile(SNDS_DICT[name])
        return QMediaContent(url)
    else:
        print("Sound %s not found!" % name)
        return None


def get_icon(name):
    if name in ICON_DICT.keys():
        return QIcon(ICON_DICT[name])
    else:
        return QIcon("blipblop_logo.png")
