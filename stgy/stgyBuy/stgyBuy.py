class StgyBuy():

	def __init__(self, actionBook, balanceBook):

		self.name = 'StgyBuyAbstract'
		self.actionBook = actionBook
		self.balanceBook = balanceBook


	def getName(self):
		return self.name



	def shouldBuy(self, symb, date):
		return 0
