import pytest
import configparser
import os
from cfltools.settings import APPFOLDER


config = configparser.ConfigParser()
config.read(APPFOLDER + '/cfltools.ini')


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
    os.remove(config['UNIT_TESTS']['db_loc'])
