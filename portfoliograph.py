#!/usr/bin/python3
from datetime import datetime
import getopt
import sys
import time
import pygame
from xml.dom import minidom
from Asset import Asset
from Index import Index
from Portfolio import Portfolio

running = True
write = sys.stdout.write
flush = sys.stdout.flush

config = minidom.parse('config.xml')
displayTimeFullList = int(config.getElementsByTagName('displayTimeFullList')[0].firstChild.data)
displayTimeList = int(config.getElementsByTagName('displayTimeList')[0].firstChild.data)
displayTimeSingle = int(config.getElementsByTagName('displayTimeSingle')[0].firstChild.data)
startFullscreen = config.getElementsByTagName('startFullscreen')[0].firstChild.data.strip()

pygame.display.init()
pygame.font.init()
pygame.mouse.set_visible(False)
pygame.display.set_caption('Portfoliograph')
xResolution = int(config.getElementsByTagName('xResolution')[0].firstChild.data)
yResolution = int(config.getElementsByTagName('yResolution')[0].firstChild.data)
tableX1 = int(xResolution / 20)
tableX2 = int(xResolution - tableX1)
bgColor = (0,0,0)
headerColor = (255,225,1)
contentColor = (235, 235, 235)
redColor = (200, 50, 50)
greenColor = (0, 200, 0)
grayColor = (128, 128, 128)
nameCut = 16
colCountTiles = 3
rowCountTiles = 3
fontName = pygame.font.SysFont('Arial', int(yResolution / 10))

if startFullscreen == "True":
    screen = pygame.display.set_mode([xResolution,yResolution],pygame.FULLSCREEN)
else:
    screen = pygame.display.set_mode([xResolution,yResolution])

portfolio = Portfolio()

def initializePortfolio():
    write("Initializing Portfolio... ")
    flush()

    items = config.getElementsByTagName('item')
    indices = config.getElementsByTagName('index')

    for item in items:
        tickerNode = item.getElementsByTagName('ticker')
        symbol = tickerNode[0].firstChild.data

        averagePriceNode = item.getElementsByTagName('averagePrice')
        averagePrice = float(averagePriceNode[0].firstChild.data)
        shareCountNode = item.getElementsByTagName('shareCount')
        shareCount = float(shareCountNode[0].firstChild.data)

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

def waitInputOrTimeout(seconds):
    global running
    done = False
    clock = pygame.time.Clock()

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                done = True
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                done = True

        dt = clock.tick(1) / 1000

        seconds -= dt

        if seconds <= 0:
            done = True

def getColorForValue(value):
    if (value > 0):
        return greenColor
    elif (value < 0):
        return redColor
    else:
        return contentColor

def getColorsDependingOnUpToDate(ticker):
    isUpdated = ticker.isUpdated()
    tickerTimestamp = ticker.getRegularMarketTime()

    if datetime.fromtimestamp(tickerTimestamp).date() == datetime.today().date():
        isUpToDate = True
    else:
        isUpToDate = False

    if not isUpdated:
        return redColor
    elif isUpdated and not isUpToDate:
        return grayColor
    elif isUpdated and isUpToDate:
        return headerColor

def displayHeader(leftHeader, rightHeader):
    fontHeaderLeft = pygame.font.SysFont('Times New Roman', int(yResolution / 10))
    textHeaderLeft = fontHeaderLeft.render(leftHeader, True, headerColor)
    textRect = textHeaderLeft.get_rect()
    textRect.topleft = (tableX1, int(yResolution / 20))
    screen.blit(textHeaderLeft, textRect)

    fontHeaderRight = pygame.font.SysFont('Times New Roman', int(yResolution / 10))
    textHeaderRight = fontHeaderRight.render(rightHeader, True, headerColor)
    textRect = textHeaderRight.get_rect()
    textRect.topright = (tableX2, int(yResolution / 20))
    screen.blit(textHeaderRight, textRect)

