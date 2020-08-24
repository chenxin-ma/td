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
