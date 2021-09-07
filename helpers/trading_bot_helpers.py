import time
import os
import json
from datetime import datetime
from binance.client import Client
from helpers.spreadsheet_snippets import SPREADSHEET_ID, BOUGHT_RANGE, SOLD_RANGE, VALUE_INPUT_OPTION, SpreadsheetSnippets, service
from helpers.project_paths import creds_path

binance_creds = json.load(open(os.path.join(creds_path, 'binance_credentials.json')))
API_KEY = binance_creds["binance_api_key"]
API_SECRET = binance_creds["binance_api_secret"]
spreadsheet = SpreadsheetSnippets(service)

print("loading trading_bot_helpers...")
binance_client = Client(api_key=API_KEY, api_secret=API_SECRET)
binance_client.API_URL = "https://api.binance.us/api"

# Returns pricePerUnit and timeOfBuy for the most recent purchase of crypto
# So the bought logs look like so, which is equavalent to following buy[i]'s
# crypto   amount   pricePerUnit   timeOfBuy
# buy[0]   buy[1]     buy[2]        buy[3]
def findLastBuy(crypto):
	values = spreadsheet.get_values(SPREADSHEET_ID, BOUGHT_RANGE)['values']
	for buy in reversed(values):
		if buy[0] == crypto:
			return float(buy[2].replace(',', '')), buy[3]
	print("failed to find last buy")
	return -1, "N/A"

def getPricePerUnit(crypto):
	return float(binance_client.get_symbol_ticker(symbol=crypto)["price"].replace(',', ''))

# Returns profit percent of currently owned crypto
def getProfitPercent(crypto="NA"):
	originalPricePerUnit, _ = findLastBuy(crypto)
	currentPricePerUnit = getPricePerUnit(crypto)
	profitPercent = (currentPricePerUnit - originalPricePerUnit) / originalPricePerUnit
	print("Last bought {0} at pricePerUnit {1}, currentPricePerUnit is {2}, so profit percent is: {3}".format(crypto, originalPricePerUnit, currentPricePerUnit, profitPercent))
	return profitPercent

# TODO implement this method
def getProfitAndTimeToProfit(crypto="NA", amount=0):
	bought_at = 0#get last recorded buy from db
	time_of_purchase = 0#get time of purchase

# FIXED
# Returns list of ticker symbols for currently owned cryptos
def getOwnedCryptosFromAcc(account):
	print("owned cryptos are: ")
	owned_cryptos = []
	balances = account["balances"]
	for crypto in balances:
		if float(crypto["free"]) > 0:
			owned_cryptos.append(crypto["asset"])
			print(crypto["asset"] + " - " + crypto["free"])
	return owned_cryptos

def hasPercentProfit(crypto, percent):
	crypto_profit_percent = getProfitPercent(crypto)
	hasProfitPercent = crypto_profit_percent >= percent
	print("checking if {0} has profit percent {1:.2f}... {2}".format(crypto, percent, hasProfitPercent))
	return hasProfitPercent

# Buys $amount worth of crypto and logs it
def buyCrypto(crypto, amount):
	order = binance_client.create_test_order(
		symbol=crypto,
		side=Client.SIDE_BUY,
		type=Client.ORDER_TYPE_MARKET,
		quoteOrderQty=amount)
	log(crypto=crypto, amount=amount, action="BUY")

# Sells crypto for current price in $ and logs it
def sellCrypto(crypto):
	quantity = binance_client.get_asset_balance(asset=crypto)["free"]
	order = binance_client.create_test_order(
			symbol=crypto,
			side=Client.SIDE_SELL,
			type=Client.ORDER_TYPE_MARKET,
			quantity=quantity)
	log(crypto=crypto, amount=quantity, action="SELL")

# Buys $20 of each crypto.
# If we have less than $20 in funds, buy into the position with rest of funds and stop buying
# If last opening found, buy into the position with rest of funds and stop buying
def buyCryptos(cryptos, funds):
	for i, crypto in enumerate(cryptos):
		if funds < 20:
			buyCrypto(crypto, funds)
			break
		elif i == len(cryptos) - 1:
			buyCrypto(crypto, funds)
			break
		else:
			buyCrypto(crypto, 20)

# Sell cryptos for current price in $
def sellCryptos(cryptos):
	for crypto in cryptos:
		sellCrypto(crypto)


# Sends an email update about trading bot's current state
def emailUpdate(email="jettpierson@gmail.com", hour=4, minute=30):
	now = datetime.now().time()
	if now.hour == hour and (now.minute == 30 or now.minute == 31):
		funds = 0#Get current account balance
		portfolio_value = 0 # Get current portfolio value
		owned_cryptos = 0#Get current positions held
		print("sent email update...")
	else:
		print("did NOT send email update...")
		# Send an email to email containing current account balance, cryptos owned, and portfolio value


def log(crypto="N/A", amount=0, action="BUY/SELL"):

	if action == "BUY":
		print("bought {0}$ worth of {1}...".format(amount, crypto))
		spreadsheet.append_values(SPREADSHEET_ID, BOUGHT_RANGE, VALUE_INPUT_OPTION,
		[   #These are the values getting stored in the sheet
    		[crypto, amount, getPricePerUnit(crypto), str(datetime.now())]
		])

	elif action == "SELL":
		profit = getProfitAndTimeToProfit(crypto=crypto, amount=amount)
		print("sold {0} {1} for {2} profit".format(amount, crypto, profit))
		spreadsheet.append_values(SPREADSHEET_ID, SOLD_RANGE, VALUE_INPUT_OPTION,
		[   #These are the values getting stored in the sheet
    		[crypto, amount, str(datetime.now())]
		])
	    
	else:
		print("logs are fucked, wasn't able to figure out what action occured for {0} {1}".format(crypto, quantity))
