#pylint: disable = redefined-outer-name, no-self-use, too-few-public-methods
"""
Tests for cfltools' log parsing functionality
"""


from random import randint
from datetime import datetime
import pytest
from cfltools.logparse import LogParser, IPAddress
from cfltools.utilities.test_utilities import dummy_configfile


LOGSIZE = 10


@pytest.fixture
def ipv4address():
    """
    Generates a random ipv4 address.
    """
    class IPv4AddrFactory():
        """Generates random ipv4 addreses."""
        def get(self):
            """Return an ipv4 address."""
            ipaddr = str(randint(1, 255)) + '.' + \
                     str(randint(1, 255)) + '.' + \
                     str(randint(1, 255)) + '.' + \
                     str(randint(1, 255))
            return ipaddr
    return IPv4AddrFactory()


@pytest.fixture
def randomdatetime():
    """
    Generates a random date. Returns a
    date and time betweem 20100101 and
    20110101.
    """
    class RandomDateTimeFactory():
        """Returns a randomly generated date and time."""
        def get(self):
            """Return a date/time"""
            # POSIX date for 20100101 0100Z: 1262350800
            # POSIX date for 20110101 0100Z: 1293886800
            # Use these dates to bracket dummy dates.
            date_posix = randint(1262350800, 1293886800)
            return str(date_posix)

        def get_iso(self):
            """Return a date/time in ISO format"""
            # Ex: 1262350800 => '2010-01-01T05:00:00'
            date_posix = randint(1262350800, 1293886800)
            date_iso = datetime.fromtimestamp(date_posix)
            return date_iso.isoformat()
    return RandomDateTimeFactory()


@pytest.fixture
def randomNumOccurances():
    """
    Generate a random number of occurances.
    """
    class RandomNumOccurFactory():
        """Generates a random number of occurances."""
        def get(self):
            """Return a random number of occurances."""
            return str(randint(1, 100))
    return RandomNumOccurFactory()


@pytest.fixture
def iplogline(ipv4address, randomdatetime, randomNumOccurances):
    """
    Generate a random IP logfile line.
    """
    class IPLogLineFactory():
        """Gives us one line of a logfile."""
        def get(self):
            """Returns a list object that is one line of a dummy logfile."""
            return [ipv4address.get(), \
                    randomdatetime.get_iso(), \
                    randomNumOccurances.get()]
    return IPLogLineFactory()


@pytest.fixture
def logfile_unprocessed(tmpdir, iplogline):
    """
    Generates a dummy CSV file for testing.
    This log file is not preprocessed.
    Use answerkey to determine what the actual number
    of occurances should have been.
    """
    answerkey = {}
    logfile = tmpdir.join("logfile.csv")
    for _i in range(1, LOGSIZE):
        line = iplogline.get()
        numOccur = int(line[2])
        answerkey[line[0]] = (line[1], numOccur)
        with open(logfile, 'a+') as file:
            file.write('ip,time\n')
            for _j in range(0, numOccur):
                file.write(line[0] + ',' + line[1] + '\n')
    yield answerkey, str(logfile)


@pytest.fixture
def logfile(tmpdir, iplogline):
    """
    Generates a dummy CSV file for testing.
    This log file is pre-processed with unique IPs and counts.
    """
    testfile = tmpdir.join("logfile.csv")
    with open(testfile, 'a') as file:
        file.write('ip,time,occurs\n')
        for _i in range(1, LOGSIZE):
            line = iplogline.get()
            file.write(line[0] + ',' + line[1] + ',' + line[2] + '\n')
    yield testfile


@pytest.fixture
def dummy_asndb(tmpdir):
    """
    Generates a dummy ASNDB for IP resolution testing.
    """
    from cfltools.utilities import asn_update
    from pyasn import pyasn
    asn_datfile = asn_update(tmpdir)
    yield pyasn(str(asn_datfile))


def test_open_file_and_checksum(logfile):
    """
    Verifies that a file can be opened and checksummed
    by LogParser() and LogFile().
    """
    from hashlib import md5
    parser = LogParser(logfile)
    with open(logfile) as file:
        data = file.read()
    test_md5 = md5(data.encode('utf-8')).hexdigest()
    assert parser.logfile.md5() == test_md5


def test_open_csv_file_and_checksum(logfile):
    """
    Verifies that a file can be opened and checksummed
    by LogParser() and LogFile().
    """
    from hashlib import md5
    parser = LogParser(logfile)
    with open(logfile) as file:
        data = file.read()
    test_md5 = md5(data.encode('utf-8')).hexdigest()
    assert parser.logfile.md5() == test_md5


def test_csvfile_getsize(logfile):
    """
    Quick test to ensure that CSVLogFile is determining
    log lengths correctly.
    """
    parser = LogParser(logfile)
    assert parser.logfile.size() == LOGSIZE



def test_findipcolumn(logfile):
    """
    Quick check to test the CSVLogFile object's 
    ability to fine the column containing IP
    addresses.
    """
    parser = LogParser(logfile)
    assert parser.logfile.ipcolumn() == 0


def test_csvfile_findtimecolumn(logfile):
    """
    Quick check to test the CSVLogFile object's 
    ability to fine the time column
    """
    parser = LogParser(logfile)
    assert parser.logfile.timecolumn() == 1


def test_csvfile_findunique(logfile_unprocessed):
    """Test the unique IP discovery features of CSVLogFile()."""
    answerkey, logfile = logfile_unprocessed
    parser = LogParser(logfile)
    successes = 0
    for key in answerkey:
        try:
            assert parser.logfile.unique[key].occurances == answerkey[key][1]
        except AssertionError as e:
            e.args += ('key: {}'.format(key),
                       'successes: {}'.format(successes))
            raise
        successes += 1


def test_ipaddress_timestampconversion():
    times = [
        'Thursday, January 1, 1970 12:16:40 AM UTC',
        'Thursday, January 1, 1970 12:33:20 AM UTC',
        'Thursday, January 1, 1970 12:50:00 AM UTC',
        'Thursday, January 1, 1970 1:06:40 AM UTC'
        ]
    ipaddr = IPAddress('0.0.0.0', 'Wed Dec 31 16:25:00 1969')
    for time in times:
        ipaddr.update_time(time)
    assert ipaddr.earliest.posix() == 1000 # corresponds to times[0]
    assert ipaddr.latest.posix() == 4000 # corresponds to times[3]


def test_ipaddress_getasn(dummy_asndb):
    """Test IPAddress() asn lookup method"""
    ipaddr = IPAddress('1.1.1.1', 'Wed Dec 31 16:25:00 2013')
    assert ipaddr.get_asn(dummy_asndb) == dummy_asndb.lookup('1.1.1.1')[0]

#TODO: unit test to check if earliest / latest times are good
#TODO: unit test to check if time stamp conversion from various formats are good




if __name__ == '__main__':
    pass
