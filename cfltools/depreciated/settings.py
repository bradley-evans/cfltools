from appdirs import user_data_dir
from os.path import dirname

APPFOLDER = user_data_dir("cfltools")
INSTALLPATH = dirname(__file__)  # will be the location of this settings.py file
