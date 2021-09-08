from helpers.trading_bot_helpers import *
from helpers.historical_data import *
from helpers.init import parse_args, get_owned_and_unowned_cryptos

watchlist = ["BTCUSDT", "ETHUSDT", "LTCUSDT", "ZENUSDT"]

#print("Running trading bot @ {0}...".format(datetime.now()))
#for crypto in watchlist:
#	get_historical_data(crypto, '5m', save = True)

# This is the main engine of the trading bot. 
def main():
	#Load Portfolio
	strategy, sellablePercent = parse_args()
	print("getting list of owned and unowned cryptos from watchlist...\n")
	owned_cryptos, unowned_cryptos = get_owned_and_unowned_cryptos(watchlist)
	print("\nunowned_cryptos: " + " ".join(unowned_cryptos))

	can_sell = []
	if owned_cryptos:
		can_sell = analyzeSellSignals(owned_cryptos, strategy=strategy, sellablePercent=sellablePercent)
	else:
		print("\nHave no cryptos to sell, skipping analyzeSellSignals...\n")

	funds = 100#TODO: Get current account balance

	if funds > 0 or can_sell:
 		analyzeBuySignals(unowned_cryptos, funds, can_sell, strategy=strategy)
	else:
		print("\nOut of funds and have no sellable cryptos, skipping analyzeBuySignals...\n")


# Looks for new openings based on strategy.buySignal()
# Buys into new openings with all current funds and sells old positions for more funds if necessary
def analyzeBuySignals(unowned_cryptos, funds, can_sell, strategy, least_invest_amount=20):
	print("\nAnalyzing buy signals for unowned cryptos...\n{0}\n".format(strategy.descriptionOfBuyStrategy()))
	should_buy = []
	for crypto in unowned_cryptos:
		if strategy.buySignal(crypto):				
			should_buy.append(crypto)
		
	if should_buy:
		# If we can sell old positions and there are more new openings than positions currently available, liquidate old positions. Otherwise, diamond hands for life.
		if can_sell and len(should_buy) >= int(floor(funds / least_invest_amount)):
			sellCryptos(can_sell)
		# Buy into new positions
		buyCryptos(should_buy, funds, least_invest_amount)
	else:
		print("\nFound no cryptos to buy...\n")

# Looks to exit current positions based on strategy.sellSignal()
# If exiting the position would not result in a loss, can sell crypto. Otherwise it's diamond hands and we try to exit properly next time.
# If the position has at least sellablePercent (0.05) profit, add it to a list of sellable positions in case we need to liquidate in favor of new openings. 
def analyzeSellSignals(owned_cryptos, strategy, sellablePercent=0.05):
	print("\nAnalyzing sell signals for owned cryptos...\n{0}\n".format(strategy.descriptionOfSellStrategy()))
	can_sell = []
	for crypto in owned_cryptos:
		if strategy.sellSignal(crypto) and hasPercentProfit(crypto, 0):			
			sellCrypto(crypto)
		elif hasPercentProfit(crypto, sellablePercent):
			print("can sell {0}...".format(crypto))
			can_sell.append(crypto)
	return can_sell

if __name__ == "__main__":
	main()