def overViewAssetsGraph():
    length = len(portfolio.getAssetList())

    ypos = int(yResolution / 20) + int(yResolution / 10 + 10)
    lines = 7
    count = 0

    displayHeader('Asset','Today%')
    assetList = portfolio.getAssetList()

    for asset in assetList:
        name = asset.getName()
        percToday = asset.getPercToday()

        textName = fontName.render(name[0:nameCut], True, contentColor)
        textRect = textName.get_rect()
        textRect.topleft = (tableX1, ypos)
        screen.blit(textName, textRect)
        textName = fontName.render(str(round(percToday, 3)), True, getColorForValue(percToday))
        textRect = textName.get_rect()
        textRect.topright = (tableX2, ypos)
        screen.blit(textName, textRect)

        pygame.display.flip()
        ypos += int(yResolution / 10 + 2)
        length -= 1
        count += 1

        if count >= lines:
            if length >= lines:
                waitInputOrTimeout(displayTimeList)
                count = 0
                screen.fill(bgColor)
                displayHeader('Asset', 'Today%')
                ypos = int(yResolution / 20) + int(yResolution / 10 + 10)
                if running == False:
                    break
            else:
                waitInputOrTimeout(displayTimeList)
                count = 0
                screen.fill(bgColor)
                displayHeader('Asset', 'Today%')
                ypos = int(yResolution / 20) + int(yResolution / 10 + 10)
                # Fill the table with old values
                for asset in assetList[-7:-length]:
                    name = asset.getName()
                    percToday = asset.getPercToday()

                    textName = fontName.render(name[0:nameCut], True, contentColor)
                    textRect = textName.get_rect()
                    textRect.topleft = (tableX1, ypos)
                    screen.blit(textName, textRect)
                    textName = fontName.render(str(round(percToday, 3)), True, getColorForValue(percToday))
                    textRect = textName.get_rect()
                    textRect.topright = (tableX2, ypos)
                    screen.blit(textName, textRect)

                    pygame.display.flip()
                    ypos += int(yResolution / 10 + 2)
                    count += 1
                if running == False:
                    break
        if length == 0:
            waitInputOrTimeout(displayTimeList)
            count = 0
            screen.fill(bgColor)
            ypos = int(yResolution / 20) + int(yResolution / 10 + 10)
            if running == False:
                break

def overViewIndicesGraph():
    global running

    screen.fill(bgColor)

    displayHeader('Index', 'Today%')

    length = len(portfolio.getIndicesList())

    ypos = int(yResolution / 20) +  int(yResolution / 10 + 10)
    lines = 7
    count = 0

    indicesList = portfolio.getIndicesList()

    for index in indicesList:
        name = index.getName()
        percToday = index.getPercToday()

        textName = fontName.render(name[0:nameCut], True, contentColor)
        textRect = textName.get_rect()
        textRect.topleft = (tableX1, ypos)
        screen.blit(textName, textRect)
        textName = fontName.render(str(round(percToday,3)), True, getColorForValue(percToday))
        textRect = textName.get_rect()
        textRect.topright = (tableX2, ypos)
        screen.blit(textName, textRect)

        pygame.display.flip()
        ypos += int(yResolution / 10 + 2)
        length -= 1
        count += 1

        if count >= lines:
            if length >= lines:
                waitInputOrTimeout(displayTimeList)
                count = 0
                screen.fill(bgColor)
                displayHeader('Index', 'Today%')
                ypos = int(yResolution / 20) + int(yResolution / 10 + 10)
                if running == False:
                    break
            else:
                waitInputOrTimeout(displayTimeList)
                count = 0
                screen.fill(bgColor)
                displayHeader('Index', 'Today%')
                ypos = int(yResolution / 20) + int(yResolution / 10 + 10)
                #Fill the table with old values
                for index in indicesList[-7:-length]:
                    name = index.getName()
                    percToday = index.getPercToday()

                    textName = fontName.render(name[0:nameCut], True, contentColor)
                    textRect = textName.get_rect()
                    textRect.topleft = (tableX1, ypos)
                    screen.blit(textName, textRect)
                    textName = fontName.render(str(round(percToday, 3)), True, getColorForValue(percToday))
                    textRect = textName.get_rect()
                    textRect.topright = (tableX2, ypos)
                    screen.blit(textName, textRect)

                    pygame.display.flip()
                    ypos += int(yResolution / 10 + 2)
                    count += 1
                if running == False:
                    break
        if length == 0:
            waitInputOrTimeout(displayTimeList)
            count = 0
            screen.fill(bgColor)
            ypos = int(yResolution / 20) + int(yResolution / 10 + 10)
            if running == False:
                break

