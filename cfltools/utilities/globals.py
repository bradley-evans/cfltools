"""
Global variables and settings used in CFLTools.
"""

from os.path import dirname
from pathlib import Path
from appdirs import user_data_dir


APPDIR = Path(user_data_dir("cfltools"))
UTILDIR = dirname(__file__)  # will be the location of this settings.py file
VERSION = '0.0.5'
