from .dataLoader import DataLoader
from dto.balanceBook import BalanceBook
from dto.actionBook import ActionBook
from config.config import *
from util.utils import *
from stgy import *

class Simulator:

    def __init__(self, symbs, stgyBuy, stgyBuyQuan, stgySell, stgyStop,
                    beginDate, endDate='', dataFirstDay='', iniValue=100000000):

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
        self.simNumdays = len(self.simDateList)

        if stgyBuy == 'Naive':
            self.stgyBuy = StgyBuyNaive(self.actionBook, self.balanceBook, 0)

        if stgyBuyQuan == 'Naive':
            self.stgyBuyQuan = StgyBuyQuanNaive(self.actionBook, self.balanceBook)

        if stgySell == 'Naive':
            self.stgySell = StgySellNaive(self.actionBook, self.balanceBook, self.simNumdays - 1)

        if stgyStop == 'Naive':
            self.stgyStop = StgyStopNaive(self.actionBook, self.balanceBook)



    def getSimDateList(self):

        return self.data.getSymbSingleDTO('AAPL')\
                .getDf(self.beginDate, self.endDate)['datetime'].tolist()



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

        self.balanceBook.update(symb, shares, price)

        transLog.info('%s %s %s %d %.3f' \
                     %(do, symb, date, abs(shares), price) )



    def run(self):


        for dateIdx, date in enumerate(tqdm(self.simDateList)):

            logger.debug('Simulator: date %s undergoing.' %date)


            for symb in self.balanceBook.getCurrentHolding():

                sellShares = self.stgySell.shouldSell(symb, date, dateIdx)
                closePrice = self.data.getSymbClosePriceAtDate(symb, date)

                if sellShares > 0:
                    self.action('sell', symb, closePrice, sellShares, date)

                shoudStop = self.stgyStop.shouldStop(symb, date)

                if shoudStop:
                    allShares = self.balanceBook.getSymbShares(symb)
                    self.action('sell', symb, closePrice, allShares, date)



            for symb in self.symbs[:2]:

                suggestBuyShares = self.stgyBuy.shouldBuy(symb, date, dateIdx)
                closePrice = self.data.getSymbClosePriceAtDate(symb, date)

                if suggestBuyShares > 0:

                    shares = self.stgyBuyQuan.sharesToBuy(suggestBuyShares)
                    self.action('buy', symb, closePrice, shares, date)















