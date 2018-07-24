import configparser
import pytest
import cfltools.config
from cfltools.settings import APPFOLDER
config = configparser.ConfigParser()


def test_defaultconfig():
    cfltools.config.initialize_tests()
    config.read(APPFOLDER + '/cfltools.ini')
    assert config['UNIT_TESTS']['testval'] == 'foo'
    testconfig = config['UNIT_TESTS']
    assert testconfig['testval'] == 'foo'


@pytest.fixture(scope="module")
def dummy_db_conn():
    """ Dummy database connection object. Will create an empty database
    for testing and tear down after.
    """
    import sqlite3
    import cfltools.dbutils as dbutils
    conn = sqlite3.connect(config['UNIT_TESTS']['db_loc'])
    dbutils.validateDB(conn)
    yield conn
    conn.close()

def test_dummydb(dummy_db_conn):
    cursor = dummy_db_conn.cursor()
    cursor.execute('SELECT * FROM isp')

