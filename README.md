# rpi-portfolio

Script for fetching different share prices and share index prices into different table layouts in shell and with pygame graphic.
Data is fetched from yahoo finance so every ticker from there will work in config.xml.
Because this script uses yahoo finance tickers please have a look at the terms of use.

Multicurrency is not supported by now... keep only tickers with the same currency in config!

portfoliograph.py  -> pygame is used to output to screen  
shellportfolio.py -> prettytable is used to generate the table outputs  
Both use requests module to fetch data from yahoo webservice.  
portfolio_config.py -> pysimplegui is used for this interface  
  -> install it with "pip3 install pySimpleGUI" on command line

Make sure all used modules are installed before using this scripts.

Headercolors:
- Yellow - everything is ok
- Gray - values not from today
- Red - problem with webservice call... ticker not up-to-date

Some examples:

./portfoliograph.py -s

![portfolio_total](https://user-images.githubusercontent.com/80522869/120933513-cdb13b00-c6fa-11eb-804a-9d45a620dfcf.jpg)

./portfoliograph.py -t

![portfoliograph_t](https://user-images.githubusercontent.com/80522869/120079610-f6ab4d80-c0b4-11eb-9776-090a8967f78c.JPG)

./portfoliograph.py -o

![portfoliograph](https://user-images.githubusercontent.com/80522869/119879741-d4d28f00-bf2b-11eb-9af2-3db6342321f5.jpg)

./shellportfolio.py [option]

option -l:

![shellportfolio_1](https://user-images.githubusercontent.com/80522869/118538929-1b1b3780-b74f-11eb-91bb-e71be624e1e3.JPG)

option -s:

![shellportfoliosoption](https://user-images.githubusercontent.com/80522869/118376548-e1202900-b5c8-11eb-80d5-42a30d257069.jpg)

option -o:

![shellportfolioooption](https://user-images.githubusercontent.com/80522869/118376560-f432f900-b5c8-11eb-84b1-af035a64a548.jpg)

option -s and -o fetches also the indices:

![shellportfolioindex](https://user-images.githubusercontent.com/80522869/118376637-7fac8a00-b5c9-11eb-84d9-8f29f0dde1b6.jpg)

I also use option -s and -o for displaying share prices on a Raspberry Pi with a small 3,5" display :)
