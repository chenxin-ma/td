from .dataLoader import DataLoader
from dto.balanceBook import BalanceBook
from dto.actionBook import ActionBook


class Simulator:

	def __init__(self, symbs, date_start='', iniValue=10000):

		dataLoader = DataLoader(symbs, date_start)
		self.data =  dataLoader.loadDailyData()

		self.balanceBook = BalanceBook(iniValue)
		self.actionBook = ActionBook()

		self.nets = {}


    def getAccountValue(self, date):

    	value = 0

    	for symb in self.balanceBook.getCurrentHolding():

    		shares = self.balanceBook.getSymbShares(symb)
    		price = self.data.getSymbClosePriceAtDate(symb, date)
    		value += shares * price

    	value += self.balanceBook.getCash()
        return value