def displayTile(startPosX, startPosY, asset):
    width = int(xResolution / colCountTiles)
    height = int(yResolution / rowCountTiles)

    if colCountTiles == 2:
        tilesFactor = 15
    if colCountTiles == 3:
        tilesFactor = 20
    if colCountTiles == 5:
        width = int(xResolution / (colCountTiles + 1))
        tilesFactor = 40

    fontFactorHeader = int(yResolution / (tilesFactor - (tilesFactor / 4)))
    fontFactorData = int(yResolution / tilesFactor)
    fontHeader = pygame.font.SysFont('Arial', fontFactorHeader)
    fontData = pygame.font.SysFont('Arial', fontFactorData)

    textNameFitting = False
    length = len(asset.getName())

    while not textNameFitting:
        textName = fontHeader.render(asset.getName()[0:length], True, getColorsDependingOnUpToDate(asset))
        if textName.get_rect().width <= (width - (width / 20)):
            textNameFitting = True
        else:
            length -= 1

    textPriceToday = fontData.render(str(round(asset.getRegularMarketPrice(), 2)), True, contentColor)
    textPriceTimeToday = fontData.render(time.strftime('%H:%M', time.localtime(asset.getRegularMarketTime())), True,
                                         contentColor)
    textPercToday = fontData.render(str(round(asset.getPercToday(), 2)) + "%", True,
                                    getColorForValue(asset.getPercToday()))
    textValueToday = fontData.render(str(round(asset.getCurrentAssetValue(), 1)), True, contentColor)
    textProfit = fontData.render(str(round(asset.getProfit(), 1)), True, getColorForValue(asset.getProfit()))
    textPercProfit = fontData.render(str(round(asset.getProfitPerc(), 1)) + "%", True,
                                     getColorForValue(asset.getProfitPerc()))


    tableX1 = int(width / 20)
    tableX2 = width - tableX1

    ypos = int(height / 20) + startPosY
    xpos = tableX1 + startPosX

    textRect = textName.get_rect()
    textRect.topleft = (xpos, ypos)
    screen.blit(textName, textRect)

    ypos += int(fontFactorHeader + 2)
    xpos = tableX1 + startPosX

    textRect = textPriceToday.get_rect()
    textRect.topleft = (xpos, ypos)
    screen.blit(textPriceToday, textRect)

    xpos = tableX2 + startPosX

    textRect = textPercToday.get_rect()
    textRect.topright = (xpos, ypos)
    screen.blit(textPercToday, textRect)

    ypos += int(fontFactorData + 2)
    xpos = tableX1 + startPosX

    textRect = textProfit.get_rect()
    textRect.topleft = (xpos, ypos)
    screen.blit(textProfit, textRect)

    xpos = tableX2 + startPosX

    textRect = textPercProfit.get_rect()
    textRect.topright = (xpos, ypos)
    screen.blit(textPercProfit, textRect)

    ypos += int(fontFactorData + 2)
    xpos = tableX1 + startPosX

    textRect = textValueToday.get_rect()
    textRect.topleft = (xpos, ypos)
    screen.blit(textValueToday, textRect)

    xpos = tableX2 + startPosX

    textRect = textPriceTimeToday.get_rect()
    textRect.topright = (xpos, ypos)
    screen.blit(textPriceTimeToday, textRect)

    pygame.display.flip()

