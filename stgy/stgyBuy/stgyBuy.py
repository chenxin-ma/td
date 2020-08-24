class StgyBuy():

	def __init__(self, multiStockDTO, actionBook, balanceBook):

		self.name = 'StgyBuyAbstract'
		self.multiStockDTO = multiStockDTO
		self.actionBook = actionBook
		self.balanceBook = balanceBook


	def getName(self):
		return self.name



	def shouldBuy(self, symb, date):
		return 0
