#!/usr/bin/env python3

import csv # csv reader functions
from pprint import pprint # pretty printing to console
from ipwhois import IPWhois # to perform whois lookups
from pycountry_convert import country_alpha2_to_country_name # convert  country codes, e.g. US to United States
from collections import Counter # count uniques in a file quickly, O(nlogn)
import sys # syscalls
from decimal import Decimal # just to show decimals with lower precision
import time # timing stuff
import warnings # specifically to suppress warnings from IPWhois' outdated repo

class IpAddress:
    def __init__(self,ip,numOccurances):
        self.ip = ip
        self.numOccurances = numOccurances
        self.didWhois = False
        self.record = 'Whois data not initialized!'
        self.country_code = 'Whois data not initialized!'
        self.country_name = 'Whois data not initialized!'
        self.asn = 'Whois data not initialized!'
        self.asn_registry = 'Whois data not initialized!'
        self.asn_country_code = 'Whois data not initialized!'
        self.asn_description = 'Whois data not initialized!'
        self.asn_date = 'Whois data not initialized!'
    def getWhois(self):
        self.didWhois = True
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            self.record = IPWhois(self.ip).lookup_rdap(depth=1)
        self.country_code = self.record['asn_country_code']
        if self.country_code == 'EU':
            self.country_name = 'European Union'
        else:
            self.country_name = str(country_alpha2_to_country_name(self.record['asn_country_code']))
        self.asn = self.record['asn']
        self.asn_registry = self.record['asn_registry']
        self.asn_description = self.record['asn_description']
        self.asn_date = self.record['asn_date']
        if self.asn == 'NA':
            self.asn = 'None provided.'
        if self.asn_registry == 'NA':
            self.asn_registry = 'None provided.'
        if self.asn_description == 'NA':
            self.asn_description = 'None provided.'
        if self.asn_date == 'NA':
            self.asn_date = 'None provided.'

def findIpColumn(row):
    import re
    iterator = 0
    print("Dynamically determining which column contains an IP address.")
    for item in row:
        # Regular expression for an IPv4 address.
        # Does not actually check to see if it's in the
        # appropriate 0-255 range, so be careful.
        aa=re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$",item)
        print('Is {} an IP address?'.format(item))
        if aa:
            print("...Yes!")
            return iterator
        print('...nope.')
        iterator = iterator + 1
    print("Could not find a column containing IP addresses!")
    print("Error in getuniqueip.py, findIpColumn()")
    exit(1)

def scrapeIPs(filename):
    file = open(filename, encoding='utf-8')
        # ^^ Had to make this encoding change due to the
        #    presence of international characters in the
        #    dataset.
    logfile_reader = csv.reader(file)       # csv reader class
    # Put all of the IP addresses into one list. #
    print('Getting the size of the logfile....\n')
    logsize = sum(1 for row in logfile_reader)  # Count the number of rows
                                                                                                    # so we can track progress later.
    # Determine which row contains an IP address.
    file.seek(0)
    next(logfile_reader)
    row = next(logfile_reader)
    ip_column = findIpColumn(row)

    file.seek(0)                                                                    # Return to the top of the csv.
    next(logfile_reader)                                                    # Skip the header row.
    print('Processing ' + str(logsize) + ' entries.')

    iterator = 0
    all_ip_address = []
    for entry in logfile_reader:
        try:
            entry_ip_address = entry[ip_column]
            all_ip_address.append(entry_ip_address)
            iterator = iterator + 1
            if iterator % 1000 == 0:
                percentDone = round(Decimal((iterator / logsize ) * 100),2)
                string = 'Currently: Scraping all IPs from file. Entry ' + str(iterator) + ' of ' + str(logsize) + ' Percent Done: ' + str(percentDone) + '%.'
                print(string,end='\r')
        except:
            print('\n* * * Invalid entry detected on line ' + str(iterator) + '.')
            iterator = iterator + 1
            print('Line data: ')
            print('Using column {} for IP address.'.format(ip_column))
            print('Data from that column, for this entry, was {}.'.format(entry[ip_column]))
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
            this_addr = address
            this_count = counted_ip_address[address]
            newIpAddress = IpAddress(this_addr,this_count)
            unique_ip_address.append(newIpAddress)
            iterator = iterator + 1
            if (iterator % 1000) == 0:
                percentDone = round(Decimal((iterator / logsize ) * 100),2)
                string = 'Currently: Creating Unique IP List. Entry ' + str(iterator) + ' of ' + str(logsize) + ' Percent Done: ' + str(percentDone) + '%.'
                print(string, end='\r')
        except:
            print('\nError creating IP address object!')
            print('Crash data:')
            print('\tThe address line was:')
            print(address)
    # Sort the list by most frequently occuring IP. #
    percentDone = 100
    string = 'Currently: Generating report. Entry ' + str(iterator) + ' of ' + str(logsize) + ' Percent Done: ' + str(percentDone) + '%.'
    print(string)
    unique_ip_address.sort(key=lambda x: x.numOccurances, reverse=True)
    return unique_ip_address

