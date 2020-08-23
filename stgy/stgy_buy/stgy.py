import pandas as pd
import matplotlib.pyplot as plt
from config.config import *

class Stgy():

    def __init__(self, sh, date_start='', priceToUse='close', init=10000):

        self.name = 'empty'
        self.sh = sh.__copy__()
        if date_start != '':
            self.sh.cutFromDate(date_start) 


        self.priceToUse = priceToUse
        self.pos = POSITION.EMPTY
        self.balance = {'cash': init, self.sh.getSymb(): 0}
        self.actionBook = {'actions':[]}

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
        i = 0
        while i < len(self.actionBook['actions']):
            
            action = self.actionBook['actions'][i]
            if action['type'] == 'buy':
                buyPrice = action['price']
            
            firstSellPrice = -1

            i += 1
            while i < len(self.actionBook['actions']):
                action = self.actionBook['actions'][i]

                if action['type'] == 'sell' and firstSellPrice == -1:
                    firstSellPrice = action['price']
                    if (buyPrice > firstSellPrice):
                        loss += 1
                    else:
                        win += 1
                if (firstSellPrice != -1 and action['type'] == 'buy' or i == len(self.actionBook['actions']) - 1):
                    break 
                i += 1

        winR = 0 if win + loss == 0 else win / (win + loss)

        return winR, win + loss


    def getTotalHoldDays(self):

        days = 0
        i = 0

        while i < len(self.actionBook['actions']):
            action = self.actionBook['actions'][i]

            if action['type'] == 'buy':
                buyDate = action['date']
            
            LastSellDate = ''
            i += 1
            while i < len(self.actionBook['actions']):
                action = self.actionBook['actions'][i]
                if action['type'] == 'sell':
                    LastSellDate = action['date']
                if (LastSellDate != '' and action['type'] == 'buy' or i == len(self.actionBook['actions']) - 1):
                    days += getDaysInterval(buyDate, LastSellDate)
                    break 
                i += 1

        return days


    def actionToBook(self, do, day, price, qty):
        self.actionBook['actions'].append({'type': do, 'date': day['datetime'], 
                                         'price': price, 'qty': qty})

    def action(self, do, day, percent=1, priceToUse=''):

        symb = self.sh.getSymb()
        date = day['datetime'] 
        if priceToUse == '':
            priceToUse = self.priceToUse
        
        if do == 'buy':
            qty = self.balance['cash'] * percent // day[priceToUse]
            buyPrice = day[priceToUse]

            self.actionToBook(do, day, buyPrice, qty)

            self.balance[symb] += qty
            self.balance['cash'] -=  self.balance[symb] * buyPrice

            if percent == 1:
                self.pos = POSITION.FULL
            else:
                self.pos = POSITION.PARTIAL

            logger.info('%s %s %s %s %d %.3f' \
                                    %(self.name, symb, do, date, qty, buyPrice) )

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

            self.actionToBook(do, day, sellPrice, qty)
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

        self.buyDate = []
        self.sellDate = []
        for action in self.actionBook['actions']:
            if action['type'] == 'buy':
                self.buyDate.append(action['date'])
            else:
                self.sellDate.append(action['date'])


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
            