import pandas, os, random
import matplotlib.pyplot as plt
from datetime import datetime
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.cryptocurrencies import CryptoCurrencies

####### Values could be customized ############

CHARTDOMAIN = 'stock'
# ['stock', 'cryptocurrency'] are the other options

REQ_TYPE = random.choice(['intraday', 'daily', 'weekly', 'monthly'])

SYMBOL = random.choice(['MSFT', 'AAPL', 'AMZN', 'GOOGL', 'FB', 'INTC', 'CSCO', 'CMCSA', 'PEP', 'ADBE', 'NVDA', 'NFLX', 'PYPL', 'COST', 'SBUX', 'QCOM', 'INTU', 'TMUS'])
# Stock Symbol

INTERVAL = random.choice([1, 5, 15, 30, 60])

OUTPUTSIZE = 'full'
#['compact', 'full'] are the other options.

PATHTOCHART = './alphavantage'
GRIDVIEW = random.chice([True, False])

PLOT = random.choice(['close', 'open', 'high', 'low'])

COLOR = random.choice(['blue', 'green', 'cyan', 'magenta', 'black', 'orange'])

RENDERLINE = 4
# Line inside Readme at which the chart to be rendered.

################### If CHARTDOMAIN is set to 'cryptocurrency' then edit these below  ####################################

CRYPTOSYMBOL = random.choice(['BTC', 'ETH'])
# Cryptocurrency symbol

CRYPTOMARKET = random.choice(['USD', 'CNY'])

CRYPTOINTERVAL = random.choice(['daily', 'weekly', 'monthly'])

CRYPTOPLOT = random.choice(['close', 'open', 'high', 'low', 'marketcapital'])

#############  Value customization end    #################

API_KEY = os.environ['ALPHA_VANTAGE_KEY']

def setup_request_object(request, symbol, interval):
    if CHARTDOMAIN == 'stock':
        try:
            ts = TimeSeries(API_KEY, output_format='pandas', indexing_type='date')
        except:
            print("Error occurred/ Number of API calls exhausted")
            return [False, False]
        if request == 'intraday': return ['intraday', ts]
        if request == 'daily': return ['daily', ts]
        if request == 'weekly': return ['weekly', ts]
        if request == 'monthly': return ['monthly', ts]
        return [False, False]

    if CHARTDOMAIN == 'cryptocurrency':
        try:
            cc = CryptoCurrencies(key=API_KEY, output_format='pandas')
        except:
            print("Error occurred/ Number of API calls exhausted")
            return [False, False]
        if CRYPTOINTERVAL == 'daily': return ['daily', cc]
        if CRYPTOINTERVAL == 'weekly': return ['weekly', cc]
        if CRYPTOINTERVAL == 'monthly': return ['monthly', cc]
        return [False, False]       

def make_request(type, object):
    if CHARTDOMAIN == 'stock':
        if type == 'intraday':
            interval = str(INTERVAL)+'min'
            return object.get_intraday(symbol=SYMBOL, interval=interval, outputsize=OUTPUTSIZE)
        if type == 'daily':
            return object.get_daily(symbol=SYMBOL)
        if type == 'weekly':
            return object.get_weekly(symbol=SYMBOL)
        if type == 'monthly':
            return object.get_monthly(symbol=SYMBOL)
    if CHARTDOMAIN == 'cryptocurrency':
        if type == 'daily':
            return object.get_digital_currency_daily(symbol=CRYPTOSYMBOL, market=CRYPTOMARKET)
        if type == 'weekly':
            return object.get_digital_currency_weekly(symbol=CRYPTOSYMBOL, market=CRYPTOMARKET)
        if type == 'monthly':
            return object.get_digital_currency_monthly(symbol=CRYPTOSYMBOL, market=CRYPTOMARKET)