def generateTextReport(unique_ip_address,filename):
    import os

    # Print our nifty new data.
    print('=== Generating report. ===')

    filepath = os.path.dirname(os.path.abspath(filename))
    outputfile_name = filepath + '/unique_ips_' + time.strftime("%Y%W%d-%H%M%S") +'.txt'
    outputfile = open(outputfile_name,'w',encoding='utf-8')
    print('Saving file to {}.'.format(outputfile_name))
    outputfile.write('Found ' + str(len(unique_ip_address)) + ' unique IP addresses.\n\n')

    iterator = 0
    logsize = len(unique_ip_address)
    start_time = time.time()
    for ip in unique_ip_address:
        outputfile.write('\t' + 'IP #' + str(iterator) + ': ' + str(ip.ip) + '\n')
        outputfile.write('\t\t| ' + 'Occurs ' + str(ip.numOccurances) + ' times.\n')
        # if ip.ip == '45.77.68.151':
        #     print('Found IP of interest: ' + ip.ip)
        #     print('It occurs ' + str(ip.numOccurances) + ' times.')
        #     outputfile.write('\t\t*** *** IP OF INTEREST *** ***\n')
        # if (iterator-1 < 100)|(str(ip.ip) == '45.77.68.151'):
        #     try:
        #         ip.getWhois()
        #         outputfile.write('\t\t|' + ' Country of origin: ' + ip.country_name + ' ' + ip.country_code + '\n')
        #         outputfile.write('\t\t|' + ' ASN Registry Information:\n')
        #         try:
        #             outputfile.write('\t\t|\tRegistry: ' + ip.asn_registry + '\n')
        #             outputfile.write('\t\t|\tNumber: ' + ip.asn + '\n')
        #             outputfile.write('\t\t|\tDescription: ' + ip.asn_description + '\n')
        #             outputfile.write('\t\t|\tAllocation date: ' + ip.asn_date + '\n')
        #         except:
        #             outputfile.write('\t\t|\tError retrieving ASN information for this entry.\n')
        #     except:
        #         print('Attempted to get IPWhois data for',str(ip.ip),'but the request failed.')
        #         outputfile.write('\t\t|\tAttempted to get IPWhois data for',str(ip.ip),'but the request failed.')
        timer = time.time() - start_time
        if ((iterator % 1000) == 0) | (timer > 5):
            start_time = time.time()
            percentDone = round(Decimal((iterator / logsize) * 100),2)
            string = 'Currently: Generating report. Entry ' + str(iterator) + ' of ' + str(logsize) + ' Percent Done: ' + str(percentDone) + '%.'
            print(string, end='\r')
        iterator = iterator + 1
    percentDone = 100
    string = 'Currently: Generating report. Entry ' + str(iterator) + ' of ' + str(logsize) + ' Percent Done: ' + str(percentDone) + '%.'
    print(string)

    outputfile.close()

##  
def run(filename):
    all_ip_address = scrapeIPs(filename)
    unique_ip_address = getUniqueIps(all_ip_address)
    generateTextReport(unique_ip_address,filename)

## Main function, allows getuniqueip to be run as a script.
#
#  Runnable in isolation if a filename is supplied to the script.
def main():
    # Load the logfile.
    try:
        filename = sys.argv[1]
    except:
        print('No argument for a default file found. Using [default.csv] as the parser target.')
        filename = 'default.csv'

    all_ip_address = scrapeIPs(filename)
    unique_ip_address = getUniqueIps(all_ip_address)
    # Generate our report. #
    generateTextReport(unique_ip_address,filename)


if __name__ == "__main__":
    main()
    print('Program complete.')
