import click
from appdirs import *
import cfltools.cflt_utils as cflt_utils

# Global Variables #
APPFOLDER = user_data_dir("cfltools")

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
def initialize():
    from pathlib import Path
    from os import makedirs
    print("in initialize()")
    # If the application's user data directory doesn't
    # exist, create it.
    if not Path(APPFOLDER).is_dir():
        makedirs(APPFOLDER)
    # If there are missing databases, create them.
    if not cflt_utils.checkforDB(APPFOLDER):
        cflt_utils.createDatabase(APPFOLDER)

@cli.command()
@click.argument('filename')
@click.option('--whois',default=0,help='Get WHOIS for top <INT> IPs.')
def getuniqueip(filename,whois):
    """
    Finds all unique IP addresses and their apperance count in FILENAME.
    The file given to this tool must be a *.csv file that contains at least one column of IP addresses.
    """
    import cfltools.logparse.getuniqueip as GetUnique
    import cfltools.logparse.getwhois as GetWhois
    GetUnique.run(filename)
    if whois:
        GetWhois.run()
