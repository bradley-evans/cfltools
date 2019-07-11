"""
Tests for sqlalchemy database objects.
"""


def test_db_ISP():
    """
    Test for ISP database object.
    """
    from cfltools.database.objects import ISP
    initial = ISP(asn=10)
    assert initial.asn == 10


def test_db_IPAddrTest():
    """
    Test for IPAddr database object.
    """
    from cfltools.database.objects import IPAddr
    initial = IPAddr(ipv4='8.8.8.8')
    assert initial.ipv4 == '8.8.8.8'


def test_db_Incident():
    """
    Test for Incident database object.
    """
    from cfltools.database.objects import Incident
    initial = Incident(incident_id=1, incident_name='TestIncident',
                       folder_loc='/test/loc/', description='TestDescription')
    assert initial.incident_id == 1
    assert initial.incident_name == 'TestIncident'


def test_db_SeenFile():
    """
    Test for ISP database object.
    """
    from cfltools.database.objects import SeenFile
    initial = SeenFile(filename='/test/loc/afile.csv')
    assert initial.filename == '/test/loc/afile.csv'


def test_db_basic_engine():
    """
    Minimal test with a memory-only database and
    an engine generated in the test function. This
    was mostly to experiment with SQLAlchemy ORM
    but the test will remain just to check the
    basic objects.
    """
    from cfltools.database.objects import Incident, ISP, SeenFile, IPAddr, makesession

    session = makesession()
    testincident = Incident(incident_id=1, incident_name='TestIncident',
                            folder_loc='/test/loc/', description='TestDescription')
    testasn = ISP(asn=10)
    testfile = SeenFile(filename='/test/loc/afile.csv', incident_id=1)
    testip = IPAddr(ipv4='8.8.8.8', asn=10)
    session.add_all([testincident, testasn, testfile, testip])
    session.commit()
    ourincident = session.query(Incident).filter_by(incident_id=1).first()
    assert ourincident == testincident
    ourfile = session.query(SeenFile).filter_by(filename='/test/loc/afile.csv').first()
    assert ourfile == testfile
    ourip = session.query(IPAddr).filter_by(ipv4='8.8.8.8').first()
    assert ourip == testip
    ourasn = session.query(ISP).filter_by(asn=10).first()
    assert ourasn == testasn


if __name__ == "__main__":
    test_db_basic_engine()
