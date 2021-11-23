from BColors import BColors

class Portfolio(object):
    
    def __init__(self):
        self.assetList = []
        self.indicesList = []
        
    def updatePortfolio(self):
        for asset in self.getAssetList():
            asset.updateTicker()
        
        for index in self.getIndicesList():
            index.updateTicker()
    
    def addAsset(self, asset):
        self.assetList.append(asset)
        
    def getAssetList(self):
        return self.assetList
        
    def getPortfolioRegularMarketPrice(self):
        portfolioRegularMarketPrice = 0.0
        
        for asset in self.assetList:
            portfolioRegularMarketPrice += float(asset.getCurrentAssetValue())
            
        return portfolioRegularMarketPrice
        
    def getPortfolioRegularMarketPrevClose(self):
        portfolioRegularMarketPrevClose = 0.0
        
        for asset in self.assetList:
            portfolioRegularMarketPrevClose += float(asset.getRegularMarketPrevClose()) * float(asset.getShareCount())
            
        return portfolioRegularMarketPrevClose
        
    def getPortfolioAveragePrice(self):
        portfolioAveragePrice = 0.0
        
        for asset in self.assetList:
            portfolioAveragePrice += float(asset.getAveragePrice()) * float(asset.getShareCount())
            
        return portfolioAveragePrice
        
    def getPortfolioPercToday(self):
        portfolioPercToday = float(self.getPortfolioRegularMarketPrice()) / float(self.getPortfolioRegularMarketPrevClose()) * 100 -100
        return portfolioPercToday

    def getPortfolioProfitToday(self):
        portfolioProfitToday = self.getPortfolioRegularMarketPrice() - self.getPortfolioRegularMarketPrevClose()
        return portfolioProfitToday
        
    def getPortfolioPercTodayColored(self):
        portfolioPercToday = self.getPortfolioPercToday()
        
        if portfolioPercToday < 0:
            portfolioPercTodayColored = BColors.FAIL + str(round(portfolioPercToday,2)) + BColors.ENDC
        elif portfolioPercToday > 0:
            portfolioPercTodayColored = BColors.OKGREEN + str(round(portfolioPercToday,2)) + BColors.ENDC
        else:
            portfolioPercTodayColored = str(round(portfolioPercToday,2))
        
        return portfolioPercTodayColored

    def getPortfolioProfit(self):
        portfolioProfit = float(self.getPortfolioRegularMarketPrevClose()) - float(self.getPortfolioAveragePrice())
        return portfolioProfit
        
    def getPortfolioProfitPerc(self):
        portfolioProfitPerc = float(self.getPortfolioRegularMarketPrice()) / float(self.getPortfolioAveragePrice()) * 100 - 100
        return portfolioProfitPerc
        
    def getPortfolioProfitColored(self):
        portfolioProfit = self.getPortfolioProfit()
        
        if portfolioProfit < 0:
            portfolioProfitColored = BColors.FAIL + str(round(portfolioProfit,2)) + BColors.ENDC
        elif portfolioProfit > 0:
            portfolioProfitColored = BColors.OKGREEN + str(round(portfolioProfit,2)) + BColors.ENDC
        else:
            portfolioProfitColored = str(round(portfolioProfit,2))
        
        return portfolioProfitColored
        
    def getPortfolioProfitPercColored(self):
        portfolioProfitPerc = self.getPortfolioProfitPerc()
        
        if portfolioProfitPerc < 0:
            portfolioProfitPercColored = BColors.FAIL + str(round(portfolioProfitPerc,2)) + BColors.ENDC
        elif portfolioProfitPerc > 0:
            portfolioProfitPercColored = BColors.OKGREEN + str(round(portfolioProfitPerc,2)) + BColors.ENDC
        else:
            portfolioProfitPercColored = str(round(portfolioProfitPerc,2))
        
        return portfolioProfitPercColored
    
    def addIndex(self, index):
        self.indicesList.append(index)
        
    def getIndicesList(self):
        return self.indicesList