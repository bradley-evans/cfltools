"""
Helper objects for CFLTools
"""
from dateparser import parse


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
                     settings={'RETURN_AS_TIMEZONE_AWARE': True
                               }).timestamp()

    def iso(self):
        """Returns an ISO formatted date time group"""
        return parse(self.raw_time,
                     settings={'RETURN_AS_TIMEZONE_AWARE': True
                               }).isoformat()
