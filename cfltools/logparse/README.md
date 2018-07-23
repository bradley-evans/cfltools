# Log Parsing Tools

Tools which parse server logs. The most pertinent information we get from these files is information associated with IP addresses. These tools are meant to:
* Discover unique IP addresses in your .csv logfile.
* Automatically get WHOIS data for the most frequently occurring IP addresses.
* Get start and end times for when IPs occur.
* Save this data to a SQL database so you can perform log correlation later.

## Design Quirks ##

### TOR Exit Node Verification ###

This program can verify if a given IP address is a TOR exit node. The way this is done is a little clumsy. Since the TOR Project doesn't actually have an API that lets me straightforwardly determine if an IP was an exit node on a given date / time, what I actually have to do is do an HTTP GET on ExonoraTor with the IP and a date. From here, I'll parse the response for strings that indicate if the IP was, in fact, an exit node at the time given. I'll use the latest date the IP appears to do this.
