from .stgyBuyQuan import StgyBuyQuan

class StgyBuyQuanNaive(StgyBuyQuan):

    def __init__(self, actionBook, balanceBook):

        StgyBuyQuan.__init__(self, actionBook, balanceBook)
        self.name = 'StgyBuyQuanNaive'


    def sharesToBuy(self, suggestBuyShares):

        return suggestBuyShares