def displayTileIndex(startPosX, startPosY, index):
    height = int(yResolution / rowCountTiles)

    if colCountTiles == 3 or colCountTiles == 2:
        tilesFactor = 20
        width = int(xResolution / 3)
    if colCountTiles == 5:
        tilesFactor = 40
        width = int(xResolution / colCountTiles)

    fontFactorHeader = int(yResolution / (tilesFactor - (tilesFactor / 4)))
    fontFactorData = int(yResolution / tilesFactor)
    fontHeader = pygame.font.SysFont('Arial', fontFactorHeader)
    fontData = pygame.font.SysFont('Arial', fontFactorData)

    textNameFitting = False
    length = len(index.getName())

    while not textNameFitting:
        textName = fontHeader.render(index.getName()[0:length], True, getColorsDependingOnUpToDate(index))
        if textName.get_rect().width <= (width - (width / 20)):
            textNameFitting = True
        else:
            length -= 1

    textPriceToday = fontData.render(str(round(index.getRegularMarketPrice(),2)), True, contentColor)
    textPriceTimeToday = fontData.render(time.strftime('%H:%M', time.localtime(index.getRegularMarketTime())), True,
                                         contentColor)
    textPercToday = fontData.render(str(round(index.getPercToday(),2)) + "%", True, getColorForValue(index.getPercToday()))

    center = int(width / 2)

    ypos = int(height / 20) + startPosY
    xpos = center + startPosX

    textRect = textName.get_rect()
    textRect.topleft = (xpos - int(textRect.width / 2), ypos)
    screen.blit(textName, textRect)

    ypos += int(fontFactorHeader + 2)
    xpos = center + startPosX

    textRect = textPriceToday.get_rect()
    textRect.topleft = (xpos - int(textRect.width / 2), ypos)
    screen.blit(textPriceToday, textRect)

    ypos += int(fontFactorHeader + 2)
    xpos = center + startPosX

    textRect = textPercToday.get_rect()
    textRect.topleft = (xpos - int(textRect.width / 2), ypos)
    screen.blit(textPercToday, textRect)

    ypos += int(fontFactorHeader + 2)

    textRect = textPriceTimeToday.get_rect()
    textRect.topleft = (xpos - int(textRect.width / 2), ypos)
    screen.blit(textPriceTimeToday, textRect)

    pygame.display.flip()

def tileView():
    global running

    screen.fill(bgColor)

    length = len(portfolio.getAssetList())
    count = 0
    tiles = colCountTiles * rowCountTiles

    assetList = portfolio.getAssetList()

    xDelta = int(xResolution / colCountTiles)
    yDelta = int(yResolution / rowCountTiles)
    row = 0
    col = 0
    x = 0
    y = 0

    for asset in assetList:

        x = col * xDelta
        y = row * yDelta
        if row == 0:
            y += 15
        displayTile(x,y,asset)
        count += 1
        length -= 1
        col += 1

        if col == colCountTiles:
            col = 0
            row += 1

        if row == rowCountTiles:
            col = 0
            row = 0

        if count >= tiles or length == 0:
            if length >= tiles:
                waitInputOrTimeout(displayTimeList)
                count = 0
                screen.fill(bgColor)
                if running == False:
                    break
            else:
                waitInputOrTimeout(displayTimeList)
                count = 0
                screen.fill(bgColor)
                #Fill the screen with old values
                if length > 0:
                    for asset in assetList[-tiles:-length]:
                        x = col * xDelta
                        y = row * yDelta
                        displayTile(x, y, asset)
                        count += 1
                        col += 1

                        if col == colCountTiles:
                            col = 0
                            row += 1

                        pygame.display.flip()
                if running == False:
                    break

