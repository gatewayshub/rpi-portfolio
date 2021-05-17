#!/usr/bin/python
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

import json
import sys
import getopt
import os
import time
import requests
import datetime
from xml.dom import minidom
from prettytable import PrettyTable


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

def getAsset(symbol):
    url = 'https://query1.finance.yahoo.com/v7/finance/quote?corsDom=finance.yahoo.com&symbols=' + symbol
    r = requests.get(url, headers=headers)            
    assetJson = json.loads(r.text)
    return assetJson

def tableView():
    t = PrettyTable(['Name'.ljust(12), 'Last Shr.'.ljust(10), 'Last'.ljust(10), ''.ljust(3), 'Today%'.ljust(10), 'Avg. price'.ljust(10), 'Profit%'.ljust(10), 'Profit'.ljust(10)])
    
    t.align = "l"
    t.sortby = "Name".ljust(12)
    
    portfolioPrice = 0
    portfolioAvgPrice = 0
    portfolioPrevClose = 0

    for item in items:
        tickerNode = item.getElementsByTagName('ticker')
        tickerName = tickerNode[0].firstChild.data
        
        while True:
            try:     
                assetJson = getAsset(tickerName)
            except KeyboardInterrupt:
                print "bye"
                sys.exit(0)
            except:
                print("Error yahoo webservice... Keep trying")
                time.sleep(2)
                continue
            else:
                break
                
        averagePriceNode = item.getElementsByTagName('averagePrice')
        averagePrice = float(averagePriceNode[0].firstChild.data)
        shareCountNode = item.getElementsByTagName('shareCount')
        shareCount = int(shareCountNode[0].firstChild.data)
        
        regularMarketPrice = assetJson['quoteResponse']['result'][0]['regularMarketPrice']
        regularMarketPreviousClose = assetJson['quoteResponse']['result'][0]['regularMarketPreviousClose']
        
        name = item.getAttribute('name')
        lastValue = round(regularMarketPrice * shareCount, 2)

        portfolioPrice += regularMarketPrice * shareCount
        portfolioAvgPrice += averagePrice * shareCount
        portfolioPrevClose += regularMarketPreviousClose * shareCount
        
        currency = assetJson['quoteResponse']['result'][0]['currency']

        percToday = regularMarketPrice / regularMarketPreviousClose * 100 - 100

        if percToday < 0:
            percTodayColored = bcolors.FAIL + str(round(percToday, 2)) + bcolors.ENDC
        elif percToday > 0:
            percTodayColored = bcolors.OKGREEN + str(round(percToday,2)) + bcolors.ENDC
        else:
            percTodayColored = str(round(percToday,2))

        profit = regularMarketPrice / averagePrice * 100 - 100
    
        if profit < 0:
            profitColored = bcolors.FAIL + str(round(profit, 2)) + bcolors.ENDC
        elif profit > 0:
            profitColored = bcolors.OKGREEN + str(round(profit,2)) + bcolors.ENDC
        else:
            profitColored = str(round(profit,2))

        profitTotal = (regularMarketPrice - averagePrice) * shareCount

        if profitTotal < 0:
            profitTotalColored = bcolors.FAIL + str(round(profitTotal,2)) + bcolors.ENDC
        elif profitTotal > 0:
            profitTotalColored = bcolors.OKGREEN + str(round(profitTotal,2)) + bcolors.ENDC
        else:
            profitTotalColored = str(round(profitTotal,2))
            

        t.add_row([str(name)[0:11].ljust(12)\
         ,str(regularMarketPrice)[0:9].ljust(10)\
         ,str(lastValue)[0:9].ljust(10)\
         ,currency[0:3].ljust(3)\
         ,percTodayColored\
         ,str(averagePrice)[0:9].ljust(10)\
         ,profitColored\
         ,profitTotalColored])
   
    ttotal = PrettyTable(['Name'.ljust(12), ''.ljust(10), 'Last'.ljust(10), ''.ljust(3), 'Today%'.ljust(10), 'Avg. price'.ljust(10), 'Profit%'.ljust(10), 'Profit'.ljust(10)])
    ttotal.align = "l"

    totalPercToday = portfolioPrice / portfolioPrevClose * 100 - 100  
    totalProfitTotal = portfolioPrice - portfolioAvgPrice
    totalProfit = portfolioPrice / portfolioAvgPrice * 100 - 100
    
    if totalPercToday < 0:
        totalPercTodayColored = bcolors.FAIL + str(round(totalPercToday,2)) + bcolors.ENDC
    elif totalPercToday > 0:
        totalPercTodayColored = bcolors.OKGREEN + str(round(totalPercToday,2)) + bcolors.ENDC
    else:
        totalPercTodayColored = str(round(totalPercToday,2))
        
    if totalProfitTotal < 0:
        totalProfitTotalColored = bcolors.FAIL + str(round(totalProfitTotal,2)) + bcolors.ENDC
    elif totalProfitTotal > 0:
        totalProfitTotalColored = bcolors.OKGREEN + str(round(totalProfitTotal,2)) + bcolors.ENDC
    else:
        totalProfitTotalColored = str(round(totalProfitTotal,2))
        
    if totalProfit < 0:
        totalProfitColored = bcolors.FAIL + str(round(totalProfit,2)) + bcolors.ENDC
    elif totalProfit > 0:
        totalProfitColored = bcolors.OKGREEN + str(round(totalProfit,2)) + bcolors.ENDC
    else:
        totalProfitColored = str(round(totalProfit,2))
    
    ttotal.add_row(["Total".ljust(12)\
     ," ".ljust(10)\
     ,str(portfolioPrice).ljust(10)\
     ," ".ljust(3)\
     ,totalPercTodayColored\
     ,portfolioAvgPrice\
     ,totalProfitColored\
     ,totalProfitTotalColored])


    t2 = PrettyTable(['Index'.ljust(12), 'Last'.ljust(10), ''.ljust(3), 'Today%'.ljust(10)])
    t2.align = "l"
    t2.sortby = "Index".ljust(12)

    for item in indices:
        tickerNode = item.getElementsByTagName('ticker')
        tickerName = tickerNode[0].firstChild.data
        
        while True:
            try:     
                assetJson = getAsset(tickerName)
            except KeyboardInterrupt:
                print "bye"
                sys.exit(0)
            except:
                print("Error yahoo webservice... Keep trying")
                time.sleep(2)
                continue
            else:
                break
                
        regularMarketPrice = assetJson['quoteResponse']['result'][0]['regularMarketPrice']
        regularMarketPreviousClose = assetJson['quoteResponse']['result'][0]['regularMarketPreviousClose']
        
        name = item.getAttribute('name')
        
        currency = assetJson['quoteResponse']['result'][0]['currency']

        percToday = regularMarketPrice / regularMarketPreviousClose * 100 - 100

        if percToday < 0:
            percTodayColored = bcolors.FAIL + str(round(percToday, 2)) + bcolors.ENDC
        elif percToday > 0:
            percTodayColored = bcolors.OKGREEN + str(round(percToday,2)) + bcolors.ENDC
        else:
            percTodayColored = str(round(percToday,2))
        

        t2.add_row([str(name)[0:11].ljust(12)\
         ,str(regularMarketPrice)[0:9].ljust(10)\
         ,currency[0:3].ljust(3)\
         ,percTodayColored ])
        write('\b\b  \b\b')
    
    os.system('clear')
    print(t) 
    print(ttotal)
    print(t2)
    x = displayTimeFullList
    write("Update in ")
    sys.stdout.flush()
    while x > 0:
        write(str(x).zfill(2))
        sys.stdout.flush()
        time.sleep(1)
        write("\b\b  \b\b")
        sys.stdout.flush()
        x -= 1

