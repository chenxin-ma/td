import pandas as pd
from tqdm import tqdm
import matplotlib
import matplotlib.pyplot as plt
plt.rcParams['figure.facecolor'] = 'white'
import seaborn as sns
import numpy as np
import os
from os import listdir
from os.path import isfile, join
import mplfinance as mpf



def find_nearest_two(array, value):
    # get the approximated index(float) in the array for the value
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    if array[idx] > value and idx > 0:
        
        return idx - (array[idx] - value) / (array[idx] - array[idx - 1]) 
    if array[idx] <= value and idx < len(array) - 1:
        return idx + (value - array[idx]) / (array[idx + 1] - array[idx]) 

    return idx



def visOptionsDist(datapath, figpath, symbs, dates=[]):

    if dates == []:
        dates = sorted([date for date in listdir(datapath / 'historical_option_daily/single/') 
                 if not isfile(join(datapath / 'historical_option_daily/single', date))])

    cols = ['totalVolume', 'openInterest']
    types = ['CALL', 'PUT']
    cmaps = ['YlGn', 'OrRd']
    oAll = pd.read_csv(datapath / 'historical_option_daily/all.csv')

    for symb in symbs:
        oS = oAll[oAll['symb'] == symb]
        nOption = len(pd.read_csv(datapath / 'historical_option_daily/single/{}/{}.csv'.format(dates[-1], symb)))

        savepath = figpath / 'options_heat/{}'.format(symb)
        if not os.path.exists(savepath):
            os.makedirs(savepath)

        cMapMaxFile = figpath / 'options_heat/{}/cMapMax.npy'.format(symb)
        if os.path.exists(cMapMaxFile):
            with open(cMapMaxFile, 'rb') as f:
                cMapMaxVol, cMapMaxOpen = np.load(f)
        else:
            # cMapMaxVol = 50000
            cMapMaxVol = oS.iloc[-100:]['ttlVol'].max() / nOption * 20
            # cMapMaxOpen = 80000
            cMapMaxOpen = oS.iloc[-100:]['ttlOpen'].max() / nOption * 2 * np.log2(nOption)
            if cMapMaxOpen > cMapMaxVol * 6:
                cMapMaxOpen = cMapMaxVol * 6
            with open(cMapMaxFile, 'wb') as f:
                np.save(f, np.array([cMapMaxVol, cMapMaxOpen]))

        optionVol = oS['ttlVol'].values
        plotKChart(datapath, figpath, symb, optionVol)

        for idx, date in enumerate(dates[-30:]):
            
            # if idx % 5 != 4:
                # continue

            if os.path.exists(savepath / '{}.png'.format(date)):
                continue


            try:
                o0 = pd.read_csv(datapath / 'historical_option_daily/single/{}/{}.csv'.format(date, symb))
                o0 = o0[o0['expirationDate'] >= date]

            except:
                continue

            try:
                oSingle = pd.read_csv(datapath / 'historical_daily/single/{}.csv'.format(symb))
                datePrice = oSingle[oSingle['datetime'] == date]
                openPrice,highPrice,lowPrice,closePrice = datePrice.values[0][:4]
            except:
                openPrice,highPrice,lowPrice,closePrice = -1, -1, -1 ,-1

            fig, axs = plt.subplots(figsize=(24, 18), nrows=2, ncols=2)
            fig.subplots_adjust(wspace=0.01)
            # fig.subplots_adjust(hspace=0.3)

            for i, col in enumerate(cols):
                for j, tp in enumerate(types):
                    o1 = o0[o0['putCall'] == tp][['strikePrice','expirationDate', col]]
                    o1 = o1.fillna(0)
                    # o1[col] = np.log10(o1[col] + 1)
                    oDraw = o1.pivot_table(index='strikePrice',columns='expirationDate',values=col)\
                              .sort_index(ascending=False)

                    if col == 'totalVolume':
                        vmax = cMapMaxVol
                    else:
                        vmax = cMapMaxOpen
                    ax = sns.heatmap(oDraw, cmap=cmaps[j], vmax=vmax, ax=axs[i][j]);
                    if openPrice != -1:
                        oIdx = find_nearest_two(oDraw.index, openPrice)
                        hIdx = find_nearest_two(oDraw.index, highPrice)
                        lIdx = find_nearest_two(oDraw.index, lowPrice)
                        cIdx = find_nearest_two(oDraw.index, closePrice)
                        ax.axhline(hIdx, color='brown', linewidth=2, ls=':')
                        ax.axhline(lIdx, color='brown', linewidth=2, ls=':')
                        ax.axhline(oIdx, color='k', linewidth=2, ls='-.')
                        ax.axhline(cIdx, color='k', linewidth=2, ls='--')
                    
                    # cbar = ax.collections[0].colorbar
                    # maxTicks = 6#int(np.round(o1[col].max())) + 1 
                    # cbar.set_ticks([i for i in range(maxTicks)])
                    # cbar.set_ticklabels([0] + ['${10^%d}$' %i for i in range(1, maxTicks)])

            fig.suptitle('%s, %s' %(symb, date), fontsize=18, x=0.45, y=0.9);
            fig.savefig(savepath / '{}.png'.format(date), dpi=150)
            plt.close('all')


