def test_findipcolumn():
    import cfltools.logparse.getuniqueip as getuniqueip
    testrow = [
            '1.1.1.1',
            'NULL',
            '0'
           ]
    column = getuniqueip.findIpColumn(testrow)
    assert column == int(testrow[2]), "Test failed in getunqiueip.findIpColumn."


def test_findtimecolumn():
    import cfltools.logparse.getuniqueip as getuniqueip
    test1 = ['79236720298','2012-01-01 00:01:01','test.com','1.1.1.1','NULL']
    column = getuniqueip.findTimeColumn(test1)
    assert column == 1, "Test failed in getuniqueip.findTimeColumn."


def test_getAsnFromUser():
    import cfltools.logparse.getwhois as getwhois
    from io import StringIO
    import sys
    asn = '00000'
    desc = 'Test ASN generated by pytest.'
    sys.stdin = StringIO('John Doe\n'
            'Internet, Inc.\n'
            'Internet, Inc. Legal Department\n'
            '123 Anystreet Ct., Anytown, CA 92912, United States\n'
            '(123)456-7890\n'
            '(123)456-7891\n'
            'abuse@internetinc.com\n'
            'This is a test entry.\n'
            'n\n'
            'y\n')
    v0,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10 = getwhois.getAsnFromUser(asn,desc)
    assert v0 == asn
    assert v1 == desc
    assert v2 == 'John Doe'
    assert v3 == 'Internet, Inc.'
    assert v4 == 'Internet, Inc. Legal Department'
    assert v5 == '123 Anystreet Ct., Anytown, CA 92912, United States'
    assert v6 == '(123)456-7890'
    assert v7 == '(123)456-7891'
    assert v8 == 'abuse@internetinc.com'
    assert v9 == 'This is a test entry.'
    assert v10 == 'N'


def test_checkAsnExists():
    import cfltools.logparse.getwhois as getwhois
    asn = '9999999'
    assert getwhois.checkAsnExists(asn) == False


def test_ASNDatabaseFileIO():
    import cfltools.logparse.getwhois as getwhois
    from io import StringIO
    import sys
    import os
    asn = '00000'
    desc = 'Test ASN generated by pytest.'
    sys.stdin = StringIO('John Doe\n'
            'Internet, Inc.\n'
            'Internet, Inc. Legal Department\n'
            '123 Anystreet Ct., Anytown, CA 92912, United States\n'
            '(123)456-7890\n'
            '(123)456-7891\n'
            'abuse@internetinc.com\n'
            'This is a test entry.\n'
            'n\n'
            'y\n')
    getwhois.addAsnToDatabase(asn,desc)
    assert getwhois.checkAsnExists(asn) == True
    getwhois.saveISPDBtoFile('testfile_asndatabasefileio.csv')
    getwhois.removeAsnFromDatabase(asn)
    assert getwhois.checkAsnExists(asn) == False
    getwhois.loadISPDBfromFile('testfile_asndatabasefileio.csv')
    assert getwhois.checkAsnExists(asn) == True
    os.remove('testfile_asndatabasefileio.csv')
    getwhois.removeAsnFromDatabase(asn)
    assert getwhois.checkAsnExists(asn) == False


def test_getTimerange():
    import cfltools.logparse.getuniqueip as getuniqueip
    unique_ip_address = [getuniqueip.IpAddress('1.1.1.1','10'),
                         getuniqueip.IpAddress('2.2.2.2','10'),
                         getuniqueip.IpAddress('3.3.3.3','10'),
                         getuniqueip.IpAddress('4.4.4.4','10'),
                         getuniqueip.IpAddress('5.5.5.5','10')]
    testfile = open('timerange_test.csv','w')
    testfile.write('id,ip,date\n')
    testfile.write('1,1.1.1.1,2018-01-01 01:01:01\n')
    testfile.write('2,1.1.1.1,2018-01-01 01:01:10\n')
    testfile.write('3,2.2.2.2,2018-02-02 02:02:02\n')
    testfile.write('4,2.2.2.2,2018-02-02 02:02:20\n')
    testfile.write('5,3.3.3.3,2018-03-03 03:03:03\n')
    testfile.write('6,3.3.3.3,2018-03-03 03:03:30\n')
    testfile.write('7,4.4.4.4,2018-04-04 04:04:04\n')
    testfile.write('7,4.4.4.4,2018-04-04 04:04:40\n')
    testfile.write('7,5.5.5.5,2018-05-05 05:05:05\n')
    testfile.write('7,5.5.5.5,2018-05-05 05:05:05\n')
    testfile.close()
    new_unique_list = getuniqueip.getTimerange('timerange_test.csv',
                                               unique_ip_address)
    assert new_unique_list[0].startTime == 1514797261
    assert new_unique_list[0].endTime == 1514797270
    assert new_unique_list[1].startTime == 1517565722
    assert new_unique_list[1].endTime == 1517565740

def test_checkExonoraTor():
    from cfltools.logparse.checkforTor import checkExonoraTor
    assert checkExonoraTor('103.28.52.93',1532174400) == True
    assert checkExonoraTor('1.1.1.1',1532174400) == False


def test_checkIPList():
    import cfltools.logparse.checkforTor as checkforTor
    iplist = checkforTor.getIPList('test')
    checkforTor.checkIPList(iplist)
    # TODO: actually assert something here.