def singleView():
    t = PrettyTable([' ', '  '])
    t.align[" "] = "l"
    t.align["  "] = "r"
    
    for item in items:
        tickerNode = item.getElementsByTagName('ticker')
        tickerName = tickerNode[0].firstChild.data
        
        while True:
            try:     
                assetJson = getAsset(tickerName)
            except KeyboardInterrupt:
                print "bye"
                sys.exit(0)
            except:
                print("Error yahoo webservice... Keep trying")
                time.sleep(2)
                continue
            else:
                break

        averagePriceNode = item.getElementsByTagName('averagePrice')
        averagePrice = float(averagePriceNode[0].firstChild.data)
        shareCountNode = item.getElementsByTagName('shareCount')
        shareCount = int(shareCountNode[0].firstChild.data)
        
        regularMarketPrice = assetJson['quoteResponse']['result'][0]['regularMarketPrice']
        regularMarketPreviousClose = assetJson['quoteResponse']['result'][0]['regularMarketPreviousClose']
        
        name = item.getAttribute('name')
        
        currency = assetJson['quoteResponse']['result'][0]['currency']

        percToday = regularMarketPrice / regularMarketPreviousClose * 100 - 100
        

        if percToday < 0:
            percTodayColored = bcolors.FAIL + str(round(percToday, 2)) + bcolors.ENDC
        elif percToday > 0:
            percTodayColored = bcolors.OKGREEN + str(round(percToday,2)) + bcolors.ENDC
        else:
            percTodayColored = str(round(percToday,2))

        profit = regularMarketPrice / averagePrice * 100 - 100

        if profit < 0:
            profitColored = bcolors.FAIL + str(round(profit, 2)) + bcolors.ENDC
        elif profit > 0:
            profitColored = bcolors.OKGREEN + str(round(profit,2)) + bcolors.ENDC
        else:
            profitColored = str(round(profit,2))

        profitTotal = (regularMarketPrice - averagePrice) * shareCount

        if profitTotal < 0:
            profitTotalColored = bcolors.FAIL + str(round(profitTotal,2)) + bcolors.ENDC
        elif profitTotal > 0:
            profitTotalColored = bcolors.OKGREEN + str(round(profitTotal,2)) + bcolors.ENDC
        else:
            profitTotalColored = str(round(profitTotal,2))

        headerName = name[0:11].ljust(12)
        headerPrice = str(regularMarketPrice).ljust(10)
        t = PrettyTable([headerName, headerPrice])
        t.align = "l"

        t._max_width = {'headerName' : 12, 'headerPrice' : 10 } 
        
        t.add_row(["Today%" ,percTodayColored])
        t.add_row(["Avg. price", averagePrice])
        t.add_row(["Currency", currency])
        t.add_row(["Profit%", profitColored])
        t.add_row(["Profit", profitTotalColored])
        t.add_row(["Shares", shareCount])
        
        os.system('clear')
        print(t)
        time.sleep(displayTimeSingle)


