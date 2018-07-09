import click
from appdirs import *
appfolder = user_data_dir("clitools")

@click.group()
def cli():
    """
    This is a set of tools for computer forensics analysts and incident responders that aids in quickly parsing and examining server logs.
    To get help with a subcommand, use cfltools subcommand --help.
    """
    print('User Data Directory: {}'.format(user_data_dir(appfolder)))
    pass

@cli.command()
def initialize():
    print("in initialize()")


@cli.command()
@click.argument('filename')
@click.option('--whois',default=10,help='Get WHOIS for top <INT> IPs.')
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
