class StgySell():

	def __init__(self, multiStockDTO, actionBook, balanceBook):

		self.name = 'StgySellAbstract'
		self.multiStockDTO = multiStockDTO
		self.actionBook = actionBook
		self.balanceBook = balanceBook


	def getName(self):
		return self.name



	def shouldSell(self, symb, date):

		return False
