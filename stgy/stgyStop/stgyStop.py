class StgyStop():

	def __init__(self, multiStockDTO, actionBook, balanceBook):

		self.name = 'StgyStopAbstract'
		self.multiStockDTO = multiStockDTO
		self.actionBook = actionBook
		self.balanceBook = balanceBook


	def getName(self):
		return self.name



	def shouldStop(self, symb, date):

		return False
