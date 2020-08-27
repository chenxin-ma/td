from util.utils import *

class Referee:

    def __init__(self, multiStockDTO, actionBook, balanceBook, netValue):

        self.multiStockDTO = multiStockDTO
        self.actionBook = actionBook
        self.balanceBook = balanceBook
        self.netValue = netValue



    def winRatio(self):

        win = 0
        loss = 0

        for symb in self.actionBook.actions:
            actions = self.actionBook.getSymbActions(symb)

            i = 0
            while i < len(actions):

                act = actions[i]

                if act['type'] == 'buy':
                    buyPrice = act['price']
                    i += 1
                    if i >= len(actions):
                        break
                        
                    sellPrice = actions[i]['price']

                    if sellPrice > buyPrice:
                        win += 1
                    else:
                        loss += 1

                    while (i < len(actions) and actions[i]['type'] != 'buy'):
                        i += 1

        return win / (win + loss)



    def yearlyReturn(self):

        keys = list(self.netValue)
        dayFirst = min(keys)
        dayLast = max(keys)

        ndays = getDaysInterval(dayFirst, dayLast)

        overallReturn = self.netValue[dayLast] / self.netValue[dayFirst]

        yearlyReturn = overallReturn ** (1 / (ndays / 365)) - 1

        return yearlyReturn * 100


