#!/usr/bin/python

import json
import sys
import getopt
import os
import time
import requests
import datetime
from xml.dom import minidom
from prettytable import PrettyTable
from Asset import Asset
from Index import Index
from Portfolio import Portfolio

def tableView():
    t = PrettyTable(['Name'.ljust(12), 'Last Shr.'.ljust(10), 'Last'.ljust(10), ''.ljust(3), 'Today%'.ljust(10), 'Avg. price'.ljust(10), 'Profit%'.ljust(10), 'Profit'.ljust(10)])
    
    t.align = "l"
    t.sortby = "Name".ljust(12)
    
    
    for asset in portfolio.getAssetList():
        t.add_row([str(asset.getName())[0:11].ljust(12)\
         ,str(asset.getRegularMarketPrice())[0:9].ljust(10)\
         ,str(asset.getCurrentAssetValue())[0:9].ljust(10)\
         ,str(asset.getCurrency())[0:3].ljust(3)\
         ,asset.getPercTodayColored()\
         ,str(asset.getAveragePrice())[0:9].ljust(10)\
         ,asset.getProfitPercColored()\
         ,asset.getProfitColored()])
   
    ttotal = PrettyTable(['Name'.ljust(12), ''.ljust(10), 'Last'.ljust(10), ''.ljust(3), 'Today%'.ljust(10), 'Avg. price'.ljust(10), 'Profit%'.ljust(10), 'Profit'.ljust(10)])
    ttotal.align = "l"

    ttotal.add_row(["Total".ljust(12)\
     ," ".ljust(10)\
     ,str(portfolio.getPortfolioRegularMarketPrice())[0:9].ljust(10)\
     ," ".ljust(3)\
     ,portfolio.getPortfolioPercTodayColored()\
     ,str(portfolio.getPortfolioAveragePrice())[0:9].ljust(10)\
     ,portfolio.getPortfolioProfitPercColored()\
     ,portfolio.getPortfolioProfitColored()])


    t2 = PrettyTable(['Index'.ljust(12), 'Last'.ljust(10), ''.ljust(3), 'Today%'.ljust(10)])
    t2.align = "l"
    t2.sortby = "Index".ljust(12)

    for index in portfolio.getIndicesList():
        t2.add_row([str(index.getName())[0:11].ljust(12)\
         ,str(index.getRegularMarketPrice())[0:9].ljust(10)\
         ,index.getCurrency()[0:3].ljust(3)\
         ,index.getPercTodayColored() ])
        write('\b\b  \b\b')
    
    os.system('clear')
    
    print(t) 
    print(ttotal)
    print(t2)
    
    x = displayTimeFullList
    write("Update in ")
    flush()
    while x > 0:
        write(str(x).zfill(2))
        flush()
        time.sleep(1)
        write("\b\b  \b\b")
        flush()
        x -= 1
    write('\b\b\b\b\b\b\b\b\b\b          \b\b\b\b\b\b\b\b\b\bUpdating...')
    flush()

def singleView():  
    for asset in portfolio.getAssetList():

        headerName = asset.getName()[0:11].ljust(12)
        headerPrice = str(asset.getRegularMarketPrice()).ljust(10)
        t = PrettyTable([headerName, headerPrice])
        t.align = "l"

        t._max_width = {'headerName' : 12, 'headerPrice' : 10 } 
        
        t.add_row(["Today%" ,asset.getPercTodayColored()])
        t.add_row(["Avg. price",str(asset.getAveragePrice())[0:9].ljust(10)])
        t.add_row(["Currency", asset.getCurrency()])
        t.add_row(["Profit%", asset.getProfitPercColored()])
        t.add_row(["Profit", asset.getProfitColored()])
        t.add_row(["Shares", str(asset.getShareCount())[0:9].ljust(10)])
        
        os.system('clear')
        print(t)
        time.sleep(displayTimeSingle)


