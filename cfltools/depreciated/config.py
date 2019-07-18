import configparser
import logging
from cfltools.settings import APPFOLDER


def initialize_defaults():
    from appdirs import user_data_dir
    config = configparser.ConfigParser()
    default_appfolder = APPFOLDER
    default_database = APPFOLDER + '/default.db'
    config['DEFAULT'] = {'appfolder': default_appfolder,
                         'db_loc': default_database,
                         'max_tor_requests': '100',
                         'max_whois_requests': '100'
                         }
    config['USER'] = {}
    with open(default_appfolder + '/cfltools.ini', 'w') as configfile:
        config.write(configfile)

def log_generator(name):
    """
    Log handler for cfltools
    """

    logger = logging.getLogger('cfltools/'+name)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(APPFOLDER+'/cfltools.log')
    c_handler.setLevel(logging.DEBUG)
    f_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger
