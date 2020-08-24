class StgySellNaive(StgySell):

	def __init__(self, lastDay):

		self.name = 'StgySellNaive'
		self.lastDay = lastDay


	def shouldSell(self, symb, date):

		if self.lastDay == date:
			return 100

		return 0


