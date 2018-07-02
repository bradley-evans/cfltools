#!/usr/bin/env python3

import csv
from pprint import pprint
from ipwhois import IPWhois
from pycountry_convert import country_alpha2_to_country_name

class IpAddress:
	type = 'ipv4'

	def __init__(ip,country):
		self.ip = ip

def main():
	# Load the logfile. Right now, this is hardcoded
	# to a CSV file called 'Activities.csv' located
	# in the same folder as the script.
	filename = 'Activities.csv'
	file = open(filename)
	logfile_reader = csv.reader(file)	# csv reader class
	unique_ip_address = []				# list to hold unique IPs found

	outputfile = open('output.txt','w')
	
	# For each entry, check if the IP address already
	# exists in our list of discovered IP addresses.
	# If not, append the IP to our list.
	next(logfile_reader)							# Skip the header row.
	for entry in logfile_reader:
		entry_ip_address = entry[2]
		ip_address_isUnique = True					# Initially assume the IP is unique.
		for found in unique_ip_address:
			if entry_ip_address == found:
				ip_address_isUnique = False			# If found, the IP is not unique. Terminate.
				break
		if ip_address_isUnique == True:				# If not found, append to the list of unique IPs.
			unique_ip_address.append(entry_ip_address)
	unique_ip_address = sorted(unique_ip_address)	# Sort the list for readability.
	# outputfile.write(unique_ip_address)


	# Print our nifty new data.
	outputfile.write('Found ' + str(len(unique_ip_address)) + ' unique IP addresses.\n\n')
	pprint(unique_ip_address)
	print(len(unique_ip_address))

	# for ip in unique_ip_address:
		

	tabs3 = '\t\t\t'
	tabs4 = '\t\t\t\t'
	for ip in unique_ip_address:
		record = IPWhois(ip).lookup_rdap(depth=1)
		outputfile.write('===== Record for ' + str(ip) + ' ======\n')
		outputfile.write('IP Address Queried:\t\t' + str(record['query']) + '\n')
		outputfile.write('Country Code:\t\t\t' + str(record['asn_country_code']) + ' ' + str(country_alpha2_to_country_name(record['asn_country_code'])) + '\n')
		outputfile.write('ASN:\t\t\t\t\t' + str(record['asn']) + '\n')
		outputfile.write('ASN Registry:\t\t\t' + str(record['asn_registry']) + '\n')
		outputfile.write('\t\t\t' + str(record['asn_description']) + '\n')
		outputfile.write('\t\t\t' + 'Allocated ' + str(record['asn_date']) + '\n')
		outputfile.write('National Internet\n         Registry:\t\t' + str(record['nir']) + '\n')
		## Contact Information ##
		outputfile.write('  ** Contact Information Discovered **\n')
		for object in record['objects']:

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
		
		outputfile.write('\n')
	outputfile.close()

main()
