"""
Command line interface for cfltools.
"""


from __future__ import print_function
import click


# Global Variables #
from cfltools.utilities import APPDIR, VERSION, log_generator
from cfltools import CLISession

logger = log_generator(__name__)
session = CLISession()


@click.group()
def cli():
    """
    This is a set of tools for computer forensics analysts and incident
    responders that aids in quickly parsing and examining server logs.
    To get help with a subcommand, use cfltools subcommand --help.
    """
    print('cfltools version {}'.format(VERSION))


@cli.command()
def about():
    """
    Prints basic application information.
    """
    import os
    installpath = os.path.dirname(__file__)
    print('Install Directory:     {}'.format(installpath))
    print('Application Directory: {}'.format(APPDIR))


# @cli.command()
# @click.option('--purge',
#               is_flag=True,
#               help='Destroy existing database and reinitalize.',
#               confirmation_prompt=True)
# def initialize(purge):
#     """
#     Create required database and other files.
#     """
#     from pathlib import Path
#     from os import makedirs
#     import configparser
#     # If the application's user data directory doesn't
#     # exist, create it.
#     if not Path(APPDIR).is_dir():
#         print('Application folder {} not detected. Creating it...'.format(APPDIR))
#         makedirs(APPDIR)
#     config = configparser.ConfigParser()
#     config.read(APPDIR + '/cfltools.ini')
#     # If there are missing databases, create them.
#     if (not cflt_utils.checkforDB(config)) | purge:
#         if purge:
#             print('Purge flag enabled. Replacing databases with default, empty database!')
#         cflt_utils.createDatabase(config)
#     cflt_config.initialize_defaults()


@cli.command()
@click.argument('filename')
@click.option('--whois', is_flag=True, help='Get WHOIS for top <INT> IPs.')
@click.option('--incidentid')
@click.option('--tor', is_flag=True, help='Identify TOR exit nodes among top <INT> IPs.')
def logparse(filename, whois, incidentid, tor):  # pylint: disable=C0103
    """
    Finds all unique IP addresses and their apperance count in FILENAME.
    The file given to this tool must be a *.csv file that contains at
    least one column of IP addresses.
    """
    logger.info("Parsing log file '%s'", filename)
    session.logparse(filename, incidentid)
    # config = configparser.ConfigParser()
    # config.read(APPDIR + '/cfltools.ini')
    # if not cflt_utils.checkIncidentNameExists(incidentid, config):
    #     print('Incident name {} does not exist.'.format(incidentid))
    #     print('Try creating the incident with `cfltools createincident` '+
    #           'or listing existing incidents with `cfltools incidents --show.`')
    #     exit(0)
    # seen = cflt_utils.checkFileWasSeen(filename, config)
    # GetUnique.run(filename, incidentid, seen)
    # if not seen:
    #     cflt_utils.markFileAsSeen(filename, incidentid, config)
    # if whois:
    #     GetWhois.run(incidentid)
    # if tor:
    #     CheckTor.run(incidentid)
    pass



@cli.command()
@click.argument('incident_name')
def createincident(incident_name):
    """
    Creates an incident to track logs associated with that event.
    """
    # from os import makedirs
    # from pathlib import Path
    # import configparser
    # config = configparser.ConfigParser()
    # config.read(APPDIR + '/cfltools.ini')
    # incident_dir = APPDIR + '/incidents/' + incident_name
    # if not Path(incident_dir).is_dir():
    #     # If a directory corresponding to a particualr incident
    #     # does not exist, create it. We will store our incident
    #     # related-data (e.g., logfiles) in this directory.
    #     makedirs(incident_dir)
    # if cflt_utils.checkIncidentNameExists(incident_name, config):
    #     print("Incident identifier {} is not unique! Select a different incident name."
    #           .format(incident_name))
    # else:
    #     cflt_utils.generateIncident(incident_name, config)
    pass


@cli.command()
@click.option('--show', is_flag=True)
def incidents(show):
    """
    List, modify, and remove incidents and incident identifiers.
    """
    # import sqlite3
    # import configparser
    # config = configparser.ConfigParser()
    # config.read(APPDIR + '/cfltools.ini')
    # conn = sqlite3.connect(config['USER']['db_loc'])
    # if show:
    #     cflt_utils.listIncidents(conn)
    # conn.close()
    pass


@cli.command()
@click.option('--saveasn', is_flag=True)
@click.option('--loadasn', is_flag=True)
@click.option('--fillmissingasn', is_flag=True)
def database(saveasn, loadasn, fillmissingasn):
    """
    Database IO operations
    """
    # import sqlite3
    # import configparser
    # config = configparser.ConfigParser()
    # config.read(APPDIR + '/cfltools.ini')
    # db_connection = sqlite3.connect(config['USER']['db_loc'])
    # if saveasn:
    #     from cfltools.logparse.getwhois import saveISPDBtoFile
    #     from cfltools.cflt_utils import safeprompt
    #     filename = safeprompt('Enter filename to save ASN database to: ',
    #                           'csv')
    #     saveISPDBtoFile(filename, db_connection)
    # if loadasn:
    #     from cfltools.logparse.getwhois import loadISPDBfromFile
    #     from cfltools.cflt_utils import safeprompt
    #     filename = safeprompt('Enter filename to load ASN database from: ',
    #                           'csv')
    #     loadISPDBfromFile(filename, db_connection)
    # if fillmissingasn:
    #     from cfltools.logparse.getwhois import getMissingASNfromUser
    #     getMissingASNfromUser(db_connection)
    pass


@cli.command()
@click.argument('incident_id')
def report(incident_id):
    """
    Command line / text reports related to incidents.
    """
    # import cfltools.reports.report
    # from cfltools.cflt_utils import checkIncidentNameExists
    # import configparser
    # config = configparser.ConfigParser()
    # config.read(APPDIR + '/cfltools.ini')
    # if checkIncidentNameExists(incident_id, config):
    #     cfltools.reports.report.reportToCLI(incident_id, config)
    # else:
    #     print('Incident {} does not exist. You can '
    #           'show a list of incidents with the command '
    #           'cfltools incidents --show'.format(incident_id))
    pass
