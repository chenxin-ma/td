from .stgySell import StgySell

class StgySellNaive(StgySell):

    def __init__(self, lastDayIdx):

        StgySell.__init__(self)
        self.name = 'StgySellNaive'
        self.lastDayIdx = lastDayIdx


    def shouldSell(self, symb, date, dateIdx):

        if self.lastDayIdx == dateIdx:
            return 100

        return 0


