import json
import talib
from config.config import *

class SingleStockDTO():

    def __init__(self, df, symb, firstDay=''):

        self.symb = symb

        if firstDay != '':
            self.o0 = df[(df['datetime'] >= firstDay)].reset_index(drop=True).copy()
        else:
            self.o0 = df.copy()

        self.dailyMap = {}
        self.refreshDailyMap()

        self.tradeCalendarMap = {}
        self.tradeCalendarMap['iToD'] = self.o0['datetime'].to_dict()
        self.tradeCalendarMap['dToI'] = {v: k for k, v in self.tradeCalendarMap['iToD'].items()}


    def __copy__(self):
        return SingleStockDTO(self.o0.copy(), self.symb)
        


    def getSymb(self):

        return self.symb


    def getDf(self, begin='', end=''):

        if begin == '' and end == '':
            return self.o0

        if begin == '' and end != '':
            return self.o0[self.o0['datetime'] <= end]
            
        if begin != '' and end == '':
            return self.o0[self.o0['datetime'] >= begin]


        return self.o0[(self.o0['datetime'] >= begin) & (self.o0['datetime'] <= end)]


    def refreshDailyMap(self):

        self.dailyMap = self.o0.set_index('datetime').to_dict('index')


    def getRowDate(self, date):

        if date not in self.dailyMap:
            return None
        return self.dailyMap[date]


    def getCloseForDate(self, date):
        
        if date not in self.dailyMap:
            return None
        return self.dailyMap[date]['close']


    # def getHighestPrice(self, sinceIPO=False, daysBack=500, end=0, priceToUse='close'):

    #     if sinceIPO:
    #         return self.o0[priceToUse].max()

    #     if (len(self.o0) < daysBack):
    #         logger.warning('Stock does not have %d days since IPO.' %daysBack)
    #         return ERROR.NOT_ENOUGH_HISTORY

    #     if end == 0:
    #         return self.o0[priceToUse].iloc[-daysBack:].max()

    #     return self.o0[priceToUse].iloc[-daysBack:-end].max()



    def getHighestPrice(self, daysBack=500, date='', dateSlide=0, priceToUse='close'):

        if date not in self.tradeCalendarMap['dToI']:
            return None

        dateidx = self.tradeCalendarMap['dToI'][date]

        if date == '':
            dateidx = -1

        stIdx = dateidx - daysBack 
        if stIdx < 0:
            stIdx = 0

        if stIdx >= dateidx + dateSlide:
            return None
        # logger.warning('%s, %d, %d, %d' %(date, stIdx, dateidx, dateSlide) )

        return self.o0[priceToUse].iloc[stIdx : dateidx + dateSlide].max()



    def setEMA(self, period, colName, priceToUse):

        if colName in self.o0.columns:
            return False

        self.o0[colName] = talib.EMA(self.o0[priceToUse], timeperiod=period)

        return True


    def setSMA(self, period, colName, priceToUse):
        
        if colName in self.o0.columns:
            return False

        self.o0[colName] = talib.SMA(self.o0[priceToUse], timeperiod=period)
        return True



    def getCol(self, colName):

        return self.o0[colName]


    def getVolatility(self, sinceIPO=False, daysBack=500, end=0, priceToUse='close'):

        # return self.o0[priceToUse].pct_change(1).iloc[-daysBack:-end].std() 

        return self.o0[priceToUse].iloc[-daysBack:-end].std() / self.o0[priceToUse].iloc[-daysBack:-end].mean()



    def tradeDateSlide(self, date, interval):

        newIdx = self.tradeCalendarMap['dToI'][date] + interval
        if newIdx not in self.tradeCalendarMap['iToD']:
            return None

        return self.tradeCalendarMap['iToD'][newIdx]

