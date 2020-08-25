from .stgyBuy import StgyBuy


class StgyBuyCupHandle(StgyBuy):


    def __init__(self, multiStockDTO, actionBook, balanceBook,
                 prevHighThres=0.04, prevNearThres=0.02, priceToUse='close'):

        StgyBuy.__init__(self, multiStockDTO, actionBook, balanceBook)
        self.name = 'StgyBuyCupHandle'

        self.prevHighThres = prevHighThres
        self.prevNearThres = prevNearThres



    def shouldBuy(self, symb, date, dateIdx):

        if symb in self.balanceBook.balance:
            return 0

        dfWindow = self.multiStockDTO.getSymbSingleDTO(symb).getDf(end=date)

        row = self.multiStockDTO.getSymbSingleDTO(symb).getRowDate(date)
        if row == None:
            return 0
        todayHigh = row['high']

        prevHigh = todayHigh * (1 + self.prevHighThres)
        resistantBoxLow = todayHigh * (1 - self.prevNearThres)
        resistantBoxHigh = todayHigh * (1 + self.prevNearThres)
        
        daysToPrevHighIdx = dfWindow[dfWindow['high'].gt(prevHigh)].index
        if len(daysToPrevHighIdx) == 0:
            return False

        earliestHighIdx = 1
        for i in range(len(daysToPrevHighIdx) - 1):
            if dfWindow.iloc[daysToPrevHighIdx[-i-2] : daysToPrevHighIdx[-i-1]]['high'].max() <= prevHigh:
                earliestHighIdx = i + 2
            else:
                break

        daysToPrevHigh = len(dfWindow) - daysToPrevHighIdx[-earliestHighIdx]
        if daysToPrevHigh < 20:
            return False

        dfFocus = dfWindow.iloc[daysToPrevHighIdx[-earliestHighIdx]:]
        inBoxIdx = dfFocus[(dfFocus['high'].gt(resistantBoxLow))].index


        prevIdx = -1
        drawdownCount = 0
        enoughDrawback = False
        for idx in inBoxIdx:
            if prevIdx == -1:
                prevIdx = idx
                continue

            if (idx - prevIdx >= 5):
                lowInStint = dfFocus.loc[prevIdx : idx]['low'].min()
                # print(day['datetime'], inBoxIdx, daysToPrevHigh, idx)

                if lowInStint < resistantBoxLow * 0.95:
                    drawdownCount += 1
                if lowInStint < resistantBoxLow * 0.8:
                    enoughDrawback = True
            
            prevIdx = idx

        if drawdownCount >= 2 and enoughDrawback == True:
            return 1

        return 0