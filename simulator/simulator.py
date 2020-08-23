from .dataLoader import DataLoader

class Simulator:

	def __init__(self, symbs, date_start='', iniValue=10000):

		dataLoader = DataLoader(symbs, date_start)
		dataLoader.loadDailyData()


