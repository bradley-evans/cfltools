class LogfileError(Exception):
    pass


class Logfile():

    def status(self, done, total, operation):
        pass

    def find_timecolumn(self, row):
        """
        Takes in a row from a logfile, and returns a column where it detects
        a valid date.
        """
        import dateparser
        iterator = 0
        for item in row:
            if item.isdigit():
                iterator += 1
                continue
            this = dateparser.parse(item)
            if this:
                return iterator
            iterator += 1
        return None

    def find_logfilesize(self):
        """
        Return the number of rows in a logfile.
        """
        import csv
        self.file.seek(0)
        reader = csv.reader(self.file)
        size = sum(1 for row in reader)
        return size

    def __init__(self, file):
        self.file = file
        self.logsize = self.find_logfilesize()


class Logfile_IP():
    getwhois = False
    gettor = False
    unique_ip_addrs = []
    all_ipaddrs = []
    query_limit = 100

    def find_ipcolumn(self, row):
        """
        Determine which column of a logfile contains an IPv4 or v6 address.
        """
        import re
        iterator = 0
        # What's below are two regular expressions that pattern match to IP
        # addresses. I tried using a library for this (netaddr) but that
        # started matching to long integers that happened to have the right
        # bits for an IP address.
        try:
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
                                      """, re.VERBOSE)
            # and that's how you regex for IPv6
            for item in row:
                ipv4_check = ipv4_address.match(item)
                ipv6_check = ipv6_address.match(item)
                if ipv4_check or ipv6_check:
                    return iterator
                iterator = iterator + 1
            raise LogfileError('Could not find a column containing an IP address.')
        except LogfileError as e:
            print(e)
            print('row: {}'.format(row))

    def find_uniqueipaddrs(self, all_ipaddrs):
        """
        Find all unique ip addresses in a list of IPs.
        Returns IPAddress() objects

        Takes in a list of tuples with format (ip,date) and returns
        a list of IpAddress() objects.
        """
        from collections import Counter
        from cfltools.logparse.ipaddress import IPAddress
        counted_ipaddrs = Counter([i[0] for i in all_ipaddrs])
        unique_ip_addrs = []
        for addr in counted_ipaddrs:
            try:
                this_addr = addr
                this_count = counted_ipaddrs[addr]
                this_ipobj = IPAddress(this_addr, this_count)
                unique_ip_addrs.append(this_ipobj)
            except UserWarning as e:
                print(e)
                print('addr: {}'.format(addr))
        return unique_ip_addrs

    def scrapeIPs(self, file, ip_column, time_column):
        """
        Scrapes all IPs and an associated timestamp from a given file.
        """
        import csv
        file.seek(0)
        all_ipaddrs = []
        reader = csv.reader(file)
        next(reader)  # skip header row
        for entry in reader:
            try:
                new_entry = (entry[ip_column], entry[time_column])
                all_ipaddrs.append(new_entry)
            except Exception as e:
                print(e)
                print('iplog row data: {}'.format(entry))
        return all_ipaddrs

    def set_getwhois(self, getwhois):
        self.getwhois = getwhois

    def set_gettor(self, gettor):
        self.gettor = gettor

    def build(self):
        # perform analysis
        import csv
        self.file.seek(0)
        reader = csv.reader(self.file)
        next(reader)
        row = next(reader)
        ip_column = self.find_ipcolumn(row)
        time_column = self.find_timecolumn(row)
        self.all_ipaddrs = self.scrapeIPs(self.file, ip_column, time_column)
        self.unique_ip_addrs = self.find_uniqueipaddrs(self.all_ipaddrs)
