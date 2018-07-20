import csv  # csv reader functions
from collections import Counter  # count uniques in a file quickly, O(nlogn)
import sys  # syscalls
from decimal import Decimal  # just to show decimals with lower precision
import time  # timing stuff


# Global Variables #
from cfltools.settings import APPFOLDER


class IpAddress:
    def __init__(self, ip, numOccurances):
        self.ip = ip
        self.numOccurances = numOccurances
        self.country_code = 'Whois data not initialized!'
        self.country_name = 'Whois data not initialized!'
        self.asn = 'Whois data not initialized!'
        self.asn_registry = 'Whois data not initialized!'
        self.asn_country_code = 'Whois data not initialized!'
        self.asn_description = 'Whois data not initialized!'


def findIpColumn(row):
    import re
    iterator = 0
    print("Dynamically determining which column contains an IP address...",
          end='')
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


def sendUniqueToDatabase(unique_ip_address, APPFOLDER, incident_id):
    print('In sendUniqueToDatabase().')
    print(APPFOLDER)
    import sqlite3
    conn = sqlite3.connect(APPFOLDER+'/incident.db')
    c = conn.cursor()
    for ip in unique_ip_address:
        c.execute("""
            INSERT INTO ipaddrs(ip,number_occurances,incident_id)
            VALUES(?,?,?)
            """, (ip.ip, ip.numOccurances, incident_id))
    conn.commit()
    conn.close()


def run(filename, incident_id, seen):
    all_ip_address = scrapeIPs(filename)
    unique_ip_address = getUniqueIps(all_ip_address)
    if not seen:
        sendUniqueToDatabase(unique_ip_address, APPFOLDER, incident_id)
    else:
        print('File was already added to database. Skipping database export.')


def main():
    pass


if __name__ == "__main__":
    main()
    print('Program complete.')
