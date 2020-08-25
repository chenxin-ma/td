from .dataLoader import DataLoader
from dto.balanceBook import BalanceBook
from dto.actionBook import ActionBook
from config.config import *
from util.utils import *
from stgy import *
from .referee import Referee

class Simulator:

    def __init__(self, symbs, stgyBuy, stgyBuyQuan, stgySell, stgyStop,
                    beginDate, endDate='', dataFirstDay='', iniValue=3000000):

        self.symbs = symbs
        dataLoader = DataLoader(symbs, dataFirstDay)
        self.multiStockDTO =  dataLoader.loadDailyData()

        self.balanceBook = BalanceBook(iniValue)
        self.actionBook = ActionBook()
        self.netValue = {}

        self.beginDate = beginDate
        if endDate == '':
            self.endDate = getTodayDate()

        self.simDateList = self.getSimDateList()
        self.simNumdays = len(self.simDateList)

        self.referee = Referee(self.multiStockDTO, self.actionBook, self.balanceBook, self.netValue)


        if stgyBuy == 'Naive':
            self.stgyBuy = StgyBuyNaive(self.multiStockDTO, self.actionBook, self.balanceBook, 0)
        elif stgyBuy == '4MA':
            self.stgyBuy = StgyBuy4MA(self.multiStockDTO, self.actionBook, self.balanceBook)
        elif stgyBuy == 'NewHigh':
            self.stgyBuy = StgyBuyNewHigh(self.multiStockDTO, self.actionBook, self.balanceBook)
        elif stgyBuy == 'CupHandle':
            self.stgyBuy = StgyBuyCupHandle(self.multiStockDTO, self.actionBook, self.balanceBook)


        if stgyBuyQuan == 'Naive':
            self.stgyBuyQuan = StgyBuyQuanNaive(self.multiStockDTO, self.actionBook, self.balanceBook, 
                                                maxPct=1./len(symbs))
        elif stgyBuyQuan == '4MA':
            self.stgyBuyQuan = StgyBuyQuanNaive(self.multiStockDTO, self.actionBook, self.balanceBook, 
                                                maxPct=0.05)        
        elif stgyBuyQuan == 'NewHigh':
            self.stgyBuyQuan = StgyBuyQuanNaive(self.multiStockDTO, self.actionBook, self.balanceBook, 
                                                maxPct=0.02)        
        elif stgyBuyQuan == 'NewHigh':
            self.stgyBuyQuan = StgyBuyQuanNaive(self.multiStockDTO, self.actionBook, self.balanceBook, 
                                                maxPct=0.02)


        if stgySell == 'Naive':
            self.stgySell = StgySellNaive(self.multiStockDTO, self.actionBook, self.balanceBook, self.simNumdays - 1)
        elif stgySell == '4MA':
            self.stgySell = self.stgyBuy
        elif stgySell == 'MultiPct':
            self.stgySell = StgySellMultiPct(self.multiStockDTO, self.actionBook, self.balanceBook)


        if stgyStop == 'Naive':
            self.stgyStop = StgyStopNaive(self.multiStockDTO, self.actionBook, self.balanceBook)



    def getSimDateList(self):

        return self.multiStockDTO.getSymbSingleDTO('AAPL')\
                .getDf(self.beginDate, self.endDate)['datetime'].tolist()



    def getAccountValue(self, date):

        value = 0

        for symb in self.balanceBook.getCurrentHolding():

            shares = self.balanceBook.getSymbShares(symb)
            price = self.multiStockDTO.getSymbClosePriceAtDate(symb, date)
            value += shares * price

        value += self.balanceBook.getCash()
        return value



    def action(self, do, symb, price, shares, date):

        if shares == 0:
            return

        if do == 'sell':
            shares = -shares

        if symb in self.balanceBook.balance and self.balanceBook.balance[symb] + shares < 0:
            return 

        self.actionBook.update(do, symb, price, abs(shares), date)
        self.balanceBook.update(symb, shares, price)

        transLog.info('%s %s %s %d %.3f' \
                     %(do, symb, date, abs(shares), price) )



    def judger(self):

        winR = self.referee.winRatio()
        yearlyR = self.referee.yearlyReturn()

        simLog.info('Simulation finished: yearly return %.3f%%, win rate %.3f' %(yearlyR, winR) )
        logger.info('Simulation finished: yearly return %.3f%%, win rate %.3f.' %(yearlyR, winR) )



    def run(self):


        for dateIdx, date in enumerate(tqdm(self.simDateList)):

            logger.debug('Simulator: date %s undergoing.' %date)


            for symb in self.balanceBook.getCurrentHolding():

                sellShares = self.stgySell.shouldSell(symb, date, dateIdx)
                closePrice = self.multiStockDTO.getSymbClosePriceAtDate(symb, date)

                if sellShares > 0:
                    self.action('sell', symb, closePrice, sellShares, date)

                shoudStop, stopPrie = self.stgyStop.shouldStop(symb, date)

                if shoudStop:
                    allShares = self.balanceBook.getSymbShares(symb)
                    self.action('sell', symb, stopPrie, allShares, date)


            todayNet = self.getAccountValue(date)
            self.netValue[date] = todayNet

            buyList = []
            for symb in self.symbs:

                shouldBuy = self.stgyBuy.shouldBuy(symb, date, dateIdx)

                if shouldBuy > 0:
                    buyList.append(symb)
            
            sharesList = self.stgyBuyQuan.sharesToBuy(buyList, date, todayNet)

            for i, symb in enumerate(buyList):
                sharesToBuy = sharesList[i]
                closePrice = self.multiStockDTO.getSymbClosePriceAtDate(symb, date)
                self.action('buy', symb, closePrice, sharesToBuy, date)


            numStock = len(self.balanceBook.getCurrentHolding())
            cashNow = self.balanceBook.getCash()
            simLog.info('Date %s, net %.2f, holding %d, cash %.2f' %(date, todayNet, numStock, cashNow))

        self.judger()






