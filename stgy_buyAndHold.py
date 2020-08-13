from stgy import *

class Stgy_BAH(Stgy):

    def __init__(self, sh, priceToUse='close', init=10000):

        Stgy.__init__(self, sh, priceToUse, init)
        self.name = "BAH"

    def simulation(self, begin='2000-01-01', end=''):

        if end == '':
            end = pd.Timestamp.now().strftime("%Y-%m-%d")

        df = self.sh.getDf(begin, end)
        day1 = df.iloc[0,:]
        dayN = df.iloc[-1,:]

        self.action('buy', day1)
        self.action('sell', dayN)
        currentValue = self.getAccountValue(dayN)

        winR, numTrans = self.getWinRatio()
        simLog.info('BAH, %s, %.3f, %.3f, %d, %.3f, %.3f' %(self.sh.getSymb(), currentValue, winR, numTrans, 
                                self.minValue, self.maxValue))

