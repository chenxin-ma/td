from .dataLoader import DataLoader
from dto.balanceBook import BalanceBook
from dto.actionBook import ActionBook
from util.utils import *
from stgy import *

class Simulator:

	def __init__(self, symbs, stgyBuy, stgyBuyQuan, stgySell, stgyStop,
					beginDate, endDate='', dataFirstDay='', iniValue=10000):

		self.symbs = symbs
		dataLoader = DataLoader(symbs, dataFirstDay)
		self.data =  dataLoader.loadDailyData()

		self.balanceBook = BalanceBook(iniValue)
		self.actionBook = ActionBook()
		self.netValue = {}

		self.beginDate = beginDate
		if endDate == '':
            self.endDate = getTodayDate()

        self.simDateList = self.getSimDateList()

        if stgyBuy == 'Naive':
        	self.stgyBuy = StgyBuyNaive(self.beginDate)

        if stgyBuyQuan == 'Naive':
        	self.stgyBuyQuan = StgyBuyQuanNaive()

        if stgySell == 'Naive':
        	self.stgySell = StgyBuyQuanNaive()

        if stgyStop == 'Naive':
        	self.stgyStop = None



    def getSimDateList(self):

    	return self.data['AAPL'].getDf(self.beginDate, self.endDate)['datetime'].tolist()



    def getAccountValue(self, date):

    	value = 0

    	for symb in self.balanceBook.getCurrentHolding():

    		shares = self.balanceBook.getSymbShares(symb)
    		price = self.data.getSymbClosePriceAtDate(symb, date)
    		value += shares * price

    	value += self.balanceBook.getCash()
        return value



    def action(self, do, symb, price, shares, date):

	    self.actionBook.update(do, symb, price, shares, date)

    	if do == 'sell':
	    	shares = -shares

	    self.balanceBook.update(symb, shares)

        transLog.info('%s %s %s %d %.3f' \
                     %(do, symb, date, abs(shares), price) )



    def run(self):


    	for dateId, date in enumerate(tqdm(self.simDateList)):

    		logger.debug('Simulator: date %s undergoing.' %date)

    		for symb in self.symbs:

    			suggestBuyShares = self.stgyBuy.shouldBuy(symb, date)
				closePrice = self.data.getSymbClosePriceAtDate(symb, date)

    			if suggestBuyShares > 0:

    				shares = self.stgyBuyQuan.sharesToBuy(suggestBuyShares)
    				action('buy', symb, closePrice, shares, date)


    			sellShares = self.stgySell.shouldSell(self.balanceBook, 
    												  self.actionBook, 
    												  symb, 
    												  date)

    			if sellShares > 0:
    				action('sell', symb, closePrice, sellShares, date)

    			shoudStop = self.stgyStop.shoudStop(symb, date)

    			if shoudStop:
    				allShares = self.balanceBook.getSymbShares(symb)
    				action('sell', symb, closePrice, allShares, date)
    				














