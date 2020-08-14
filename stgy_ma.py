from stgy import *

class Stgy_MA(Stgy):

    def __init__(self, sh, short=5, med=10, far=20, farest=30, ema=False, priceToUse='close', init=10000):
        
        Stgy.__init__(self, sh, priceToUse, init)
        self.name = 'MA'

        self.short = short
        self.med = med
        self.far = far
        self.farest = farest
        self.ema = ema
        if ema:
            self.maType = 'ema'
        else:
            self.maType = 'sma'

        self.columnShort = self.maType + str(short)
        self.columnMed = self.maType + str(med)
        self.columnFar = self.maType + str(far)
        self.columnFarest = self.maType + str(farest)

        self.generateMAs()



    def generateMAs(self):

        if self.maType == 'ema':
            self.sh.getEMA(self.short, self.priceToUse)
            self.sh.getEMA(self.med, self.priceToUse)
            self.sh.getEMA(self.far, self.priceToUse)
            self.sh.getEMA(self.farest, self.priceToUse)
        else:
            self.sh.getSMA(self.short, self.priceToUse)
            self.sh.getSMA(self.med, self.priceToUse)
            self.sh.getSMA(self.far, self.priceToUse)
            self.sh.getSMA(self.farest, self.priceToUse)
        logger.debug('MA data for %s generated.' %self.sh.getSymb())


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


    def tooHigh(self, day):
        if day['close'] > day[self.columnShort] * (1 + 0.07):
            return True
        return False


    def simulation(self, begin='2000-01-01', end=''):

        if end == '':
            end = pd.Timestamp.now().strftime("%Y-%m-%d")

        df = self.sh.getDf(begin, end).copy().reset_index()
        df['value'] = self.balance['cash']

        day = df.iloc[1]
        dayM1 = df.iloc[0]


        for i in range(2, len(df)):
        # for idx, day in self.sh.getDf(begin, end).iterrows():

            dayM2 = dayM1
            dayM1 = day
            day = df.iloc[i]
            action = 0

            # logger.debug('Simulation on date: %s.' %day['datetime'] )
            if pd.isna(day[self.columnFar]):
                continue


            if self.pos == POSITION.EMPTY and self.duoPai(day) and not self.duoPai(dayM1):
                if not self.isStrugle(day):
                    self.action('buy', day) 
                    self.pos = POSITION.FULL
                    action == 1

            if self.pos == POSITION.FULL and self.kongPai(day):
                self.action('sell', day)
                self.pos = POSITION.EMPTY
                action == 1

            if action == 0 and self.pos == POSITION.FULL and self.isCrossDown(day, dayM1, dayM2):
                self.action('sell', day)
                self.pos = POSITION.EMPTY
                action == 1

            elif action == 0 and self.pos == POSITION.EMPTY and self.isCrossUp(day, dayM1, dayM2):
                self.action('buy', day) 
                self.pos = POSITION.FULL
                action == 1

            if action == 0 and self.pos == POSITION.FULL and self.tooHigh(day):
                self.action('sell', day)
                self.pos = POSITION.EMPTY
                action == 1

            df.loc[i, 'value'] = self.getAccountValue(day)

        currentValue = self.getAccountValue(day)
        winR, numTrans = self.getWinRatio()
        holdDays = self.getTotalHoldDays()
        self.plot(df)
        simLog.info('MA, %s, %.3f, %.3f, %d, %.3f, %.3f, %d' %(self.sh.getSymb(), currentValue, winR, numTrans, 
                                self.minValue, self.maxValue, holdDays))



    def plot(self, df):

        fig, axs = plt.subplots(figsize=(12, 7), nrows=2, ncols=1)

        axs[0].plot(df['datetime'], df['close'], color='red')
        # axs[0].plot(df['datetime'], df[self.columnShort], color='cyan')
        # axs[0].plot(df['datetime'], df[self.columnMed], color='deepskyblue')
        # axs[0].plot(df['datetime'], df[self.columnFar], color='plum')
        # axs[0].plot(df['datetime'], df[self.columnFarest], color='purple')
        axs[0].plot(self.buyDate, df[df['datetime'].isin(self.buyDate)]['close'],
                                     '^', markersize=10, color='m')
        axs[0].plot(self.sellDate, df[df['datetime'].isin(self.sellDate)]['close'],
                                     'v', markersize=10, color='black')
        axs[0].set_xticks(axs[0].get_xticks()[::100])

        axs[1].plot(df['datetime'], df['value'])
        axs[1].plot(self.buyDate, df[df['datetime'].isin(self.buyDate)]['value'],
                                     '^', markersize=10, color='m')
        axs[1].plot(self.sellDate, df[df['datetime'].isin(self.sellDate)]['value'],
                                     'v', markersize=10, color='black')
        axs[1].set_xticks(axs[1].get_xticks()[::100])


        figPath = root / 'res/plots/{}'.format(self.name)
        if not os.path.exists(figPath):
            os.makedirs(figPath)
        plt.savefig(figPath / '{}.png'.format(self.sh.getSymb()))
        plt.close()
