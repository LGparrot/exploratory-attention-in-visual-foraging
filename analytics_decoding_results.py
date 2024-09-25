#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 18:31:52 2023

@author: parrot


wrangling decoding results 



"""
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import numpy as np
from data_cleaning import remove_outliers







def bootstrap(data, n=1000, func=np.mean):
    """
    Generate `n` bootstrap samples, evaluating `func`
    at each resampling. `bootstrap` returns a function,
    which can be called to obtain confidence intervals
    of interest.
    """
    simulations = list()
    sample_size = len(data)
    xbar_init = np.mean(data)
    for c in range(n):
        itersample = np.random.choice(data, size=sample_size, replace=True)
        simulations.append(func(itersample))
    simulations.sort()
    def ci(p):
        """
        Return 2-sided symmetric confidence interval specified
        by p.
        """
        u_pval = (1+p)/2.
        l_pval = (1-u_pval)
        l_indx = int(np.floor(n*l_pval))
        u_indx = int(np.floor(n*u_pval))
        return(simulations[l_indx],simulations[u_indx])
        print (ci)
    return(ci)


'''
load data
'''
curr_dir=os.getcwd()

print (f'you are here: {curr_dir}')


#chance accurcies based on bootsrapped permuations
perms=pd.read_csv('/Users/lasseguldener/Desktop/results_decoding/allNullaccs_info_pl_vs_control_pl-detection_n19_p01_r3_p0.05.csv')



#load accs of sig. cluster after groupclusterthrsholding
cluster_accs=pd.read_csv('/Users/lasseguldener/Desktop/results_decoding/final_accs_pl-detection_n19_p01_r3_p0.05.csv')


'''
get 95%CI fo Null distribution
'''
null_ci_95=stats.t.interval(0.95, len(perms['accuracy'])-1, 
                            loc=np.mean(perms['accuracy']), 
                            scale=stats.sem(perms['accuracy']))
#meaningless if not normal or highly skwed 

filt_df=perms.loc[:,perms.columns !='NO']
print (len(filt_df.accuracy))#len equals number of voxels of mask that was used (pl-detection)
#get all out above and below quantiles
# filt_df = filt_df.drop(filt_df[(filt_df.accuracy > np.percentile(filt_df.accuracy, 95)) 
#                                & (filt_df.accuracy < np.percentile(filt_df.accuracy, 5))].index)

plt.hist(filt_df.accuracy,bins=30,normed=True)
plt.show()

# filt_df =filt_df[(filt_df > np.percentile(filt_df.accuracy, 5)).all(axis=1)]
# filt_df =filt_df[(filt_df < np.percentile(filt_df.accuracy, 95)).all(axis=1)]
# print (len(filt_df.accuracy))





null_ci_95=stats.t.interval(0.95, len(filt_df['accuracy'])-1, 
                            loc=np.mean(filt_df['accuracy']), 
                            scale=stats.sem(filt_df['accuracy']))


boot=bootstrap(filt_df.accuracy, n=1000, func=np.mean)
cintervals = [boot(i) for i in (.95, .99, .995)]
print (cintervals)

ci_up_95=cintervals[0][1]

'''
create strip plot
'''

d={'ROI':['PL-detection']*len(cluster_accs['accuracy']),'Decoding accuracy':cluster_accs['accuracy']}
dfr=pd.DataFrame(d)


plt.figure(figsize=(8,6))



sns.stripplot(x="ROI", 
                 y="Decoding accuracy", 
                   data=dfr,palette="crest",zorder=0)
sns.pointplot(x="ROI", 
                  y="Decoding accuracy", join=False,
                    data=dfr, estimator=np.mean, color='black',
                    ci="sd")


plt.axhline(ci_up_95,0.39, 0.61, color='red',ls='--',lw=0.5)#Ani
plt.ylim(0.48, 0.53)
plt.axhspan(0.47, ci_up_95, 0.39, 0.61,facecolor='gray', alpha=0.35)

plt.savefig(curr_dir +'/fmri/decoding_clusters.svg')


'''
get max accs
'''

the_max=list(cluster_accs.max())
the_max
two_max=list(cluster_accs.accuracy.nlargest(2))

cluster_accs.loc[cluster_accs.accuracy == two_max[0]]























