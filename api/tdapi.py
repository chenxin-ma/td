import tdameritrade as td
from config.config import *
import pandas as pd
from os import listdir
from os.path import isfile, join
import logging


class TDAPI:

    def __init__(self):
        self.client = td.TDClient(consumer_id, refresh_token, access_token, [account_id])


    def pullHistPriceForAll(self, symbList=[]):
        
        if (len(symbList) == 0):
            sybms = pd.read_csv(datapath / 'symbols/all.csv')['Symbol'].values
        else:
            sybms = symbList

        for i in tqdm(range(len(sybms))):
            symb = sybms[i] 
            try:
                filename = datapath / 'historical_daily/single/{}.csv'.format(symb)

                if path.exists(filename):
                    continue

                o0 = self.client.historyDF(symb, periodType='year',
                                    period='20',
                                    frequencyType='daily',
                                    frequency='1',
                                    needExtendedHoursData=False,
                                    startDate='946731600000', #endDate=''
                           )
                o0['datetime'] = o0['datetime'].astype(str).str.split(' ').str[0]
                o0.to_csv(filename, index=False, float_format='%.3f')
            except:
                continue



    def pullTodayPriceForAllBatch(self):

        symbAll = [f[:-4] for f in listdir(datapath / 'historical_daily/single/') 
                 if isfile(join(datapath / 'historical_daily/single', f)) and f.endswith('.csv')]
        symbAll = sorted(symbAll)

        today_date = pd.Timestamp.now().strftime("%Y-%m-%d")
        bs = 100

        for i in tqdm(range(len(symbAll) // bs + 1)):
            strs = ','.join([symb for symb in symbAll[i * bs : (i + 1) * bs]])

            oBatch = self.client.quoteDF(strs)
            oBatch['datetime'] = today_date

            oBatch_ = oBatch[['symbol','openPrice','highPrice','lowPrice','regularMarketLastPrice',
                                    'totalVolume','datetime']].copy()
            oBatch_ = oBatch_.round(3)

            for index, row in oBatch_.iterrows():
                symb = row['symbol']
                try:
                    oSymb = pd.read_csv(datapath / 'historical_daily/single/{}.csv'.format(symb))

                    if oSymb.iloc[-1]['datetime'] == today_date:
                        oSymb = oSymb.iloc[:-1].copy()

                    rowToday = row[['openPrice','highPrice','lowPrice','regularMarketLastPrice',
                                        'totalVolume','datetime']].values

                    oSymb.loc[len(oSymb)] = rowToday
                    oSymb.to_csv(datapath / 'historical_daily/single/{}.csv'.format(symb), 
                                            index=False, float_format='%.3f')
                except:
                    logger.warning('%s fails to update today.' %symb)
                    print(symb)
                    continue




    def pullTodayPrice(self, symbList=[]):

        today_date = pd.Timestamp.now().strftime("%Y-%m-%d")

        if (len(symbList) == 0):
            sybms = pd.read_csv(datapath / 'symbols/options.csv')['Symbol'].sort_values().values
        else:
            sybms = symbList
        for i in tqdm(range(len(sybms))):

            oBatch = self.client.quoteDF(symb)
            oBatch['datetime'] = today_date

            oBatch_ = oBatch[['symbol','openPrice','highPrice','lowPrice','regularMarketLastPrice',
                                    'totalVolume','datetime']].copy()
            oBatch_ = oBatch_.round(3)

            oSymb = pd.read_csv(datapath / 'historical_daily/single/{}.csv'.format(symb))

            if oSymb.iloc[-1]['datetime'] == today_date:
                oSymb = oSymb.iloc[:-1].copy()

            rowToday = oBatch_.iloc[0][['openPrice','highPrice','lowPrice','regularMarketLastPrice',
                                'totalVolume','datetime']].values

            oSymb.loc[len(oSymb)] = rowToday
            oSymb.to_csv(datapath / 'historical_daily/single/{}.csv'.format(symb), 
                                    index=False, float_format='%.3f')



    def pullOptionDfForAll(self, symbList=[]):
        
        cols = ['putCall','description','bid','ask','mark','delta','gamma','theta','vega','rho',
            'totalVolume','openInterest','strikePrice','expirationDate']
        today_date = pd.Timestamp.now().strftime("%Y-%m-%d")

        if (len(symbList) == 0):
            sybms = pd.read_csv(datapath / 'symbols/options.csv')['Symbol'].sort_values().values
        else:
            sybms = symbList

        savepath = datapath / 'historical_option_daily/single/{}'.format(today_date)
        if not os.path.exists(savepath):
            os.makedirs(savepath)

        for i in tqdm(range(len(sybms))):
            symb = sybms[i] 
            while 1:
                try:
                    filename = savepath / '{}.csv'.format(symb)

                    if path.exists(filename):
                        break

                    o0 = self.client.optionsDF(symb)

                    if o0 is None:
                        break

                    o0 = o0[cols]
                    o0['expirationDate'] = o0['expirationDate'].dt.date

                    o0.to_csv(filename, index=False, float_format='%.3f')
                    break
                except:
                    time.sleep(0.1)
                    continue


    def pullFundamentalForAll(self):

        sybms = pd.read_csv(datapath / 'symbols/all.csv')['Symbol'].values

        bs = 50
        dic_fund = {}
        for i in tqdm(range(len(sybms) // bs + 1)):
            
            strs = ','.join(sybms[i * bs : (i + 1) * bs])
            while 1:
                try:
                    res = c.fundamental(strs)
                    break
                except:
                    continue
                
            dic_fund = {**dic_fund , **res}

        with open(datapath / 'fundamental/all.json', 'w') as fp:
            json.dump(dic_fund, fp, sort_keys=True, indent=4)
        