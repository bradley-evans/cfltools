"""
Session objects for CFLTools
"""

import logging
from cfltools.database import makesession
from cfltools.utilities import Config, log_generator, asn_update
from cfltools.logparse import LogParser
from datetime import date


logger = log_generator(__name__)


class Session():
    """
    High level objects that describes a CFLTools session.
    Performs integration across CFLTools submodules.
    """
    def __init__(self, db=None):
        self.config = Config()
        if db is None:
            # This is set up to allow a dummy DB to be loaded
            # for testing.
            self.database = makesession(self.config.read("db_loc"))
        else:
            self.database = db
        self.logparser = None

    def logparse(self, filename):
        """Parse a log within a session"""
        if self.config.read("asn_datfile") is None:
            logger.info("Updating ASN file.")
            self.config.write("asn_datfile", asn_update())
            self.config.write("asn_lastupdate", date.today().strftime("%Y-%m-%d"))
        self.logparser = LogParser(filename)

    def __del__(self):
        # TODO: write all stuff to database
        pass


class CLISession(Session):
    """
    A command line session of CFLTools.
    """

    def __init__(self, db=None):
        Session.__init__(self, db)

    def logparse(self, filename, incidentid=None):
        """Parse a log within a command line session."""
        Session.logparse(self, filename)
        if incidentid is None:
            logger.warning("No incident ID was provided!")


class FlaskSession(Session):
    """
    A Flask session of CFLTools.
    """
    def __init__(self, db=None):
        Session.__init__(self, db)

    def logparse(self, filename, incidentid=None):
        """Parse a log within a Flask GUI session."""
        Session.logparse(self, filename)
        if incidentid is None:
            logger.warning("No incident ID was provided!")
