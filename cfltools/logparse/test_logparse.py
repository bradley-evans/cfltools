def test_findipcolumn():
    import cfltools.logparse.getuniqueip as getuniqueip
    testrow = [
            '1.1.1.1',
            'NULL',
            '0'
           ]
    column = getuniqueip.findIpColumn(testrow)
    assert column == int(testrow[2]), "Test failed in getunqiueip.findIpColumn."
