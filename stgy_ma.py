from stgy import *

class Stgy_MA(Stgy):

    def __init__(self, sh, short=21, med=55, far=100, ema=False, priceToUse='close', init=10000):
        
        Stgy.__init__(self, sh, priceToUse, init)
        self.name = 'MA'

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

        self.generateMAs()


    def generateMAs(self):

        if self.maType == 'ema':
            self.sh.getEMA(self.short, self.priceToUse)
            self.sh.getEMA(self.med, self.priceToUse)
            self.sh.getEMA(self.far, self.priceToUse)
        else:
            self.sh.getSMA(self.short, self.priceToUse)
            self.sh.getSMA(self.med, self.priceToUse)
            self.sh.getSMA(self.far, self.priceToUse)
        logger.debug('MA data for %s generated.' %self.sh.getSymb())


    def buyCheck(self, day, lastDay):

        if self.pos == POSITION.FULL or lastDay is None:
            return False

        # MA55 should go up
        if day[self.columnFar] <= lastDay[self.columnFar] * (1 + 0.001):
            return False

        if (day[self.priceToUse] > day[self.columnShort] and day[self.columnShort] > day[self.columnMed]):
            logger.debug('%dSMA %.3f > %dSMA %.3f.' %(self.med, day[self.columnShort], self.far, day[self.columnMed]))
            self.pos = POSITION.FULL
            return True

        return False


    def sellCheck(self, day):

        if self.pos == POSITION.EMPTY:
            return False

        if (day[self.priceToUse] < day[self.columnShort]):
            self.pos = POSITION.EMPTY
            return True



    def simulation(self, begin='2000-01-01', end=''):

        if end == '':
            end = pd.Timestamp.now().strftime("%Y-%m-%d")

        lastDay = None
        for idx, day in self.sh.getDf(begin, end).iterrows():

            # logger.debug('Simulation on date: %s.' %day['datetime'] )
            if pd.isna(day[self.columnFar]):
                continue

            buy = self.buyCheck(day, lastDay)
            if buy:
                self.action('buy', day) 
                continue

            sell = self.sellCheck(day)
            if sell:
                self.action('sell', day)
                currentValue = self.getAccountValue(day)

            lastDay = day

        currentValue = self.getAccountValue(day)
        winR, numTrans = self.getWinRatio()
        holdDays = self.getTotalHoldDays()
        simLog.info('MA, %s, %.3f, %.3f, %d, %.3f, %.3f, %d' %(self.sh.getSymb(), currentValue, winR, numTrans, 
                                self.minValue, self.maxValue, holdDays))