def save_chart(values, crypto_market):
    chart_save_path = PATHTOCHART + '/chart.png'
    # Clear previous chart
    if os.path.exists(chart_save_path):
        os.remove(chart_save_path)
        print("Old chart removed")

    #Get Timestamps
    now = datetime.now().strftime("%b %d, %Y(%H:%M:%S)")

    # Set plot dimensions
    fig = plt.figure(num=None, figsize=(12, 8))
    ax  = fig.add_subplot()

    # Save new chart
    if CHARTDOMAIN == 'stock':
        if PLOT == 'open': plot = '1. open'
        if PLOT == 'high': plot = '2. high'
        if PLOT == 'low': plot = '3. low'
        if PLOT == 'close': plot = '4. close'
        ax.set_title(
            "Latest Data -> OPEN : {} | HIGH : {} | LOW : {} | CLOSE : {} \n\n {} {} value chart of {} - Last updated at {}"
            .format(values['1. open'][0], values['2. high'][0], values['3. low'][0], values['4. close'][0], REQ_TYPE, PLOT, SYMBOL, now)
            )
        values[plot].plot(color=COLOR)
        plt.ylabel('Price in USD')
        plt.xlabel('TimeFrame')
        if GRIDVIEW: plt.grid()
        plt.savefig(chart_save_path)
        print("Saved new chart")

    if CHARTDOMAIN == 'cryptocurrency':
        if CRYPTOPLOT == 'open'  and crypto_market == 'CNY': plot = '1a. open (CNY)'
        if CRYPTOPLOT == 'open'  and crypto_market == 'USD': plot = '1b. open (USD)'
        if CRYPTOPLOT == 'high'  and crypto_market == 'CNY': plot = '2a. high (CNY)'
        if CRYPTOPLOT == 'high'  and crypto_market == 'USD': plot = '2b. high (USD)'
        if CRYPTOPLOT == 'low'   and crypto_market == 'CNY': plot = '3a. low (CNY)'
        if CRYPTOPLOT == 'low'   and crypto_market == 'USD': plot = '3b. low (USD)'
        if CRYPTOPLOT == 'close' and crypto_market == 'CNY': plot = '4a. close (CNY)'
        if CRYPTOPLOT == 'close' and crypto_market == 'USD': plot = '4b. close (USD)'
        if CRYPTOPLOT == 'marketcapital':
            plot = '6. market cap (USD)'
            crypto_market = 'USD'
        if crypto_market == 'CNY':    
            ax.set_title(
                "Latest Data({} market) -> OPEN : {} | HIGH : {} | LOW : {} | CLOSE : {} \n\n {} {} value chart of {} - Last updated at {}"
                .format(crypto_market, values['1a. open (CNY)'][0], values['2a. high (CNY)'][0], values['3a. low (CNY)'][0], values['4a. close (CNY)'][0], CRYPTOINTERVAL, CRYPTOPLOT, CRYPTOSYMBOL, now)
                )
        if crypto_market == 'USD':    
            ax.set_title(
                "Latest Data({} market) -> OPEN : {} | HIGH : {} | LOW : {} | CLOSE : {} \n\n {} {} value chart of {} - Last updated at {}"
                .format(crypto_market, values['1b. open (USD)'][0], values['2b. high (USD)'][0], values['3b. low (USD)'][0], values['4b. close (USD)'][0], CRYPTOINTERVAL, CRYPTOPLOT, CRYPTOSYMBOL, now)
                )                
        values[plot].plot(color=COLOR)
        plt.ylabel('Price')
        plt.xlabel('TimeFrame')
        if GRIDVIEW: plt.grid()
        plt.savefig(chart_save_path)
        print("Saved new chart")    

def rewrite_readme():
    alt_text = 'AlphaVantage-Action-Bot-Chart'
    now = datetime.now().strftime("%b %d, %Y(%H:%M:%S)")
    promote_text = "**Realtime Stock/Crytpocurrency Chart📈  Rendered By [AlphaVantage-Action-Bot](https://github.com/manojnaidu619/AlphaVantage-Action-Bot) | Last updated the above chart on {} **".format(now)
    code_line = f'![{alt_text}]({PATHTOCHART}/chart.png)'
    readme = './README.md'
    line = RENDERLINE-1
    parsed_data = []

    def insert_string(array, pos, data):
        array.insert(pos, "{} \n".format(data))
        array.insert(pos + 1, "{} \n".format(promote_text))

    with open(readme, 'r') as file: data = file.readlines()
    for index, x in enumerate(data):
        to_remove = False
        if x.startswith("![{}]".format(alt_text)): to_remove = True
        if x.startswith('**Realtime Stock/Crytpocurrency Chart'): to_remove = True
        if not to_remove: parsed_data.append(x)    
    data = parsed_data        
    insert_string(data, line, code_line)    
    with open(readme, 'w') as file: file.writelines( data )
        

# Driver Code
request_type, request_object = setup_request_object(REQ_TYPE, SYMBOL, INTERVAL)
if (request_type != False and request_object != False):
    values, columns = make_request(request_type, request_object)
    save_chart(values, CRYPTOMARKET)
    rewrite_readme()

    
