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

    for symb in symbs:
        for date in dates:
            o0 = pd.read_csv(datapath / 'historical_option_daily/single/{}/{}.csv'.format(date, symb))
            o0 = o0[o0['expirationDate'] >= date]
            # o0 = o0[(o0['strikePrice'] > 300) & (o0['strikePrice'] < 500)]

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
                    o1[col] = np.log10(o1[col] + 1)
                    oDraw = o1.pivot_table(index='strikePrice',columns='expirationDate',values=col).sort_index(ascending=False)
                    ax = sns.heatmap(oDraw, cmap=cmaps[j], vmax=6.01, ax=axs[i][j]);
                    if openPrice != -1:
                        oIdx = find_nearest_two(oDraw.index, openPrice)
                        hIdx = find_nearest_two(oDraw.index, highPrice)
                        lIdx = find_nearest_two(oDraw.index, lowPrice)
                        cIdx = find_nearest_two(oDraw.index, closePrice)
                        ax.axhline(hIdx, color='brown', linewidth=2, ls=':')
                        ax.axhline(lIdx, color='brown', linewidth=2, ls=':')
                        ax.axhline(oIdx, color='k', linewidth=2, ls='-.')
                        ax.axhline(cIdx, color='k', linewidth=2, ls='--')
                    
                    cbar = ax.collections[0].colorbar
                    maxTicks = 7#int(np.round(o1[col].max())) + 1 
                    cbar.set_ticks([i for i in range(maxTicks)])
                    cbar.set_ticklabels([0] + ['${10^%d}$' %i for i in range(1, maxTicks)])

            savepath = figpath / 'options_heat/{}'.format(symb)
            if not os.path.exists(savepath):
                os.makedirs(savepath)

            fig.suptitle('%s, %s' %(symb, date), fontsize=18, x=0.45, y=0.9);
            fig.savefig(savepath / '{}.png'.format(date), dpi=150)