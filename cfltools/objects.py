"""
Session objects for CFLTools
"""

import logging
from cfltools.database import makesession
from cfltools.utilities import Config, log_generator
from cfltools.logparse import LogParser



class Session():
    """
    High level objects that describes a CFLTools session.
    Performs integration across CFLTools submodules.
    """
    def __init__(self):
        self.config = Config()
        self.database = makesession(self.config.read("db_loc"))
        self.logger = log_generator(__name__).setLevel(logging.INFO)
        self.logparser = None

    def logparse(self, filename):
        """Parse a log within a session"""
        self.logparser = LogParser(filename)

    def __del__(self):
        # TODO: write all stuff to database
        pass


class CLISession(Session):
    """
    A command line session of CFLTools.
    """

    def __init__(self):
        Session.__init__(self)

    def logparse(self, filename, incidentid=None):
        """Parse a log within a command line session."""
        Session.logparse(self, filename)
        if incidentid is None:
            self.logger.warning("No incident ID was provided!")
