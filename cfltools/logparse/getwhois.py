from cfltools.settings import APPFOLDER, INSTALLPATH


def loadISPDBfromFile(filename):
    """Loads ASN information for known ISPs into the ISP table of the database.
    Requires that the csv file used for data import be standardized.
    """
    import csv
    import sqlite3
    db_loc = APPFOLDER + '/incident.db'
    conn = sqlite3.connect(db_loc)
    c = conn.cursor()
    query = """
        INSERT INTO isp
        VALUES (?,?,?,?,?,?,?,?,?,?,?)
        """
    with open(filename,'r') as input:
        csv_in = csv.reader(input)
        for data in csv_in:
            asn = data[0]
            if not checkAsnExists(asn):
                c.execute(query,tuple(data))
    conn.commit()
    conn.close()


def saveISPDBtoFile(filename):
    """Saves the current contents of the ASN database to the install directory.
    """
    import csv
    import sqlite3
    db_loc = APPFOLDER + '/incident.db'
    conn = sqlite3.connect(db_loc)
    c = conn.cursor()
    query = """
        SELECT * FROM isp
        """
    data = c.execute(query).fetchall()
    with open(filename,'w') as out:
        csv_out = csv.writer(out)
        for row in data:
            csv_out.writerow(row)
    conn.close()


def removeAsnFromDatabase(asn):
    """Helper function which removes ISP information from database.

    Parameters:
        asn: ASN to be removed.
    """
    import sqlite3
    db_loc = APPFOLDER+'/incident.db'
    conn = sqlite3.connect(db_loc)
    c = conn.cursor()
    query = """
        DELETE FROM isp
        WHERE asn=?
        """
    c.execute(query,(asn,))
    conn.commit()
    conn.close()


def getAsnFromUser(asn,desc):
    """Helper function to manually enter ISP abuse data into the database.

    Parameters:
        asn: The ASN number of the ISP or entity controlling the IP address, usually
            obtained via a WHOIS lookup.
        desc: The description of the ASN owner, usually the name of an ISP.
    """
    from cfltools.cflt_utils import safeprompt
    print('\n')
    print('--- Manual ISP Entry ---')
    print('ISP ASN:     '.format(asn))
    print('Description: '.format(desc))
    print('Please fill out the following information for this ASN from'
          'data obtained from search.org.')
    contact_name =          input('Enter contact name:  ')
    online_service =        input('Online service name: ')
    online_attn =           input('Attn:                ')
    online_serv_address =   input('Address:             ')
    phone =                 input('Phone:               ')
    fax =                   input('Fax:                 ')
    email =                 input('Email:               ')
    notes =                 input('Notes:               ')
    req_nda =               safeprompt('Requires NDA? [Y/N]: ','YN')
    print('--- Entry complete.  ---')
    return (asn, desc, contact_name, online_service, online_attn, online_serv_address,
            phone, fax, email, notes, req_nda)


def addAsnToDatabase(asn,desc):
    """Helper function which adds ISP information to the database.

    Parameters:
        asn: The ASN number of the ISP or entity controlling the IP address, usually
            obtained via a WHOIS lookup.
        desc: The description of the ASN owner, usually the name of an ISP.
    """
    import sqlite3
    db_loc = APPFOLDER+'/incident.db'
    conn = sqlite3.connect(db_loc)
    c = conn.cursor()
    query = """
        INSERT INTO isp(asn, description, contact_name, online_service, online_attn,
                        online_serv_address, phone, fax, email, notes, req_nda
                       )
        VALUES(?,?,?,?,?,?,?,?,?,?,?)
        """
    try:
        c.execute(query, getAsnFromUser(asn,desc))
    except UserWarning:
        # Entry is not unique!
        pass
    conn.commit()
    conn.close()


def checkAsnExists(asn):
    """Verifies if an ASN number exists in the database.
    Returns true if exists, false if not.
    Parameters:
        asn: String representing an ASN number.
    """
    import sqlite3
    db_loc = APPFOLDER+'/incident.db'
    conn = sqlite3.connect(db_loc)
    c = conn.cursor()
    query = """
        SELECT asn FROM isp
        WHERE asn = ?
        """
    asnlist = c.execute(query, (asn,)).fetchall()
    conn.close()
    if len(asnlist) > 0:
        return True
    return False


def addWhoisToDatabase(iplist):
    """Helper function which adds whois information to the database.

    Parameters:
        iplist: A list of dicts that contain relevant ipwhois data.
    """
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
        c.execute(query, (
            ip['country_code'],
            ip['country'],
            ip['asn'],
            ip['asn_description'],
            'Y',  # Mark the entry as having recieved a good whois query.
            ip['ip'],
            )
        )
    conn.commit()
    conn.close()


def getWhois(iplist):
    """Function which obtains ipwhois data for a list of IP addresses.

    Parameters:
        iplist: A list of strings that contain IP addresses.
    """
    import warnings
    from ipwhois import IPWhois
    from pycountry_convert \
        import country_alpha2_to_country_name as convertCountry
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
    """Function that retrieves all IPs associated with incident_name.
    Returns a list of ip address strings.
    Parameters:
        incident_name: String representing the incident name.
    """
    import sqlite3
    db_loc = APPFOLDER+'/incident.db'
    conn = sqlite3.connect(db_loc)
    c = conn.cursor()
    iplist = c.execute("""
        SELECT ip,number_occurances FROM ipaddrs
        WHERE incident_id = ?
        """, (incident_name,)).fetchall()
    # Get unique values only
    conn.close()
    return iplist


def run(incident_name):
    """Function run when the module is called from the CLI.
    Parameters:
        incident_name: String representing an incident name.
    """
    print(APPFOLDER)
    iplist = getIPlist(incident_name)
    iplist_whois = getWhois(iplist)
    addWhoisToDatabase(iplist_whois)


def asScript():
    print('Running getwhois as script.')
    pass

if __name__ == '__main__':
    asScript()
