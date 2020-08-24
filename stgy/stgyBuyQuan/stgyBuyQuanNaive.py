from .stgyBuyQuan import StgyBuyQuan

class StgyBuyQuanNaive(StgyBuyQuan):

    def __init__(self):

        StgyBuyQuan.__init__(self)
        self.name = 'StgyBuyQuanNaive'


    def sharesToBuy(self, suggestBuyShares):

        return suggestBuyShares

