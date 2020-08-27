import os
from tqdm import tqdm
from shutil import copyfile
from config.config import *
from api import *
from dto import *
from simulator import *
import pandas as pd
import argparse


def updateDB():


    td = TDAPI()
    # td.pullHistPriceForAll()
    td.pullOptionDfForAll()
    # td.pullTodayPriceForAllBatch()
    # td.pullTodayPrice('BIGC')


def main():


    lSymb = 'sp500'
    symbs = pd.read_csv(datapath / 'lists/{}.csv'.format(lSymb))['Symbol'].values
    beginDate = '2018-01-01'
    # symbs = ['AAPL']

    ['Naive', 'Naive', 'Naive', 'Naive']
    ['4MA', 'Naive', '4MA', 'Naive']
    ['NewHigh', 'NewHigh', 'MultiPct', 'Naive']
    ['CupHandle', 'NewHigh', 'MultiPct', 'Naive']
    simulator = Simulator(symbs, 'CupHandle', 'NewHigh', 'MultiPct', 'Naive', 
                            beginDate=beginDate,
                            endDate='',
                            dataFirstDay='2017-01-01'
                            )

    simulator.run()
    return 

    # symbs = ['THC']
    for idx, symb in enumerate(tqdm(symbs)):

        o0 = pd.read_csv(datapath / 'historical_daily/single/{}.csv'.format(symb), 
                     dtype={'open': 'float', 'high': 'float', 'low': 'float', 'close': 'float',
                           'datetime': 'str', 'symb': 'str'})

        sh = SingleStockDTO(o0, symb)

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
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=str, required=True, help="")
    args = parser.parse_args()

    if args.mode == '1':
        main()
    elif args.mode == '2':
        updateDB()