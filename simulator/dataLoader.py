import pandas as pd
from config.config import *
from dto.singleStockDTO import SingleStockDTO
from dto.multiStockDTO import MultiStockDTO

class DataLoader:

    def __init__(self, symbs, firstDay=''):

        self.symbs = symbs
        self.firstDay = firstDay


    def loadDailyData(self):

        dailyData = {}

        dailyDataPath = datapath / 'historical_daily/single/'
        loadFormat = {'open': 'float', 'high': 'float', 'low': 'float', 'close': 'float',
                           'datetime': 'str', 'symb': 'str'}

        logger.info('DataLoader: loading daily data...')

        lastDates = set()
        firstDates = set()
        for idx, symb in enumerate(tqdm(self.symbs)):

            filePath = dailyDataPath / '{}.csv'.format(symb)
            if not path.exists(filePath):
                logger.warning('DataLoader: %s data not exist!' %symb)
                continue

            oSymb = pd.read_csv(filePath, dtype=loadFormat)

            ssd = SingleStockDTO(oSymb, symb, self.firstDay)

            lastDates.add(ssd.getDf().iloc[-1]['datetime'])
            firstDates.add(ssd.getDf().iloc[0]['datetime'])

            dailyData[symb] = ssd

        if len(lastDates) == 1 and len(firstDates) == 1:
            logger.info('DataLoader: loading %d stocks, all good.' %(len(self.symbs)))
        elif len(lastDates) > 1 and len(firstDates) == 1:
            logger.info('DataLoader: loading %d stocks, last dates inconsistent!' %(len(self.symbs)))
        elif len(lastDates) == 1 and len(firstDates) > 1:
            logger.info('DataLoader: loading %d stocks, first dates inconsistent!' %(len(self.symbs)))
        else:
            logger.info('DataLoader: loading %d stocks, first and last dates inconsistent!' %(len(self.symbs)))

        return MultiStockDTO(dailyData, self.firstDay)

