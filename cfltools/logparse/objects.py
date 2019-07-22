"""
Objects for log parsing
"""

from pyasn import pyasn
from cfltools.utilities import Time, Config, log_generator, APPDIR


# Instantiate the logger.
logger = log_generator(__name__)


class IPAddress():
    """
    Describes an individual IP address found in a log
    with scope of one incident.
    """

    def __init__(self, ip, raw_timestamp):
        self.ip = ip
        self.earliest = Time(raw_timestamp)
        self.latest = self.earliest
        self.occurances = 1

    def update_time(self, raw_timestamp):
        """
        Update time if supplied time is earlier
        or later than the previously known times
        of appearance.
        """
        newtime = Time(raw_timestamp)
        if newtime.posix() < self.earliest.posix():
            self.earliest = newtime
        if newtime.posix() > self.latest.posix():
            self.latest = newtime

    def asn(self, asndb):
        """
        Returns the ASN of the IP address.
        Feed this method a precompiled ASN database (DAT file).
        """
        return asndb.lookup(self.ip)[0]


class LogFile():

    def _import(self):
        """
        Method prototype for _import.
        Implement these in children to ensure that
        _parse gets a standard format in self.log.
        """
        raise NotImplementedError

    def _parse(self):
        """
        Parent method that looks for all the unique IPs
        in self.log.
        """
        logger.debug("Parsing entries for unique IPs in %s", self.filename)
        for entry in self.log:
            ip = entry[0]
            timestamp = entry[1]
            if ip in self.unique:
                self.unique[ip].occurances += 1
                self.unique[ip].update_time(timestamp)
            else:
                self.unique[ip] = IPAddress(ip, timestamp)

    def __init__(self, filename):
        logger.debug("Importing %s.", filename)
        self.filename = filename
        self.log = []
        self.errors = []
        self.unique = {}

    def md5(self):
        """
        Get the MD5 checksum of the log file.
        """
        from hashlib import md5
        with open(self.filename) as file:
            data = file.read()
        return md5(data.encode('utf-8')).hexdigest()