def tileViewIndices():
    global running

    screen.fill(bgColor)

    length = len(portfolio.getIndicesList())
    count = 0
    tiles = 9

    indicesList = portfolio.getIndicesList()

    xDelta = int(xResolution / 3)
    yDelta = int(yResolution / 3)
    row = 0
    col = 0
    x = 0
    y = 0

    for index in indicesList:

        x = col * xDelta
        y = row * yDelta
        if row == 0:
            y += 15
        displayTileIndex(x, y, index)
        count += 1
        length -= 1
        col += 1

        if col == 3:
            col = 0
            row += 1

        if row == 3:
            col = 0
            row = 0

        if count >= tiles or length == 0:
            if length >= tiles:
                waitInputOrTimeout(displayTimeList)
                count = 0
                screen.fill(bgColor)
                if running == False:
                    break
            else:
                waitInputOrTimeout(displayTimeList)
                count = 0
                screen.fill(bgColor)
                # Fill the screen with old values
                if length > 0:
                    for index in indicesList[-tiles:-length]:
                        x = col * xDelta
                        y = row * yDelta
                        displayTileIndex(x, y, index)
                        count += 1
                        col += 1

                        if col == 3:
                            col = 0
                            row += 1

                        pygame.display.flip()
                if running == False:
                    break

def displayTotalHead():
    screen.fill(bgColor)

    tableX1 = int(xResolution / 3.5)
    tableX2 = int(xResolution - tableX1)

    ypos = int(yResolution / 20)

    center = int(xResolution / 2)

    fontFactorHeader = int(yResolution / 8)
    fontFactorData = int(yResolution / 15)
    fontHeader = pygame.font.SysFont('Arial', fontFactorHeader)
    fontData = pygame.font.SysFont('Arial', fontFactorData)

    textHeader = fontHeader.render("Total Portfolio", True, headerColor)
    textRect = textHeader.get_rect()

    textRect.topleft = (int(center - textRect.width / 2), int(yResolution / 20))
    screen.blit(textHeader, textRect)

    ypos += fontFactorHeader + 20

    textRegularMarketPrice = fontHeader.render(str(round(portfolio.getPortfolioRegularMarketPrice(), 2)), True,
                                             contentColor)
    textPercToday = fontData.render(str(round(portfolio.getPortfolioPercToday(), 2)) + "%", True,
                                    getColorForValue(portfolio.getPortfolioPercToday()))
    textProfitToday = fontData.render(str(round(portfolio.getPortfolioProfitToday(), 2)), True,
                                    getColorForValue(portfolio.getPortfolioProfitToday()))
    textProfit = fontData.render(str(round(portfolio.getPortfolioProfit(), 2)), True,
                                 getColorForValue(portfolio.getPortfolioProfit()))
    textProfitPerc = fontData.render(str(round(portfolio.getPortfolioProfitPerc(), 2)) + "%", True,
                                     getColorForValue(portfolio.getPortfolioProfitPerc()))

    textRect = textProfitToday.get_rect()
    textRect.topleft = (tableX1, ypos)
    screen.blit(textProfitToday, textRect)

    textRect = textPercToday.get_rect()
    textRect.topright = (tableX2, ypos)
    screen.blit(textPercToday, textRect)

    ypos += fontFactorData + 8

    textRect = textProfit.get_rect()
    textRect.topleft = (tableX1, ypos)
    screen.blit(textProfit, textRect)

    textRect = textProfitPerc.get_rect()
    textRect.topright = (tableX2, ypos)
    screen.blit(textProfitPerc, textRect)

    ypos += fontFactorData + 20

    textRect = textRegularMarketPrice.get_rect()
    textRect.topleft = (int(xResolution / 2 - textRect.width / 2), ypos)
    screen.blit(textRegularMarketPrice, textRect)

