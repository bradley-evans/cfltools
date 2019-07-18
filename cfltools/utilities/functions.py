"""
CFLTools general helper functions
"""
import logging
from .globals import APPDIR


def log_generator(name):
    """
    Log handler for cfltools
    """

    logger = logging.getLogger('cfltools | ' + name)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(APPDIR/'cfltools.log')
    c_handler.setLevel(logging.DEBUG)
    f_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    # Make this configurable from a config file.
    logger.setLevel(logging.DEBUG)

    return logger