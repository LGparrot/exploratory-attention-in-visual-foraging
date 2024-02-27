#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 15:18:06 2022

@author: lasseguldener
"""
import numpy as np
import pandas as pd
import seaborn as sns
import os
import matplotlib.pyplot as plt
from data_wrangling_behavioral_w11_fmri import group_dataset_fmri,nsubs
from load_animal_data_osf import animals_dataset
from matplotlib.collections  import PathCollection
from matplotlib.lines  import Line2D
from scipy import stats
#import statannot
sns.set_theme(style="darkgrid",palette="pastel")


#mako 
#rocket


wdir=os.getcwd()

wdir=wdir+'/fmri/'

if not os.path.exists(wdir):
    os.mkdir(wdir)


'''
plot tri dur for first and second half 


'''






'''
normalizing (z)

'''
lst_G=lst[0]+lst[2]+lst[4]
lst_H=lst[1]+lst[3]+lst[5]
#lst_G=[item for sublist in lst_G for item in sublist]
data_G = np.array(lst_G)
z_G =stats.zscore(data_G)#(data_G-np.mean(data_G))/np.std(data_G)
lG=list(z_G)


#lst_H=[item for sublist in lst_H for item in sublist]
data_H = np.array(lst_H)
z_H = stats.zscore(data_H)#(data_H-np.mean(data_H))/np.std(data_H)
lH=list(z_H)
lst=lG+lH







'''
#=============================================================================
# plot parameter distribution on group level, combining box and strip plot
#=============================================================================V
'''


#function
def plotting(l1,label_y,plot_name,nsubs):
    
    l2=[[0.5]*len(nsubs),[0.75]*len(nsubs),[1]*len(nsubs)]
    l1=[item for sublist in l1 for item in sublist]
    l2=[item for sublist in l2 for item in sublist]
    
    d = {f'{label_y}': l1, 'Patch quality': l2, #
            }
    
       
    dataSet= pd.DataFrame(data=d)
    
    
    fig, axs =plt.subplots(figsize=(8,6))
    
    sns.boxplot(data=dataSet, x='Patch quality', y=label_y, 
            meanprops={'marker' : 'D', 'markeredgecolor' : 'black', 'markersize' : 8, 'label':'mean'},
            medianprops={'visible': False}, whiskerprops={'visible': False},
            showmeans=True, showfliers=False, showbox=False, showcaps=False)
    sns.stripplot(ax=axs,data=dataSet, x='Patch quality', y=label_y, 
                  palette="viridis",
              dodge=True, jitter=0.05, zorder=0)
    #plt.axhline(8.9, color='black',ls='--',lw=0.5)
    # plt.axhline(90,0.1779, 0.842, color='black',ls='-',lw=1)
    # plt.axvline(0.03,0.77,0.95, color='black',ls='-',lw=1,zorder=0)
    # plt.axvline(2.03,0.77,0.95, color='black',ls='-',lw=1,zorder=0)
    # plt.text(1.03, 91, '*',fontsize='xx-large')
    # plt.legend()
    
    # plt.axhline(15.2,0.163, 0.83, color='black',ls='-',lw=1)
    # plt.axvline(-0.01,0.75,0.95, color='black',ls='-',lw=1,zorder=0)
    # plt.axvline(2,0.85,0.95, color='black',ls='-',lw=1,zorder=0)
    # plt.legend()
    # plt.axhline(14.5,0.5, 0.83, color='black',ls='-',lw=1)
    # plt.axhline(14, 0.163, 0.5, color='black',ls='-',lw=1)
    # plt.axvline(1,0.80,0.905, color='black',ls='-',lw=1,zorder=0)
    # #plt.axvline(2.03,0.87,0.93, color='black',ls='-',lw=1,zorder=0)
    # plt.text(1.5,14.3, '*',fontsize='xx-large')
    # plt.text(1.0, 15.2, '*',fontsize='xx-large')
    # plt.text(0.5, 14.2, '*',fontsize='xx-large')
    #plt.legend()
   
    
    #plt.savefig(wdir +f'/joint_analysis/{label_y}_hum_gerbils.svg')
    #plt.savefig(wdir +f'{plot_name}_hum_fmri.svg')
    #plt.savefig(wdir +f'{plot_name}_hum_fmri.png')


'''
        1. Trial duration
'''
#input list, list of lists that are dic keys...
lst=[group_dataset_fmri['mean_trial_dur_patch_leaving_low'],
      group_dataset_fmri['mean_trial_dur_patch_leaving_med'],
      group_dataset_fmri['mean_trial_dur_patch_leaving_high']]

plotting(lst,'Trial Duration in s','TrialDur',nsubs)  


''' 
        2. $$$ Reward
'''
lst=[group_dataset_fmri['mean$_patch_leaving_low'],
      group_dataset_fmri['mean$_patch_leaving_med'],
      group_dataset_fmri['mean$_patch_leaving_high']]

plotting(lst,'Mean number of rewards','Reward',nsubs)  

''' 
        3. Target Probability
'''
lst=[group_dataset_fmri['meanTP_patch_leaving_low'],
      group_dataset_fmri['meanTP_patch_leaving_med'],
      group_dataset_fmri['meanTP_patch_leaving_high']]

plotting(lst,'Remaining reward probability at leaving','TP',nsubs) 










'''
plot relation between GUT, residence time and total earnings by patch quality 

'''

lst_fmri_gut=[group_dataset_fmri['GUT_patch_leaving_low'],
      group_dataset_fmri['GUT_patch_leaving_med'],
      group_dataset_fmri['GUT_patch_leaving_high']]



lst_fmri_tridur=[group_dataset_fmri['mean_trial_dur_patch_leaving_low'],
                 group_dataset_fmri['mean_trial_dur_patch_leaving_med'],
                 group_dataset_fmri['mean_trial_dur_patch_leaving_high']]



earnings=[group_dataset_fmri['tot$_patch_leaving_low'],
                 group_dataset_fmri['tot$_patch_leaving_med'],
                 group_dataset_fmri['tot$_patch_leaving_high']]


n=len(lst_fmri_gut[0])# get number of observations (i.e., subjects)

## transform point credits into euro
for ele in range(len(group_dataset_fmri['tot$_patch_leaving_low'])):
    earnings[0][ele] = [item for sublist in earnings[0][ele] for item in sublist]
    earnings[0][ele] =np.nansum(earnings[0][ele])*0.05
    earnings[1][ele] = [item for sublist in earnings[1][ele] for item in sublist]
    earnings[1][ele] =sum(earnings[1][ele])*0.05
    earnings[2][ele] = [item for sublist in earnings[2][ele] for item in sublist]
    earnings[2][ele] =sum(earnings[2][ele])*0.05
    
n=len(lst_fmri_tridur[0])
lst_fmri_gut=[item for sublist in lst_fmri_gut for item in sublist]
lst_fmri_tridur=[item for sublist in lst_fmri_tridur for item in sublist]
earnings=[item for sublist in earnings for item in sublist]
patch=['50%']*(n)+['75%']*(n)+['100%']*(n)

types=['GUT']*n+['residence time']*n
types=types*3


d = {'GUT in s': lst_fmri_gut, 'Patch quality': patch,'Residence time in s': lst_fmri_tridur #
            }


def do_reg_scatter_plot(any_df,key1,key2,key3,label):
    
    dataSet= pd.DataFrame(data=d)
    
    plt.subplots(figsize=(8,6))
    
    sns.regplot(data=dataSet,x=key1, y=key2,
                       line_kws = {"color": "gray"},ci = 95)
    
    #reg_pl.savefig(wdir +'corr_GUTxTriDur.svg')
      
    sns.scatterplot(data=dataSet, x=key1, y=key2,
                            hue=key3,palette="viridis",zorder=1) 
    #sns_plot = plotted.get_figure()
    
    #plt.savefig(wdir +label+'.svg')
    
    return plt
    
do_reg_scatter_plot(d,"Residence time in s",#order is key here!!
                    "GUT in s","Patch quality",
                    'GUTbyResTime')



d = {'Total earnings in €': earnings, 'Patch quality': patch,'GUT in s': lst_fmri_gut#
            }

do_reg_scatter_plot(d,"GUT in s",
                    "Total earnings in €",
                    "Patch quality",
                    'GUTbyResTime')
















import seaborn as sns
sns.set_theme(style="darkgrid")

# Load an example dataset with long-form data
#fmri = sns.load_dataset("fmri")

#time point 


source_keys=['ANI','HUM_BEH','HUM_FMRI']




cr=[
    group_dataset['lastCR_7_patch_leaving_low'],
    group_dataset['lastCR_6_patch_leaving_low'],
    group_dataset['lastCR_5_patch_leaving_low'],
    group_dataset['lastCR_4_patch_leaving_low'],
    group_dataset['lastCR_3_patch_leaving_low'],
     group_dataset['lastCR_2_patch_leaving_low'],
     group_dataset['lastCR_patch_leaving_low'],
     group_dataset['lastCR_7_patch_leaving_med'],
    group_dataset['lastCR_6_patch_leaving_med'],
     group_dataset['lastCR_5_patch_leaving_med'],
    group_dataset['lastCR_4_patch_leaving_med'],
     group_dataset['lastCR_3_patch_leaving_med'],
     group_dataset['lastCR_2_patch_leaving_med'],
     group_dataset['lastCR_patch_leaving_med'],
     group_dataset['lastCR_7_patch_leaving_high'],
    group_dataset['lastCR_6_patch_leaving_high'],
     group_dataset['lastCR_5_patch_leaving_high'],
    group_dataset['lastCR_4_patch_leaving_high'],
     group_dataset['lastCR_3_patch_leaving_high'],
     group_dataset['lastCR_2_patch_leaving_high'],
     group_dataset['lastCR_patch_leaving_high']
     ]



cr=[
    #animals_dataset['CR_last_reward_5_50%'],
    #animals_dataset['CR_last_reward_4_50%'],
    animals_dataset['CR_last_reward_3_50%'],
    animals_dataset['CR_last_reward_2_50%'],
    animals_dataset['mean_CR_last_reward_50%'],
    #animals_dataset['CR_last_reward_5_75%'],
    #animals_dataset['CR_last_reward_4_75%'],
    animals_dataset['CR_last_reward_3_75%'],
    animals_dataset['CR_last_reward_2_75%'],
    animals_dataset['mean_CR_last_reward_75%'],
    #animals_dataset['CR_last_reward_5_100%'],
    #animals_dataset['CR_last_reward_4_100%'],
    animals_dataset['CR_last_reward_3_100%'],
    animals_dataset['CR_last_reward_2_100%'],
    animals_dataset['mean_CR_last_reward_100%']
    ]
    
   


cr=[
    group_dataset_fmri['lastCR_7_patch_leaving_low'],
    group_dataset_fmri['lastCR_6_patch_leaving_low'],
    group_dataset_fmri['lastCR_5_patch_leaving_low'],
    group_dataset_fmri['lastCR_4_patch_leaving_low'],
    group_dataset_fmri['lastCR_3_patch_leaving_low'],
     group_dataset_fmri['lastCR_2_patch_leaving_low'],
     group_dataset_fmri['lastCR_patch_leaving_low'],
     group_dataset_fmri['lastCR_7_patch_leaving_med'],
    group_dataset_fmri['lastCR_6_patch_leaving_med'],
     group_dataset_fmri['lastCR_5_patch_leaving_med'],
    group_dataset_fmri['lastCR_4_patch_leaving_med'],
     group_dataset_fmri['lastCR_3_patch_leaving_med'],
     group_dataset_fmri['lastCR_2_patch_leaving_med'],
     group_dataset_fmri['lastCR_patch_leaving_med'],
     group_dataset_fmri['lastCR_7_patch_leaving_high'],
    group_dataset_fmri['lastCR_6_patch_leaving_high'],
     group_dataset_fmri['lastCR_5_patch_leaving_high'],
    group_dataset_fmri['lastCR_4_patch_leaving_high'],
     group_dataset_fmri['lastCR_3_patch_leaving_high'],
     group_dataset_fmri['lastCR_2_patch_leaving_high'],
     group_dataset_fmri['lastCR_patch_leaving_high']
     ]




av_cr=avmc_hum+avmc_hum_fmri
null_ci_95=stats.t.interval(0.95, len(av_cr)-1, 
                            loc=np.mean(av_cr), 
                            scale=stats.sem(av_cr))

null_ci_95=stats.t.interval(0.95, len(avmc_ani)-1, 
                            loc=np.mean(avmc_ani), 
                            scale=stats.sem(avmc_ani))


tp=['-2']*len(cr[0])+['-1']*len(cr[0])+['last']*len(cr[0])#last three captures 
#tp=['-3']*len(cr[0])+['-2']*len(cr[0])+['-1']*len(cr[0])+['last']*len(cr[0])#last four captures 
#tp=['-5']*len(cr[0])+['-4']*len(cr[0])+['-2']*len(cr[0])+['-1']*len(cr[0])+['last']*len(cr[0])#last 5
#tp=['-6']*len(cr[0])+['-5']*len(cr[0])+['-4']*len(cr[0])+['-3']*len(cr[0])+['-2']*len(cr[0])+['-1']*len(cr[0])+['last']*len(cr[0])#last 7
tp=tp*3
#pt=['50%']*(len(cr[0])*5)+['75%']*(len(cr[0])*5)+['100%']*(len(cr[0])*5)
pt=['50%']*(len(cr[0])*7)+['75%']*(len(cr[0])*7)+['100%']*(len(cr[0])*7)
pt=['50%']*(len(cr[0])*3)+['75%']*(len(cr[0])*3)+['100%']*(len(cr[0])*3)
cr=[item for sublist in cr for item in sublist]

d = {'ICR': cr, 'Patch Type': pt, 'Reward Capture':tp
        }
dataSet= pd.DataFrame(data=d)

plt.figure(figsize=(8,6))

pl=sns.pointplot("Reward Capture", "ICR", hue="Patch Type",
    data=dataSet, dodge=True, join=True,errorbar='se',palette="viridis")

#pl.axhline(np.mean(lst_hum), color='red',ls='--',lw=0.5)#Hum
pl.axhline(np.mean(avmc_ani), color='black',ls='--',lw=0.5)#Ani
#pl.axhline(np.mean(avmc_hum_fmri), color='black',ls='--',lw=0.5)#
#pl.axhline(np.mean(av_cr), color='black',ls='--',lw=0.5)#
plt.ylim(0, 0.8)#ani
plt.axhspan(null_ci_95[0], null_ci_95[1], facecolor='gray', alpha=0.35)
#plt.ylim(0, 0.5)#hum
sns_plot = pl.get_figure()
#sns_plot.savefig(wdir +f'ICR_vs_MCR_last_hits_HUM_fmri.svg')
sns_plot.savefig(wdir +f'/joint_analysis/last_ICR_by_epoch_gerbils.svg')
# Plot the responses for different events and regions
# sns.lineplot(x="Fixation", y="ICR",
#              hue="patch type",style="patch type",
#              errorbar=('ci', 10),
#              data=dataSet)



#viridis

'''
plot last CR as function of block 

            FMRI
'''

all_cr=[item for sublist in group_dataset_fmri['CR_blockwise_low'] for item in sublist]
blocks=['1','2','3','4','5','6']*6+['1','2','3','4','5']+['1','2','3','4','5','6']*13
patch=['low']*len(all_cr)+['med']*len(all_cr)+['high']*len(all_cr)
blocks=blocks*3
cr_m=[item for sublist in group_dataset_fmri['CR_blockwise_med'] for item in sublist]
cr_h=[item for sublist in group_dataset_fmri['CR_blockwise_high'] for item in sublist]
all_cr=all_cr+cr_m+cr_h

d = {'Last ICR': all_cr, 'Patch Type': patch, 'Epoch':blocks
        }
dataSet= pd.DataFrame(data=d)


plt.figure(figsize=(8,6))

pl=sns.pointplot("Epoch", "Last ICR", hue="Patch Type",
    data=dataSet, dodge=True, join=True,errorbar='se',palette="viridis")

#pl.axhline(np.mean(lst_hum), color='red',ls='--',lw=0.5)#Hum
#pl.axhline(np.mean(avmc_ani), color='red',ls='--',lw=0.5)#Ani
#pl.axhline(np.mean(avmc_hum_fmri), color='black',ls='--',lw=0.5)#Ani
pl.axhline((np.mean(avmc_hum)+np.mean(avmc_hum_fmri))/2, color='black',ls='--',lw=0.5)#Ani
plt.ylim(0, 0.5)#ani
#plt.ylim(0, 0.5)#hum
sns_plot = pl.get_figure()
sns_plot.savefig(wdir +f'last_ICR_by_epoch_HUM_fmri.svg')


