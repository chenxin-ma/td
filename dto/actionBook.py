class ActionBook:

    def __init__(self):

        self.actions = {}


    def getSymbActions(self, symb):

        if symb not in self.actions:
            logger.error('ActionBook: symb %s not exsits!')
            return None

        return self.actions['symb']