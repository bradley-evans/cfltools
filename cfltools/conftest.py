import pytest
import configparser
import os
from cfltools.settings import APPFOLDER


if not os.path.exists(APPFOLDER):
    os.makedirs(APPFOLDER)
open(APPFOLDER + '/cfltools.ini', 'a').close()
config = configparser.ConfigParser()


def initialize_tests():
    if not os.path.exists(APPFOLDER):
        os.makedirs(APPFOLDER)
    config['DEFAULT'] = {'testval': 'foo',
                            'db_loc': APPFOLDER + '/test.db',
                            'max_tor_requests': '10',
                            'max_whois_requests': '10'
                            }
    config['UNIT_TESTS'] = {}
    config['USER'] = {}
    with open(APPFOLDER + '/cfltools.ini', 'w') as configfile:
        config.write(configfile)


@pytest.fixture(scope="module")
def dummy_db_conn():
    """ Dummy database connection object. Will create an empty database
    for testing and tear down after.
    """
    import sqlite3
    import cfltools.dbutils as dbutils
    initialize_tests()
    conn = sqlite3.connect(config['UNIT_TESTS']['db_loc'])
    dbutils.validateDB(conn)
    yield conn
    conn.close()
    os.remove(config['UNIT_TESTS']['db_loc'])


@pytest.fixture(scope="module")
def dummy_config():
    configstring = '[DEFAULT]\n' \
                   'testval = foo\n' \
                   'db_loc = {}/test.db\n' \
                   'max_tor_requests = 10\n' \
                   'max_whois_requests = 10\n' \
                   '[UNIT_TESTS]\n' \
                   '[USER]\n' \
                   .format(APPFOLDER)
    config = configparser.ConfigParser()
    config.read_string(configstring)
    yield config
