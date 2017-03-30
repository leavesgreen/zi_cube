class aa():
    sdic = {}

    def __init__(self):
        self.ta = "ddd"
        self.tb = "ccc"
        self.sdic={}
        self.sdic["k1"] = "v1"
        self.sdic["k2"] = "v2"
    def __getattr__(self,s):
        if self.sdic.has_key(s):
            return self.sdic.get(s)
        else:
            raise AttributeError

if __name__=="__main__":
    a = aa();
    print getattr(a,'ta')
    print getattr(a,'k2')
    print getattr(a,'k3')
