from .stgyStop import StgyStop

class StgyStopNaive(StgyStop):

    def __init__(self, multiStockDTO, actionBook, balanceBook):

        StgyStop.__init__(self, multiStockDTO, actionBook, balanceBook)
        self.name = 'StgyStopNaive'





