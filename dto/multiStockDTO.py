
class MultiStockDTO():

	def __init__(self, dailyData, date_start):

		self.data = dailyData
		if date_start == '':
			self.date_start = '2020-01-01'
		else:
			self.date_start = date_start

	

	def getSymbSingleDTO(self, symb):

		return self.data[symb]


	def getSymbClosePriceAtDate(self, symb, date):

		return self.data[symb].getCloseForDate(date)
