class StgySell():

	def __init__(self, actionBook, balanceBook):

		self.name = 'StgySellAbstract'
		self.actionBook = actionBook
		self.balanceBook = balanceBook


	def getName(self):
		return self.name



	def shouldSell(self, symb, date):

		return False
