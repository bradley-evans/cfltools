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

`cfltools ip [FILENAME].csv --incidentid=[INCIDENT_NAME] [--whois]`

An incident identifier is required and must correspond to an incident you have already named using `cfltools createincident`. The `--whois` flag is optional. If it is present, it will pull the top 100 uniquely occuring IPs and perform an automatic ipwhois query on them. It will then add that information to the database.

# Example Workflow

This workflow assumes a "first run" -- program was just installed and no other work has been done.

### Initializing the Database

Perform `cfltools initialize` to create the initial incident database.

### Create an incident

Information in `cfltools` is organized into "incidents." In the database, each datapoint is assoicated with a unique incident identifier that allows you to associate information with that incident and corelate it across others. Before we import a logfile, we need to identify what incident that logfile is associated with. Since we just initialized the database, that means we will need to create a new incident identifier. To do that, use:

`cfltools createincident [INCIDENTID]`

If you ever forget your incident names, you can use `cfltools incident --show` to list incidents.

### Add a logfile to the incident.

You have a logfile that contains some IP addresses. To perform simple IP analysis on this log, we can use the IP analysis tools in `cfltools`. Invoke:

`cfltools ip [FILENAME] --incidentid [INCIDENTID] --whois`

The `--whois` flag tells `cfltools` to perform whois queries on the IPs associated with that incident. So that we don't make ISPs angry, we examine only the top 100 (or so, this will become a user-configurable option later) entries. 

This tool will scrape the IPs from the database, identify which of them are unique, and do whois queries on them. It will remember what files it has already seen. It will then store counts for IP address occurances and tag them with an event ID.

### Identify Internet Service Providers for follow-up

It is often necessary for an analyst to go to an ISP for more information about an IP address that occurs repeatedly in their logs. The `ip` tools will give you a general description of what provider is associated with an IP, but it is generally left to the analyst to go out and find abuse contact information for that organization. We can't automate that away (no central database for that information exists), but we can help reduce the number of times it is necessary to do so.

`cfltools` stores a database of ISPs that have been seen, by thier Autonomous System Number (ASN). You can use `cfltools database --fillmissingasn` to go through your list of unique IP addresses and manually fill in abuse contact information associated with each IP's ISP. This way, you only have to do the lookup once. To save your ASN database, use `cfltools database --saveasn`. If you or your colleagues have a shared list of ASNs, you can load those in using `cfltools database --loadasn`. Note that loading will ignore any ASNs that already exist in the database.

# Acknowledgements

cyber@ucr, the UCR cybersecurity students organization (@ucrcyber)

The Bourns College of Engineering at the University of California, Riverside
