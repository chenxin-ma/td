import json
import talib


class SingleStockDTO():

    def __init__(self, df, symb, firstDay=''):

        self.symb = symb

        if firstDay != '':
            self.o0 = df[(df['datetime'] >= firstDay)].copy()
        else:
            self.o0 = df.copy()

        self.dailyMap = self.o0.set_index('datetime').to_dict('index')



    def __copy__(self):
        return SingleStockDTO(self.o0.copy(), self.symb)
        


    def getSymb(self):

        return self.symb


    def getDf(self, begin='', end=''):

        if begin == '' and end == '':
            return self.o0

        return self.o0[(self.o0['datetime'] >= begin) & (self.o0['datetime'] <= end)]


    def getCloseForDate(self, date):

        return self.dailyMap[date]['close']


    def getHighestPrice(self, sinceIPO=False, daysBack=500, end=0, priceToUse='close'):

        if sinceIPO:
            return self.o0[priceToUse].max()

        if (len(self.o0) < daysBack):
            logger.warning('Stock does not have %d days since IPO.' %daysBack)
            return ERROR.NOT_ENOUGH_HISTORY

        if end == 0:
            return self.o0[priceToUse].iloc[-daysBack:].max()

        return self.o0[priceToUse].iloc[-daysBack:-end].max()


    def getEMA(self, period=21, priceToUse='close'):

        colName = 'ema%d' %period
        if colName in self.o0.columns:
            return self.o0[colName]

        self.o0[colName] = talib.EMA(self.o0[priceToUse], timeperiod=period)
        return self.o0[colName]


    def getSMA(self, period=21, priceToUse='close'):
        
        colName = 'sma%d' %period
        if colName in self.o0.columns:
            return self.o0[colName]

        self.o0[colName] = talib.SMA(self.o0[priceToUse], timeperiod=period)
        return self.o0[colName]


    def getVolatility(self, sinceIPO=False, daysBack=500, end=0, priceToUse='close'):

        # return self.o0[priceToUse].pct_change(1).iloc[-daysBack:-end].std() 

        return self.o0[priceToUse].iloc[-daysBack:-end].std() / self.o0[priceToUse].iloc[-daysBack:-end].mean()




