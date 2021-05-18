from Ticker import Ticker

class Index(Ticker):
    def __init__(self, symbol, name):
        super(Index,self).__init__(symbol)
        self.name = name
    
    def getName(self):
        return self.name
