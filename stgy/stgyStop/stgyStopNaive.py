from .stgyStop import StgyStop

class StgyStopNaive(StgyStop):

    def __init__(self, multiStockDTO, actionBook, balanceBook, stopR=0.06):

        StgyStop.__init__(self, multiStockDTO, actionBook, balanceBook)
        self.name = 'StgyStopNaive'
        self.stopR = stopR


    def shouldStop(self, symb, date):

        if self.balanceBook.getSymbShares(symb) == 0:
            return False, None

        singleDTO = self.multiStockDTO.getSymbSingleDTO(symb)
        lowPrice = singleDTO.getRowDate(date)['low']

        lastBuyPrice = self.actionBook.getLastBuyAction(symb)['price']

        if lowPrice < lastBuyPrice * (1 - self.stopR):
            return True, lowPrice

        return False, None



