from helpers.trading_bot_helpers import getPricePerUnit, getProfitPercent
from helpers.historical_data import get_historical_data
from helpers.maths import slope
from datetime import timedelta, datetime
import pandas as pd

class AvgStrategy():

    def __init__(self, config=None, interval='5m', window=30):
        print("Loading AvgStrategy...")
        if config:
            self.sellPercent = float(config.get('sellPercent'))
            self.buyPercent = float(config.get('buyPercent'))
            self.slope_num_intervals = int(config.get('slope_num_intervals'))
        else:
            self.sellPercent = 0.02
            self.buyPercent = 0.02
            self.slope_num_intervals = 3
        self.interval = interval
        self.window = window

    def getAvgPriceAndTrendSlope(self, crypto):
        data = get_historical_data(crypto, self.interval, save = True)

        window_start = datetime.now() - timedelta(days=self.window)
        avg = data[(pd.to_datetime(data['timestamp']) > window_start)]['close'].mean()
        print('{}AvgPrice since {} for {} = {}'.format(self.interval, window_start, crypto, avg))

        if self.slope_num_intervals < 0:
            sys.exit("num_interval cannot be less than 0.\n Also, 0 means entire window")
        elif self.slope_num_intervals == 0 or self.slope_num_intervals >= len(data):
            print("num_intervals was equal to or greater than window size.\n Price must trend upward for ENTIRE price history window")
            trendSlope = slope(data['close'])
        else:
            trendSlope = slope(data['close'][-self.slope_num_intervals:])
        print('{} trendSlope since {} intervals for {}  was {}'.format(self.interval, self.slope_num_intervals, crypto, trendSlope))


        return float(avg), float(trendSlope)

    def descriptionOfBuyStrategy(self):
        return "Buying using AvgStrategy:\nIf current Price per Unit is {0}% less than {1}d average, buy!".format(self.buyPercent*-100, self.window)
    def descriptionOfSellStrategy(self):
        return "Selling using AvgStrategy:\nIf currently at {0}% profit and Price per Unit is not below {1}d average, sell!".format(self.sellPercent*100, self.window)
    
    # If price below avg by buyPercent, then buy! Otherwise, hold your chips Partner.
    def buySignal(self, crypto):
        ppu = getPricePerUnit(crypto)
        avg, trendSlope = self.getAvgPriceAndTrendSlope(crypto)
        percentDiff = (ppu - avg) / avg
        
        if percentDiff <= self.buyPercent and trendSlope > 0:
            print("Buy signal for {0} is TRUE with percent diff {1}% ".format(crypto, percentDiff*100)+
                  "and trendSlope {0}".format(trendSlope))
            return True
        else:
            print("Buy signal for {0} is FALSE with percent diff {1}% ".format(crypto, percentDiff*100)+
                  "and trendSlope {0}".format(trendSlope))
            return False
    
    # If we reached sellPercent and price isn't below avg, then sell. Otherwise, diamond hands Brother!
    def sellSignal(self, crypto):
        ppu = getPricePerUnit(crypto)
        avg, trendSlope = self.getAvgPriceAndTrendSlope(crypto)
        
        if trendSlope > 0:
            print("Sell signal for {0} is FALSE because crypto is trending upwards w/ slope {1}".format(crypto, trendSlope))
            return False
        elif getProfitPercent(crypto) >= self.sellPercent and ppu >= self.getAvgPrice(crypto):
            print("Sell signal for {0} is TRUE".format(crypto))
            return True
        else:
            print("Sell signal for {0} is FALSE".format(crypto))
            return False