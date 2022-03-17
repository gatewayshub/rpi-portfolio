import PySimpleGUI as sg
from xml.dom import minidom
import os

config = minidom.parse('config.xml')

# For reading and maniplating xml
items = config.getElementsByTagName('item')
indices = config.getElementsByTagName('index')
settings = config.getElementsByTagName('settings')[0].childNodes

# For displaying data nodes in listboxes
tickerNodeList = []
indexNodeList = []
settingsNodeList = []

def refreshListBoxes(window):
    #Refresh both listboxes with new list values
    refreshNodeLists()
    window['indexBox'].update(indexNodeList)
    window['assetBox'].update(tickerNodeList)

def deleteIndexButtonPressed(window, values):

    for index in indices:
        name = index.getAttribute("name")
        if name == values['indexBox'][0]:
            parentNode = index.parentNode
            parentNode.removeChild(index)

    refreshListBoxes(window)
    window['-indexName-'].update("")
    window['-indexTicker-'].update("")

def deleteAssetButtonPressed(window, values):

    for item in items:
        name = item.getAttribute("name")
        if name == values['assetBox'][0]:
            parentNode = item.parentNode
            parentNode.removeChild(item)

    refreshListBoxes(window)
    window['-Name-'].update("")
    window['-Ticker-'].update("")
    window['-averagePrice-'].update("")
    window['-shareCount-'].update("")

def addAssetButtonPressed(window, values):

    newAsset = config.createElement("item")
    newAsset.setAttribute("name", "e.g. NEL")

    nodes = ['ticker','averagePrice','shareCount']
    for node in nodes:
        newNode = config.createElement(node)
        newTextNode = config.createTextNode("0")
        newNode.appendChild(newTextNode)
        newAsset.appendChild(newNode)


    itemsNode = config.getElementsByTagName('assets')
    itemsNode[0].appendChild(newAsset)

    refreshListBoxes(window)

    window['-Name-'].update("e.g. NEL")
    window['-Ticker-'].update("e.g. D7G.F")
    window['-averagePrice-'].update("e.g. 1.20")
    window['-shareCount-'].update("e.g. 300")

def addIndexButtonPressed(window,values):
    global config

    newIndex = config.createElement("index")
    newIndex.setAttribute("name", "e.g. DAX")

    nodes = ['ticker']
    for node in nodes:
        newNode = config.createElement(node)
        newTextNode = config.createTextNode("e.g. ^DAXI")
        newNode.appendChild(newTextNode)
        newIndex.appendChild(newNode)

    itemsNode = config.getElementsByTagName('indices')
    itemsNode[0].appendChild(newIndex)

    refreshListBoxes(window)

    window['-indexName-'].update("DAX")
    window['-indexTicker-'].update("^DAXI")

def updateIndexButtonPressed(window, values):
    for index in indices:
        name = index.getAttribute("name")
        if name == values['indexBox'][0]:
            nameValue = values['-indexName-']
            index.setAttribute("name", nameValue)

            tickerNode = index.getElementsByTagName('ticker')
            tickerNode[0].firstChild.replaceWholeText(values['-indexTicker-'])

            refreshListBoxes(window)

def updateAssetButtonPressed(window, values):
    for item in items:
        name = item.getAttribute("name")
        if name == values['assetBox'][0]:
            nameValue = values['-Name-']
            item.setAttribute("name", nameValue)

            tickerNode = item.getElementsByTagName('ticker')
            tickerNode[0].firstChild.replaceWholeText(values['-Ticker-'])

            averagePriceNode = item.getElementsByTagName('averagePrice')
            averagePriceNode[0].firstChild.replaceWholeText(values['-averagePrice-'])

            shareCountNode = item.getElementsByTagName('shareCount')
            shareCountNode[0].firstChild.replaceWholeText(values['-shareCount-'])

            refreshListBoxes(window)

