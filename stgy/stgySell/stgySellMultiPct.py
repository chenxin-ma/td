from .stgySell import StgySell

class StgySellMultiPct(StgySell):

    def __init__(self, multiStockDTO, actionBook, balanceBook):

        StgySell.__init__(self, multiStockDTO, actionBook, balanceBook)
        self.name = 'StgySellMultiPct'

        self.jianCangProfitThres = [1.05, 1.1, 1.2, 1.3, 1.4, 1.5]
        self.jianCangPos = [0.1, 0.25, 0.3, 0.15, 0.1, 1]
        self.jianCangZhiYingThres = [1.01, 1.04, 1.12, 1.2, 1.25, 1.4]
        self.jianCangIdx = 0
        self.maxTimes = len(self.jianCangProfitThres)


    def shouldSell(self, symb, date, dateIdx):

        jianCangPct = 0
        datePrice = singleDTO.getRowDate(date)[self.priceToUse]
		lastBuyPrice = ''

        while self.jianCangIdx < self.maxTimes:
            if datePrice >= lastBuyPrice * self.jianCangProfitThres[self.jianCangIdx]:
                jianCangPct += self.jianCangPos[self.jianCangIdx]
                self.jianCangIdx += 1
            else:
                break

        if self.jianCangIdx > 0 and self.jianCangIdx < self.maxTimes:
            if day[self.priceToUse] / self.lastBuyPrice < self.jianCangZhiYingThres[self.jianCangIdx - 1]:
                return self.balanceBook.getSymbShares(symb)

        return int(round(self.balanceBook.getSymbShares(symb) * jianCangPct))
