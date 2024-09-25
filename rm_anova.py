#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 10:09:51 2022

@author: parrot
"""
import pandas as pd 
import numpy as np      
from statsmodels.stats.anova import AnovaRM # 
import scikit_posthocs as sp
import pingouin as pg


import statsmodels.api as sm
import matplotlib.pyplot as plt

    
def single_rm_anova(av_name,l1,n):
    
    print (f'### Descriptives of {av_name}  ###')
    print (f' mean 50%: {np.mean(l1[0])},sd: {np.std(l1[0])}')
    print (f' mean 75%: {np.mean(l1[1])},sd: {np.std(l1[1])}')
    print (f' mean 100%: {np.mean(l1[2])},sd: {np.std(l1[2])}')
    
    
    dv=[item for sublist in l1 for item in sublist]
    patch=[[0.5]*n,[0.75]*n,[1]*n]
    patch=[item for sublist in patch for item in sublist]
    sub=list(range(n))*3
    
    
    #create Q-Q plot with 45-degree line added to plot
    data=np.array(dv)
    z = (data-np.mean(data))/np.std(data)
    fig = sm.qqplot(z, line='45')
    plt.show()
    
    resp=int(input('if normal, press 1, otherwise 0 :'))
    
    
    #mk dic then pd.dataframe 
    
    d = {av_name: dv, 'patch_type': patch,'sub': sub #'sub':nsubs
         
        }
    dataSet= pd.DataFrame(data=d)
    
    
    #run anovva using two packages

    if resp ==1:
        print(f'###  single factor rm-ANOVA for {av_name} ###')
        #print(AnovaRM(dataSet, av_name, 'sub', within=['patch_type']).fit())
        res = pg.rm_anova(dv=av_name, within='patch_type', 
                          subject='sub', data=dataSet, detailed=True, correction=True)
    else:
        print(f'###  Friedmann-Test for {av_name} ###')
        res=pg.friedman(dv=av_name, within='patch_type', 
                      subject='sub', data=dataSet, method="f")
        
        
    print ('###')
    print (res.round(3)) 
    #print (res['p-spher'])
    print ('F-value =',res['F'][0])
    #print ('DOF:',res['ddof1'][0],res['ddof2'][0])
    if res['p-spher'][0] < 0.05:
        print ('sphericity is violated !')
        print ('###')
        print ('GG-corrected p:')
        print (res['p-GG-corr'])
        if res['p-GG-corr'][0] < 0.05:
             print ('###')
             print ('Post-hoc t-tests (bonferroni-corrected)')
             #print(sp.posthoc_ttest(dataSet, val_col=av_name, group_col='patch_type', p_adjust='bonferroni'))
             print (dataSet.pairwise_tukey(dv=av_name, between='patch_type').round(3))

    
    elif res['p-unc'] [0]<0.05:
        
        print ('p-val:',res['p-unc'][0])
        print ('###')
        print ('Post-hoc t-tests (Tuckey)')
        #print(sp.posthoc_ttest(dataSet, val_col=av_name, group_col='patch_type', p_adjust='bonferroni'))
        print (dataSet.pairwise_tukey(dv=av_name, between='patch_type').round(3))

       
    return res#None






         
def rm_2by3_anova(av_name,l1,n):
    print (f'### Descriptives of {av_name}  ###')
    print (f' ICR 50%: {np.mean(l1[0])},sd: {np.std(l1[0])}')
    print (f' MCR 50%: {np.mean(l1[1])},sd: {np.std(l1[1])}')
    print (f' ICR 75%: {np.mean(l1[2])},sd: {np.std(l1[2])}')
    print (f' MCR 75%: {np.mean(l1[3])},sd: {np.std(l1[3])}')
    print (f' ICR 100%: {np.mean(l1[4])},sd: {np.std(l1[4])}')
    print (f' MCR 100%: {np.mean(l1[5])},sd: {np.std(l1[5])}')
    
    
    dv=[item for sublist in l1 for item in sublist]
    patch=[[0.5]*(n*2),[0.75]*(n*2),[1]*(n*2)]
    patch=[item for sublist in patch for item in sublist]
    types=['ICR']*n+['MCR']*n
    types=types*3
    sub=list(range(n))*6
    
    
    #create Q-Q plot with 45-degree line added to plot
    data=np.array(dv)
    z = (data-np.mean(data))/np.std(data)
    fig = sm.qqplot(z, line='45')
    plt.show()
    
    

    #mk dic then pd.dataframe 
    
    d = {av_name: dv, 'patch_type': patch,'sub': sub ,'type':types
         
        }
    dataSet= pd.DataFrame(data=d)
    
    #spher, W, chisq, dof, pval = pg.sphericity(dataSet)
    
    #spericity for within factor patch
    # p_spher=round(pg.sphericity(dataSet, dv=av_name, subject='sub',
    #         within='patch_type')[-1],3)
    
    spher, _, chisq, dof, p_val_spher = pg.sphericity(dataSet, dv=av_name,
                                           subject='sub',
                                          within=['patch_type', 'type'])
    
    #print (f'p value Mauchly test for patch type:{p_spher}')
    print(f' Interaction: sphericity:{spher}, CHI^2:{round(chisq, 3)}, df:{dof}, p:{round(p_val_spher, 3)}')
    
    
    
    #run anovva using two packages
    print(f'###  2X3 factor rm-ANOVA for {av_name} ###')
    #print(AnovaRM(dataSet, av_name, 'sub', within=['patch_type']).fit())
    res = pg.rm_anova(dv=av_name, within=['patch_type','type'], effsize="np2",
                      subject='sub', data=dataSet, detailed=True, correction=True)
    
    
    # res=pg.friedman(dv=av_name, within=['patch_type','type'], 
    #                   subject='sub', data=dataSet, method="f")
    print (res.round(3))
    print ('###')

    #print (res['p-spher'])
    print ('F-value =',res['F'][0])
    print ('DOF1:',res['ddof1'])
    print ('DOF2',res['ddof2'])
    print ('DOF2',res['ddof2'])
    if round(p_val_spher,3) < 0.05:
        print ('sphericity is violated !')
        print ('###')
        print ('GG-corrected p:')
        print (res['p-GG-corr'])
        if res['p-GG-corr'][0] < 0.05:
              print ('###')
              print ('Post-hoc t-tests (Tuckey)')
              #print(sp.posthoc_ttest(dataSet, val_col=av_name, group_col='patch_type', p_adjust='bonferroni'))
              print (dataSet.pairwise_tukey(dv=av_name, between='patch_type').round(3))

     
    
    
    elif res['p-unc'] [1]<0.05 or res['p-unc'] [2]<0.05:
        
        print ('p-val:',res['p-unc'][2])
        print ('###')
        print ('Post-hoc t-tests)')
        #print(sp.posthoc_ttest(dataSet, val_col=av_name, group_col='patch_type', p_adjust='bonferroni'))
        #print (dataSet.pairwise_tukey(dv=av_name, between=['patch_type','type']).round(3))
        posthocs = pg.pairwise_ttests(dv=av_name, within=['patch_type','type'], subject='sub',
                              padjust='fdr_bh', data=dataSet, correction='auto' )
        
        print(posthocs)

       
    return res
            




# #t-tests/non-param
# from scipy import stats
# stats.ttest_1samp(rvs, popmean=0.5, alternative='greater')
# #stats.wilcoxon()





