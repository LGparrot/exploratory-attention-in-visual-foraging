#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 14:02:03 2023

@author: lasseguldener
"""



import pandas as pd
import numpy as np
from data_wrangling_behavioral_w11_fmri import group_dataset_fmri



'''
# =============================================================================
#   OUTLIERS?
# =============================================================================
'''

kyes=['']

d={'sub':nsubs,'n_trial':group_dataset_fmri['mean_nTrials_patch_leaving']}
df=pd.DataFrame(data=d)

def remove_outliers(df, q=0.01):
    #remove sub
    filt_df=df.loc[:,df.columns !='sub']
    
    #get quantiles
    low = q
    high = 1-q
    quant_df = filt_df.quantile([low, high])
    
    #filter
    filt_df = filt_df.apply(lambda x: x[(x>quant_df.loc[low,x.name]) & 
                                    (x < quant_df.loc[high,x.name])], axis=0)
    #bring back sub id                            
    filt_df = pd.concat([df.loc[:,'sub'], filt_df], axis=1)
    #drop nan
    #filt_df.dropna(inplace=True)
    #print ('filtered data')
    #print(filt_df['n_trial'].describe())
    return filt_df

filt_df=remove_outliers(df, q=0.01)