def updateSettingButtonPressed(window, values):
    for setting in settings:
        #minidom problems with \n creating new node... therefore filter out all textnode which only have \n as values here
        if setting.nodeType == minidom.Node.TEXT_NODE and "\n" in setting.nodeValue:
            pass
        else:
            name = setting.tagName
            if name == values['settingsBox'][0]:
                settingValue = values['-settingValue-']
                setting.firstChild.replaceWholeText(settingValue)

def refreshNodeLists():
    #refreshNodeLists with uptodate data from minidom xml
    global tickerNodeList
    global indexNodeList
    global settingsNodeList
    global items
    global indices
    global settings


    items = config.getElementsByTagName('item')
    indices = config.getElementsByTagName('index')
    settings = config.getElementsByTagName('settings')[0].childNodes


    tickerNodeList.clear()
    indexNodeList.clear()
    settingsNodeList.clear()

    for item in items:
        tickerNode = item.getElementsByTagName('ticker')
        name = item.getAttribute('name')
        tickerNodeList.append(name)

    for index in indices:
        tickerNode = index.getElementsByTagName('ticker')
        name = index.getAttribute('name')
        indexNodeList.append(name)

    for setting in settings:
        #minidom problems with \n creating new node... therefore filter out all textnode which only have \n as values here
        if setting.nodeType == minidom.Node.TEXT_NODE and "\n" in setting.nodeValue:
            pass
        else:
            settingsNodeList.append(setting.tagName)

def updateIndexBoxValues(window, values):
    #Update values inside value box on the right after choosing new entry in the index list box on the left
    for index in indices:
        name = index.getAttribute("name")
        if name == values['indexBox'][0]:
            window['-indexName-'].update(name)
            tickerNode = index.getElementsByTagName('ticker')
            symbol = tickerNode[0].firstChild.data
            window['-indexTicker-'].update(symbol)

def updateAssetBoxValues(window, values):
    # Update values inside value box on the right after choosing new entry in the asset list box
    for item in items:
        name = item.getAttribute("name")
        if name == values['assetBox'][0]:
            window['-Name-'].update(name)
            tickerNode = item.getElementsByTagName('ticker')
            symbol = tickerNode[0].firstChild.data
            window['-Ticker-'].update(symbol)

            averagePriceNode = item.getElementsByTagName('averagePrice')
            averagePrice = float(averagePriceNode[0].firstChild.data)
            window['-averagePrice-'].update(averagePrice)

            shareCountNode = item.getElementsByTagName('shareCount')
            shareCount = float(shareCountNode[0].firstChild.data)
            window['-shareCount-'].update(shareCount)

def updateSettingsBoxValues(window,values):
    # Update values inside value box on the right after choosing new entry in the setting list box
    for setting in settings:
        # minidom problems with \n creating new node... therefore filter out all textnode which only have \n as values here
        if setting.nodeType == minidom.Node.TEXT_NODE and "\n" in setting.nodeValue:
            pass
        else:
            name = setting.tagName
            if name == values['settingsBox'][0]:
                window['-settingName-'].update(name)
                settingValue = setting.childNodes[0].nodeValue
                window['-settingValue-'].update(settingValue)

def saveConfigPressed():
    #Problems with toprettyxml() so we have to save file and read it again to manipulate formatting
    file = open('config_new.xml','w')
    xmlText = config.toprettyxml()
    file.write(xmlText)
    file.close()

    #Save original file
    file = open('config.xml','r')
    origXmlText = ""
    for line in file:
        origXmlText += line
    file_bak = open('config_bak.xml', 'w')
    file_bak.write(origXmlText)
    file_bak.close()
    file.close

    file = open('config_new.xml','r')
    xmlTextFormatted = ""
    for line in file:
        if not line.isspace():
            xmlTextFormatted += line
        else:
            pass
    destFile = open('config.xml', 'w')
    destFile.write(xmlTextFormatted)
    destFile.close()
    file.close()

    os.remove("config_new.xml")

