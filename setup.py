import glob
import json
import os

# Use setuptools compulsorily, as the distutils doesn't work out well for the
# installation procedure. The 'install_requires' and 'data_files' have better
# support in setuptools.
from setuptools import setup


with open(os.path.join("blipblop", "info.json")) as infofile:
    infodict = json.load(infofile)

NAME = infodict["NAME"]
VERSION = infodict["VERSION"]
AUTHOR = infodict["AUTHOR"]
CONTACT = infodict["CONTACT"]
HOMEPAGE = infodict["HOMEPAGE"]
CLASSIFIERS = infodict["CLASSIFIERS"]
DESCRIPTION = infodict["DESCRIPTION"]

README = "README.md"
with open(README) as f:
    description_text = f.read()

packages = [
    "blipblop",
]

install_req = ["PyQt5"]

data_files = [("icons", glob.glob(os.path.join("icons", "*.png"))),
              ("icons", glob.glob(os.path.join("icons", "*.ic*"))),
              ("sounds", glob.glob(os.path.join("sounds", "*.wav"))),
              (".", ["LICENSE"]),
              ("docs", glob.glob(os.path.join("docs", "*.md")))
              ]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    author_email=CONTACT,
    url=HOMEPAGE,
    packages=packages,
    install_requires=install_req,
    include_package_data=True,
    data_files=data_files,
    long_description=description_text,
    long_description_content_type="text/markdown",
    classifiers=CLASSIFIERS,
    license="BSD",
    entry_points={
        "gui_scripts": ["blipblop = blipblop:main []"],
        "console_scripts": ["blipblop = blipblop:main []"]
        }
)
