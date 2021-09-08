import argparse
import json
from strategies.EMACrossStrategy import EMACrossStrategy
from strategies.AvgStrategy import AvgStrategy
from helpers.trading_bot_helpers import binance_client, getOwnedCryptosFromAcc

def get_strategy(strategy_name, config, interval, window):
	if strategy_name is AvgStrategy.__name__:
		return AvgStrategy(config, interval, window)
	elif strategy_name is EMACrossStrategy.__name__:
		return EMACrossStrategy(config, interval, window)

# Returns strategy, take_profit
def parse_args():
	print("Parsing arguments...")
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--strategy', default='AvgStrategy',
		help="strategy used by the trading bot. Default: AvgStrategy")
	parser.add_argument('-c', '--config', type=json.loads, default='{\"sellPercent\":\"0.02\", \"buyPercent\":\"0.02\", \"slope_num_intervals\":\"3\"}',
		help="dictionary of configurations for the specified strategy. Default: to {\"sellPercent\":\"0.02\", \"buyPercent\":\"0.02\", \"slope_num_intervals\":\"3\"}")
	parser.add_argument('-hi', '--historical-interval', default='5m', choices=["1m", "5m", "1h", "1d"],
		help="interval of historical data, i.e. the frequency of datapoints. Default: 5m")
	parser.add_argument('-hw', '--historical-window', type=int, default='30',
		help="window of historical data in days, i.e. the X latest days of data. Default: 30")
	parser.add_argument('-sp', '--sellable-percent', type=float, default=0.01,
		help="The profit percent that must have been made before a crypto will be sellable. Default: 0.01")
	args = parser.parse_args()
	return get_strategy(args.strategy, args.config, args.historical_interval, args.historical_window), args.sellable_percent

def get_owned_and_unowned_cryptos(watchlist):
	account = binance_client.get_account()
	owned_cryptos = set(getOwnedCryptosFromAcc(account)) - set(['USD'])

	return owned_cryptos, set(watchlist) - set(owned_cryptos)

