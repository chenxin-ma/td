from .stgyBuyQuan import StgyBuyQuan
from config.config import *

class StgyBuyQuanNaive(StgyBuyQuan):

    def __init__(self, multiStockDTO, actionBook, balanceBook, maxShareOnce=1000, maxPct=0.1):

        StgyBuyQuan.__init__(self, multiStockDTO, actionBook, balanceBook)
        self.name = 'StgyBuyQuanNaive'

        self.maxShareOnce = maxShareOnce
        self.maxPct = maxPct


    def sharesToBuy(self, suggestBuyShares, date, net):

        res = []
        cash = self.balanceBook.getCash()
        for symb in suggestBuyShares:
            closePrice = self.multiStockDTO.getSymbClosePriceAtDate(symb, date)

            share = min(net * self.maxPct // closePrice, cash // closePrice)
            share = min(self.maxShareOnce, share)

            cash -= share * closePrice
            res.append(share)
            if share == 0:
                transLog.info('%s is at a buy point, but cash is not enough.' %(symb) )

        return res


        

