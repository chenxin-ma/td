from .stgyBuy import StgyBuy

class StgyBuyNaive(StgyBuy):

    def __init__(self, firstDayIdx):

        StgyBuy.__init__(self)
        self.name = 'StgyBuyNaive'
        self.firstDayIdx = firstDayIdx


    def shouldBuy(self, symb, date, dateIdx):

        if self.firstDayIdx == dateIdx:
            return 100

        return 0


