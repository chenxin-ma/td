class ActionBook:

    def __init__(self):

        self.actions = {}




    def getSymbActions(self, symb):

        if symb not in self.actions:
            logger.error('ActionBook: symb %s not exsits!')
            return None

        return self.actions[symb]



    def update(self, do, symb, price, shares, date):

        if symb not in self.actions:
            self.actions[symb] = []

        self.actions[symb].append({'type': do, 'date': date, 
                             'price': price, 'shares': shares})


    def getLastBuyAction(self, symb):

        actionList = self.actions[symb]

        for i in range(len(actionList)):
            if actionList[-i - 1]['type'] == 'buy':
                return actionList[-i - 1]

        return None


    def isAfterBuy(self, symb):
        return len(self.actions[symb]) > 0 and self.actions[symb][-1]['type'] == 'buy'