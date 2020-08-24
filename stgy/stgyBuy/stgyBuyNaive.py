from .stgyBuy import StgyBuy

class StgyBuyNaive(StgyBuy):

    def __init__(self, multiStockDTO, actionBook, balanceBook, firstDayIdx):

        StgyBuy.__init__(self, multiStockDTO, actionBook, balanceBook)
        self.name = 'StgyBuyNaive'
        self.firstDayIdx = firstDayIdx


    def shouldBuy(self, symb, date, dateIdx):

        if self.firstDayIdx == dateIdx:
            return 100

        return 0


