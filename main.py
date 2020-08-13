import os
from tqdm import tqdm
from tdapi import *
from data import *
from stgy_ma import Stgy_MA


def main():

    logging.basicConfig(level=logging.DEBUG)

    td = TDAPI()
    # td.pullHistPriceForAllSymb()
    # td.pullTodayPriceForAll()

    symb = 'ROKU'
    o0 = pd.read_csv(datapath / 'historical_daily/single/{}.csv'.format(symb), 
                 dtype={'open': 'float', 'high': 'float', 'low': 'float', 'close': 'float',
                       'datetime': 'str', 'symb': 'str'})

    sh = StockHistory(o0, symb)

    # print(sh.getHighestPrice())
    # print(sh.getSMA(21))

    stgy_MA = Stgy_MA(sh)
    stgy_MA.simulation()

if __name__ == "__main__":

    main()