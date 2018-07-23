import configparser
import cfltools.config
from cfltools.settings import APPFOLDER


def test_defaultconfig():
    cfltools.config.initialize_tests()
    config = configparser.ConfigParser()
    config.read(APPFOLDER + '/cfltools.ini')
    assert config['UNIT_TESTS']['testval'] == 'foo'
    testconfig = config['UNIT_TESTS']
    assert testconfig['testval'] == 'foo'
