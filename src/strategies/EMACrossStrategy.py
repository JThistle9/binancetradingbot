
class EMACrossStrategy():

	def __init__(self, config=None, interval="5m", window=30):
		self.interval = interval
		self.window = window

	# If new trend is better than old trend, then buy! Otherwise, hold your chips Partner!
	def buySignal(crypto):
				# TODO: Implement getOld and getNew
		oldEMA = getOldEMA(interval, window)
		newEMA = getNewEMA(interval, window)

		if newEMA > oldEMA:
			return True
		else:
			return False

	# If new trend is worse than old trend, then sell. Otherwise, diamond hands Brother!
	def sellSignal(crypto, interval="1-second", window="1-day"):

		oldEMA = getOldEMA(interval, window)
		newEMA = getNewEMA(interval, window)

		if newEMA < oldEMA:
			return True
		else:
			return False