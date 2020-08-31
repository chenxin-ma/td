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

        loggerPath.info('TDapi: Begin to merge today\'s option data')
        self.mergeOptionDfForOneDay(today_date)
        loggerPath.info('TDapi: Begin to merge option data for all dates')
        self.mergeOptionAllDays()
        loggerPath.info('TDapi: Begin to detect anomaly option trades.')
        self.anomalyOptionTradeDetector(today_date)



    def mergeOptionDfForOneDay(self, date):

        longTermThres = (pd.Timestamp(date) + pd.DateOffset(months=1)).strftime("%Y-%m-%d")

        optSymb = [f[:-4] for f in listdir(datapath / 'historical_option_daily/single/{}/'.format(date)) 
                         if isfile(join(datapath / 'historical_option_daily/single/{}/'.format(date), f)) and f.endswith('.csv')]

        cols = ['symb','date','callVol','longCVol','putVol','longPVol','pcVolR','ttlVol','callOpen','longCOpen','putOpen','longPOpen','pcOpenR','ttlOpen','vol/Open','vol/Share','open/Share']

        oS = pd.DataFrame(columns=cols)
        for symb in tqdm(optSymb):
            o0 = pd.read_csv(datapath / 'historical_option_daily/single/{}/{}.csv'.format(date,symb) )
            d4 = o0.groupby('putCall')[['totalVolume','openInterest']].sum().unstack().values
            tts = dic_fund[symb]['fundamental']['sharesOutstanding']
            ttlV = d4[0] + d4[1]
            ttlO = d4[2] + d4[3]
            pcVR = d4[1] / d4[0] if d4[0] != 0 else None
            pcOR = d4[3] / d4[2] if d4[2] != 0 else None
            voR = ttlV / ttlO if ttlO != 0 else 0
            vsR = ttlV * 100 / tts if tts != 0 else 0
            osR = ttlO * 100 / tts if tts != 0 else 0
            o0Long = o0[o0['expirationDate'] >= longTermThres]
            if len(o0Long) > 0:
                d4Long = o0Long.groupby('putCall')[['totalVolume','openInterest']].sum().unstack().values
                longCallVol = d4Long[0]
                longPutVol = d4Long[1]
                longCallOpen = d4Long[2]
                longPutOpen = d4Long[3]
            else:
                longCallVol, longPutVol, longCallOpen, longPutOpen = 0, 0, 0, 0
                
            line = [symb, date, d4[0], longCallVol, d4[1], longPutVol, pcVR, ttlV, 
                    d4[2], longCallOpen, d4[3], longPutOpen, pcOR, ttlO, 
                    voR, vsR, osR]
            oS.loc[len(oS)] = line

        oS[['pcVolR','pcOpenR','vol/Open','vol/Share','open/Share']]\
        = oS[['pcVolR','pcOpenR','vol/Open','vol/Share','open/Share']].astype(float)
        oS = oS.round(3)
        oS.to_csv(datapath / 'historical_option_daily/merge/{}.csv'.format(date), index=False, float_format='%.3f')



    def mergeOptionAllDays(self):

        dates = [f for f in listdir(datapath / 'historical_option_daily/single/') 
                         if not isfile(join(datapath / 'historical_option_daily/single/', f))]
        oDaily = {}
        for date in dates:
            oDaily[date] = pd.read_csv(datapath / 'historical_option_daily/merge/{}.csv'.format(date))
        oAll = pd.concat([oDaily[date] for date in oDaily])

        oAll.sort_values(['symb','date']).to_csv(datapath / 'historical_option_daily/all.csv', 
                                            index=False, float_format='%.3f')



    def anomalyOptionTradeDetector(self, todayDate):

        colCheck = ['longCVol','longPVol','longCOpen','longPOpen']
        watch = set()
        longTermThres = (pd.Timestamp(date) + pd.DateOffset(months=1)).strftime("%Y-%m-%d")

        cols = ['date','symb', 'detectedColumn', 'todayValue','pastMean','stockPriceChg','stockVolChg','optionName']
        oWatch = pd.DataFrame(columns=cols)
        for symb, oSymb in oAll.groupby('symb'):
            oSymb = oSymb.sort_values('date')
            todayRow = oSymb.iloc[-1]
            prevRows = oSymb.iloc[-20:-1]
            for col in colCheck:
                if col.endswith('Vol') and todayRow[col] > prevRows[col].mean() * 3 and todayRow[col] > 1000 \
                or col.endswith('Open') and todayRow[col] > prevRows[col].mean() * 1.5 and todayRow[col] > 10000:
                    
                    oSingle = pd.read_csv(datapath / 'historical_daily/single/{}.csv'.format(symb))
                    dayChange = (oSingle.iloc[-1]['close'] / oSingle.iloc[-2]['close'] - 1) * 100
                    volIncrease = oSingle.iloc[-1]['volume'] / oSingle.iloc[-21:-1]['volume'].mean()
                    oOption = pd.read_csv(datapath / 'historical_option_daily/single/{}/{}.csv'.format(todayDate, symb))
                
                    longTermThres = (pd.Timestamp(todayDate) + pd.DateOffset(months=1)).strftime("%Y-%m-%d")
                    o0Long = oOption[oOption['expirationDate'] >= longTermThres]
                    o0LongC = o0Long[o0Long['putCall'] == 'CALL']
                    o0LongP = o0Long[o0Long['putCall'] == 'PUT']
                    if col[4] == 'C':
                        bigOrder = o0LongC[o0LongC['totalVolume'] > todayRow[col] * 0.5]['description']
                    elif col[4] == 'P':
                        bigOrder = o0LongP[o0LongP['totalVolume'] > todayRow[col] * 0.5]['description']
                        
                    if len(bigOrder) > 0:
                        theOne = bigOrder.values[0]
                    else:
                        theOne = ''
        #             if abs(dayChange) < 3:
                    row = [todayDate, symb, col, todayRow[col], '{0:.2f}'.format(prevRows[col].mean()), 
                           '{0:.2f}'.format(dayChange), '{0:.2f}'.format(volIncrease), theOne]
                    print(row[1:])
                    oWatch.loc[len(oWatch)] = row

        oWatch.to_csv(datapath / 'historical_option_daily/watch/{}.csv'.format(todayDate),index=False )
                        


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
        