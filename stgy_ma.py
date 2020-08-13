import pandas as pd
import logging
from config import *

class Stgy_MA():

	def __init__(self, sh, short=8, med=21, far=55, ema=False, priceToUse='close'):

		self.sh = sh 
		self.short = short
		self.med = med
		self.far = far
		self.ema = ema
		if ema:
			self.maType = 'ema'
		else:
			self.maType = 'sma'

		self.columnShort = self.maType + str(short)
		self.columnMed = self.maType + str(med)
		self.columnFar = self.maType + str(far)

		self.priceToUse = priceToUse
		self.generateMAs()

		self.pos = POSITION.EMPTY

	def generateMAs(self):

		if self.maType == 'ema':
			self.sh.getEMA(self.short, self.priceToUse)
			self.sh.getEMA(self.med, self.priceToUse)
			self.sh.getEMA(self.far, self.priceToUse)
		else:
			self.sh.getSMA(self.short, self.priceToUse)
			self.sh.getSMA(self.med, self.priceToUse)
			self.sh.getSMA(self.far, self.priceToUse)
		logging.info('MA data for %s generated.' %self.sh.getSymb())


	def buyCheck(self, day):

		if self.pos == POSITION.FULL:
			return False

		if (day[self.priceToUse] > day[self.columnMed] and day[self.columnMed] > day[self.columnFar]):
			logging.debug('%dSMA %.3f > %dSMA %.3f.' %(self.med, day[self.columnMed], self.far, day[self.columnFar]))
			self.pos = POSITION.FULL
			return True

		return False


	def sellCheck(self, day):

		if self.pos == POSITION.EMPTY:
			return False

		if (day[self.priceToUse] < day[self.columnMed]):
			self.pos = POSITION.EMPTY
			return True


	def simulation(self):

		for idx, day in self.sh.getDf().iterrows():

			# logging.debug('Simulation on date: %s.' %day['datetime'] )
			if pd.isna(day[self.columnFar]):
				continue

			buy = self.buyCheck(day)
			if buy:
				logging.warning('BUY %s: price %.3f on %s.' \
								%(self.sh.getSymb(), day[self.priceToUse], day['datetime'] ) ) 
				continue

			sell = self.sellCheck(day)
			if sell:
				logging.warning('SELL %s: price %.3f on %s.' \
								%(self.sh.getSymb(), day[self.priceToUse], day['datetime'] ) ) 




