"""
Tests for utilities
"""

import pytest
from cfltools.utilities import Config, Time, APPDIR


@pytest.fixture
def dummy_configfile(tmpdir):
    conf_loc = tmpdir/'testconfig.ini'
    config = Config(conf_loc)
    yield conf_loc


def test_config_initialize_and_read(tmpdir):
    """
    Tests the opening of a new config file, and reading
    of expected defaults.
    """
    test_config = Config(tmpdir/'testconfig.ini')
    try:
        assert test_config.read('appfolder') == APPDIR.as_posix()
    except AssertionError as e:
        e.args += ('value from config: {}'.format(test_config.read('appfolder')),
                   'control value:     {}'.format(APPDIR.as_posix()))
        raise
    assert test_config.read('db_loc') == (APPDIR / 'cfltools.db').as_posix()


def test_config_write_then_read(tmpdir):
    """
    Writes an arbitrary value and then reads it.
    """
    test_config = Config(tmpdir/'testconfig.ini')
    test_config.write('foo', 'bar')
    assert test_config.read('foo') == 'bar'
    test_config.write('dead', 'beef')
    assert test_config.read('foo') == 'bar'
    assert test_config.read('dead') == 'beef'
    test_config.write('foo', 'fizzbuzz')
    assert test_config.read('foo') == 'fizzbuzz'

def test_multiple_config_open(tmpdir):
    config1 = Config(tmpdir/'testconfig.ini')
    assert config1.read('appfolder') == APPDIR.as_posix()
    config1 = Config(tmpdir/'testconfig.ini')
    assert config1.read('appfolder') == APPDIR.as_posix()
    config2 = Config(tmpdir/'testconfig.ini')
    assert config2.read('appfolder') == APPDIR.as_posix()
    config1.write('appfolder', 'beepboop')
    assert config2.read('appfolder') == 'beepboop'


def test_update_asn(tmpdir):
    from cfltools.utilities import asn_update
    from os.path import exists
    newfile = asn_update(tmpdir)
    assert exists(newfile)

def test_time():
    time = Time("Friday, January 2, 1970 3:46:40 AM")
    assert time.posix() == 100000

