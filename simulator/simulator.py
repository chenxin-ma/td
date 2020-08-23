from .dataLoader import DataLoader
from dto.balanceBook import BalanceBook
from dto.actionBook import ActionBook


class Simulator:

	def __init__(self, symbs, date_start='', iniValue=10000):

		dataLoader = DataLoader(symbs, date_start)
		self.data =  dataLoader.loadDailyData()

		self.balanceBook = BalanceBook(iniValue)
		self.actionBook = ActionBook()


