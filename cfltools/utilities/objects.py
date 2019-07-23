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

    def __init__(self, configfile_loc=APPDIR/'cfltools.ini'):
        logger.debug("Creating a Config() object, using %s", configfile_loc)
        self.parser = ConfigParser()
        self.configfile = configfile_loc
        if not exists(configfile_loc):
            f = open(configfile_loc, 'w')
            f.close()
        self.parser.read(self.configfile)
        default_appfolder = APPDIR
        default_database = APPDIR / 'cfltools.db'
        if not self.parser.has_section("DEFAULT"):
            logger.debug("Writing defaults to configfile %s", self.configfile)
            self.parser.set("DEFAULT","appfolder",default_appfolder.as_posix())
            self.parser.set("DEFAULT","db_loc",default_database.as_posix())
            self.parser.set("DEFAULT","max_tor_requests","100")
            self.parser.set("DEFAULT","max_whois_requests","100")
            self.parser.write(open(configfile_loc,'w'))
            # self.parser['DEFAULT'] = {'appfolder': default_appfolder.as_posix(),
            #                           'db_loc': default_database.as_posix(),
            #                           'max_tor_requests': '100',
            #                           'max_whois_requests': '100'
            #                           }
            # with open(self.configfile, 'wb') as file:
            #     self.parser.write(file)
        if not self.parser.has_section("USER"):
            self.parser.add_section("USER")
            self.parser.write(open(configfile_loc,'w'))
            # self.parser['USER'] = {}
            # with open(self.configfile, 'wb') as file:
            #     self.parser.write(file)

    def read(self, attr):
        """
        Reader for configuration files.
        Returns value of the setting.
        """
        # self.parser.read(self.configfile)
        if attr in self.parser['USER']:
            # If there is a user setting for the attribute, we
            # prefer to return that value.
            return str(self.parser['USER'][attr])
        if attr in self.parser['DEFAULT']:
            # Otherwise, return the default value.
            return str(self.parser['DEFAULT'][attr])
        # If the value doesn't exist, return None and
        # handle the error in the calling function.
        logger.warning("Setting %s not found in %s!", attr, self.configfile)
        return None

    def write(self, attr, newvalue):
        """
        Writer for configuration files.
        Does not return.
        """
        # parser.read(self.configfile)
        if type(newvalue) is not str:
            newvalue = str(newvalue)
        self.parser['USER'][attr] = newvalue
        with open(self.configfile, 'a') as file:
            self.parser.write(file)
        logger.info("Changed %s to %s", attr, newvalue)