class CSVLogFile(LogFile):
    """Logfile object for CSV files."""
    def __init__(self, filename):
        LogFile.__init__(self, filename)
        self._import()
        self._parse()

    def _import(self):
        from csv import reader
        logger.debug("Importing IP log from %s", self.filename)
        self.log = []
        ipcolumn = self.ipcolumn()
        timecolumn = self.timecolumn()
        with open(self.filename) as file:
            file.seek(0)
            r = reader(file)
            next(r) # skip header
            for entry in r:
                try:
                    self.log.append((entry[ipcolumn], entry[timecolumn]))
                except UserWarning:
                    logger.warning("""
                        Could not import line: {}\n
                        Invalid entry detected. CFLTools has determined that the
                        IPs are stored in column {} and timestamps in {}.\n
                        These may be empty or malformed in the source logfile.
                        """.format(entry, ipcolumn, timecolumn))
                    self.errors.append(['ImportError', entry])

    def reader(self):
        """Returns a CSV reader object"""
        from csv import reader
        file = open(self.filename, encoding='utf-8')
        return reader(file)

    def size(self):
        """Returns the line length of a CSV file."""
        return sum(1 for row in self.reader())

    def ipcolumn(self):
        """
        Return the column of the logfile containing IP addresses.
        If one is not detected, return -1.
        """
        import re
        reader = self.reader()
        #
        next(reader) # skip to row 2
        row = next(reader)
        iterator = 0
        # What's below are two regular expressions that pattern match to IP
        # addresses. I tried using a library for this (netaddr) but that
        # started matching to long integers that happened to have the right
        # bits for an IP address.
        ipv4_address = re.compile("""
                                  ^(?:(?:[0-9]|[1-9][0-9]|1[0-9]
                                  {2}|2[0-4][0-9]|25[0-5])\\.)
                                  {3}(?:[0-9]|[1-9][0-9]|1[0-9]
                                  {2}|2[0-4][0-9]|25[0-5])$
                                  """, re.VERBOSE)
        ipv6_address = re.compile("""
                                  ^(?:(?:[0-9A-Fa-f]{1,4}:)
                                  {6}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|
                                  (?:(?:[0-9]|[1-9][0-9]|1[0-9]
                                  {2}|2[0-4][0-9]|25[0-5])\\.)
                                  {3}(?:[0-9]|[1-9][0-9]|1[0-9]
                                  {2}|2[0-4][0-9]|25[0-5]))|::
                                  (?:[0-9A-Fa-f]{1,4}:)
                                  {5}(?:[0-9A-Fa-f]{1,4}:
                                  [0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]
                                  {2}|2[0-4][0-9]|25[0-5])\\.)
                                  {3}(?:[0-9]|[1-9][0-9]|1[0-9]
                                  {2}|2[0-4][0-9]|25[0-5]))|(?:[0-9A-Fa-f]{1,4})?::
                                  (?:[0-9A-Fa-f]{1,4}:)
                                  {4}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|
                                  (?:(?:[0-9]|[1-9][0-9]|1[0-9]
                                  {2}|2[0-4][0-9]|25[0-5])\\.)
                                  {3}(?:[0-9]|[1-9][0-9]|1[0-9]
                                  {2}|2[0-4][0-9]|25[0-5]))|
                                  (?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4})?::
                                  (?:[0-9A-Fa-f]{1,4}:)
                                  {3}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|
                                  (?:(?:[0-9]|[1-9][0-9]|1[0-9]
                                  {2}|2[0-4][0-9]|25[0-5])\\.)
                                  {3}(?:[0-9]|[1-9][0-9]|1[0-9]
                                  {2}|2[0-4][0-9]|25[0-5]))|
                                  (?:(?:[0-9A-Fa-f]{1,4}:){,2}[0-9A-Fa-f]{1,4})?::
                                  (?:[0-9A-Fa-f]{1,4}:)
                                  {2}(?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|
                                  (?:(?:[0-9]|[1-9][0-9]|1[0-9]
                                  {2}|2[0-4][0-9]|25[0-5])\\.)
                                  {3}(?:[0-9]|[1-9][0-9]|1[0-9]
                                  {2}|2[0-4][0-9]|25[0-5]))|
                                  (?:(?:[0-9A-Fa-f]{1,4}:){,3}[0-9A-Fa-f]{1,4})?::
                                  [0-9A-Fa-f]{1,4}:(?:[0-9A-Fa-f]{1,4}:
                                  [0-9A-Fa-f]{1,4}|(?:(?:[0-9]|[1-9][0-9]|1[0-9]
                                  {2}|2[0-4][0-9]|25[0-5])\\.)
                                  {3}(?:[0-9]|[1-9][0-9]|1[0-9]
                                  {2}|2[0-4][0-9]|25[0-5]))|
                                  (?:(?:[0-9A-Fa-f]{1,4}:){,4}[0-9A-Fa-f]{1,4})?::
                                  (?:[0-9A-Fa-f]{1,4}:[0-9A-Fa-f]{1,4}|
                                  (?:(?:[0-9]|[1-9][0-9]|1[0-9]
                                  {2}|2[0-4][0-9]|25[0-5])\\.)
                                  {3}(?:[0-9]|[1-9][0-9]|1[0-9]
                                  {2}|2[0-4][0-9]|25[0-5]))|
                                  (?:(?:[0-9A-Fa-f]{1,4}:){,5}[0-9A-Fa-f]{1,4})?::
                                  [0-9A-Fa-f]{1,4}|(?:(?:[0-9A-Fa-f]{1,4}:)
                                  {,6}[0-9A-Fa-f]{1,4})?::)$
                                  """, re.VERBOSE)  # and that's how you regex IPv6
        for item in row:
            ipv4_check = ipv4_address.match(item)
            ipv6_check = ipv6_address.match(item)
            if ipv4_check or ipv6_check:
                return iterator
            iterator = iterator + 1
        return -1

    def timecolumn(self):
        """
        Return the column of the logfile containing a time.
        If one is not detected, return -1.
        """
        from dateparser import parse
        reader = self.reader()
        next(reader) # skip to row 2
        row = next(reader)
        iterator = 0
        for item in row:
            if item.isdigit():
                # This is a hacky way of avoiding integers from
                # being detected as date/time information
                iterator += 1
                continue
            this = parse(item)
            if this:
                return iterator
            iterator += 1
        return -1



class LogParser():
    """
    Primary object for handling IP logs.
    """

    def __init__(self, filename):
        self.filename = filename
        if self.filetype() == 'csv':
            self.logfile = CSVLogFile(filename)
        elif self.filetype() == 'unsupported':
            raise NotImplementedError
        else:
            raise NotImplementedError
        self.config = Config()

    def filetype(self):
        """
        Returns a string describing the filetype
        of the logfile. This lets us use the correct
        logfile object later.
        If the filetype is unsupported, returns
        'unsupported'.
        """
        if str(self.filename).lower().endswith('.csv'):
            return 'csv'
        logger.error("File %s is not supported.", self.filename)
        return 'unsupported'
