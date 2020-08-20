import os
from tqdm import tqdm
from tdapi import *
from data import *
from stgy_ma import Stgy_MA
from stgy_breakout import Stgy_BO
from stgy_buyAndHold import Stgy_BAH
from stgy_cupHandle import Stgy_CH
from shutil import copyfile

def main():


    td = TDAPI()
    # td.pullHistPriceForAll()
    td.pullOptionDfForAll(its=1)
    # td.pullTodayPriceForAllBatch()
    # $td.pullTodayPrice('ABCB')
    return 

    lSymb = 'forest'
    sybms = pd.read_csv(datapath / 'lists/{}.csv'.format(lSymb))['Symbol'].values
    beginDate = '2020-08-18'
    # sybms = ['THC']
    for idx, symb in enumerate(tqdm(sybms)):

        o0 = pd.read_csv(datapath / 'historical_daily/single/{}.csv'.format(symb), 
                     dtype={'open': 'float', 'high': 'float', 'low': 'float', 'close': 'float',
                           'datetime': 'str', 'symb': 'str'})

        sh = StockHistory(o0, symb)

        # stgy_MA = Stgy_MA(sh)
        # stgy_MA.simulation(begin=beginDate)

        # stgy_BO = Stgyx_BO(sh)
        # stgy_BO.simulation(begin=beginDate)

        stgy_CH = Stgy_CH(sh, '2019-01-01')
        stgy_CH.simulation(begin=beginDate)

        # stgy_BAH = Stgy_BAH(sh)
        # stgy_BAH.simulation(begin=beginDate)

    copyfile(simLogPath, root / 'res/{}_{}_sim.csv'.format(lSymb, beginDate))
    copyfile(loggerpath, root / 'res/{}_{}_trans.txt'.format(lSymb, beginDate))


if __name__ == "__main__":

    main()