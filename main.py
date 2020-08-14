import os
from tqdm import tqdm
from tdapi import *
from data import *
from stgy_ma import Stgy_MA
from stgy_buyAndHold import Stgy_BAH
from shutil import copyfile

def main():


    # td = TDAPI()
    # td.pullHistPriceForAllSymb()
    # td.pullTodayPriceForAll()

    lSymb = 'ndx100'
    sybms = pd.read_csv(datapath / 'lists/{}.csv'.format(lSymb))['Symbol'].values
    beginDate = '2018-01-01'
    # sybms = ['AAL']
    for symb in sybms:
        o0 = pd.read_csv(datapath / 'historical_daily/single/{}.csv'.format(symb), 
                     dtype={'open': 'float', 'high': 'float', 'low': 'float', 'close': 'float',
                           'datetime': 'str', 'symb': 'str'})

        sh = StockHistory(o0, symb)

        stgy_MA = Stgy_MA(sh)
        stgy_MA.simulation(begin=beginDate)

        stgy_BAH = Stgy_BAH(sh)
        stgy_BAH.simulation(begin=beginDate)

    copyfile(simLogPath, root / 'res/{}_{}_sim.csv'.format(lSymb, beginDate))
    copyfile(loggerpath, root / 'res/{}_{}_trans.txt'.format(lSymb, beginDate))


if __name__ == "__main__":

    main()