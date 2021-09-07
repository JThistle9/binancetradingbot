from helpers.trading_bot_helpers import getPricePerUnit, getProfitPercent
from helpers.historical_data import get_historical_data
from datetime import timedelta, datetime
import pandas as pd

class AvgStrategy():

    def __init__(self, config=None, interval='5m', window=30):
        print("Loading AvgStrategy...")
        if config:
            self.sellPercent = float(config.get('sellPercent'))
            self.buyPercent = float(config.get('buyPercent'))
        else:
            self.sellPercent = 0.02
            self.buyPercent = 0.02
        self.interval = interval
        self.window = window

    def getAvgPrice(self, crypto):
        data = get_historical_data(crypto, self.interval, save = True)
        window_start = datetime.now() - timedelta(days=self.window)
        avg = data[(pd.to_datetime(data['timestamp']) > window_start)]['close'].mean()
        print('{}AvgPrice since {} for {} = {}'.format(self.interval, window_start, crypto, avg))
        return float(avg)

    def descriptionOfBuyStrategy(self):
        return "Buying using AvgStrategy:\nIf current Price per Unit is {0}% less than 5-minute average, buy!".format(self.buyPercent*-100)
    def descriptionOfSellStrategy(self):
        return "Selling using AvgStrategy:\nIf currently at {0}% profit and Price per Unit is not below 5-minute average, sell!".format(self.sellPercent*100)
    
    # If price below avg by buyPercent, then buy! Otherwise, hold your chips Partner.
    def buySignal(self, crypto):
        ppu = getPricePerUnit(crypto)
        avg = self.getAvgPrice(crypto)
        percentDiff = (ppu - avg) / avg
        
        if percentDiff <= self.buyPercent:
            print("Buy signal for {0} is TRUE with percent diff {1}%".format(crypto, percentDiff*100))
            return True
        else:
            print("Buy signal for {0} is FALSE with percent diff {1}%".format(crypto, percentDiff*100))
            return False
    
    # If we reached sellPercent and price isn't below avg, then sell. Otherwise, diamond hands Brother!
    def sellSignal(self, crypto):
        
        if getProfitPercent(crypto) >= self.sellPercent and getPricePerUnit(crypto) >= self.getAvgPrice(crypto):
            print("Sell signal for {0} is TRUE".format(crypto))
            return True
        else:
            print("Sell signal for {0} is FALSE".format(crypto))
            return False