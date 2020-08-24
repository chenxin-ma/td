from .stgyBuy import StgyBuy


class StgyBuy4MA(StgyBuy):

    def __init__(self, multiStockDTO, actionBook, balanceBook, 
    				short=5, med=10, far=20, farest=30, ema=False):

        StgyBuy.__init__(self, multiStockDTO, actionBook, balanceBook)
        self.name = 'StgyBuy4MA'

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


    def shouldBuy(self, symb, date, dateIdx):

        if self.firstDayIdx == dateIdx:
            return 100

        return 0


