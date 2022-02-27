import json
import requests
from BColors import BColors

class Ticker(object):
    headers = {
    "Host": "query1.finance.yahoo.com:443",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
    "sec-ch-ua-mobile": "?0",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36"
    } 
    yahooUrl = 'https://query1.finance.yahoo.com/v7/finance/quote?corsDom=finance.yahoo.com&symbols='

    def __init__(self, symbol):
        self.symbol = symbol
        self.regularMarketPrice = 0
        self.regularMarketTime = 0
        self.regularMarketPrevClose = 0
        self.percToday = 0
        self.currency = ""
        self.updated = False
        self.updateTicker()

    def getOnlineJson(self):
        try:
            url = Ticker.yahooUrl + self.symbol
            r = requests.get(url, headers=Ticker.headers)
            assetJson = json.loads(r.text)
        except:
            print("Yahoo webservice not reachable")
            return None
        return assetJson
   
    def updateTicker(self):
        assetJson = self.getOnlineJson()
        if assetJson:
            try:
                self.regularMarketPrice = assetJson['quoteResponse']['result'][0]['regularMarketPrice']
                self.regularMarketTime = assetJson['quoteResponse']['result'][0]['regularMarketTime']
                self.regularMarketPrevClose = assetJson['quoteResponse']['result'][0]['regularMarketPreviousClose']
                self.percToday = self.regularMarketPrice / self.regularMarketPrevClose * 100 - 100
                self.currency = assetJson['quoteResponse']['result'][0]['currency']
                self.updated = True
            except:
                print("Ticker not updating due to yahoo webservice delivering odd information")
                self.updated = False
        else:
            self.updated = False
            print("Update Ticker not updating asset due to problems with yahoo webservice")

    def isUpdated(self):
        return self.updated

    def getRegularMarketPrice(self):
        return self.regularMarketPrice

    def getRegularMarketTime(self):
        return self.regularMarketTime
        
    def getRegularMarketPrevClose(self):
        return self.regularMarketPrevClose
        
    def getCurrency(self):
        return self.currency
        
    def getPercToday(self):
        return self.percToday
        
    def getPercTodayColored(self):
        percToday = self.getPercToday()
        
        if percToday < 0:
            percTodayColored = BColors.FAIL + str(round(percToday,2)) + BColors.ENDC
        elif percToday > 0:
            percTodayColored = BColors.OKGREEN + str(round(percToday,2)) + BColors.ENDC
        else:
            percTodayColored = str(round(percToday,2))
            
        return percTodayColored
        
