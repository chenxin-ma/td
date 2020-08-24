class StgyBuyNaive(StgyBuy):

	def __init__(self, firstDay):

        StgyBuy.__init__(self)
		self.name = 'StgyBuyNaive'
		self.firstDay = firstDay


	def shouldBuy(self, symb, date):

		return self.firstDay == date


