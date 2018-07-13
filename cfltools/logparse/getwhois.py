from cfltools.settings import APPFOLDER

def addWhoisToDatabase(iplist):
    import sqlite3
    db_loc = APPFOLDER+'/incident.db'
    conn = sqlite3.connect(db_loc)
    c = conn.cursor()
    query = """
        UPDATE ipaddrs
        SET country_code=?,country=?,asn=?,asn_description=?,whois_done=?
        WHERE ip=?
    """
    for ip in iplist:
        c.execute(query,
            (ip['country_code'],ip['country'],ip['asn'],ip['asn_description'],'Y',ip['ip'],))
    conn.commit()
    conn.close()


def getWhois(iplist):
    import warnings
    from ipwhois import IPWhois
    from pycountry_convert import country_alpha2_to_country_name as convertCountry
    # iplist is a list of tuples of form (ip,numoccurances).
    # Sort the list by number of occurances.
    iplist.sort(key=lambda x: x[1], reverse=True)
    iplist = [x[0] for x in iplist]
    iplist_whois = []
    i = 0
    # Some of the sources for WHOIS data perform rate limiting.
    # To prevent behavior that could be seen as abusive, we will
    # limit our search to the most frequently occuring IPs in
    # a set of logs. The variable below controls how many of the
    # top IPs to query.
    query_limit = 10
    for ip in iplist:
        status = 'Currently: Getting WHOIS data for IP {}    '.format(ip)
        print(status, end='\r')
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=UserWarning)
            ipwhoisdata = IPWhois(ip).lookup_rdap(depth=1)
        # We'll return a dict. Start by initializing.
        record = {}
        record['ip'] = ip
        record['country_code'] = ipwhoisdata['asn_country_code']
        if record['country_code'] == 'EU':
            record['country'] = 'European Union'
        else:
            record['country'] = convertCountry(record['country_code'])
        record['asn'] = ipwhoisdata['asn']
        record['asn_description'] = ipwhoisdata['asn_description']
        iplist_whois.append(record)
        i += 1
        if (i > query_limit):
            # Stop at the query limiter.
            print('\nWHOIS query complete.')
            break
    return iplist_whois


def getIPlist(incident_name):
    # This will just grab a list of IPs assocaited
    # with an incident. Output is a tuple of
    # the ip address and its frequency of occurance
    # in that incident.
    import sqlite3
    db_loc = APPFOLDER+'/incident.db'
    conn = sqlite3.connect(db_loc)
    c = conn.cursor()
    iplist = c.execute('SELECT ip,number_occurances FROM ipaddrs WHERE incident_id = ?',(incident_name,)).fetchall()
    # Get unique values only
    conn.close()
    return iplist


def run(incident_name):
    print('In logparse.getwhois.run()')
    print(APPFOLDER)
    iplist = getIPlist(incident_name)
    iplist_whois = getWhois(iplist)
    addWhoisToDatabase(iplist_whois)


def asScript():
    print('Running getwhois as script.')


if __name__ == '__main__':
    asScript()
