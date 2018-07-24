import configparser
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

def initialize_tests():
    config = configparser.ConfigParser()
    config['UNIT_TESTS'] = {'testval': 'foo',
                            'db_loc': APPFOLDER + '/test.db',
                            'max_tor_requests': '10',
                            'max_whois_requests': '10'
                            }

    with open(APPFOLDER + '/cfltools.ini', 'w') as configfile:
        config.write(configfile)
