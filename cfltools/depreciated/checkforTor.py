from cfltools.settings import APPFOLDER, INSTALLPATH


def checkExonoraTor(ip,posix_time):
    """Check if an IP was a TOR exit node at a particular time by querying ExonoraTor.

    Sends the request via https and reads the content returned for a string
    indicating that the IP was in fact an exit node.

    Parameters:
        ip: The IP address being examined.
        posix_time: A POSIX/UNIX timestamp (seconds from epoch)

    Returns:
        True if the response contains 'Result is positive', false otherwise.
    """
    import time, requests
    from datetime import datetime
    date = datetime.fromtimestamp(posix_time).strftime('%Y-%m-%d')
    url = 'https://exonerator.torproject.org/?ip=' + str(ip) + '&timestamp=' + date + '&lang=en'
    response = requests.get(url).content
    if str(response).find('Result is positive') > 0:
        return True
    elif str(response).find('Result is negative') > 0:
        return False
    print('Could not determine if {} is an exit node.'.format(ip))
    raise UserWarning


def checkIPList(iplist, conn, config):
    import time
    c = conn.cursor()
    query = """
        UPDATE ipaddrs
        SET is_tor_exit_node=?
        WHERE ip=?
        """
    isTor = False
    query_limit = int(config['USER']['max_tor_requests'])
    iterator = 0
    print('Checking for TOR exit nodes...')
    for item in iplist:
        time.sleep(1)
        isTor = checkExonoraTor(item[0],item[1])
        if isTor:
            c.execute(query, ('Y', item[0], ))
        else:
            c.execute(query, ('N', item[0], ))
        if iterator > query_limit:
            break
        iterator += 1


def getIPList(incidentid, conn):
    c = conn.cursor()
    query = """
        SELECT ip, end_time FROM ipaddrs
        WHERE incident_id = ?
        """
    data = c.execute(query, (incidentid,)).fetchall()
    return data


def run(incidentid):
    import sqlite3
    import configparser
    config = configparser.ConfigParser()
    config.read(APPFOLDER + '/cfltools.ini')
    db_connection = sqlite3.connect(config['USER']['db_loc'])
    iplist = getIPList(incidentid, db_connection)
    checkIPList(iplist, db_connection, config)
