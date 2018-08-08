class Logfile():

    def find_logfilesize(self):
        """
        Return the number of rows in a logfile.
        """
        import csv
        file = open(self.filename, encoding='utf-8')
        logfile_reader = csv.reader(file)
        size = sum(1 for row in logfile_reader)
        return size

    def __init__(self, filename):
        self.filename = filename
        self.logsize = self.find_logfilesize()


class Logfile_IP():
    getwhois = False
    gettor = False

    def find_uniqueipaddrs(self):
        import csv
        self.file = open(self.filename, encoding='utf-8')
        logfile_reader = csv.reader(file)

    def set_getwhois(self, getwhois):
        self.getwhois = getwhois

    def set_gettor(self, gettor):
        self.gettor = gettor

    def analyze(self):
        # perform analysis
        pass