def singleTotalScreen():
    global running
    displayTotalHead()

    assetList = portfolio.getAssetList()
    length = len(assetList)
    assetList.sort(key=lambda x: x.getCurrentAssetValue(), reverse=True)

    count = 0
    tiles = 15

    xDelta = int(xResolution / 5)
    yDelta = int(yResolution / 2 / 3)
    row = 0
    col = 0
    x = 0
    y = 0

    for asset in assetList:
        x = col * xDelta
        y = int(row * yDelta + yResolution / 2)
        x += int((xResolution / 5 - xResolution / 6)/2)
        if row == 0:
            y += 15
        displayTile(x, y, asset)
        count += 1
        length -= 1
        col += 1

        if col == 5:
            col = 0
            row += 1

        if row == 3:
            col = 0
            row = 0

        if count >= tiles or length == 0:
            if length >= tiles:
                waitInputOrTimeout(displayTimeList)
                count = 0
                screen.fill(bgColor)
                displayTotalHead()
                if running == False:
                    break
            else:
                waitInputOrTimeout(displayTimeList)
                count = 0
                # Fill the screen with old values
                if length > 0 and running == True:
                    screen.fill(bgColor)
                    displayTotalHead()
                    for asset in assetList[-tiles:-length]:
                        x = col * xDelta
                        y = int(row * yDelta + yResolution / 2)
                        x += int((xResolution / 5 - xResolution / 6)/2)
                        if row == 0:
                            y += 15
                        displayTile(x, y, asset)
                        count += 1
                        col += 1

                        if col == 5:
                            col = 0
                            row += 1

                        pygame.display.flip()
                if running == False:
                    break

def singleTotalIndexScreen():
    global running
    displayTotalHead()

    indexList = portfolio.getIndicesList()
    length = len(indexList)

    count = 0
    tiles = 15

    xDelta = int(xResolution / 5)
    yDelta = int(yResolution / 2 / 3)
    row = 0
    col = 0
    x = 0
    y = 0

    for index in indexList:
        x = col * xDelta
        y = int(row * yDelta + yResolution / 2)
        x += int((xResolution / 5 - xResolution / 6)/2)
        if row == 0:
            y += 15
        displayTileIndex(x, y, index)
        count += 1
        length -= 1
        col += 1

        if col == 5:
            col = 0
            row += 1

        if row == 3:
            col = 0
            row = 0

        if count >= tiles or length == 0:
            if length >= tiles:
                waitInputOrTimeout(displayTimeList)
                count = 0
                screen.fill(bgColor)
                displayTotalHead()
                if running == False:
                    break
            else:
                waitInputOrTimeout(displayTimeList)
                count = 0
                # Fill the screen with old values
                if length > 0 and running == True:
                    screen.fill(bgColor)
                    displayTotalHead()
                    for index in indexList[-tiles:-length]:
                        x = col * xDelta
                        y = int(row * yDelta + yResolution / 2)
                        x += int((xResolution / 5 - xResolution / 6)/2)
                        if row == 0:
                            y += 15
                        displayTileIndex(x, y, index)
                        count += 1
                        col += 1

                        if col == 5:
                            col = 0
                            row += 1

                        pygame.display.flip()
                if running == False:
                    break

def main():
    global running, colCountTiles
    running = True

    try:
        opts, args = getopt.getopt(sys.argv[1:], "tsoc:")
    except getopt.GetoptError:
        print('portfoliograph.py -t|-o|-c2|-c3|-s')
        sys.exit(2)

    if len(sys.argv) != 2:
        print('portfoliograph.py -t|-o|-c2|-c3|-s')
        sys.exit(2)

    initializePortfolio()

    for opt, arg in opts:
        if opt == '-s':
            colCountTiles = 5
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        running = False

                if running == False: break
                singleTotalScreen()
                if running == False: break
                singleTotalIndexScreen()
                if running == False: break
                portfolio.updatePortfolio()
                if running == False: break

        elif opt == '-o':
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        running = False

                if running == False: break
                overViewIndicesGraph()
                if running == False: break
                overViewAssetsGraph()
                if running == False: break
                portfolio.updatePortfolio()
                if running == False: break

        elif opt == '-t' or opt == '-c':
            if arg == '2' or arg == '3':
                colCountTiles = int(arg)
            else:
                colCountTiles = 3
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                        running = False

                if running == False: break
                tileViewIndices()
                if running == False: break
                tileView()
                if running == False: break
                portfolio.updatePortfolio()
                if running == False: break

    pygame.quit()
    sys.exit(0)

if __name__ == '__main__':
    main()
