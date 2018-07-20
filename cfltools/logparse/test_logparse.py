def test_findipcolumn():
    import cfltools.logparse.getuniqueip as getuniqueip
    testrow = [
            '1.1.1.1',
            'NULL',
            '0'
           ]
    column = getuniqueip.findIpColumn(testrow)
    assert column == int(testrow[2]), "Test failed in getunqiueip.findIpColumn."

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
    getwhois.removeAsnFromDatabase(asn)
    assert getwhois.checkAsnExists(asn) == False
