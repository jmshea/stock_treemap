'''Module to create custom, interactive stock portfolio tree maps. Pulls data from Yahoo! Finance.
Uses Plotly to create interactive treemaps. Intended for running within Jupyter Lab (or Notebook).

Main function is stock_treemap, which takes a CSV argument and optional dictionary mapping
stock tickers to sectors (strings).

Also provided separate function to replot if sectors are updated (without having to wait
for data to be pulled from Yahoo Finance, which can be quite slow). '''
__version__ = '1.6'

import yfinance as yf
from tqdm import tqdm
import numpy as np
import pandas as pd
import plotly.express as px

def plot_df( df, cash_balance, interactive, html_file):
        '''Not intended to be called directly.  See stock_treemap or update_sectors() instead.
        '''

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




        df['stock']=df.index.str.upper() + '<br>' + df['percent change (day)'].astype(str) + '%'
        for stock in df.index:
        #print(stock, df.loc[stock, "market value"])
            if df.loc[stock, "market value"] >1000:
                df.loc[stock, "stock+price"]="<b>" + stock.upper() + "</b>" \
                + "<br>Price: $" + "{:.2f}".format(df.loc[stock, 'price']) \
                + "<br>Value: $"+"{:.1f}".format(df.loc[stock, "market value"]/1000)+"k"
            else:
                df.loc[stock, "stock+price"]="<b>" + stock.upper()  + "</b>" \
                + "<br>Price: $" + "{:.2f}".format(df.loc[stock, 'price']) \
                + "<br>Value: $"+"{:.0f}".format(df.loc[stock, "market value"])




        fig = px.treemap(df,
                         path=['sector','stock'], 
                         values='market value',
                         color='percent change (day)',
                         color_continuous_scale='RdYlGn',
                         color_continuous_midpoint=0,
                         title=my_title,
                         custom_data=['stock+price']#,
                         #hover_data={'percent change (day)':':.2f'}
                        )

        # Update customdata for Sectors to show percent change of sector
        for i, data in enumerate(fig.data[0]['customdata']):
            if data[0].find("?")>0:
                fig.data[0]['customdata'][i][0]="{:.1f}%".format(fig.data[0]['customdata'][i][1])

        fig.update_traces(hovertemplate='%{customdata[0]}')


        if interactive:
            fig.show()
        if html_file != '':
            fig.write_html(html_file, include_plotlyjs='cdn')




def stock_treemap( csv_file, sectors={}, cash_balance=0, interactive=True, html_file='' ):
        '''
        Pull financial data for stocks from Yahoo finance and generate a treemap
        to illustrate performance by sectors

        Inputs:
        csv_file = a CSV file with columns ticker (standard stock ticker symbol) and shares (number of shares owned)
        sectors (optional)= a dictionary that maps ticker symbols to sectors, both of which are strings
        cash_balance (optional) = amount not in stocks that will be added to give whole portfolio balance
        interactive (optional) = whether to display the interactive graph (presumably in a Jupyter environment).
                                 Default is True
        html_file (optional) = if a non-empty string is provided, the rendered graph will be saved as the
                               specified name

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

        plot_df( df, cash_balance, interactive, html_file)

        return df



def update_sectors(df, sectors, cash_balance=0, interactive=True, html_file='' ):

    '''
    use on dataframe created by stock_treemap to update sectors for stocks and replot the treemap.
    does not pull any financial data from online.

    inputs:
    df = a pandas dataframe created by stock_treemap (or containing all the same columns)
    sectors = a dictionary that maps ticker symbols to sectors, both of which are strings
    cash_balance (optional) = amount not in stocks that will be added to give whole portfolio balance
    interactive (optional) = whether to display the interactive graph (presumably in a Jupyter environment).
                             Default is True
    html_file (optional) = if a non-empty string is provided, the rendered graph will be saved as the
                           specified name


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


    plot_df( df, cash_balance, interactive, html_file)

    return df
