"""
CFLTools general helper functions
"""
import logging
from os.path import exists
from os import makedirs
from .globals import APPDIR


def log_generator(name):
    """
    Log handler for cfltools
    """

    if not exists(APPDIR/'cfltools.log'):
        makedirs(APPDIR, exist_ok=True)
        logfile = open(APPDIR/'cfltools.log', 'w+')
        logfile.write("CFLTools Event Log\n")
        logfile.close()

    logger = logging.getLogger('cfltools | ' + name)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(APPDIR/'cfltools.log')
    c_handler.setLevel(logging.DEBUG)
    f_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    # Make this configurable from a config file.
    logger.setLevel(logging.DEBUG)

    return logger
logger = log_generator(__name__)


def asn_update(target=APPDIR):
    """
    Gets an updated ASN data file and returns that new
    file's location.
    """
    from .pyasn import download_asn_table, convert_asn_table
    bz2file = download_asn_table(target)
    newfile = convert_asn_table(bz2file, target)
    logger.info("New ASN .dat file created at %s", newfile)
    return newfile
