from .stgyStop import StgyStop

class StgyStopNaive(StgyStop):

    def __init__(self, actionBook, balanceBook):

        StgyStop.__init__(self, actionBook, balanceBook)
        self.name = 'StgyStopNaive'





