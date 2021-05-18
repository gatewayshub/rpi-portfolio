from Ticker import Ticker
from BColors import BColors

class Asset(Ticker):

    def __init__(self, symbol, name, averagePrice, shareCount):
        super(Asset,self).__init__(symbol)
        
        self.name = name
        self.averagePrice = averagePrice
        self.shareCount = shareCount
        
    def getName(self):
        return self.name
        
    def getAveragePrice(self):
        return self.averagePrice
        
    def getShareCount(self):
        return self.shareCount
        
    def getProfit(self):
        profit = (float(self.getRegularMarketPrice()) - float(self.getAveragePrice())) * float(self.getShareCount())
        return profit
        
    def getProfitPerc(self):
        profitPerc = float(self.getRegularMarketPrice()) / float(self.getAveragePrice()) * 100 - 100
        return profitPerc
        
    def getProfitColored(self):
        profit = self.getProfit()
        
        if profit < 0:
            profitColored = BColors.FAIL + str(round(profit,2)) + BColors.ENDC
        elif profit > 0:
            profitColored = BColors.OKGREEN + str(round(profit,2)) + BColors.ENDC
        else:
            profitColored = str(round(profit,2))
        
        return profitColored
        
    def getProfitPercColored(self):
        profitPerc =  self.getProfitPerc()
        
        if profitPerc < 0:
            profitPercColored = BColors.FAIL + str(round(profitPerc,2)) + BColors.ENDC
        elif profitPerc > 0:
            profitPercColored = BColors.OKGREEN + str(round(profitPerc,2)) + BColors.ENDC
        else:
            profitPercColored = str(round(profitPerc,2))
        
        return profitPercColored
        
    def getCurrentAssetValue(self):
        currentAssetValue = float(self.getRegularMarketPrice()) * float(self.getShareCount())
        return currentAssetValue
            
        
        