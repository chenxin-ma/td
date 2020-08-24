class StgyBuyQuan():

	def __init__(self, multiStockDTO, actionBook, balanceBook):

		self.name = 'StgyBuyQuanAbstract'
		self.multiStockDTO = multiStockDTO
		self.actionBook = actionBook
		self.balanceBook = balanceBook


	def getName(self):
		return self.name