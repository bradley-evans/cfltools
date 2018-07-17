# Log Parsing Tools

Tools which parse server logs. The most pertinent information we get from these files is information associated with IP addresses. These tools are meant to:
* Discover unique IP addresses in your .csv logfile.
* Automatically get WHOIS data for the most frequently occurring IP addresses.
* Get start and end times for when IPs occur.
* Save this data to a SQL database so you can perform log correlation later.
