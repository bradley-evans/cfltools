#!/usr/bin/env python3

import csv
from pprint import pprint
from ipwhois import IPWhois
from pycountry_convert import country_alpha2_to_country_name
from collections import Counter
import sys

class IpAddress:
	def __init__(self,ip,numOccurances):
		self.ip = ip
		self.numOccurances = numOccurances

def main():
	# Load the logfile. Right now, this is hardcoded
	# to a CSV file called 'Activities.csv' located
	# in the same folder as the script.
	filename = 'Instagram_user_lookup_API_request_logs.csv'
	file = open(filename, encoding='utf-8')		# Had to make this encoding change due to the
												# presence of international characters in the
												# dataset.
	logfile_reader = csv.reader(file)	# csv reader class
	unique_ip_address = []				# list to hold unique IPs found

	outputfile = open('output2.txt','w',encoding='utf-8')
	
	# For each entry, check if the IP address already
	# exists in our list of discovered IP addresses.
	# If not, append the IP to our list.
	print('Getting the size of the logfile....\n')
	logsize = sum(1 for row in logfile_reader)		# Count the number of rows
													# so we can track progress later.
	
	file.seek(0)									# Return to the top of the csv.
	next(logfile_reader)							# Skip the header row.
	print('Processing ' + str(logsize) + ' entries.')



	# Put all of the IP addresses into one list. #
	iterator = 0
	all_ip_address = []
	for entry in logfile_reader:
		try: 
			entry_ip_address = entry[14]
			all_ip_address.append(entry_ip_address)
			iterator = iterator + 1
			if iterator % 1000 == 0:
				percentDone = ( iterator / logsize ) * 100
				string = 'Currently: Scraping all IPs from file. Entry ' + str(iterator) + ' of ' + str(logsize) + ' Percent Done: ' + str(percentDone) + '%.'
				print(string,end='\r')
		except:
			print('* * * Invalid entry detected on line ' + str(iterator) + '.')
			print('Line data: ')
			print(entry)

	print('\n')

	# Run Counter() on the complete list of IPs. #
	iterator = 0
	counted_ip_address = Counter(all_ip_address)
	unique_ip_address = []
	print('Creating list of unique IPs.')
	logsize = len(counted_ip_address)
	for address in counted_ip_address:
		try:
			this_addr = address
			this_count = counted_ip_address[address]
			newIpAddress = IpAddress(this_addr,this_count)
			unique_ip_address.append(newIpAddress)
			iterator = iterator + 1
			if (iterator % 1000) == 0:
				percentDone = ( iterator / logsize ) * 100
				string = 'Currently: Creating Unique IP List. Entry ' + str(iterator) + ' of ' + str(logsize) + ' Percent Done: ' + str(percentDone) + '%.'
				print(string, end='\r')
		except:
			print('Error creating IP address object!')
			print('Crash data:')
			print('\tThe address line was:')
			print(address)

	# Sort the list by most frequently occuring IP.
	unique_ip_address.sort(key=lambda x: x.numOccurances, reverse=True)

	# Print our nifty new data.
	outputfile.write('Found ' + str(len(unique_ip_address)) + ' unique IP addresses.\n\n')

	iterator = 1
	for ip in unique_ip_address:
		outputfile.write('\t' + 'IP #' + str(iterator) + ': ' + str(ip.ip) + '\n')
		outputfile.write('\t\t| ' + 'Occurs ' + str(ip.numOccurances) + ' times.\n')
		iterator = iterator + 1
	outputfile.write('\n\nRetrieving WHOIS records.\n\n')
		

	tabs3 = '\t\t\t'
	tabs4 = '\t\t\t\t'
	for ip in unique_ip_address:
		record = IPWhois(ip.ip).lookup_rdap(depth=1)
		outputfile.write('===== Record for ' + str(ip.ip) + ' ======\n')
		try:
			outputfile.write('IP Address Queried:\t\t' + str(record['query']) + '\n')
			outputfile.write('Country Code:\t\t\t' + str(record['asn_country_code']) + ' ' + str(country_alpha2_to_country_name(record['asn_country_code'])) + '\n')
			outputfile.write('ASN:\t\t\t\t\t' + str(record['asn']) + '\n')
			outputfile.write('ASN Registry:\t\t\t' + str(record['asn_registry']) + '\n')
			outputfile.write('\t\t\t' + str(record['asn_description']) + '\n')
			outputfile.write('\t\t\t' + 'Allocated ' + str(record['asn_date']) + '\n')
			outputfile.write('National Internet\n         Registry:\t\t' + str(record['nir']) + '\n')
		except:
			outputfile.write('\tError collecting whois data for '+ str(ip.ip))
		## Contact Information ##
		outputfile.write('  ** Contact Information Discovered **\n')
		for object in record['objects']:
			try:
				this_object = record['objects'][object]
				outputfile.write(tabs3 + str(this_object['contact']['name']) + ' ' + str(object) + '\n')
				outputfile.write(tabs3 + 'Role: ' + str(this_object['contact']['role']) + '\n' )
				addr = this_object['contact']['address'][0]['value']
				addr = addr.replace('\n','\n\t\t\t\t ')
				outputfile.write(tabs4 + addr + '\n')
				email = this_object['contact']['email']
				if str(type(email)) == '<class \'list\'>':
					for entry in email:
						outputfile.write(tabs4 + entry['value'] + '\n')
				else:
					outputfile.write(tabs4 + 'No email provided!' + '\n')

				phone = this_object['contact']['phone']
				if str(type(phone)) == '<class \'list\'>':
					for entry in phone:
						outputfile.write(tabs4 + entry['value'] + '\n')
				else:
					outputfile.write('No phone provided!\n')
			except:
				outputfile.write('Error processing contact information for this IP.')
				print('Error processing contact information for',str(ip.ip))		
		outputfile.write('\n')
	outputfile.close()

main()
print('Program complete.')
