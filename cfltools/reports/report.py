from cfltools.settings import APPFOLDER

class IpAddressReport():

    def populateWhois(self, asn):
        import sqlite3
        db_loc = self.config['USER']['db_loc']
        conn = sqlite3.connect(db_loc)
        def dict_factory(cursor,row):
            d = {}
            for idx, col in enumerate(cursor.description):
                d[col[0]] = row[idx]
            return d
        conn.row_factory = dict_factory
        c = conn.cursor()
        query = """
            SELECT * from isp
            WHERE asn = ?
            """
        whois = c.execute(query,(asn,)).fetchone()
        conn.close()
        return whois

    def getNumOccurances(self, ip):
        import sqlite3
        db_loc = self.config['USER']['db_loc']
        conn = sqlite3.connect(db_loc)
        c = conn.cursor()
        query = """
            SELECT number_occurances, incident_id FROM ipaddrs
            WHERE ip=?
            """
        data = c.execute(query,(ip,)).fetchall()
        conn.close()
        return data

    def checkWatchlist():
        # TODO: check if this IP exists in a watchlist.
        pass

    def __init__(self, ip, asn, config):
        from cfltools.logparse.getwhois import checkAsnExists
        self.config = config
        self.ip = ip
        self.occurances = self.getNumOccurances(self.ip)
        self.asn = asn
        import sqlite3
        conn = sqlite3.connect(config['USER']['db_loc'])
        if checkAsnExists(asn, conn):
            self.isWhoisDone = True
            self.whois = self.populateWhois(asn)
        else:
            self.isWhoisDone = False
        conn.close()


class IpAddressReport_CLI(IpAddressReport):

    def printCLI(self):
        string = self.printTextReport()
        print(string)

    def printTextReport(self):
        """ Generates a string for this IP so it can be printed
        to a file or elsewhere.
        """
        string = '\n=== IP address {} ===\n'.format(self.ip)
        if len(self.occurances) > 1:
            string = string + 'This IP appears in multiple incidents!\n'
        for incident in self.occurances:
            string = string +\
                'Occurs {} times in incident {}.\n'.format(incident[0],
                                                           incident[1])
        if self.isWhoisDone:
            string += 'ASN:     {}\n'.format(self.whois['asn'])
            string += 'Desc:    {}\n'.format(self.whois['description'])
            string += 'Email:   {}\n'.format(self.whois['email'])
            string += 'Phone:   {}\n'.format(self.whois['phone'])
            string += 'Fax:     {}\n'.format(self.whois['fax'])
            string += 'Notes:   {}\n'.format(self.whois['notes'])
            string += 'Attn:    {}\n'.format(self.whois['online_attn'])
            string += 'Address: {}\n'.format(self.whois['online_serv_address'])
            string += 'Service: {}\n'.format(self.whois['online_service'])
            if (self.whois['req_nda'] == 'Y'):
                string += 'This service provider requires an NDA.\n'
        return string


def reportUniqueIP(incidentid, config):
    """Reports unique IP addresses associated with an incident.

    Parameters:
        incidentid: The incident identifier.
    Returns:
        iplist: A list of IpAddressReport_CLI objects corresponding
            to the IP addresses found with the incident.
    """
    import sqlite3
    conn = sqlite3.connect(config['USER']['db_loc'])
    c = conn.cursor()
    query = """
        SELECT ip, asn FROM ipaddrs
        WHERE incident_id = ?
        """
    data = c.execute(query, (incidentid,)).fetchall()
    conn.close()
    iplist = []
    for entry in data:
        this = IpAddressReport_CLI(entry[0],entry[1], config)
        iplist.append(this)
    return iplist


def reportToCLI(incidentid, config):
    print('Report for incident {}'.format(incidentid))
    iplist = reportUniqueIP(incidentid, config)
    for record in iplist:
        record.printCLI()


def run():
    pass


def asScript():
    pass


if __name__ == '__main__':
    asScript()
