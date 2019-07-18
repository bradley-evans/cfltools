"""
Tests for utilities
"""

from cfltools.utilities import Config
from cfltools.utilities import APPDIR

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
