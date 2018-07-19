from cfltools.settings import APPFOLDER

class IpAddressReport():

    def populateWhois(self, asn):
        import sqlite3
        db_loc = APPFOLDER + '/incident.db'
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
        db_loc = APPFOLDER + '/incident.db'
        conn = sqlite3.connect(db_loc)
        c = conn.cursor()
        query = """
            SELECT number_occurances, incident_id FROM ipaddrs
            WHERE ip=?
            """
        data = c.execute(query,(ip,)).fetchall()
        return data

    def checkWatchlist():
        # TODO: check if this IP exists in a watchlist.
        pass

    def __init__(self, ip, asn):
        from cfltools.logparse.getwhois import checkAsnExists
        self.ip = ip
        self.occurances = self.getNumOccurances(self.ip)
        self.asn = asn
        if checkAsnExists(asn):
            self.isWhoisDone = True
            self.whois = self.populateWhois(asn)
        else:
            self.isWhoisDone = False


class IpAddressReport_CLI(IpAddressReport):

    def printCLI(self):
        print('=== IP address {} ==='.format(self.ip))
        if len(self.occurances) > 1:
            print('This IP appears in multiple incidents!')
        for incident in self.occurances:
            print('Occurs {} times in incident {}.'.format(incident[0],incident[1]))
        if self.isWhoisDone:
            from pprint import pprint
            # TODO: don't print this so lazily
            pprint(self.whois)
        else:
            print('Whois was not performed on this entry.')
            pass
        print('\n')

    def printFile(filename):
        pass


def reportUniqueIP(incidentid):
    """Reports unique IP addresses associated with an incident.

    Parameters:
        incidentid: The incident identifier.
    Returns:
        iplist: A list of IpAddressReport_CLI objects corresponding
            to the IP addresses found with the incident.
    """
    import sqlite3
    db_loc = APPFOLDER + '/incident.db'
    conn = sqlite3.connect(db_loc)
    c = conn.cursor()
    query = """
        SELECT ip, asn FROM ipaddrs
        """
    data = c.execute(query).fetchall()
    c.close()
    iplist = []
    for entry in data:
        this = IpAddressReport_CLI(entry[0],entry[1])
        iplist.append(this)
    return iplist


def reportToCLI(incidentid):
    iplist = reportUniqueIP(incidentid)
    for record in iplist:
        record.printCLI()


def run():
    pass


def asScript():
    pass


if __name__ == '__main__':
    asScript()
