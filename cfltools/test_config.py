import configparser
import pytest
import cfltools.config
from cfltools.settings import APPFOLDER
config = configparser.ConfigParser()


def test_defaultconfig(dummy_config):
    import os.path
    assert os.path.isfile(APPFOLDER + '/cfltools.ini') == True
    assert dummy_config["UNIT_TESTS"]["testval"] == 'foo'
    testconfig = dummy_config['UNIT_TESTS']
    assert testconfig['testval'] == 'foo'


def test_dummydb(dummy_db_conn):
    cursor = dummy_db_conn.cursor()
    cursor.execute('SELECT * FROM isp')
