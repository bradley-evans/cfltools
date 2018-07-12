import click
from appdirs import *
import cfltools.cflt_utils as cflt_utils

# Global Variables #
from cfltools.settings import *


@click.group()
def cli():
    """
    This is a set of tools for computer forensics analysts and incident responders that aids in quickly parsing and examining server logs.
    To get help with a subcommand, use cfltools subcommand --help.
    """
    # TODO: print program version here.
    print('User Data Directory: {}'.format(user_data_dir(APPFOLDER)))
    pass


@cli.command()
@click.option('--purge', is_flag=True, help='Destroy existing database and reinitalize.')
def initialize(purge):
    """
    Create required database and other files.
    """
    from pathlib import Path
    from os import makedirs
    # If the application's user data directory doesn't
    # exist, create it.
    if not Path(APPFOLDER).is_dir():
        makedirs(APPFOLDER)
    # If there are missing databases, create them.
    if (not cflt_utils.checkforDB(APPFOLDER)) | purge:
        if purge:
            print('Purge flag enabled. Replacing databases with default, empty database!')
        cflt_utils.createDatabase(APPFOLDER)


@cli.command()
@click.argument('filename')
@click.option('--whois', default=0, help='Get WHOIS for top <INT> IPs.')
@click.option('--incidentid', required=True)
def getuniqueip(filename, whois, incidentid):
    """
    Finds all unique IP addresses and their apperance count in FILENAME.
    The file given to this tool must be a *.csv file that contains at least one column of IP addresses.
    """
    import cfltools.logparse.getuniqueip as GetUnique
    import cfltools.logparse.getwhois as GetWhois
    if not cflt_utils.checkIncidentNameExists(incidentid):
        print('Incident name {} does not exist.'.format(incidentid))
        print('Try creating the incident with `cfltools createincident` '+
              'or listing existing incidents with `cfltools incidents --show.`')
        exit(0)
    seen = cflt_utils.checkFileWasSeen(filename)
    GetUnique.run(filename, APPFOLDER, incidentid, seen)
    if not seen:
        cflt_utils.markFileAsSeen(filename, incidentid)
    if whois:
        GetWhois.run()


@cli.command()
@click.argument('incident_name')
def createincident(incident_name):
    """
    Creates an incident to track logs associated with that event.
    """
    from os import makedirs
    from pathlib import Path
    incident_dir = APPFOLDER + '/incidents/' + incident_name
    if not Path(incident_dir).is_dir():
        # If a directory corresponding to a particualr incident
        # does not exist, create it. We will store our incident
        # related-data (e.g., logfiles) in this directory.
        makedirs(incident_dir)
    if cflt_utils.checkIncidentNameExists(incident_name):
        print("Incident identifier {} is not unique! Select a different incident name.".format(incident_name))
    else:
        cflt_utils.generateIncident(incident_name)


@cli.command()
@click.option('--show',is_flag=True)
def incidents(show):
    if show:
        cflt_utils.listIncidents()