def main():
    global items
    global indices

    refreshNodeLists()

    layout = [
        [
            sg.vtop(
                [sg.Listbox(list(tickerNodeList), key='assetBox', size=(15,10), enable_events=True),
                     sg.Frame('Asset',
                        [
                            [
                                sg.Text('Name', size=(10, 1)),
                                sg.InputText(key='-Name-')
                            ],
                            [
                                sg.Text('Ticker', size=(10, 1)),
                                sg.InputText(key='-Ticker-')
                            ],
                            [
                                sg.Text('averagePrice', size=(10, 1)),
                                sg.InputText(key='-averagePrice-')
                            ],
                            [
                                sg.Text('shareCount', size=(10, 1)),
                                sg.InputText(key='-shareCount-')
                            ]
                        ]
                     )
                ]
            )
        ],
        [
            sg.Button('Update', key='updateAssetButton'),
            sg.Button('Add', key='addAssetButton'),
            sg.Button('Delete', key='deleteAssetButton')
        ],
        [
            sg.Listbox(list(indexNodeList), key='indexBox', size=(15, 10), enable_events=True),
            sg.Frame('Asset',
                     [
                         [
                             sg.Text('Name', size=(10, 1)),
                             sg.InputText(key='-indexName-')
                         ],
                         [
                             sg.Text('Ticker', size=(10, 1)),
                             sg.InputText(key='-indexTicker-')
                         ],
                     ]
                     )
        ],
        [
            sg.Button('Update', key='updateIndexButton'),
            sg.Button('Add', key='addIndexButton'),
            sg.Button('Delete', key='deleteIndexButton')
        ],
        [
            sg.Listbox(list(settingsNodeList), key='settingsBox', size=(15, 10), enable_events=True),
            sg.Frame('Settings',
                     [
                         [
                             sg.Text('Name', size=(10, 1)),
                             sg.InputText(key='-settingName-')
                         ],
                         [
                             sg.Text('Value', size=(10, 1)),
                             sg.InputText(key='-settingValue-')
                         ],
                     ]
                     )
        ],
        [
            sg.Button('Update', key='updateSettingButton'),
        ],
        [
            sg.Button('Save Config', key='saveConfigButton', button_color='red')
        ]

    ]

    window = sg.Window("rpi-portfolio-config", layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        if event == 'assetBox':
            updateAssetBoxValues(window,values)
        if event == 'indexBox':
            updateIndexBoxValues(window,values)
        if event == 'settingsBox':
            updateSettingsBoxValues(window,values)
        if event == 'updateAssetButton':
            try:
                updateAssetButtonPressed(window, values)
            except IndexError:
                sg.Window("No asset selected!", [[sg.Text('No asset selected!'),
                                                  sg.Button('OK')]]).read(close=True)
        if event == 'updateIndexButton':
            try:
                updateIndexButtonPressed(window, values)
            except IndexError:
                sg.Window("No index selected!", [[sg.Text('No index selected!'),
                                                  sg.Button('OK')]]).read(close=True)
        if event == 'updateSettingButton':
            try:
                updateSettingButtonPressed(window, values)
            except IndexError:
                sg.Window("No index selected!", [[sg.Text('No setting selected!'),
                                                  sg.Button('OK')]]).read(close=True)
        if event == 'addAssetButton':
            addAssetButtonPressed(window, values)
        if event == 'addIndexButton':
            addIndexButtonPressed(window,values)
        if event == 'deleteAssetButton':
            try:
                deleteAssetButtonPressed(window, values)
            except IndexError:
                sg.Window("No asset selected!", [[sg.Text('No asset selected!'),
                                                  sg.Button('OK')]]).read(close=True)
        if event == 'deleteIndexButton':
            try:
                deleteIndexButtonPressed(window, values)
            except IndexError:
                sg.Window("No index selected!", [[sg.Text('No index selected!'),
                                                  sg.Button('OK')]]).read(close=True)

        if event == 'saveConfigButton':
            saveConfigPressed()

if __name__ == '__main__':
    main()

