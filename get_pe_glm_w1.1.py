#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 10:25:26 2023

@author: parrot
"""

'''
plotting signal changes in % for GLM copes

'''
import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np




outdir=os.getcwd()
text_dir='/Users/lasseguldener/Desktop/GLM_results_n19/featqueries/'



subs=[6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,25]

lables=['patch-leaving > control','patch-leaving > detection']
copes={}
for key in lables:
   copes['{0}'.format(key)]=[] 
  

cope1_hrf=[] 
cope3_hrf=[] 

'''
load txt files from featquery output & select the mean signal change in %

'''         
for sub in subs:
    
    if sub < 10:
        with open(text_dir + f'sub0{sub}/report.txt') as f:
            lines = f.readlines()
    else:
         with open(text_dir + f'sub{sub}/report.txt') as f:
            lines = f.readlines()
        
    print(lines)
    mean_signal_change=lines[0].split(' ')[5]#entire row as single string, so split it by tab and select the right index
    mean_signal_change=float(mean_signal_change)
    cope1_hrf.append(mean_signal_change)
    
    if sub < 10:
        with open(text_dir + f'cope3/sub0{sub}/report.txt') as f:
            lines = f.readlines()
    else:
         with open(text_dir + f'cope3/sub{sub}/report.txt') as f:
            lines = f.readlines()
        
    #print(lines)
    mean_signal_change=lines[0].split(' ')[5]#entire row as single string, so split it by tab and select the right index
    mean_signal_change=float(mean_signal_change)
    cope3_hrf.append(mean_signal_change)
 



'''
mk pointplot and add single subjects estimates 

'''
d={'ROI':['cope1']*len(subs)+['cope2']*len(subs),'signal change':cope1_hrf+cope3_hrf}
dfr=pd.DataFrame(d)


plt.figure(figsize=(8,6))

sns.stripplot(x="ROI", 
                 y="signal change", 
                   data=dfr);
sns.pointplot(x="ROI", 
                 y="signal change", hue="ROI",join=False,
                   data=dfr, estimator=np.mean, 
                   ci="sd");

plt.axhline(0.0, color='gray',ls='--',lw=0.5)#Ani

plt.savefig(outdir +'/fmri/glm_sig_change_cope1&3.svg')








