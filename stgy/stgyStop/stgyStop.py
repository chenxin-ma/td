class StgyStop():

	def __init__(self, actionBook, balanceBook):

		self.name = 'StgyStopAbstract'
		self.actionBook = actionBook
		self.balanceBook = balanceBook


	def getName(self):
		return self.name



	def shouldStop(self, symb, date):

		return False
