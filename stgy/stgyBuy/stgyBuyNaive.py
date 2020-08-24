class StgyBuyNaive(StgyBuy):

	def __init__(self, firstDay):

        StgyBuy.__init__(self)
		self.name = 'StgyBuyNaive'
		self.firstDay = firstDay


	def shouldBuy(self, symb, date):

		if self.firstDay == date:
			return 100

		return 0


