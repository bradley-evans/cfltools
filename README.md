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

## Usage

### `--getuniqueips`

To extract all unique IPs and frequency of appearance from a logfile, use `cfltools --getuniqueips <filename.csv>`. The file must be a `*.csv` file. 
