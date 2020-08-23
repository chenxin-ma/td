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


    def update(self, symb, shares, price):

        if symb not in self.balance:
            self.balance[symb] = shares

        else:
            self.balance[symb] += shares

        if self.balance[symb] == 0:
            del self.balance[symb]
            
        if self.balance[symb] < 0:
            logger.error('BalanceBook: short a symb(%s) is not supported yet!' %(symb) )


        self.balance['cash'] -= shares * price
        if self.balance['cash'] < 0:
            logger.error('BalanceBook: Margin account is not supported yet!' )