def plotKChart(datapath, figpath, symb, optionVol=[], saving=True, days=100):

    try:
        oSingle = pd.read_csv(datapath / 'historical_daily/single/{}.csv'.format(symb)
                                    ,index_col=5,parse_dates=True).iloc[-days:]
        oSingle.index.name = 'Date'
    except:
        return 

    if len(optionVol) == 0:
        oAll = pd.read_csv(datapath / 'historical_option_daily/all.csv')
        oS = oAll[oAll['symb'] == symb]
        optionVol = oS['ttlVol'].values


    savepath = figpath / 'options_heat/{}'.format(symb)
    if not os.path.exists(savepath):
        os.makedirs(savepath)

    if days - len(optionVol) > 0:
        optionVol = np.pad(optionVol, (days - len(optionVol), 0), 'constant')
    else:
        optionVol = optionVol[-days:]

    apds = [
            mpf.make_addplot(optionVol,type='bar', width=0.7,
                         alpha=0.7, color='C3',panel=1)
           ]

    save = dict(fname=str(savepath/'{}_candle.png'.format(symb)),
                dpi=150,
                pad_inches=0.1)

    mc = mpf.make_marketcolors(up='g',down='r')
    s = mpf.make_mpf_style(base_mpl_style='seaborn-whitegrid', marketcolors=mc)
    # s = mpf.make_mpf_style(base_mpf_style='classic',rc={'figure.facecolor':'lightgray'})

    if saving:
        mpf.plot(oSingle, type='candle', 
            style=s,
            title='%s' %symb,
            volume=True,
            panel_ratios=(3,1), 
            figratio=(11,8),
            addplot=apds,
            savefig=save
            )
    else:
        mpf.plot(oSingle, type='candle', 
            style=s,
            title='%s' %symb,
            volume=True,
            panel_ratios=(3,1), 
            figratio=(11,8),
            addplot=apds,
            )


def plotSingleOptionDailyPrice(datapath, figpath, optionName, saving=True):

    symb, expirationDate, strikePrice, cp = optionName.split('_')
    strikePrice = float(strikePrice)
    cp = cp.upper() 

    datesAvailable = [f for f in listdir(datapath / 'historical_option_daily/single/') 
                     if not isfile(join(datapath / 'historical_option_daily/single/', f))]

    datesAvailable = np.sort(datesAvailable)

    rows = {}
    for date in datesAvailable:

        dailyDataFile = datapath / 'historical_option_daily/single/{}/{}.csv'.format(date, symb)
        
        if os.path.exists(dailyDataFile):

            oDailyData = pd.read_csv(dailyDataFile)

            rowCall = oDailyData[(oDailyData['putCall'] == 'CALL') & \
                    (oDailyData['strikePrice'].between(strikePrice - 0.01, strikePrice + 0.01)) & \
                    (oDailyData['expirationDate'] == expirationDate)].copy()

            rowPut = oDailyData[(oDailyData['putCall'] == 'PUT') & \
                    (oDailyData['strikePrice'].between(strikePrice - 0.01, strikePrice + 0.01)) & \
                    (oDailyData['expirationDate'] == expirationDate)].copy()

            if (len(rowCall) > 0 or len(rowPut) > 0):
                if 'bid' in rowCall.columns and 'ask' in rowCall.columns:

                    rowCall['callMarket'] = (rowCall['bid'] + rowCall['ask'] ) / 2 * 100
                    putmarket = (rowPut.iloc[0]['bid'] + rowPut.iloc[0]['ask'] ) / 2 * 100
                    rowCall['putMarket'] = putmarket
                    rowCall['straddleMarket'] = rowCall['putMarket'] + rowCall['callMarket']

                    rowCall['date'] = date
                    
                    rows[date] = rowCall

    oOptionDaily = pd.concat([rows[date] for date in rows])
    oOptionDaily['price'] = (oOptionDaily['bid'] + oOptionDaily['ask'] ) / 2

    try:
        oSingle = pd.read_csv(datapath / 'historical_daily/single/{}.csv'.format(symb)
                                    ,parse_dates=False)
    except:
        return 

    oOptionDailyMerge = oOptionDaily.merge(oSingle, how='left', left_on='date', right_on='datetime')
    oOptionDailyMerge['datetime'] = pd.to_datetime(oOptionDailyMerge['datetime'])
    oOptionDailyMerge = oOptionDailyMerge.set_index('datetime')
    oOptionDailyMerge.index.name = 'Date'

    oOptionDailyMerge.dropna(how='any', inplace=True)

    apds = [
            mpf.make_addplot(oOptionDailyMerge['straddleMarket'].values, 
                # type='plot', 
                width=2,
                # alpha=0.7, 
                color='C3',panel=1),
            mpf.make_addplot(oOptionDailyMerge['callMarket'].values, 
                # type='plot', 
                width=1,
                # alpha=0.7, 
                color='C2',panel=1),
            mpf.make_addplot(oOptionDailyMerge['putMarket'].values, 
                # type='plot', 
                width=1,
                # alpha=0.7, 
                color='C1',panel=1),
            mpf.make_addplot(oOptionDailyMerge['close'].values, 
                # type='plot', 
                width=0,
                # alpha=0.7, 
                color='C4',panel=0)
           ]

    mc = mpf.make_marketcolors(up='g',down='r')
    s = mpf.make_mpf_style(base_mpl_style='seaborn-whitegrid', marketcolors=mc)

    mpf.plot(oOptionDailyMerge, type='candle', 
            style=s,
            title='%s' %symb,
            volume=False,
            panel_ratios=(1,1), 
            figratio=(11,8),
            addplot=apds,
            )