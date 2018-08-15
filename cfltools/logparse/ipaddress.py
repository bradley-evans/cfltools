class IPAddress():

    def get_tor(self):

    def get_whois(self):
        import warnings
        from ipwhois import IPWhois
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UserWarning)
                self.whois = IPWhois(self.ip).lookup_rdap(depth=1)
        except Exception as e:
            print(e)
            print('ip: {}'.format(self.ip))
    
    def __init__(self, ip, count):
        self.ip = ip
        self.count = count
        self.whois = ''
        self.is_tor = False
        self.did_whois = False
        self.did_tor = False