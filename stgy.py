import pandas as pd
from config import *
import matplotlib.pyplot as plt


class Stgy():

    def __init__(self, sh, priceToUse='close', init=10000):

        self.name = 'empty'
        self.sh = sh 

        self.priceToUse = priceToUse
        self.pos = POSITION.EMPTY
        self.balance = {'cash': init, self.sh.getSymb(): 0}
        self.buyPrice = []
        self.sellPrice = []
        self.buyDate = []
        self.sellDate = []
        self.maxValue = 0
        self.minValue = MAX_INTEGER


    def getAccountValue(self, day):

        symb = self.sh.getSymb()
        value = self.balance['cash'] + self.balance[symb] * day[self.priceToUse]
        if value > self.maxValue:
            self.maxValue = value
        if value < self.minValue:
            self.minValue = value

        return value


    def getWinRatio(self):

        win = 0
        loss = 0
        for i in range(len(self.sellPrice)):
            if self.buyPrice[i] <= self.sellPrice[i]:
                win += 1
            else:
                loss += 1

        if win + loss == 0:
            winR = 0
        else:
            winR = win / (win + loss)
        return winR, win + loss


    def getTotalHoldDays(self):

        days = 0
        for i in range(len(self.sellDate)):
            days += getDaysInterval(self.buyDate[i], self.sellDate[i])
        return days


    def action(self, do, day, percent=1, priceToUse=''):

        symb = self.sh.getSymb()
        date = day['datetime'] 
        if priceToUse == '':
            priceToUse = self.priceToUse
        
        if do == 'buy':
            qty = self.balance['cash'] * percent // day[priceToUse]
            buyPrice = day[priceToUse]
            self.buyPrice.append(buyPrice)
            self.buyDate.append(date)

            self.balance[symb] += qty
            self.balance['cash'] -=  self.balance[symb] * buyPrice

            if percent == 1:
                self.pos = POSITION.FULL
            else:
                self.pos = POSITION.PARTIAL

            logger.info('%s %s %s %s %d %.3f' \
                                    %(self.name, symb, do, date, qty, self.buyPrice[-1]) )

        elif do == 'sell':

            sellPrice = day[priceToUse]
            if percent == 1:
                qty = self.balance[symb]
            else:
                qty = min(int(percent * self.getAccountValue(day) // sellPrice), self.balance[symb])

            if qty == self.balance[symb]:
                self.pos = POSITION.EMPTY
            elif qty < self.balance[symb]:
                self.pos = POSITION.PARTIAL

            if qty == 0:
                return 

            self.sellPrice.append(sellPrice)
            self.sellDate.append(date)
            # transNet = sellPrice - self.buyPrice[-1]
            # holdDays = getDaysInterval(self.buyDate[-1], date)

            self.balance['cash'] += qty * sellPrice
            self.balance[symb] -= qty


            logger.info('%s %s %s %s %d %.3f' \
                                    %(self.name, symb, do, date, qty, sellPrice) ) 

            # logger.info('%s %s buy %s %d %.3f sell %s %d %.3f %.3f %d' \
            #     %(self.name, symb, self.buyDate[-1], qty, self.buyPrice[-1], 
            #        date, qty, sellPrice, transNet, holdDays) )



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
        plt.close('all') 
            