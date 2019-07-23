"""
Helper objects for CFLTools
"""

from os.path import exists
from configparser import ConfigParser
from dateparser import parse
from .functions import log_generator
from .globals import APPDIR


# Instantiate the logger.
logger = log_generator(__name__)


class Time():
    """
    Special class to process times for logs.
    Need this to control a number of different
    possible date time formats.
    """

    """
    TODO: DateParser runs extremely slowly here,
    especially considering the raw quantity of
    data we're processing sometimes. Need a better
    way to process raw dates/times
    """
    def __init__(self, raw_time):
        self.raw_time = raw_time

    def posix(self):
        """Returns time as POSIX time (integer)"""
        return parse(self.raw_time,
                     settings={'TIMEZONE': 'UTC',
                               'RETURN_AS_TIMEZONE_AWARE': True,
                               }).timestamp()

    def iso(self):
        """Returns an ISO formatted date time group"""
        return parse(self.raw_time,
                     settings={'TIMEZONE': 'UTC',
                               'RETURN_AS_TIMEZONE_AWARE': True
                               }).isoformat()


class Config():
    """Configuration file object."""
    def __init__(self, configfile_loc=APPDIR/'cfltools.ini'):
        logger.debug("Creating a Config() object, using %s", configfile_loc)
        parser = ConfigParser()
        self.configfile = configfile_loc
        if not exists(configfile_loc):
            f = open(configfile_loc, 'w')
            f.close()
        parser.read(self.configfile)
        default_appfolder = APPDIR
        default_database = APPDIR / 'cfltools.db'
        if not parser.has_option("DEFAULT", "appfolder"):
            logger.debug("Writing defaults to configfile %s", self.configfile)
            parser.set("DEFAULT", "appfolder", default_appfolder.as_posix())
            parser.set("DEFAULT", "db_loc", default_database.as_posix())
            parser.set("DEFAULT", "max_tor_requests", "100")
            parser.set("DEFAULT", "max_whois_requests", "100")
            parser.write(open(configfile_loc, 'w'))
        if not parser.has_section("USER"):
            parser.add_section("USER")
            parser.write(open(configfile_loc, 'w'))
        del parser

    def read(self, attr):
        """
        Reader for configuration files.
        Returns value of the setting.
        """
        parser = ConfigParser()
        parser.read(self.configfile)
        if attr in parser['USER']:
            val = str(parser['USER'][attr])
            del parser
            # If there is a user setting for the attribute, we
            # prefer to return that value.
            return val
        if attr in parser['DEFAULT']:
            val = str(parser['DEFAULT'][attr])
            del parser
            # Otherwise, return the default value.
            return val
        # If the value doesn't exist, return None and
        # handle the error in the calling function.
        logger.warning("Setting %s not found in %s!", attr, self.configfile)
        return None

    def write(self, attr, newvalue):
        """
        Writer for configuration files.
        Does not return.
        """
        parser = ConfigParser()
        parser.read(self.configfile)
        if type(newvalue) is not str:
            newvalue = str(newvalue)
        parser['USER'][attr] = newvalue
        with open(self.configfile, 'w') as file:
            parser.write(file)
            file.close()
        logger.info("Changed %s to %s", attr, newvalue)
        del parser
