import pandas as pd
import math
import json
import os.path
import time
from helpers.project_paths import creds_path, historicals_path
from binance.client import Client
from datetime import timedelta, datetime
from dateutil import parser
 

binance_creds = json.load(open(os.path.join(creds_path, 'binance_credentials.json')))
binance_api_key = binance_creds["binance_api_key"]
binance_api_secret = binance_creds["binance_api_secret"]

### CONSTANTS
binsizes = {"1m": 1, "5m": 5, "1h": 60, "1d": 1440}
batch_size = 750
binance_client = Client(api_key=binance_api_key, api_secret=binance_api_secret)


### FUNCTIONS
def minutes_of_new_data(crypto, kline_size, data):
    if len(data) > 0:
        old = parser.parse(data["timestamp"].iloc[-1])
    else:
        old = datetime.strptime('1 Jan 2017', '%d %b %Y')
    new = pd.to_datetime(binance_client.get_klines(symbol=crypto, interval=kline_size)[-1][0], unit='ms')
    return old, new

# Can be used like so: data = get_historical_data(crypto="BTCUSD", kline_size="5m", save = True)
def get_historical_data(crypto, kline_size, save = True):
    # Gets cached data
    filename = '%s-%s-data.csv' % (crypto, kline_size)
    file_path = os.path.join(historicals_path, filename)
    if os.path.isfile(file_path):
        data_df = pd.read_csv(file_path)
    else:
        data_df = pd.DataFrame()

    # Gets date of latest cached data
    oldest_point, newest_point = minutes_of_new_data(crypto, kline_size, data_df)
    delta_min = (newest_point - oldest_point).total_seconds()/60
    available_data = math.ceil(delta_min/binsizes[kline_size])

    if delta_min > 0:
        if oldest_point == datetime.strptime('1 Jan 2017', '%d %b %Y'):
            print('Downloading all available %s data for %s. Be patient..!' % (kline_size, crypto))
        else:
            print('Downloading %d minutes of new data available for %s, i.e. %d instances of %s data.' % (delta_min, crypto, available_data, kline_size))

        # Downloads newest data since cached data
        klines = binance_client.get_historical_klines(crypto, kline_size, oldest_point.strftime("%d %b %Y %H:%M:%S"), newest_point.strftime("%d %b %Y %H:%M:%S"))
        data = pd.DataFrame(klines, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
        data['timestamp'] = pd.to_datetime(data['timestamp'], unit='ms')

        # Appends freshly downloaded data to cached data
        if len(data_df) > 0:
            temp_df = pd.DataFrame(data)
            data_df = data_df.append(temp_df)
        else:
            data_df = data
        data_df.set_index('timestamp', inplace=True)
        # Caches all data
        if save: data_df.to_csv(file_path)
        print('Cached {}!'.format(filename))
    else:
        print('Cache already up to date for %s' % crypto)
    
    return data_df