import configparser
import pytest
import cfltools.config
from cfltools.settings import APPFOLDER
config = configparser.ConfigParser()


def test_defaultconfig():
    config.read(APPFOLDER + '/cfltools.ini')
    assert config['UNIT_TESTS']['testval'] == 'foo'
    testconfig = config['UNIT_TESTS']
    assert testconfig['testval'] == 'foo'


def test_dummydb(dummy_db_conn):
    cursor = dummy_db_conn.cursor()
    cursor.execute('SELECT * FROM isp')
