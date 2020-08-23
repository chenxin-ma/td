class BalanceBook:

    def __init__(self, initValue):

        self.balance = {}
        self.balance['cash'] = initValue



    def getCash(self):
        return self.balance['cash']



    def getSymbShares(self, symb):

        if symb not in self.balance:
            logger.error('BalanceBook: symb %s not exsits!')
            return None

        return self.balance[symb]


    def getCurrentHolding(self):

        holding = []
        for symb in self.balance:
            if symb == 'cash':
                continue

            holding.append(symb)

        return holding