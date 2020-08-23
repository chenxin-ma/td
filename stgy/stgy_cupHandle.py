from stgy import *

class Stgy_CH(Stgy):

    def __init__(self, sh, date_start='', prevHighThres=0.04, prevNearThres=0.02, stopR=0.05, 
                                priceToUse='close', init=10000):

        Stgy.__init__(self, sh, date_start, priceToUse, init)
        self.name = 'CH'
        self.prevHighThres = prevHighThres
        self.prevNearThres = prevNearThres
        self.stopR = stopR

        self.jianCangProfitThres = [1.05, 1.1, 1.2, 1.3, 1.4, 1.5]
        self.jianCangPos = [0.1, 0.25, 0.3, 0.15, 0.1, 1]
        self.jianCangZhiYingThres = [1.01, 1.04, 1.12, 1.2, 1.2, 1.2]
        self.jianCangIdx = 0

        self.lastBuyPrice = 0


    def buyCheck(self, day, df, i):

        dfWindow = df.iloc[:i+1]
        today = day['high']

        prevHigh = today * (1 + self.prevHighThres)
        resistantBoxLow = today * (1 - self.prevNearThres)
        resistantBoxHigh = today * (1 + self.prevNearThres)
        
        daysToPrevHighIdx = dfWindow[dfWindow['high'].gt(prevHigh)].index
        if len(daysToPrevHighIdx) == 0:
            return False

        earliestHighIdx = 1
        for i in range(len(daysToPrevHighIdx) - 1):
            if dfWindow.iloc[daysToPrevHighIdx[-i-2] : daysToPrevHighIdx[-i-1]]['high'].max() <= prevHigh:
                earliestHighIdx = i + 2
            else:
                break

        daysToPrevHigh = len(dfWindow) - daysToPrevHighIdx[-earliestHighIdx]
        if daysToPrevHigh < 20:
            return False

        dfFocus = dfWindow.iloc[daysToPrevHighIdx[-earliestHighIdx]:]
        inBoxIdx = dfFocus[(dfFocus['high'].gt(resistantBoxLow))].index


        prevIdx = -1
        drawdownCount = 0
        enoughDrawback = False
        for idx in inBoxIdx:
            if prevIdx == -1:
                prevIdx = idx
                continue

            if (idx - prevIdx >= 5):
                lowInStint = dfFocus.loc[prevIdx : idx]['low'].min()
                # print(day['datetime'], inBoxIdx, daysToPrevHigh, idx)

                if lowInStint < resistantBoxLow * 0.95:
                    drawdownCount += 1
                if lowInStint < resistantBoxLow * 0.8:
                    enoughDrawback = True
            
            prevIdx = idx

        if drawdownCount >= 2 and enoughDrawback == True:
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


        df = self.sh.getDf().copy().reset_index()
        if (len(df) == 0):
            return

        df['value'] = self.balance['cash']

        simDays = len(self.sh.getDf(begin, end))

        for i in range(len(df) - simDays, len(df)):

            day = df.iloc[i]

            if self.pos == POSITION.EMPTY and self.buyCheck(day, df, i):
                self.action('buy', day) 
                self.jianCangIdx = 0
                self.lastBuyPrice = day[self.priceToUse]

            if self.pos == POSITION.FULL and self.stopSellCheck(day):
                self.action('sell', day)

            if self.pos != POSITION.EMPTY:
                sellPct = self.sellHighCheck(day)
                if sellPct > 0:
                    self.action('sell', day, sellPct)

            df.loc[i, 'value'] = self.getAccountValue(day)

        currentValue = df.iloc[-1]['value']
        winR, numTrans = self.getWinRatio()
        holdDays = self.getTotalHoldDays()
        
        if drawing:
            self.plot(df.iloc[len(df) - simDays:])
        simLog.info('%s, %s, %.3f, %.3f, %d, %.3f, %.3f, %d' %(self.name, 
                                self.sh.getSymb(), currentValue, winR, numTrans, 
                                self.minValue, self.maxValue, holdDays))


