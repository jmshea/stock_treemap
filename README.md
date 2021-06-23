# stock_treemap 
Want to make a cool stock diagram, like those on finviz: https://finviz.com/map.ashx , but
for your own portfolio? 

This library generates tree maps for stock portfolios using Python, Yahoo Finance, and Plotly. This code
is designed to be run within a Jupyter environment or can be used to create an html file of the 
resulting plot. More details of requirements are further below.

You will need to create a CSV file that has 2 columns: ticker and stocks. The ticker
column should contain the stock ticker symbols for each stock you own. The shares
column should contain the number of shares that you own. An example is shown below:

```
ticker,shares
aapl,20
amd,10
amzn,2
googl,1
ethe,30
gbtc,4
```

If this file is called 'example.csv', then you can create a tree map as follows:

```
from stock_treemap import stock_treemap, update_sectors
stock_treemap('example.csv')
```

An animated GIF showing an example of the output is below:
![Example tree map created by stock_treemap()](https://raw.githubusercontent.com/jmshea/stock_treemap/main/example.gif)

For more advanced options, see the function help (although it is still in progress with recent updates
to provide saving to HTML.)

Requirements
---
Requires
* yfinance
* tqdm
* numpy
* pandas
* plotly
  * Note that Plotly requires plug-ins to work properly in Jupyter environments.
See https://plotly.com/python/getting-started/

If you find this useful... 
 <a href="https://www.buymeacoffee.com/jshea" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
