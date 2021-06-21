'''Module to create custom, interactive stock portfolio tree maps. Pulls data from Yahoo! Finance.
Uses Plotly to create interactive treemaps. Intended for running within Jupyter Lab (or Notebook).

Main function is stock_treemap, which takes a CSV argument and optional dictionary mapping
stock tickers to sectors (strings).

Also provided separate function to replot if sectors are updated (without having to wait
for data to be pulled from Yahoo Finance, which can be quite slow). '''
__version__ = '1.3'

import yfinance as yf
from tqdm import tqdm
import numpy as np
import pandas as pd
import plotly.express as px


def stock_treemap( csv_file, sectors={}, cash_balance=0 ):
        '''
        Pull financial data for stocks from Yahoo finance and generate a treemap
        to illustrate performance by sectors

        Inputs:
        csv_file = a CSV file with columns ticker (standard stock ticker symbol) and shares (number of shares owned)
        sectors (optional)= a dictionary that maps ticker symbols to sectors, both of which are strings
        cash_balance (optional) = amount not in stocks that will be added to give whole portfolio balance

        Returns:
        df = a Pandas dataframe with the stock price, last price, market value, day's value change by stock,
        and % change from previous day

        Outputs:

        Shows an interactive graph using plotly. Meant to be run in Jupyter Lab and requires appropriate
        Jupyter Lab plug ins. See: https://plotly.com/python/getting-started/
        '''
        df=pd.read_csv(csv_file)
        
        # Set index and add the columns we will need
        df.set_index('ticker', inplace=True)
        df['price']=0
        df['previous close']=0
        df['market value']=0
        df['change (day)']=0
        df['percent change (day)']=0
        df['sector']=''
        
        
        # Now pull in the stock data from Yahoo! Finance:
        with tqdm(total=len(df)) as pbar:
            for ticker,row  in df.iterrows():
                stock=yf.Ticker(ticker)
                #print(ticker," ", end="")
                info=stock.info
                df.loc[ticker, 'price']=info['regularMarketPrice']
                df.loc[ticker, 'previous close']=info['previousClose']
                if ticker in sectors:
                    df.loc[ticker, 'sector']=sectors[ticker]
                    #print(stock_sectors[ticker])
                elif 'sector' in info:
                    df.loc[ticker, 'sector']=info['sector']
                    #print(info['sector'])
                else:
                    print("No sector info for", ticker)
                    print("You may want to add that to your stock_sectors dict")
                    df.loc[ticker, 'sector']='Misc'
                pbar.update()
        df['market value']=df['price']*df['shares']

        df['change (day)'] = (df['price']-df['previous close'])*df['shares']

        df['percent change (day)'] = np.round((df['price']-df['previous close'])/df['previous close']*100,2)

        if cash_balance > 0:
                title_start="Porfolio value: &#36;"
        else:
                title_start="Stocks value: &#36;"


        total_value=df['market value'].sum() + cash_balance
        if total_value<100_000:
                my_title=title_start + str(int(np.round(total_value))) + ", Today's change: &#36;" \
                        + str(int(np.round(df['change (day)'].sum())))
        else:
                my_title=title_start + str(int(np.round(total_value/1000))) +'k' + ", Today's change: &#36;" \
                        + str(int(np.round(df['change (day)'].sum())))




        fig = px.treemap(df, 
                         path=['sector',df.index], 
                         values='market value',
                         color='percent change (day)',
                        color_continuous_scale='RdBu',
                         color_continuous_midpoint=0,
                         title=my_title,
                         hover_data={'percent change (day)':':.2f'}

                        )
        fig.show()


        return df



def update_sectors(df, sectors, cash_balance=0 ):

    '''
    use on dataframe created by stock_treemap to update sectors for stocks and replot the treemap.
    does not pull any financial data from online.

    inputs:
    df = a pandas dataframe created by stock_treemap (or containing all the same columns)
    sectors = a dictionary that maps ticker symbols to sectors, both of which are strings
    cash_balance (optional) = amount not in stocks that will be added to give whole portfolio balance

    returns:
    df = a pandas dataframe with the stock price, last price, market value, day's value change by stock,
    and % change from previous day

    outputs:

    shows an interactive graph using plotly. meant to be run in jupyter lab and requires appropriate
    jupyter lab plug ins. see: https://plotly.com/python/getting-started/

    '''

    for ticker,row  in df.iterrows():
        if ticker in sectors:
            df.loc[ticker, 'sector']=sectors[ticker]

    if cash_balance > 0:
        title_start="Porfolio value: &#36;"
    else:
        title_start="Stocks value: &#36;"


    total_value=df['market value'].sum() + cash_balance
    if total_value<100_000:
        my_title=title_start + str(int(np.round(total_value))) + ", Today's change: &#36;" \
                + str(int(np.round(df['change (day)'].sum())))
    else:
        my_title=title_start + str(int(np.round(total_value/1000))) +'k' + ", Today's change: &#36;" \
                + str(int(np.round(df['change (day)'].sum())))



    fig = px.treemap(df, 
                     path=['sector',df.index], 
                     values='market value',
                     color='percent change (day)',
                    color_continuous_scale='RdBu',
                     color_continuous_midpoint=0,
                     title=my_title,
                     hover_data={'percent change (day)':':.2f'}
                    )

    fig.show()

    return df
