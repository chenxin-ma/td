class StgySellNaive(StgySell):

	def __init__(self, lastDay):

        StgySell.__init__(self)
		self.name = 'StgySellNaive'
		self.lastDay = lastDay


	def shouldSell(self, symb, date):

		if self.lastDay == date:
			return 100

		return 0


