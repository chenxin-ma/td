from .stgyBuy import StgyBuy
from config.config import *

class StgyBuy4MA(StgyBuy):

    def __init__(self, multiStockDTO, actionBook, balanceBook,
    				short=5, med=10, far=20, farest=30, ema=False, priceForMA='close'):

        StgyBuy.__init__(self, multiStockDTO, actionBook, balanceBook)
        self.name = 'StgyBuy4MA'

        self.short = short
        self.med = med
        self.far = far
        self.farest = farest
        self.ema = ema
        if ema:
            self.maType = 'ema'
        else:
            self.maType = 'sma'
        self.priceForMA = priceForMA

        self.columnShort = self.maType + str(short)
        self.columnMed = self.maType + str(med)
        self.columnFar = self.maType + str(far)
        self.columnFarest = self.maType + str(farest)

        self.generateMAs()



    def generateMAs(self):

        for symb in self.multiStockDTO.data:
            singleStockDTO = self.multiStockDTO.data[symb]
            if self.maType == 'ema':
                s1 = singleStockDTO.setEMA(self.short, self.columnShort, self.priceForMA)
                s2 = singleStockDTO.setEMA(self.med, self.columnMed, self.priceForMA)
                s3 = singleStockDTO.setEMA(self.far, self.columnFar, self.priceForMA)
                s4 = singleStockDTO.setEMA(self.farest, self.columnFarest, self.priceForMA)
            else:
                s1 = singleStockDTO.setSMA(self.short, self.columnShort, self.priceForMA)
                s2 = singleStockDTO.setSMA(self.med, self.columnMed, self.priceForMA)
                s3 = singleStockDTO.setSMA(self.far, self.columnFar, self.priceForMA)
                s4 = singleStockDTO.setSMA(self.farest, self.columnFarest, self.priceForMA)

            singleStockDTO.refreshDailyMap()
            if s1 == s2 == s3 == s4 == False:
                return

        logger.info('StgyBuy4MA: MA columns generated.')


    def duoPai(self, day):

        if (day[self.columnShort] > day[self.columnMed] > day[self.columnFar] > day[self.columnFarest]):
            return True

        return False



    def kongPai(self, day):

        if day[self.columnShort] < day[self.columnMed] < day[self.columnFar]:
            return True
            
        return False


    def isCrossDown(self, day, day2, day3):

        if self.duoPai(day2) and self.duoPai(day3):
            if day2[self.columnShort] > day2[self.columnMed] \
            and day[self.columnShort] < day[self.columnMed]:
                return True

        return False


    def isCrossUp(self, day, day2, day3):

        if self.kongPai(day2) and self.kongPai(day3):
            if day2[self.columnMed] < day2[self.columnFar] \
            and day[self.columnMed] > day[self.columnFar]:
                return True

        return False


    def isStrugle(self, day):

        if abs(day[self.columnMed] - day[self.columnFar]) / day[self.columnFar] < 0.003 \
        or abs(day[self.columnFar] - day[self.columnFarest]) / day[self.columnFarest] < 0.002:
            return True

        return False



    def tradeDateSlide(self, date, interval):

        return self.multiStockDTO.getSymbSingleDTO(symb).tradeDateSlide(date, interval)

        return None


    def getPrevious3Days(self, symb, date):

        dateP1 = self.tradeDateSlide(symb, date, -1)
        dateP2 = self.tradeDateSlide(symb, date, -2)

        if dateP1 == None or dateP2 == None:
            return None, None, None

        singleStockDTO = self.multiStockDTO.data[symb]
        day0 = singleStockDTO.getRowDate(date)
        dayP1 = singleStockDTO.getRowDate(dateP1)
        dayP2 = singleStockDTO.getRowDate(dateP2)

        return day0, dayP1, dayP2


    def shouldBuy(self, symb, date, dateIdx):

        if symb in self.balanceBook.balance:
            return 0

        day0, dayP1, dayP2 = self.getPrevious3Days(symb, date)
        if day0 == None or dayP2 == None:
            return 0

        if self.duoPai(day0) and not self.duoPai(dayP1):
            if not self.isStrugle(day0):
                return 1

        if self.isCrossUp(day0, dayP1, dayP2):
            return 1

        return 0



    def shouldSell(self, symb, date, dateIdx):

        day0, dayP1, dayP2 = self.getPrevious3Days(symb, date)
        if day0 == None or dayP2 == None:
            return 0

        if self.kongPai(day0):
            return self.balanceBook.getSymbShares(symb)

        if self.isCrossDown(day0, dayP1, dayP2):
            return self.balanceBook.getSymbShares(symb)

        return 0