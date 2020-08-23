from .stgy import *

class Stgy_BO(Stgy):


    def __init__(self, sh, backFar=200, backClose=5, breakR=0.01, stopR=0.03, priceToUse='close', init=10000):
        
        Stgy.__init__(self, sh, priceToUse, init)
        self.name = 'BO'
        self.backFar = backFar
        self.backClose = backClose
        self.prevHigh = 0
        self.breakR = breakR
        self.stopR = stopR
        self.earliest = 0

        self.jianCangProfitThres = [1.05, 1.1, 1.2, 1.3, 1.4, 1.5]
        self.jianCangPos = [0.1, 0.25, 0.3, 0.15, 0.1, 1]
        self.jianCangZhiYingThres = [1.01, 1.04, 1.12, 1.2, 1.25, 1.4]
        self.jianCangIdx = 0

        self.lastBuyPrice = 0

    def rebalanceJianCangThres(self, vol):

        volToMaxVol = min(vol / 0.18, 1)
        self.jianCangProfitThres = [(thres - 1) * volToMaxVol + 1 for thres in self.jianCangProfitThres]
        self.jianCangZhiYingThres = [(thres - 1) * volToMaxVol + 1 for thres in self.jianCangZhiYingThres]


    def buyCheck(self, day, numDaysCap):

        if day[self.priceToUse] >= self.prevHigh * (1 - self.breakR) \
                and day[self.priceToUse] <= self.prevHigh * (1 + 3 * self.breakR):

            prevHighFar = self.sh.getHighestPrice(daysBack=self.earliest, 
                            end=self.backClose+numDaysCap, priceToUse='high')

            # print(day['datetime'], prevHighFar, self.prevHigh, self.backClose+numDaysCap)
            if prevHighFar == self.prevHigh:
                return True

        return False


    def stopSellCheck(self, day):

        if day[self.priceToUse] < self.lastBuyPrice * (1 - self.stopR):
            return True

        return False


    def sellHighCheck(self, day):

        jianCangPct = 0
        while (self.jianCangIdx < len(self.jianCangProfitThres) ):
            if day[self.priceToUse] >= self.lastBuyPrice * self.jianCangProfitThres[self.jianCangIdx]:
                jianCangPct += self.jianCangPos[self.jianCangIdx]
                self.jianCangIdx += 1
            else:
                break

        if self.jianCangIdx > 0 and self.jianCangIdx < len(self.jianCangProfitThres):
            if day[self.priceToUse] / self.lastBuyPrice < self.jianCangZhiYingThres[self.jianCangIdx - 1]:
                return 1

        return min(jianCangPct, 1)


    def simulation(self, begin='2000-01-01', end=''):
        
        if end == '':
            end = pd.Timestamp.now().strftime("%Y-%m-%d")

        if self.prevHigh == ERROR.NOT_ENOUGH_HISTORY:
            return 

        df = self.sh.getDf(begin, end).copy().reset_index()
        df['value'] = self.balance['cash']

        self.earliest = self.backFar + len(df)
        self.prevHigh = self.sh.getHighestPrice(daysBack=self.earliest, end=len(df), priceToUse='high')

        self.vol = self.sh.getVolatility(daysBack=400 + len(df), end=len(df))
        self.rebalanceJianCangThres(self.vol)

        for i in range(len(df)):

            day = df.iloc[i]

            if self.pos == POSITION.EMPTY and self.buyCheck(day, len(df) - i):
                self.action('buy', day) 
                self.jianCangIdx = 0
                self.lastBuyPrice = day[self.priceToUse]

            if self.pos == POSITION.FULL and self.stopSellCheck(day):
                self.action('sell', day)

            if self.pos != POSITION.EMPTY:
                sellPct = self.sellHighCheck(day)
                if sellPct > 0:
                    self.action('sell', day, sellPct)

            self.prevHigh = max(self.prevHigh, day['high'])

            df.loc[i, 'value'] = self.getAccountValue(day)

        currentValue = self.getAccountValue(day)
        winR, numTrans = self.getWinRatio()
        holdDays = self.getTotalHoldDays()
        
        if drawing:
            self.plot(df)
        simLog.info('%s, %s, %.3f, %.3f, %d, %.3f, %.3f, %d' %(self.name, 
                                self.sh.getSymb(), currentValue, winR, numTrans, 
                                self.minValue, self.maxValue, holdDays))








