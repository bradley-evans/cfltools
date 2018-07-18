# cfltools: Computer Forensic Laboratory Tools
A logfile analysis tool for cyber forensics investigators.

Designed by Bradley Evans, written in Python 3.

Project begun July 2018.

## Project Scope

These tools are meant to help a security analyst rapidly examine individual logfiles associated with a particular security incident. The tools are meant to extract commonly required information for an incident responder (e.g., all unique IP addresses that occur in a logfile and associated WHOIS information for the most frequently occuring IPs) and streamline the analysis process.

They are based on my observation of cyber investigations.

## How it Works

### Static Analysis versus Log Correlation

Most of the time, an incident responder wants to collect all the logs that are associated with a given incident into a single folder. This program will provide tools that allow for analysis within that folder. I call these folders "incident folders." 

The program will also be able to import that information into a central sqlite (under development) database so that you can do log correlation.

### General Assumptions

These tools make some general assumptions about the work you're doing. Among the most important are:
* That logfiles you are using are *completely static*. The program detects if it has seen a logfile before by taking a hash of the file. Generally, I'm presuming that the logs you are feeding into this program need to be treated as evidence, so will remain unchanged (filename, contents, and so on) from the start of your analysis until the end. If you need to rename a file for archival purposes (I've noticed that some data dumps are fairly standardized and some use the same filenames repeatedly), you should rename the file before importing it with this tool.
* That data is generally using an IP address as your common identifying marker. This is imperfect, but it's what we have for right now.

## Usage

### Incident Identifiers and `createincident`

All log analysis tasks must have an incident identifier associated with them. To create an incident, use:

`cfltools createincident [INCIDENT_NAME]`

For example, to create an incident named `intrusion_10JUL`, use `cfltools createincident intrusion_10JUL`. This will create the named incident and a folder in your `%APPDIR%` that the program will use to store logs and other information associated with the incident.

The program will not allow you to create an incident with the same name as another. If it detects that you have done this, it will return an error.

If you forget what you have named an incident, you can call `cfltools incidents --show` to show a listing of incidents currently in the database.

### Getting Unique IPs from a logfile

One of the main uses of `cfltools` is to pull and catalog all uniquely-occuring IP addresses from a logfile. To use this feature, you invoke the following:

`cfltools getuniqueip [FILENAME].csv --incidentid=[INCIDENT_NAME] [--whois]`

An incident identifier is required and must correspond to an incident you have already named using `cfltools createincident`. The `--whois` flag is optional. If it is present, it will pull the top 100 uniquely occuring IPs and perform an automatic ipwhois query on them. It will then add that information to the database.

# Acknowledgements

cyber@ucr, the UCR cybersecurity student's organization
The Bourns College of Engineering at the University of California, Riverside
