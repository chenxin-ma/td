from .stgyBuy import StgyBuy


class StgyBuyNewHigh(StgyBuy):

    def __init__(self, multiStockDTO, actionBook, balanceBook,
                 backFar=2000, backClose=5, breakR=0.02, priceToUse='close'):

        StgyBuy.__init__(self, multiStockDTO, actionBook, balanceBook)
        self.name = 'StgyBuyNewHigh'

        self.backFar = backFar
        self.backClose = backClose

        self.breakR = breakR
        self.earliest = 0

        self.priceToUse = priceToUse



    def shouldBuy(self, symb, date, dateIdx):

        if symb in self.balanceBook.balance:
            return 0

        singleDTO = self.multiStockDTO.getSymbSingleDTO(symb)

        prevHigh = singleDTO.getHighestPrice(daysBack=self.backFar, date=date, priceToUse='high')

        datePrice = singleDTO.getRowDate(date)[self.priceToUse]
        if datePrice >= prevHigh and datePrice <= prevHigh * (1 + self.breakR):

            prevHighFar = singleDTO.getHighestPrice(daysBack=self.backFar, date=date,
                            dateSlide=-self.backClose, priceToUse='high')

            if prevHighFar == prevHigh:
                return 1

        return 0




