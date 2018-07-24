from cfltools.settings import APPFOLDER
import configparser
config = configparser.ConfigParser()
config.read(APPFOLDER + '/cfltools.ini')


def loadISPDBfromFile(filename, conn):
    """Loads ASN information for known ISPs into the ISP table of the database.
    Requires that the csv file used for data import be standardized.
    """
    import csv
    c = conn.cursor()
    query = """
        INSERT INTO isp
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """
    with open(filename,'r') as input:
        csv_in = csv.reader(input)
        for data in csv_in:
            asn = data[0]
            if not checkAsnExists(asn, conn):
                from pprint import pprint
                pprint(data)
                c.execute(query,tuple(data))
    conn.commit()


def saveISPDBtoFile(filename, conn):
    """Saves the current contents of the ASN database to the install directory.
    """
    import csv
    c = conn.cursor()
    query = """
        SELECT * FROM isp
        """
    data = c.execute(query).fetchall()
    with open(filename,'w') as out:
        csv_out = csv.writer(out)
        for row in data:
            csv_out.writerow(row)


def removeAsnFromDatabase(asn, conn):
    """Helper function which removes ISP information from database.

    Parameters:
        asn: ASN to be removed.
        conn: A sqlite3 database connection.
    """
    c = conn.cursor()
    query = """
        DELETE FROM isp
        WHERE asn=?
        """
    c.execute(query,(asn,))
    conn.commit()


def getAsnFromUser(asn, desc):
    """Helper function to manually enter ISP abuse data into the database.

    Parameters:
        asn: The ASN number of the ISP or entity controlling the IP address,
            usually obtained via a WHOIS lookup.
        desc: The description of the ASN owner, usually the name of an ISP.
    """
    from cfltools.cflt_utils import safeprompt

    def checkBlank(string):
        if string == '':
            string = 'NONE'
        return string
    confirmed = False
    while not confirmed:
        print('\n')
        print('--- Manual ISP Entry ---')
        print('ISP ASN:     {}'.format(asn))
        print('Description: {}'.format(desc))
        print('Please fill out the following information for this ASN from'
              'data obtained from search.org. If the information is not'
              'available, simply press ENTER to leave the line blank.')
        contact_name = checkBlank(input('Enter contact name:  '))
        online_service = checkBlank(input('Online service name: '))
        online_attn = checkBlank(input('Attn:                '))
        online_serv_address = checkBlank(input('Address:             '))
        phone = checkBlank(input('Phone:               '))
        fax = checkBlank(input('Fax:                 '))
        email = checkBlank(input('Email:               '))
        notes = checkBlank(input('Notes:               '))
        req_nda = safeprompt('Requires NDA? [Y/N]: ','YN')
        print('Contact name:        {}'.format(contact_name))
        print('Online service name: {}'.format(online_service))
        print('Attn:                {}'.format(online_attn))
        print('Service address:     {}'.format(online_serv_address))
        print('Phone:               {}'.format(phone))
        print('Fax:                 {}'.format(fax))
        print('Email:               {}'.format(email))
        print('Notes:               {}'.format(notes))
        print('Requires NDA:        {}'.format(req_nda))
        req_confirm = safeprompt('Is the above information ' +
                                 'correct? [Y/N]: ', 'YN')
        if req_confirm == 'Y':
            confirmed = True
    print('--- Entry complete.  ---')
    return (asn, desc, contact_name, online_service, online_attn,
            online_serv_address, phone, fax, email, notes, req_nda)


def addAsnToDatabase(asn, desc, conn):
    """Helper function which adds ISP information to the database.

    Parameters:
        asn: The ASN number of the ISP or entity controlling the IP address,
            usually obtained via a WHOIS lookup.
        desc: The description of the ASN owner, usually the name of an ISP.
    """
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


def checkAsnExists(asn, conn):
    """Verifies if an ASN number exists in the database.
    Returns true if exists, false if not.
    Parameters:
        asn: String representing an ASN number.
    """
    c = conn.cursor()
    query = """
        SELECT asn FROM isp
        WHERE asn = ?
        """
    asnlist = c.execute(query, (asn,)).fetchall()
    if len(asnlist) > 0:
        return True
    return False


def addWhoisToDatabase(iplist, conn):
    """Helper function which adds whois information to the database.

    Parameters:
        iplist: A list of dicts that contain relevant ipwhois data.
    """
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


def getIPlist(incident_name, conn):
    """Function that retrieves all IPs associated with incident_name.
    Returns a list of ip address strings.
    Parameters:
        incident_name: String representing the incident name.
    """
    c = conn.cursor()
    iplist = c.execute("""
        SELECT ip,number_occurances FROM ipaddrs
        WHERE incident_id = ?
        """, (incident_name,)).fetchall()
    # Get unique values only
    return iplist


def getMissingASNfromUser(conn):
    """Collect missing ASNs from user.
    """
    from cfltools.cflt_utils import safeprompt
    query = """
        SELECT asn, asn_description FROM ipaddrs
        WHERE whois_done = 'Y'
        """
    asnlist = c.execute(query).fetchall()
    asnlist = list(set(asnlist))    # Get unique values only 
    conn.close()
    iterator = 1
    numNewEntry = 0
    for entry in asnlist:
        asn = entry[0]
        if asn == None:
            continue
        if not checkAsnExists(asn, conn):
            numNewEntry = numNewEntry + 1
    for entry in asnlist:
        asn = entry[0]
        desc = entry[1]
        if not checkAsnExists(asn, conn):
            if asn == None:
                continue
            print('Currently reviewing new ASN entry {} '\
                  'of {}.'.format(iterator,numNewEntry))
            answer = safeprompt('Enter entry for {}? '\
                                '[Y/N]: '.format(entry[1]),'YN')
            if answer == 'Y':
                iterator = iterator + 1
                addAsnToDatabase(asn, desc)
            else:
                break
    print('ASN entry complete.')


def run(incident_name):
    """Function run when the module is called from the CLI.
    Parameters:
        incident_name: String representing an incident name.
    """
    import sqlite3
    db_connection = sqlite3.connect(config['USER']['db_loc'])
    iplist = getIPlist(incident_name, db_connection)
    iplist_whois = getWhois(iplist)
    addWhoisToDatabase(iplist_whois, db_connection)
    db_connection.close()


def asScript():
    print('Running getwhois as script.')
    pass

if __name__ == '__main__':
    asScript()
