#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 09:15:49 2023

@author: parrot
"""

'''
descriptives
'''
import numpy as np
from data_wrangling_behavioral_w11_fmri import group_dataset_fmri, TrialFinder
from beh_ana_foraging_final_osf import group_dataset
from get_pe_glm_w1_1 import single_rm_anova
from scipy import stats
import os

wdir=os.getcwd()
keys=[
        'mean$_patch_leaving_low','mean$_patch_leaving_med','mean$_patch_leaving_high',
        'mean_trial_dur_patch_leaving_low','mean_trial_dur_patch_leaving_med','mean_trial_dur_patch_leaving_high',
        'lastITT_patch_leaving_low','lastITT_patch_leaving_med','lastITT_patch_leaving_high',
        'GUT_patch_leaving_low','GUT_patch_leaving_med','GUT_patch_leaving_high',
        'lastCR_patch_leaving_low','lastCR_patch_leaving_med','lastCR_patch_leaving_high',
        'total$_patch_leaving','list_tri_dur','list_reward',
      
      'lastCR_7_patch_leaving_low','lastCR_6_patch_leaving_low','lastCR_5_patch_leaving_low',
    'lastCR_4_patch_leaving_low','lastCR_3_patch_leaving_low','lastCR_2_patch_leaving_low',

    
    'lastCR_7_patch_leaving_med','lastCR_6_patch_leaving_med','lastCR_5_patch_leaving_med',
    'lastCR_4_patch_leaving_med','lastCR_3_patch_leaving_med','lastCR_2_patch_leaving_med',

    
    'lastCR_7_patch_leaving_high','lastCR_6_patch_leaving_high','lastCR_5_patch_leaving_high',
    'lastCR_4_patch_leaving_high','lastCR_3_patch_leaving_high','lastCR_2_patch_leaving_high',

      'mean_ITT_patch_leaving_low','mean_ITT_patch_leaving_med','mean_ITT_patch_leaving_high',

    'list_gut',
    
     'meanCR_patch_leaving_low','meanCR_patch_leaving_med','meanCR_patch_leaving_high'

      ]


# single_rm_anova('reward',[group_dataset_fmri['mean$_patch_leaving_low'],
#                           group_dataset_fmri['mean$_patch_leaving_med'],
#                           group_dataset_fmri['mean$_patch_leaving_high']],
#                           len(group_dataset_fmri['mean$_patch_leaving_high']))
                          

nsubs=len(group_dataset_fmri['mean$_patch_leaving_low'])+len(group_dataset['mean$_patch_leaving_low'])

for k in keys:
    group_dataset_fmri[k]=group_dataset_fmri[k]+group_dataset[k]
    #group_dataset_fmri[k]=[item for sublist in group_dataset_fmri[k] for item in sublist]
    print ('###########')
    print (k)

