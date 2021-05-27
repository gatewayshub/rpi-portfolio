#!/usr/bin/python

import os
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

pygame.display.init()
pygame.font.init()
xResolution = 420
yResolution = 320
tableX1 = int(xResolution / 20)
tableX2 = int(xResolution / 1.6)
bgColor = (0,0,0)
headerColor = (255,225,1)
contentColor = (235, 235, 235)
redColor = (200, 0, 0)
greenColor = (0, 200, 0)
nameCut = 16
screen = pygame.display.set_mode([xResolution,yResolution])
#screen = pygame.display.set_mode([xResolution,yResolution],pygame.FULLSCREEN)

portfolio = Portfolio()

os.system('clear')
write("\033[?25l")
flush()


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

        dt = clock.tick(30) / 1000

        seconds -= dt

        if seconds <= 0:
            done = True

def displayHeader(leftHeader, rightHeader):
    fontHeaderLeft = pygame.font.SysFont('Times New Roman', int(yResolution / 10))
    textHeaderLeft = fontHeaderLeft.render(leftHeader, True, headerColor)
    screen.blit(textHeaderLeft, (tableX1, int(yResolution / 20)))

    fontHeaderRight = pygame.font.SysFont('Times New Roman', int(yResolution / 10))
    textHeaderRight = fontHeaderRight.render(rightHeader, True, headerColor)
    screen.blit(textHeaderRight, (tableX2, int(yResolution / 20)))

def getColorForValue(value):
    if (value > 0):
        return greenColor
    elif (value < 0):
        return redColor
    else:
        return contentColor

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

        fontName = pygame.font.SysFont('Times New Roman', int(yResolution / 10))
        textName = fontName.render(name[0:nameCut], True, contentColor)
        screen.blit(textName, (tableX1, ypos))

        fontName = pygame.font.SysFont('Times New Roman', int(yResolution / 10))
        textName = fontName.render(str(round(percToday, 3)), True, getColorForValue(percToday))
        screen.blit(textName, (tableX2, ypos))

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

                    fontName = pygame.font.SysFont('Times New Roman', int(yResolution / 10))
                    textName = fontName.render(name[0:nameCut], True, contentColor)
                    screen.blit(textName, (tableX1, ypos))

                    fontName = pygame.font.SysFont('Times New Roman', int(yResolution / 10))
                    textName = fontName.render(str(round(percToday, 3)), True, getColorForValue(percToday))
                    screen.blit(textName, (tableX2, ypos))

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

        fontName = pygame.font.SysFont('Times New Roman', int(yResolution / 10))
        textName = fontName.render(name[0:nameCut], True, contentColor)
        screen.blit(textName, (tableX1, ypos))

        fontName = pygame.font.SysFont('Times New Roman', int(yResolution / 10))
        textName = fontName.render(str(round(percToday,3)), True, getColorForValue(percToday))
        screen.blit(textName, (tableX2, ypos))

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

                    fontName = pygame.font.SysFont('Times New Roman', int(yResolution / 10))
                    textName = fontName.render(name[0:nameCut], True, contentColor)
                    screen.blit(textName, (tableX1, ypos))

                    fontName = pygame.font.SysFont('Times New Roman', int(yResolution / 10))
                    textName = fontName.render(str(round(percToday, 3)), True, getColorForValue(percToday))
                    screen.blit(textName, (tableX2, ypos))

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


def main():
    global running
    running = True

    initializePortfolio()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        overViewIndicesGraph()
        if running == False: break
        overViewAssetsGraph()
        if running == False: break
        portfolio.updatePortfolio()
        if running == False: break


    pygame.quit()
    sys.exit(0)

if __name__ == '__main__':
    main()