def overView():
    lines = 7
    count = 0
    t = PrettyTable(['Name', 'Today%'.ljust(10)])
    t.align = "l"
    t._max_width = {'Name' : 12, 'today%' : 10 } 
    
    length = len(items)
    
    for item in items:
        tickerNode = item.getElementsByTagName('ticker')
        tickerName = tickerNode[0].firstChild.data
        
        while True:
            try:     
                assetJson = getAsset(tickerName)
            except KeyboardInterrupt:
                print "bye"
                sys.exit(0)
            except:
                print("Error yahoo webservice... Keep trying")
                time.sleep(2)
                continue
            else:
                break

        regularMarketPrice = assetJson['quoteResponse']['result'][0]['regularMarketPrice']
        regularMarketPreviousClose = assetJson['quoteResponse']['result'][0]['regularMarketPreviousClose']
        
        name = item.getAttribute('name')

        percToday = regularMarketPrice / regularMarketPreviousClose * 100 - 100
        
        if percToday < 0:
            percTodayColored = bcolors.FAIL + str(round(percToday, 2)) + bcolors.ENDC
        elif percToday > 0:
            percTodayColored = bcolors.OKGREEN + str(round(percToday,2)) + bcolors.ENDC
        else:
            percTodayColored = str(round(percToday,2))

        t.add_row([str(name)[0:11].ljust(12)\
         ,percTodayColored])
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
   
    length = len(indices)

    for item in indices:
        tickerNode = item.getElementsByTagName('ticker')
        tickerName = tickerNode[0].firstChild.data
        
        while True:
            try:     
                assetJson = getAsset(tickerName)
            except KeyboardInterrupt:
                print "bye"
                sys.exit(0)
            except:
                print("Error yahoo webservice... Keep trying")
                time.sleep(2)
                continue
            else:
                break
        
        regularMarketPrice = assetJson['quoteResponse']['result'][0]['regularMarketPrice']
        regularMarketPreviousClose = assetJson['quoteResponse']['result'][0]['regularMarketPreviousClose']
        
        name = item.getAttribute('name')

        percToday = regularMarketPrice / regularMarketPreviousClose * 100 - 100
        
        if percToday < 0:
            percTodayColored = bcolors.FAIL + str(round(percToday, 2)) + bcolors.ENDC
        elif percToday > 0:
            percTodayColored = bcolors.OKGREEN + str(round(percToday,2)) + bcolors.ENDC
        else:
            percTodayColored = str(round(percToday,2))

        t.add_row([str(name)[0:11].ljust(12)\
         ,percTodayColored])
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

config = minidom.parse('config.xml')

displayTimeFullList = int(config.getElementsByTagName('displayTimeFullList')[0].firstChild.data)
displayTimeList = int(config.getElementsByTagName('displayTimeList')[0].firstChild.data)
displayTimeSingle = int(config.getElementsByTagName('displayTimeSingle')[0].firstChild.data)

items = config.getElementsByTagName('item')
indices = config.getElementsByTagName('index')

os.system('clear')
sys.stdout.write("\033[?25l")
sys.stdout.flush()

try:
    opts, args = getopt.getopt(sys.argv[1:],"slo")
except getopt.GetoptError:
    print 'testticker.py -slo'
    sys.exit(2)

for opt, arg in opts:
    if opt == '-o':
        while True:
            try:
                overViewIndices() 
                overView()
            except KeyboardInterrupt:
                print "Bye"
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
            except KeyboardInterrupt:
                print "Bye"
                sys.exit()
            except SystemExit:
                sys.exit()
            except:
                print("Exception occured") 
    elif opt == '-l':
        while True:
            try:
                tableView()
            except KeyboardInterrupt:
                print "Bye"
                sys.exit()
            except SystemExit:
                sys.exit()
            except:
                print("Exception occured")
  

