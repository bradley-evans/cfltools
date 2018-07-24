import csv  # csv reader functions
from collections import Counter  # count uniques in a file quickly, O(nlogn)
from decimal import Decimal  # just to show decimals with lower precision


# Global Variables #
from cfltools.settings import APPFOLDER


class IpAddress:
    def __init__(self, ip, numOccurances):
        self.ip = ip
        self.numOccurances = numOccurances
        self.startTime = float('inf')
        self.endTime = float('-inf')


def findTimeColumn(row):
    """Dynamically determine which column of a log file contains dates.

    Parameters:
        row: A row of a logfile
    Returns:
        iterator: An integer defining the row that contains a valid date
            string.
    """
    from timestring import Date
    iterator = 0
    for item in row:
        if item.isdigit():
            # This is a hacky way of avoiding integers from
            # being detected as date/time information
            iterator += 1
            continue
        try:
            this = Date(item)
            return iterator
        except:
            iterator += 1
    return None


def findIpColumn(row):
    import re
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
            print('Found!')
            return iterator
        iterator = iterator + 1
    print("Could not find a column containing IP addresses!")
    print("Error in getuniqueip.py, findIpColumn()")
    exit(1)


def scrapeIPs(filename):
    """Scrapes all IP addresses from a logfile.
    """
    # Encoding must be UTF-8 to allow for international chars
    file = open(filename, encoding='utf-8')
    logfile_reader = csv.reader(file)       # csv reader class
    # Put all of the IP addresses into one list. #
    print('Getting the size of the logfile....\n')
    # Count the number of rows so we can track progress later.
    logsize = sum(1 for row in logfile_reader)
    # Determine which row contains an IP address.
    file.seek(0)
    next(logfile_reader)
    row = next(logfile_reader)
    ip_column = findIpColumn(row)
    file.seek(0)  # Return to the top of the csv.
    next(logfile_reader)  # Skip the header row.
    print('Processing ' + str(logsize) + ' entries.')

    iterator = 0
    all_ip_address = []
    for entry in logfile_reader:
        try:
            # For each entry, we will append that entry's IP address to
            # a list of all the IPs. We'll return that list later.
            entry_ip_address = entry[ip_column]
            all_ip_address.append(entry_ip_address)
            iterator = iterator + 1
            if iterator % 1000 == 0:
                percentDone = round(Decimal((iterator / logsize) * 100), 2)
                string = 'Currently: Scraping all IPs from file. Entry ' + \
                         str(iterator) + ' of ' + str(logsize) + \
                         ' Percent Done: ' + str(percentDone) + '%.'
                print(string, end='\r')
        except UserWarning:
            print('\n* * * Invalid entry detected on line ' + str(iterator) +
                  '.')
            iterator = iterator + 1
            print('Line data: ')
            print('Using column {} for IP address.'.format(ip_column))
            print('Data from that column, for this entry, '
                  'was {}.'.format(entry[ip_column]))
            print(entry)
    print('\n')
    return all_ip_address


def getUniqueIps(all_ip_address):
    # Run Counter() on the complete list of IPs. #
    iterator = 0
    counted_ip_address = Counter(all_ip_address)
    unique_ip_address = []
    print('=== Creating list of unique IPs. ===')
    logsize = len(counted_ip_address)
    for address in counted_ip_address:
        try:
            # Create a new IpAddress() object for each discovered
            # IP. Store the address and the counts for its appearance
            # in that object.
            this_addr = address
            this_count = counted_ip_address[address]
            newIpAddress = IpAddress(this_addr, this_count)
            unique_ip_address.append(newIpAddress)
            iterator = iterator + 1
            if (iterator % 1000) == 0:
                percentDone = round(Decimal((iterator / logsize) * 100), 2)
                string = 'Currently: Creating Unique IP List. Entry ' + \
                         str(iterator) + ' of ' + str(logsize) + \
                         ' Percent Done: ' + str(percentDone) + '%.'
                print(string, end='\r')
        except UserWarning:
            print('\nError creating IP address object!')
            print('Crash data:')
            print('\tThe address line was:')
            print(address)
    # Sort the list by most frequently occuring IP. #
    percentDone = 100
    string = 'Currently: Generating report. Entry ' + str(iterator) + \
             ' of ' + str(logsize) + ' Percent Done: ' + str(percentDone) + \
             '%.'
    print(string, '\n')
    unique_ip_address.sort(key=lambda x: x.numOccurances, reverse=True)
    return unique_ip_address


def sendUniqueToDatabase(unique_ip_address, APPFOLDER, incident_id, conn):
    print(APPFOLDER)
    c = conn.cursor()
    for ip in unique_ip_address:
        c.execute("""
            INSERT INTO ipaddrs(ip,number_occurances,incident_id,
                                start_time,end_time)
            VALUES(?,?,?,?,?)
            """, (ip.ip, ip.numOccurances, incident_id, ip.startTime,
                  ip.endTime))
    conn.commit()


def getTimerange(filename, unique_ip_address):
    """Naive method to determine the time range during which an IP
    address appears in a logfile.

    This is sort of hacky. I'm using timestring to process fairly arbitrary
    text input strings for dates from logs, converting those into POSIX
    dates and times, and then comparing that to a simple integer stored
    in the object to establish our range.

    Parameters:
        filename: The logfile we are examining in this job.
        unique_ip_address: A list of IpAddress() objects.

    Returns:
        unique_ip_address: A list of unique IPAddress()
            objects with dates included.
    """
    import csv
    from timestring import Date
    print('Determining date/time ranges for each unique IP...')
    file = open(filename, 'r', encoding='utf-8')
    logfile_reader = csv.reader(file)
    next(logfile_reader)
    row = next(logfile_reader)
    ip_column = findIpColumn(row)
    time_column = findTimeColumn(row)
    file.seek(0)
    next(logfile_reader)
    # TODO: get this runtime under O(n^2)
    for ip in unique_ip_address:
        file.seek(0)
        for entry in logfile_reader:
            if ip.ip == entry[ip_column]:
                entry_time = Date(entry[time_column])
                if ip.startTime > entry_time.to_unixtime():
                    ip.startTime = entry_time.to_unixtime()
                if ip.endTime < entry_time.to_unixtime():
                    ip.endTime = entry_time.to_unixtime()
    return unique_ip_address


def run(filename, incident_id, seen):
    all_ip_address = scrapeIPs(filename)
    unique_ip_address = getUniqueIps(all_ip_address)
    unique_ip_address = getTimerange(filename, unique_ip_address)
    if not seen:
        import sqlite3
        db_connection = sqlite3.connect(config['USER']['db_loc'])
        sendUniqueToDatabase(unique_ip_address, APPFOLDER, incident_id, db_connection)
        db_connection.close()
    else:
        print('File was already added to database. Skipping database export.')


def main():
    pass


if __name__ == "__main__":
    main()