def overView():
    lines = 7
    count = 0
    t = PrettyTable(['Name', 'Today%'.ljust(10)])
    t.align = "l"
    t._max_width = {'Name' : 12, 'today%' : 10 } 

    length = len(portfolio.getAssetList())
    
    for asset in portfolio.getAssetList():

        t.add_row([str(asset.getName())[0:11].ljust(12)\
         ,asset.getPercTodayColored()])
        count += 1
        length -= 1
        
        if count >= lines:
            if length >= lines:
                os.system('clear')
                print(t)
                time.sleep(displayTimeList)
                count = 0
                t.clear_rows()
            else:
                os.system('clear')
                print(t)
                time.sleep(displayTimeList)
                count = 0
                x = length - 1
                while x >= 0:
                    t.del_row(x)
                    x -= 1
        if length == 0:
            os.system('clear')
            print(t)
            time.sleep(displayTimeList)
                

def overViewIndices():
    lines = 7
    count = 0
    t = PrettyTable(['Name', 'Today%'.ljust(10)])
    t.align = "l"
    t._max_width = {'Name' : 12, 'today%' : 10 } 

    length = len(portfolio.getIndicesList())
    
    for index in portfolio.getIndicesList():

        t.add_row([str(index.getName())[0:11].ljust(12)\
         ,index.getPercTodayColored()])
        count += 1
        length -= 1
        
        if count >= lines:
            if length >= lines:
                os.system('clear')
                print(t)
                time.sleep(displayTimeList)
                count = 0
                t.clear_rows()
            else:
                os.system('clear')
                print(t)
                time.sleep(displayTimeList)
                count = 0
                x = length - 1
                while x >= 0:
                    t.del_row(x)
                    x -= 1
        if length == 0:
            os.system('clear')
            print(t)
            time.sleep(displayTimeList)
                



write = sys.stdout.write
flush = sys.stdout.flush

config = minidom.parse('config.xml')

displayTimeFullList = int(config.getElementsByTagName('displayTimeFullList')[0].firstChild.data)
displayTimeList = int(config.getElementsByTagName('displayTimeList')[0].firstChild.data)
displayTimeSingle = int(config.getElementsByTagName('displayTimeSingle')[0].firstChild.data)

items = config.getElementsByTagName('item')
indices = config.getElementsByTagName('index')

os.system('clear')
write("\033[?25l")
flush()

portfolio = Portfolio()

write("Initializing Portfolio... ")
flush()

for item in items:
    tickerNode = item.getElementsByTagName('ticker')
    symbol = tickerNode[0].firstChild.data
                     
    averagePriceNode = item.getElementsByTagName('averagePrice')
    averagePrice = float(averagePriceNode[0].firstChild.data)
    shareCountNode = item.getElementsByTagName('shareCount')
    shareCount = int(shareCountNode[0].firstChild.data)
        
    name = item.getAttribute('name')

    asset = Asset(symbol, name, averagePrice, shareCount)
    
    portfolio.addAsset(asset)
    
for index in indices:
    tickerNode = index.getElementsByTagName('ticker')
    symbol = tickerNode[0].firstChild.data
    
    name = index.getAttribute('name')
    
    indexAsset = Index(symbol, name)
    
    portfolio.addIndex(indexAsset)
    
write("done")
flush()

try:
    opts, args = getopt.getopt(sys.argv[1:],"slo")
except getopt.GetoptError:
    print ('testticker.py -slo')
    sys.exit(2)

for opt, arg in opts:
    if opt == '-o':
        while True:
            try:
                overViewIndices() 
                overView()
                portfolio.updatePortfolio()
            except KeyboardInterrupt:
                print ("Bye")
                sys.exit()
            except SystemExit:
                sys.exit()
            except:
                print("Exception occured") 
    if opt == '-s':
        while True:
            try: 
                overViewIndices()
                singleView()
                portfolio.updatePortfolio()
            except KeyboardInterrupt:
                print ("Bye")
                sys.exit()
            except SystemExit:
                sys.exit()
            except:
                print("Exception occured") 
    elif opt == '-l':
        while True:
            try:
                tableView()
                portfolio.updatePortfolio()
            except KeyboardInterrupt:
                print ("Bye")
                sys.exit()
            except SystemExit:
                sys.exit()
            except:
                print("Exception occured")
  

