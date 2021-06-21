# stock_treemap 
Want to make a cool stock diagram, like those on finviz: https://finviz.com/map.ashx ? 

This library generates tree maps for stock portfolios using Python, Yahoo Finance, and Plotly. This code
is meant to be run within a Jupyter environment. More details of requirements are further below.

You will need to create a CSV file that has 2 columns: ticker and stocks. The ticker
column should contain the stock ticker symbols for each stock you own. The shares
column should contain the number of shares that you own. An example is shown below:

```
ticker,shares
aapl,20
amd,20
amzn,2
gbtc,40
```

If this file is called 'example.csv', then you can create a tree map as follows:

```
from stock_treemap import stock_treemap, update_sectors
stock_treemap('example.csv')
```

A static example of the output is shown below:
![Example tree map created by stock_treemap()](https://raw.githubusercontent.com/jmshea/stock_treemap/main/example.png)

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
