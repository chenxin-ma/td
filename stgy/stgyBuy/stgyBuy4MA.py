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

        if s1 == s2 == s3 == s4 == False:
            return

        logger.info('StgyBuy4MA: MA columns generated.')



    def shouldBuy(self, symb, date, dateIdx):

        return 0
