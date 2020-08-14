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


    def action(self, do, day):

        symb = self.sh.getSymb()
        date = day['datetime'] 
        
        if do == 'buy':
            qty = self.balance['cash'] // day[self.priceToUse]
            buyPrice = day[self.priceToUse]
            self.buyPrice.append(buyPrice)
            self.buyDate.append(date)

            self.balance[symb] += qty
            self.balance['cash'] -=  self.balance[symb] * buyPrice

            # logger.info('%s %s %s %s %d %.3f' \
            #                         %(self.name, symb, do, date, qty, self.buyPrice[-1]) )

        elif do == 'sell':
            qty = self.balance[symb]
            sellPrice = day[self.priceToUse]
            self.sellPrice.append(sellPrice)
            self.sellDate.append(date)
            transNet = sellPrice - self.buyPrice[-1]
            holdDays = getDaysInterval(self.buyDate[-1], date)

            self.balance['cash'] += self.balance[symb] * sellPrice
            self.balance[symb] -= self.balance[symb]

            # logger.info('%s %s %s %s %d %.3f %.3f %d' \
            #                         %(self.name, symb, do, date, qty, sellPrice, transNet, holdDays) ) 

            logger.info('%s %s buy %s %d %.3f sell %s %d %.3f %.3f %d' \
                %(self.name, symb, self.buyDate[-1], qty, self.buyPrice[-1], 
                   date, qty, sellPrice, transNet, holdDays) )


            