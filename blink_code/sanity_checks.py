#!/bin/env python
#==========================
# author: Maria Elidaiana
# email: mariaeli@brandeis.edu
#==========================

'''
This code produce sanity check plots for the matched BlinK catalogs.
'''
import numpy as np
import matplotlib.pyplot as plt
import sys
import glob
from astropy.table import Table
import pandas as pd
import seaborn as sns
sns.set(color_codes=True)
from matplotlib.ticker import NullFormatter

split = False #If True do individual plots, if False plot all the catalogs quantities together.

fitsdir  = glob.glob("/data/des71.b/data/luidhy/single_catalogs/blink_griz/blink_t1/cat/*.fits")
fitsname = [i.split('/')[9] for i in fitsdir] 

def plot_spread_x_mag(band, df, outsufix):
    print 
    print '--- Catalog used: ', outsufix
    
    spmodel = df['SPREAD_MODEL_'+band]
    mgauto = df['MAG_AUTO_'+band]
    clstar = df['CLASS_STAR_'+band]
    flags = df['FLAGS_'+band]
    mgerrauto =  df['MAGERR_AUTO_'+band]
    snr = 1.086/mgerrauto

    print 'Band: ', band
    print 'Ntot:', len(mgauto)
    print 'N_mag_auto=99.:', len(mgauto[mgauto==99.])

    #Check psf

    mask0 = (flags>=0) & (flags<3) & (snr>20) & (mgauto!=99.)
    mask1 = (flags>=0) & (flags<3) & (snr>20) & (np.abs(spmodel)<0.003) & (mgauto!=99.) 
    mask2 = (flags>=0) & (flags<3) & (snr>20) & (np.abs(spmodel)>0.003) & (mgauto!=99.)
    mask3 = (flags>=0) & (flags<3) & (snr>20) & (np.abs(spmodel)>0.003) & (np.abs(clstar)>0.95) & (mgauto!=99.)


    nullfmt = NullFormatter()         # no labels

    # definitions for the axes
    left, width = 0.1, 0.65
    bottom, height = 0.1, 0.65
    bottom_h = left_h = left + width + 0.02

    rect_scatter = [left, bottom, width, height]
    rect_histx = [left, bottom_h, width, 0.2]
    rect_histy = [left_h, bottom, 0.2, height]


    plt.figure(1, figsize=(8, 8))
    axScatter = plt.axes(rect_scatter)
    axHistx = plt.axes(rect_histx)
    axHisty = plt.axes(rect_histy)
    # no labels
    axHistx.xaxis.set_major_formatter(nullfmt)
    axHisty.yaxis.set_major_formatter(nullfmt)
    # the scatter plot:
    #plt.plot(mgauto[mask0], spmodel[mask0], 'k.')
    axScatter.plot(mgauto[mask1], spmodel[mask1], 'k.', label='flags(0,3)& SNR>20 & |spread_model|<0.003 & mag_auto!=99. N='+str(len(mgauto[mask1])) )
    axScatter.plot(mgauto[mask2], spmodel[mask2], 'c.', label='flags(0,3)& SNR>20 & |spread_model|>0.003 & mag_auto!=99. N='+str(len(mgauto[mask2])) )
    axScatter.plot(mgauto[mask3], spmodel[mask3], 'r.', label='flags(0,3)& SNR>20 & |spread_model|>0.003 & |class_star|>0.95 & mag_auto!=99.  N='+str(len(mgauto[mask3])) )

    try:
        binx = np.linspace(min(mgauto[mask0]), max(mgauto[mask0]), num=20)
        biny = np.linspace(min(spmodel[mask0]), max(spmodel[mask0]), num=20)
    except ValueError:
        binx = np.linspace(13, 23, num=20)
        biny = np.linspace(-0.04, 0.04, num=20)

    axHistx.hist(mgauto[mask1], bins=binx, color='k')
    axHistx.hist(mgauto[mask2], bins=binx, color='c')
    axHistx.hist(mgauto[mask3], bins=binx, color='r')
    axHisty.hist(spmodel[mask1], bins=biny, orientation='horizontal', color='k')
    axHisty.hist(spmodel[mask2], bins=biny, orientation='horizontal', color='c')
    axHisty.hist(spmodel[mask3], bins=biny, orientation='horizontal', color='r')


    axScatter.set_xlabel('MAG_AUTO')
    axScatter.set_ylabel('SPREAD_MODEL')
    axScatter.legend(loc='best', fontsize=7)
    axScatter.text(13, -0.03, 'N = '+ str(len(mgauto)) + ', N (mag!=99) = ' + str(len(mgauto[mask0]))  )

    plt.savefig('spread_model_x_mag_auto_'+band+'_'+outsufix+'.png')
    plt.close()

if split:

    for i in range(len(fitsname)):
        filename = '/data/des71.b/data/luidhy/single_catalogs/blink_griz/blink_t1/cat/'+fitsname[i]
        cat = Table.read(filename)
        df = cat.to_pandas()
        plot_spread_x_mag('G', df, fitsname[i].replace('.fits',''))
else:
    dfs=[]
    for i in range(len(fitsname)):
        filename = '/data/des71.b/data/luidhy/single_catalogs/blink_griz/blink_t1/cat/'+fitsname[i] 
        cat = Table.read(filename)
        df = cat.to_pandas()
        dfs.append(df)
    df_all = pd.concat([dfs[i] for i in range(len(dfs))]) #you can save this dataframe as a fits file
    plot_spread_x_mag('Z', df_all, 'all')
