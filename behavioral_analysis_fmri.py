#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 17 10:36:09 2021

@author: lasseguldener
"""
from __future__ import division

'''
###    FORAGING PILOTS SFB C02 - WP1.1
###    behavioral analysis 
'''

import os
import numpy as np
import pandas as pd
from ast import literal_eval
from scipy import stats
import matplotlib.pyplot as plt
import math
from ast import literal_eval

import scipy.stats as stats
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math

from lifelines import CoxPHFitter
import pandas as pd

#import rm_anova
from statsmodels.stats.anova import AnovaRM


#sns.set_theme(style="darkgrid")

sns.set_theme(style="darkgrid",palette="pastel")



'''
###  directories
'''

datapath=os.getcwd()+'/'

'''
###  info varis
'''

version='random_loc'#'fixed_loc'
number_of_targets=40#40
nBlocks=6
#nSubs=range(21,40)


nsubs=[6,7,8,9,10,11,12]





'''
###  functions
'''

cox_params={}
cox_params['start']=[]
cox_params['end']=[]



#mk dic to save data on group level
group_dataset_fmri={}

'''
list containing lables for all variables / parameters of interest 
'''
key_list=['sub','reward','ITT','trial_dur','early_break','patch_leaving','exhaustive_search','last_target_RT','nTrials','mean_nTrials_patch_leaving',
      'meanTP_patch_leaving','meanTP_forced_leaving',
      'relTP_patch_leaving_low','meanTP_patch_leaving_low','relTP_patch_leaving_med','meanTP_patch_leaving_med','relTP_patch_leaving_high',
      'meanTP_patch_leaving_high','total$_patch_leaving','mean$_patch_leaving_low','mean$_patch_leaving_med','mean$_patch_leaving_high',
      'mean_ITT_patch_leaving_low','mean_ITT_patch_leaving_med','mean_ITT_patch_leaving_high',
      'lastITT_patch_leaving_low','lastITT_patch_leaving_med','lastITT_patch_leaving_high',
      'meanCR_patch_leaving_low','meanCR_patch_leaving_med','meanCR_patch_leaving_high',
      'mean_nTrials_patch_leaving_low','mean_nTrials_patch_leaving_med','mean_nTrials_patch_leaving_high',
      'mean_trial_dur_patch_leaving_low','mean_trial_dur_patch_leaving_med','mean_trial_dur_patch_leaving_high',
      'mean$_forced_leaving','mean$_patch_leaving',
      'lastCR_patch_leaving_low','lastCR_patch_leaving_med','lastCR_patch_leaving_high',
      'GUT_patch_leaving_low','GUT_patch_leaving_med','GUT_patch_leaving_high','full_search',
      'GUT_early_break','mean$_early_break','mean_ITT_early_break','meanTP_early_break',
      'mean_trial_dur_early_break','mean_nTrials_early_break','meanCR_early_break','lastCR_early_break',
      'overall_CR',
      'lastCR_2_patch_leaving_low',
      'lastCR_3_patch_leaving_low',
      'lastCR_2_patch_leaving_med',
      'lastCR_3_patch_leaving_med',
      'lastCR_2_patch_leaving_high',
      'lastCR_3_patch_leaving_high',




      ]
          
for key in key_list:
   group_dataset_fmri['{0}'.format(key)]=[] 
  



'''
helper functions 
'''

#this func finds the correct indices 
def all_indices(value, qlist):
        indices = []
        idx = -1
        while True:
            try:
                idx = qlist.index(value, idx+1)
                indices.append(idx)
            except ValueError:
                break
        return indices
    
    
    
def TrialFinder(ind,dv): #ind = indices (list), dic=dic with condis for odd and even , dv = dependent variable
    dvXcondition=[]
    

    if len(ind)>0:
        av=np.zeros(shape=(len(ind)))
        av=av.tolist()        

        for i in range(len(ind)):
            av[i] = dv[ind[i]]
        
        dvXcondition.append(av)
    
    else:
        av=np.nan
        dvXcondition.append([np.nan])
    
    return dvXcondition[0]

'''
function  that reads out csv/tsv file , averages across blocks and results in one dic per subj session

'''


def load_file(version,sub,nBlocks,number_of_targets,keys):
    number_of_search_targets=number_of_targets
    all_rew=[]
    singl_subj={}
    for key in keys:
        singl_subj['{0}'.format(key)]=[] 

    sub=int(sub)
    reward=0
    singl_subj['sub'].append(sub)
    
 
    if sub ==2:
        nb=4
    else:nb=5
    
    for n_block in range(0,5):

        df=pd.read_csv(datapath +f"/human_foraging/data/beh/sub-{sub}/beh-data_sub-0{sub}_block-0{n_block}.tsv",sep='\t',error_bad_lines=False)
        
        for ele in range(len(df['reward_ons'])):
            df['reward_ons'][ele]=literal_eval(df['reward_ons'][ele])
            df['detection'][ele]=literal_eval(df['detection'][ele])
            df['reward_prob_next_target'][ele]=literal_eval(df['reward_prob_next_target'][ele])
            df['responseTime'][ele]=literal_eval(df['responseTime'][ele])
             
                
        ITT=[]
        search_dur=[]
        reward2=[]
        trial_type=[]
        search_time=[]
        patchleaving=0
        exhaustivesearch=0
        last_targ_det=[]
        count_trial=0
        euro=[]
        
        time_first_half=[]
        time_second_half=[]
        time_first=[]
        time_second=[]
        time_third=[]
        time_fourth=[]
        
        sec_last_low=[]
        third_last_low=[]
        
        sec_last_med=[]
        third_last_med=[]
        
        sec_last_high=[]
        third_last_high=[]
        
        start=[]
        end=[]
        trial_time=[]
        split_time=[]
        
        last_cr=[]
        start_prob=[]
        
        tp_ex=[]
        tp=[]
        giving_up_time=[]
        
        #for block in range(nBlocks):
        intertarget_time=[]
        ICR=[]

        
        reward+=sum(df['reward'])
        nTrials=len(df['fix'])
    
        singl_subj['nTrials'].append(len(df['fix']))
        #group_dataset_fmri['nTrials'].append(nTrials)
       
        
       
        '''
        number of trials is not pre-determined due to the countdown...
        
    
        '''
        for trial in range(nTrials):
            intertarget_time=[]
                
            start.append(df['search'][trial])
            end.append(df['end of search'][trial])
            start_prob.append(df['start_prob'][trial])
            #if trial >1:
            euro.append(df['reward'][trial])
            
            all_rew.append(df['reward'][trial])
            if sub == 20:
                print ('reward',euro[trial])
            if len(df['responseTime'][trial]) >0:
                 count_trial+=1
                 
            if 'early break' in df['trial type'][trial]:
                trial_type.append(0)
                
            else:trial_type.append(1)
                
            for targ in range(len(df['detection'][trial])):
              
                
                if targ < len(df['detection'][trial])-1:
                    diff=df['detection'][trial][targ+1]-df['detection'][trial][targ]
                    intertarget_time.append(diff)
                    
                elif targ == len(df['detection'][trial]):
                    diff=df['detection'][trial][targ-1]-df['detection'][trial][targ-2]
                    intertarget_time.append(diff)
                    ICR.append(1/diff)
                    
                    
                    
                for idx, item in enumerate(df['detection'][trial]):
                    
                    if idx == len(df['detection'][trial]) - 1:
                                  
                        last_itt=item - df['detection'][trial][idx-1]
                        #print (f'last ITT: {last_itt}')
                        last_cr.append(last_itt)
                        
         
            #take response time of last target (i.e, time of detection - search onset )
            if df['reward'][trial] <  number_of_search_targets:
                patchleaving+=1
                search_time.append(1)
                reward2.append(0)
                
                if len(df['detection'][trial]) >0:
                    giving_up_time.append(df['end of search'][trial]-df['detection'][trial][-1])
                else:giving_up_time.append(np.nan)
                
                all_det=len(df['responseTime'][trial])
                try:
                    detection_last_target=df['responseTime'][trial][all_det-1]
                except IndexError:
                    detection_last_target=np.nan
                    
                last_targ_det.append(detection_last_target)
                # target_prob_pl=(number_of_search_targets-all_det)/number_of_search_targets
                
                # if sub ==11:
                #     print ('tp',target_prob_pl)
                    
                if len (df['reward_prob_next_target'][trial]) >1:
                    tp_pl=df['reward_prob_next_target'][trial][-2:]
                elif len (df['reward_prob_next_target'][trial]) >0:
                    tp_pl=df['reward_prob_next_target'][trial][-1:]
                else:tp_pl=[np.nan]
                tp.append(tp_pl[0])
                
                    
                
            elif df['reward'][trial] ==number_of_search_targets:
                search_time.append(0)
                exhaustivesearch+=1
                reward2.append(1)
                tp_ex=df['reward_prob_next_trial'][trial][-2:]
                tp_ex.append(tp[0])
                #target_prob_ex=(number_of_targets-all_det)/35.0
                #tp_ex.append(target_prob_ex)
            
            
            
            if not type(df['search_dur_patch_leaving'][trial])==list:
                search_dur.append(df['search_dur_patch_leaving'][trial])
            else:
                search_dur.append(np.nan)
                
            ITT.append(intertarget_time)
            
            if df['start_prob'][trial]==0.5:
            
                if len(intertarget_time)>1:
                    
                    sec_last_low.append(1/intertarget_time[len(intertarget_time)-2])
                                                     
                    if len(intertarget_time)>2:                                
                        
                        third_last_low.append(1/intertarget_time[len(intertarget_time)-3])
                                                         
                    else:third_last_low.append(np.nan)
                    
                else:sec_last_low.append(np.nan)
                
            elif df['start_prob'][trial]==0.75:
                
                if len(intertarget_time)>1:
                    
                    sec_last_med.append(1/intertarget_time[len(intertarget_time)-2])
                                                     
                    if len(intertarget_time)>2:                                
                        
                        third_last_med.append(1/intertarget_time[len(intertarget_time)-3])
                                                         
                    else:third_last_med.append(np.nan)
                    
                else:sec_last_med.append(np.nan)
            
            elif df['start_prob'][trial]==1:
                
                if len(intertarget_time)>1:
                    
                    sec_last_high.append(1/intertarget_time[len(intertarget_time)-2])
                                                     
                    if len(intertarget_time)>2:                                
                        
                        third_last_high.append(1/intertarget_time[len(intertarget_time)-3])
                                                         
                    else:third_last_high.append(np.nan)
                    
                else:sec_last_high.append(np.nan)

  
    
        print ('###')
        print ('sub %i'%sub)
        
        #print (last_cr)
        #print (intertarget_time)
      
        matrix=list(zip(reward2,search_time,trial_type))
        matrix2=list(zip(reward2,search_time,trial_type,start_prob))
    
        
        #mk use of indices function to find number of trials for each condition
        patch_leaving_indis=all_indices((0,1,1),matrix)  
        early_break_indis=all_indices((0,1,0),matrix)
        forced_leaving_indis=all_indices((0,0,1),matrix)
    
        
        '''
                get indices for each prob condition
        '''
        
        patch_leaving_indis_low=all_indices((0,1,1,0.5),matrix2)  
        early_break_indis_low=all_indices((0,1,0,0.5),matrix2)
        forced_leaving_indis_low=all_indices((0,0,1,0.5),matrix2)
        
        patch_leaving_indis_med=all_indices((0,1,1,0.75),matrix2)  
        early_break_indis_med=all_indices((0,1,0,0.75),matrix2)
        forced_leaving_indis_med=all_indices((0,0,1,0.75),matrix2)
        
        patch_leaving_indis_high=all_indices((0,1,1,1.0),matrix2)  
        early_break_indis_high=all_indices((0,1,0,1.0),matrix2)
        forced_leaving_indis_high=all_indices((0,0,1,1.0),matrix2)
        
        
        ITT_patch_leaving=TrialFinder(patch_leaving_indis,ITT)
        ITT_early_break=TrialFinder(early_break_indis,ITT)
        rew_early_break=TrialFinder(early_break_indis,euro)
        rew_patch_leaving=TrialFinder(patch_leaving_indis,euro)
        
        
        '''
                collect values for each prob condi
                
        '''
        rew_patch_leaving_low=TrialFinder(patch_leaving_indis_low,euro)
        rew_patch_leaving_med=TrialFinder(patch_leaving_indis_med,euro)
        rew_patch_leaving_high=TrialFinder(patch_leaving_indis_high,euro)
        
        giving_up_time_low=TrialFinder(patch_leaving_indis_low,giving_up_time)
        giving_up_time_med=TrialFinder(patch_leaving_indis_med,giving_up_time)
        giving_up_time_high=TrialFinder(patch_leaving_indis_high,giving_up_time)
    
        
        
        ITT_patch_leaving_low=TrialFinder(patch_leaving_indis_low,ITT)
        ITT_patch_leaving_med=TrialFinder(patch_leaving_indis_med,ITT)
        ITT_patch_leaving_high=TrialFinder(patch_leaving_indis_high,ITT)
        
        tp_patch_leaving_low=TrialFinder(patch_leaving_indis_low,tp)
        tp_patch_leaving_med=TrialFinder(patch_leaving_indis_med,tp)
        tp_patch_leaving_high=TrialFinder(patch_leaving_indis_high,tp)
        
        searchdur_patch_leaving_low=TrialFinder(patch_leaving_indis_low,search_dur)
        #print (searchdur_patch_leaving_low)
        #searchdur_patch_leaving_low=[item for item in searchdur_patch_leaving_low if type(item)!=str]
        #print (searchdur_patch_leaving_low)
        
        searchdur_patch_leaving_med=TrialFinder(patch_leaving_indis_med,search_dur)
        #searchdur_patch_leaving_med=[item for item in searchdur_patch_leaving_med if type(item)!=str]
        
        searchdur_patch_leaving_high=TrialFinder(patch_leaving_indis_high,search_dur)
        #searchdur_patch_leaving_high=[item for item in searchdur_patch_leaving_high if type(item)!=str]
        
        last_cr_low=TrialFinder(patch_leaving_indis_low,last_cr)
        last_cr_med=TrialFinder(patch_leaving_indis_med,last_cr)
        last_cr_high=TrialFinder(patch_leaving_indis_high,last_cr)
    
        
        
        '''
        forced switch => early break 
    
        '''
        
        
        giving_up_time_early_break=TrialFinder(early_break_indis,giving_up_time)
        rew_early_break=TrialFinder(early_break_indis,euro)
        ITT_early_break=TrialFinder(early_break_indis,ITT)
        tp_early_break=TrialFinder(early_break_indis,tp)
        searchdur_early_break=TrialFinder(early_break_indis,search_dur)
        last_cr_early_break=TrialFinder(early_break_indis_low,last_cr)

        





        #add everything to the dictionary 
    
        
        try:
            singl_subj['trial_dur'].append(np.nanmedian(search_dur))
        except TypeError:
            singl_subj['trial_dur'].append(np.nan)
        singl_subj['last_target_RT'].append(last_targ_det)
        singl_subj['patch_leaving'].append(patchleaving)
        singl_subj['early_break'].append(len(early_break_indis))
        singl_subj['reward'].append(reward)

        
        singl_subj['full_search'].append(exhaustivesearch)
        singl_subj['mean_nTrials_patch_leaving'].append(len(patch_leaving_indis))
    
        
        singl_subj['meanTP_patch_leaving'].append(np.nanmedian(tp))
            
        singl_subj['mean$_patch_leaving'].append(np.nanmedian(rew_patch_leaving))
        singl_subj['total$_patch_leaving'].append(sum(euro))

                
        '''
                save for each prob condi
                
        '''
    
        singl_subj['mean_nTrials_patch_leaving_low'].append(len(patch_leaving_indis_low))
        singl_subj['mean_trial_dur_patch_leaving_low'].append(np.nanmedian(searchdur_patch_leaving_low))
        singl_subj['mean$_patch_leaving_low'].append(np.nanmedian(rew_patch_leaving_low))
        if len(ITT_patch_leaving_low) >1:
            ITT_patch_leaving_low = [x for x in ITT_patch_leaving_low if len(x) > 0]
            ITT_patch_leaving_low=[item for sublist in ITT_patch_leaving_low for item in sublist]
        singl_subj['mean_ITT_patch_leaving_low'].append(np.nanmedian(ITT_patch_leaving_low))
        singl_subj['relTP_patch_leaving_low'].append(np.nanmedian(tp_patch_leaving_low)/0.5)
        singl_subj['meanTP_patch_leaving_low'].append(np.nanmedian(tp_patch_leaving_low))
        singl_subj['meanCR_patch_leaving_low'].append(1/np.nanmean(ITT_patch_leaving_low))

        
        singl_subj['mean_nTrials_patch_leaving_med'].append(len(patch_leaving_indis_med))
        singl_subj['mean_trial_dur_patch_leaving_med'].append(np.nanmedian(searchdur_patch_leaving_med))
        singl_subj['mean$_patch_leaving_med'].append(np.nanmedian(rew_patch_leaving_med))
        if len(ITT_patch_leaving_med) >1:
            ITT_patch_leaving_med = [x for x in ITT_patch_leaving_med if len(x) > 0]
            ITT_patch_leaving_med=[item for sublist in ITT_patch_leaving_med for item in sublist]
        singl_subj['mean_ITT_patch_leaving_med'].append(np.nanmedian(ITT_patch_leaving_med))
        singl_subj['relTP_patch_leaving_med'].append(np.nanmedian(tp_patch_leaving_med)/0.75)
        singl_subj['meanTP_patch_leaving_med'].append(np.nanmedian(tp_patch_leaving_med))
        singl_subj['meanCR_patch_leaving_med'].append(1/np.nanmean(ITT_patch_leaving_med))
    
        singl_subj['mean_nTrials_patch_leaving_high'].append(len(patch_leaving_indis_high))
        singl_subj['mean_trial_dur_patch_leaving_high'].append(np.nanmedian(searchdur_patch_leaving_high))
        singl_subj['mean$_patch_leaving_high'].append(np.nanmedian(rew_patch_leaving_high))
        if len(ITT_patch_leaving_high) >1:
            ITT_patch_leaving_high = [x for x in ITT_patch_leaving_high if len(x) > 0]
            ITT_patch_leaving_high=[item for sublist in ITT_patch_leaving_high for item in sublist]
        singl_subj['mean_ITT_patch_leaving_high'].append(np.nanmedian(ITT_patch_leaving_high))
        singl_subj['relTP_patch_leaving_high'].append(np.nanmedian(tp_patch_leaving_high)/1.0)
        singl_subj['meanTP_patch_leaving_high'].append(np.nanmedian(tp_patch_leaving_high))
        singl_subj['meanCR_patch_leaving_high'].append(1/np.nanmean(ITT_patch_leaving_high))
        
       
        singl_subj['lastCR_2_patch_leaving_low'].append(np.nanmean(sec_last_low))
        singl_subj['lastCR_3_patch_leaving_low'].append(np.nanmean(third_last_low))
        
        singl_subj['lastCR_2_patch_leaving_med'].append(np.nanmean(sec_last_med))
        singl_subj['lastCR_3_patch_leaving_med'].append(np.nanmean(third_last_med))
        
        singl_subj['lastCR_2_patch_leaving_high'].append(np.nanmean(sec_last_high))
        singl_subj['lastCR_3_patch_leaving_high'].append(np.nanmean(third_last_high))        
            
        singl_subj['GUT_patch_leaving_low'].append(np.nanmedian(giving_up_time_low))
        singl_subj['GUT_patch_leaving_med'].append(np.nanmedian(giving_up_time_med))
        singl_subj['GUT_patch_leaving_high'].append(np.nanmedian(giving_up_time_high))

        singl_subj['lastCR_patch_leaving_low'].append(1/np.nanmean(last_cr_low))
        singl_subj['lastCR_patch_leaving_med'].append(1/np.nanmean(last_cr_med))
        singl_subj['lastCR_patch_leaving_high'].append(1/np.nanmean(last_cr_high))
        
        singl_subj['lastITT_patch_leaving_low'].append(np.nanmean(last_cr_low))
        singl_subj['lastITT_patch_leaving_med'].append(np.nanmean(last_cr_med))
        singl_subj['lastITT_patch_leaving_high'].append(np.nanmean(last_cr_high))
        singl_subj['overall_CR'].append(sum(euro)/(10*60))
        
        
        
        '''
        control condition 
        
        '''

        
        singl_subj['mean_nTrials_early_break'].append(len(early_break_indis))
        singl_subj['mean_trial_dur_early_break'].append(np.nanmedian(searchdur_early_break))
        singl_subj['mean$_early_break'].append(np.nanmedian(rew_early_break))
        if len(ITT_early_break) >1:
            print (ITT_early_break)
            ITT_early_break = [x for x in ITT_early_break if len(x) > 0]
            ITT_early_break=[item for sublist in ITT_early_break for item in sublist]
        # singl_subj['mean_ITT_early_break'].append(np.nanmedian(ITT_early_break))
        singl_subj['meanTP_early_break'].append(np.nanmedian(tp_early_break))
        singl_subj['meanCR_early_break'].append(1/np.nanmean(ITT_early_break))
        singl_subj['lastCR_early_break'].append(1/np.nanmean(last_cr_early_break))
        singl_subj['GUT_early_break'].append(np.nanmedian(giving_up_time_early_break))
        
        
        
        
        # 'relTP_forced_switch','meanTP_forced_switch','total$_forced_switch',
        # 'mean_ITT_forced_switch','lastITT_forced_switch'

        

    # for key in singl_subj:
    #     #singl_subj[key]=list(singl_subj[key])
       
    avgDict={}
    for k,v in singl_subj.items():
    # v is the list of grades for student k
        if len(v)>0:
            if type(v[0])==list:
                try:
                    singl_subj[k]=[item for sublist in singl_subj[k] for item in sublist]
                except TypeError:
                    pass
                if k != 'nTrials' or  k != 'patch_leaving':
                    try:
                        avgDict[k] = np.nanmean(v)
                    except AttributeError:
                        try:
                            singl_subj[k]=[item for sublist in singl_subj[k] for item in sublist]
                        except TypeError:
                            print ('####    ERROR     ####')
                            print (f'TypeError with {k}')
                            print ('please check!')
                            print (type(singl_subj[k]))
                            print ('####')
                            pass
                else:
                    avgDict[k] = np.nansum(v)
            else:
                if k != 'nTrials' or  k != 'patch_leaving':
                    try:
                        avgDict[k] = np.nanmean(v)
                    except AttributeError:
                        singl_subj[k]=[item for sublist in singl_subj[k] for item in sublist]
                        print (k)
                        print (type(singl_subj[k]))
                else:
                    avgDict[k] = np.nansum(v)

    #avgDict['overall_CR']=sum(all_rew)/(60*60)
            
    avgDict['total$_patch_leaving']=reward/(60*60)
    return avgDict


'''
run analysis
'''

for sub in  nsubs:
    one_sub=load_file(version,sub,nBlocks,number_of_targets,key_list)
    

    for key in key_list:    
            try:
                group_dataset_fmri[key].append(one_sub[key])
            except KeyError:
                pass


for key in key_list:   
    if len(group_dataset_fmri[key])<1:     
        group_dataset_fmri.pop(key, 0)
        
'''
write to tsv

'''
tsv_file= datapath + f"beh-data-all_subs.tsv"
data=pd.DataFrame(group_dataset_fmri) 
if not os.path.isfile(tsv_file):
    data.to_csv(datapath +f"beh-data-all_subs.tsv",
                sep=',',index=False,header=True)
else:
     with open(tsv_file,'a') as f:
         data.to_csv(f, header=False,index=False)
 
        
 
'''
start calculations
'''
#group_df=pd.DataFrame(group_dataset_fmri) 
mean_reward=np.mean(group_dataset_fmri['reward'])
#[item for sublist in group_dataset_fmri['ITT'] for item in sublist]
#[item for sublist in group_dataset_fmri['trial_dur'] for item in sublist]
#mean_ITT=np.mean(group_dataset_fmri['ITT'][0])  
ntrials_all=(np.mean(group_dataset_fmri['mean_nTrials_patch_leaving_low'])+np.mean(group_dataset_fmri['mean_nTrials_patch_leaving_med'])+np.mean(group_dataset_fmri['mean_nTrials_patch_leaving_high']))/3.0

'''
        get some out put
'''
print('######')
print('## means ##')
print ('$:',mean_reward)
#print ('ITT:',mean_ITT)
print('######')

print ('mean number of trials')

print ('nTrials patch leaving low prob: %.4f '%(np.mean(group_dataset_fmri['mean_nTrials_patch_leaving_low'])))
print('######')
print ('nTrials patch leaving med prob: %.4f '%(np.mean(group_dataset_fmri['mean_nTrials_patch_leaving_med'])))
print('######')
print ('nTrials patch leaving high prob: %.4f '%(np.mean(group_dataset_fmri['mean_nTrials_patch_leaving_high'])))
print('######')
print ('mean $$$ patch leaving low prob: %.4f +/- %.4f SD'%(np.mean(group_dataset_fmri['mean$_patch_leaving_low']),np.mean(group_dataset_fmri['sd$_patch_leaving_low'])))
print('######')
print ('mean $$$ patch leaving med prob: %.4f +/- %.4f SD'%(np.mean(group_dataset_fmri['mean$_patch_leaving_med']),np.mean(group_dataset_fmri['sd$_patch_leaving_med'])))
print('######')
print ('mean $$$ patch leaving high prob: %.4f +/- %.4f SD'%(np.mean(group_dataset_fmri['mean$_patch_leaving_high']),np.mean(group_dataset_fmri['sd$_patch_leaving_high'])))
print('######')

print ('mean target probability of last target for patch leaving low prob: %.4f +/- %.4f SD'%(np.mean(group_dataset_fmri['meanTP_patch_leaving_low']),np.mean(group_dataset_fmri['sdTP_patch_leaving_low'])))
print('######')
print ('mean target probability of last target for patch leaving medium prob: %.4f +/- %.4f SD'%(np.mean(group_dataset_fmri['meanTP_patch_leaving_med']),np.mean(group_dataset_fmri['sdTP_patch_leaving_med'])))
print('######')
print ('mean target probability of last target for patch leaving high prob: %.4f +/- %.4f SD'%(np.mean(group_dataset_fmri['meanTP_patch_leaving_high']),np.mean(group_dataset_fmri['sdTP_patch_leaving_high'])))

print('######')
print ('mean InterTargTime for patch leaving low prob: %.4f +/- %.4f SD'%(np.mean(group_dataset_fmri['mean_ITT_patch_leaving_low']),np.mean(group_dataset_fmri['sd_ITT_patch_leaving_low'])))
print('######')
print ('mean InterTargTime for patch leaving med prob: %.4f +/- %.4f SD'%(np.mean(group_dataset_fmri['mean_ITT_patch_leaving_med']),np.mean(group_dataset_fmri['sd_ITT_patch_leaving_med'])))
print('######')
print ('mean InterTargTime for patch leaving high prob: %.4f +/- %.4f SD'%(np.mean(group_dataset_fmri['mean_ITT_patch_leaving_high']),np.mean(group_dataset_fmri['sd_ITT_patch_leaving_high'])))
print('######')

print ('mean CollRate for patch leaving low prob: %.4f +/- %.4f SD'%(np.mean(group_dataset_fmri['meanCR_patch_leaving_low']),np.mean(group_dataset_fmri['sdCR_patch_leaving_low'])))
print('######')
print ('mean CollRate for patch leaving med prob: %.4f +/- %.4f SD'%(np.mean(group_dataset_fmri['meanCR_patch_leaving_med']),np.mean(group_dataset_fmri['sdCR_patch_leaving_med'])))
print('######')
print ('mean CollRate for patch leaving high prob: %.4f +/- %.4f SD'%(np.mean(group_dataset_fmri['meanCR_patch_leaving_high']),np.mean(group_dataset_fmri['sdCR_patch_leaving_high'])))
print('######')

'''
# =============================================================================
#   OUTLIERS?
# =============================================================================
'''
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
    print ('filtered data')
    print(filt_df['n_trial'].describe())
    return filt_df

# filt_df=remove_outliers(df, q=0.01)



# #outlier_reward=TrialFinder([5,16],group_dataset_fmri['total$_patch_leaving'])
# filt_df['old_n_trial']=group_dataset_fmri['mean_nTrials_patch_leaving']
# filt_df['n_trial_high']=group_dataset_fmri['mean_nTrials_patch_leaving_high']
# filt_df['n_trial_med']=group_dataset_fmri['mean_nTrials_patch_leaving_med']
# filt_df['n_trial_low']=group_dataset_fmri['mean_nTrials_patch_leaving_low']





'''
    plotting with seaborn
    
'''
def plotting(l1,label_y,plot_name,subs):
    
    l2=[[0.5]*len(subs),[0.75]*len(subs),[1]*len(subs)]
    l1=[item for sublist in l1 for item in sublist]
    l2=[item for sublist in l2 for item in sublist]
    
    plotted = sns.boxplot(x=l2, y=l1)
    plotted.set(xlabel='Start Reward Probability', ylabel=label_y)
    #https://stackoverflow.com/questions/36578458/how-does-one-insert-statistical-annotations-stars-or-p-values-into-matplotlib
    # x1, x2 = 0, 1   # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
    # y, h, col = max(l1) + 0.02, 0.02, 'k'
    # plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c=col)
    # plt.text((x1+x2)*.5, y+h, "**", ha='center', va='bottom', color=col)
    # x1, x2 = 1, 2   # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
    # y, h, col = max(l1) + 0.04, 0.04, 'k'
    # plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c=col)
    # plt.text((x1+x2)*.5, y+h, "**", ha='center', va='bottom', color=col)
    # x1, x2 = 0, 2   # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
    # y, h, col = max(l1) + 0.06,0.06, 'k'
    # plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c=col)
    # plt.text((x1+x2)*.5, y+h, "**", ha='center', va='bottom', color=col)
    
    # y1=0.5*np.mean(group_dataset_fmri['meanTP_patch_leaving_low'])
    # x1=round(30-np.mean(group_dataset_fmri['meanTP_patch_leaving_low'])*30)
    # y2=0.75*np.mean(group_dataset_fmri['meanTP_patch_leaving_med'])
    # x2=round(45-np.mean(group_dataset_fmri['meanTP_patch_leaving_med'])*45)
    # y3=0.75*np.mean(group_dataset_fmri['meanTP_patch_leaving_high'])
    # x3=round(60-np.mean(group_dataset_fmri['meanTP_patch_leaving_high'])*60)
    # plt.scatter(0, y1, marker='o', s=200)
    # plt.scatter(1, y2, marker='o', s=200)
    # plt.scatter(2, y3, marker='o', s=200)

    
    
    sns_plot = plotted.get_figure()
    sns_plot.savefig(datapath +f'random_loc/exp_decay/data/final/final/{plot_name}.svg')
    plt.close()
    return None

 
# ''' 
#         1.number of trials
# '''
# lst=[group_dataset_fmri['mean_nTrials_patch_leaving_low'],
#      group_dataset_fmri['mean_nTrials_patch_leaving_med'],
#      group_dataset_fmri['mean_nTrials_patch_leaving_high']]

# plotting(lst,'Number of Trials','Ntrials',nsubs)  


''' 
        2. Trial duration
'''
lst=[group_dataset_fmri['mean_trial_dur_patch_leaving_low'],
      group_dataset_fmri['mean_trial_dur_patch_leaving_med'],
      group_dataset_fmri['mean_trial_dur_patch_leaving_high']]

plotting(lst,'Trial Duration in sec','TrialDur',nsubs)  


# ''' 
#         3. $$$ Reward
# '''
lst=[group_dataset_fmri['mean$_patch_leaving_low'],
      group_dataset_fmri['mean$_patch_leaving_med'],
      group_dataset_fmri['mean$_patch_leaving_high']]

# plotting(lst,'Mean Earnings in Cents per Patch','Reward',nsubs)  

''' 
        4. Target Probability
'''
lst=[group_dataset_fmri['meanTP_patch_leaving_low'],
      group_dataset_fmri['meanTP_patch_leaving_med'],
      group_dataset_fmri['meanTP_patch_leaving_high']]

plotting(lst,'P reward at leaving','TP',nsubs) 


# ''' 
#         5. ITT
# '''
# lst=[group_dataset_fmri['mean_ITT_patch_leaving_low'],
#       group_dataset_fmri['mean_ITT_patch_leaving_med'],
#       group_dataset_fmri['mean_ITT_patch_leaving_high']]

# plotting(lst,'Mean Intertarget Time in sec','ITT',nsubs) 


''' 
# =============================================================================
#         6. Collection Rate - does CR drop according to marginal value theory below average CR before patch leaving?
# =============================================================================
'''




# #wide format
# hal1 = group_dataset_fmri['meanCR_patch_leaving_low']+group_dataset_fmri['meanCR_patch_leaving_med']+group_dataset_fmri['meanCR_patch_leaving_high']
# hal1=[float(i) for i in hal1 ]
# hal2 =group_dataset_fmri['lastCR_patch_leaving_low']+group_dataset_fmri['lastCR_patch_leaving_med']+group_dataset_fmri['lastCR_patch_leaving_high']
# hal2=[float(i) for i in hal2 ]
# condi=['low']*((len(nsubs)))+['med']*((len(nsubs)))+['high']*((len(nsubs)))
# df = pd.DataFrame(np.c_[hal1, hal2, condi]) # modified @Elliots dataframe production
# df['average']=df[0]
# df['last']=df[1]
# df['Prob']=df[2]
# df = df.melt(id_vars=['Prob'], value_vars=['average', 'last'])
# df['value']=[float(i) for i in df['value']]
# sns.factorplot("Prob", hue="variable", y="value", data=df, kind="box")

# #remove outliers 
# q = df["value"].quantile(0.95)
# for ele in range(len(df['value'])):
#     if df["value"][ele] > q:
#         print (df["value"][ele])
#         df["value"][ele]=np.nan
        
# # x1, x2 = 1, 2   # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
# # y, h, col = max(l1) + 0.02, 0.02, 'k'
# # plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c=col)
# # plt.text((x1+x2)*.5, y+h, "**", ha='center', va='bottom', color=col)
# # x1, x2 = 0, 1   # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
# # y, h, col = max(l1) + 0.04, 0.04, 'k'
# # plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c=col)
# # plt.text((x1+x2)*.5, y+h, "**", ha='center', va='bottom', color=col)
# # x1, x2 = 0, 2   # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
# # y, h, col = max(l1) + 0.06,0.06, 'k'
# # plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c=col)
# #     # plt.text((x1+x2)*.5, y+h, "**", ha='center', va='bottom', color=col)
# #new plot
# sns_plot=sns.factorplot("Prob", hue="variable", y="value", data=df, kind="box")
# sns_plot.savefig(datapath + f'random_loc/exp_decay/data/final/final/CR_av_vs_last.png')
# plt.close()


'''
# =============================================================================
# statistics
# =============================================================================

'''

'''
# # =============================================================================
# # costume function to test one-sided
# # =============================================================================

# '''
# def t_test(x,y,alternative='both-sided'):
    
#          m_x=np.nanmean(x)
#          std_x=np.nanstd(x) 
#          m_y=np.nanmean(y)
#          std_y=np.nanstd(y)  
         
#          '''remove outlier'''
         
#          print (y)
#          x = np.array(x)
#          x = x[(x>np.quantile(x,0.01)) & (x<np.quantile(x,0.99))].tolist()
        
#          y = np.array(y)
#          y = y[(y>np.quantile(y,0.01)) & (y<np.quantile(y,0.99))].tolist()
        
         
#          print (y)
              
#          tval, double_p = stats.ttest_ind(x,y,equal_var = False)
#          if alternative == 'both-sided':
#              pval = double_p
#          elif alternative == 'greater':
#              if np.mean(x) > np.mean(y):
#                  pval = double_p/2.
#              else:
#                  pval = 1.0 - double_p/2.
#          elif alternative == 'less':
#              if np.mean(x) < np.mean(y):
#                  pval = double_p/2.
#              else:
#                  pval = 1.0 - double_p/2.
        
#          print ('######')
#          print (f'Mean x: {m_x}, SD = {std_x}')
#          print (f'Mean y: {m_y}, SD = {std_y}')
#          print ('######')
#          print (f't = {tval}')           
#          print (f'p = {pval}')        
         
#          return None
     
        
# '''
# # =============================================================================
# # get results for average collection rate versus CR at patch leaving -> Marginal Value Theorem 
#     should be same or last CR should drop below average 

# # =============================================================================

'''

plot probability decrease as a function of collected targets 

'''
from math import e

# p1=[]
# p075=[]
# p05=[]
# all_p=[p1,p075,p05]
# ps=[1,0.75,0.5]
# for count, prob in enumerate(ps, 0):
#     print(count, prob)
#     for r in range(1,14):
#         star_prob=prob
#         potenz=(-(r-1)/5)
#         decay_func=star_prob*e**potenz
#         all_p[count].append(decay_func)
        
        
# df = pd.DataFrame(np.c_[all_p[0], all_p[1],all_p[2]]) # modified @Elliots dataframe production
# ax = sns.lineplot(data=df, dashes=[(2, 2), (2, 2),(2, 2)])
# plt.legend(labels=["1","0.75","0.5"])
# ax.set(xlabel='Number of obtained rewards', ylabel='Reward Probability')
# sns_plot = ax.get_figure()
# # y1=0.5*np.mean(group_dataset_fmri['meanTP_patch_leaving_low'])
# # x1=round(30-np.mean(group_dataset_fmri['meanTP_patch_leaving_low'])*30)
# # y2=0.75*np.mean(group_dataset_fmri['meanTP_patch_leaving_med'])
# # x2=round(45-np.mean(group_dataset_fmri['meanTP_patch_leaving_med'])*45)
# # y3=0.75*np.mean(group_dataset_fmri['meanTP_patch_leaving_high'])
# # x3=round(60-np.mean(group_dataset_fmri['meanTP_patch_leaving_high'])*60)
# # plt.scatter(x3, y3, marker='o', s=200)
# # plt.scatter(x2, y2, marker='o', s=200)
# # plt.scatter(x1, y1, marker='o', s=200)
# #sns_plot.savefig(datapath +f'random_loc/exp_decay/data/final/final/Prob-decay.svg')





'''
# =============================================================================
# t-tests trial dur = low < med and high p <.001
# =============================================================================

'''



# rm_anova.single_rm_anova('Mean Trial Duration',[group_dataset_fmri['mean_trial_dur_patch_leaving_low'],
#                 group_dataset_fmri['mean_trial_dur_patch_leaving_med'],
#                 group_dataset_fmri['mean_trial_dur_patch_leaving_high']],len(nsubs))   


# '''
#       target probability

# '''
# rm_anova.single_rm_anova('Target Probability',[group_dataset_fmri['meanTP_patch_leaving_low'], 
#                group_dataset_fmri['meanTP_patch_leaving_med'],
#                group_dataset_fmri['meanTP_patch_leaving_high']],len(nsubs))



# rm_anova.single_rm_anova('Target Probability',[group_dataset_fmri['relTP_patch_leaving_low'], 
#                group_dataset_fmri['relTP_patch_leaving_med'],
#                group_dataset_fmri['relTP_patch_leaving_high']],len(nsubs))

# '''
#         reward

# '''

# rm_anova.single_rm_anova('Mean Reward',[group_dataset_fmri['mean$_patch_leaving_low'], 
#                                 group_dataset_fmri['mean$_patch_leaving_med'],
#                                 group_dataset_fmri['mean$_patch_leaving_high']],len(nsubs))


# '''
#         ITT

# '''

# rm_anova.single_rm_anova('ITT',[group_dataset_fmri['mean_ITT_patch_leaving_low'], 
#                                 group_dataset_fmri['mean_ITT_patch_leaving_med'],
#                                 group_dataset_fmri['mean_ITT_patch_leaving_high']],len(nsubs))




# '''
#         Giving Up Time

# '''

# rm_anova.single_rm_anova('Giving Up Time',[group_dataset_fmri['GUT_patch_leaving_low'], 
#                                 group_dataset_fmri['GUT_patch_leaving_med'],
#                                 group_dataset_fmri['GUT_patch_leaving_high']],len(nsubs))

'''
# =============================================================================
#     COX prop harzard model
#   
    
     Schätzung des Einflusses unabhängiger Variablen auf die Dauer bis zum Eintreten von Ereignissen („Überlebenszeit“) bzw. deren Hazardrate
    
    #https://stackoverflow.com/questions/56787015/is-it-possible-to-run-a-cox-proportional-hazards-model-with-an-exponential-distr
    
    #https://lifelines.readthedocs.io/en/latest/Survival%20analysis%20with%20lifelines.html
    
    #https://stackoverflow.com/questions/48640937/function-to-run-kaplanmeier-modelpython
    

    Survival analysis =
    
     Cox’s regression model can be viewed as a state-dependent rule of thumb, 
     where the state of the animal is represented by a set of explanatory variables 
     that significantly influence its tendency to leave a patch.
# =============================================================================      
'''


#create observation vector (dichotom: 0 vs 1 ) for 
# E=np.zeros(len(nsubs))
# for ele in range(len(group_dataset_fmri['mean_trial_dur_patch_leaving_low'])):
#     if group_dataset_fmri['mean_trial_dur_patch_leaving_low'][ele] > 20:
#         E[ele]=1
#     else:E[ele]=0
    

# E1=np.zeros(len(nsubs))
# for ele in range(len(group_dataset_fmri['mean_trial_dur_patch_leaving_med'])):
#     if group_dataset_fmri['mean_trial_dur_patch_leaving_med'][ele] > 20:
#         E1[ele]=1
#     else:E1[ele]=0
    

    
# E2=np.zeros(len(nsubs))
# for ele in range(len(group_dataset_fmri['mean_trial_dur_patch_leaving_high'])):
#     if group_dataset_fmri['mean_trial_dur_patch_leaving_high'][ele] > 20:
#         E2[ele]=1
#     else:E2[ele]=0
    
    
    
# E=np.zeros(len(nsubs))
# for ele in range(len(group_dataset_fmri['GUT_patch_leaving_low'])):
#     if group_dataset_fmri['GUT_patch_leaving_low'][ele] > 4:
#         E[ele]=1
#     else:E[ele]=0
    

# E1=np.zeros(len(nsubs))
# for ele in range(len(group_dataset_fmri['GUT_patch_leaving_med'])):
#     if group_dataset_fmri['GUT_patch_leaving_med'][ele] > 4:
#         E1[ele]=1
#     else:E1[ele]=0
    

    
# E2=np.zeros(len(nsubs))
# for ele in range(len(group_dataset_fmri['GUT_patch_leaving_high'])):
#     if group_dataset_fmri['GUT_patch_leaving_high'][ele] > 4:
#         E2[ele]=1
#     else:E2[ele]=0
    



'''
# =============================================================================
#         Kaplan Meyer
# =============================================================================

'''
from lifelines import KaplanMeierFitter
kmf = KaplanMeierFitter()


'''
# =============================================================================
#         determine dependent Variable and covs
# =============================================================================
        
'''
T1 = group_dataset_fmri['mean_trial_dur_patch_leaving_low']
T2 = group_dataset_fmri['mean_trial_dur_patch_leaving_med']
T3 = group_dataset_fmri['mean_trial_dur_patch_leaving_high']
T_TD=T1+T2+T3

T11 = group_dataset_fmri['GUT_patch_leaving_low']
T21 = group_dataset_fmri['GUT_patch_leaving_med']
T31 = group_dataset_fmri['GUT_patch_leaving_high']

T_GUT=T11+T21+T31

E_all=[1]*(len(nsubs)*3)#make vector with observed events 
all_cov1=group_dataset_fmri['meanTP_patch_leaving_low']+group_dataset_fmri['meanTP_patch_leaving_med']+group_dataset_fmri['meanTP_patch_leaving_high']
all_cov2=group_dataset_fmri['lastCR_patch_leaving_low']+group_dataset_fmri['lastCR_patch_leaving_med']+group_dataset_fmri['lastCR_patch_leaving_high']

patch_type=[2]*len(nsubs)+[1]*len(nsubs)+[0]*len(nsubs)#Cov3

ax = plt.subplot(111)
kmf.fit(T1, label="low")
kmf.plot(ax=ax,ci_force_lines=False)
kmf.fit(T2, label="medium")
kmf.plot(ax=ax,ci_force_lines=False)
kmf.fit(T3, label="high")
b=kmf.plot(ax=ax,ci_force_lines=False)
plt.ylim(0, 1);
plt.title('Survival function of exploiting a patch for the three display types')

#b.get_figure().savefig(datapath + f'random_loc/exp_decay/data/final/final/KM_low.png')
plt.close()



'''
# =============================================================================
#         Cox Regression
# =============================================================================
        
        basic tendency to leave the patch (baseline hazard) * hazard ratio, 
        which gives the combined effect of all the explanatory variables
        
        h0(t) is the baseline hazard function,i.e.,the innate patch leaving tendency 
        t is the time since the last renewal point, 
        and βi are the coefficients that provide the relative contribution of p covariates
        
        the model can be a tool for assessing, using experimental data, 
        which factors in the analysis affect the leaving tendency.
        
        
         h(t)=h0(t)exp{∑pi=1βizi} 
         
         
         A joint effect of the covariates leading to a hazard ratio greater than one 
         will be interpreted as having an increasing effect on patch-leaving tendency, 
         while a hazard ratio lower than one will be interpreted in the opposite way. 
         Covariates can be time-dependent or fixed. The baseline hazard, 
         which is the hazard rate when all the covariates are equal to zero, 
         is left unspecified.
         
         
         https://lifelines.readthedocs.io/en/latest/Survival%20Regression.html
              
'''

def run_CoxReg(observations,duration,cov1,cov2,cov3):#cov should be list
    
    d = {'obsv': observations, 'dur': duration,'Reward Probability': cov1,
         'Last Collection Rate':cov2,'Patch Type':cov3}
    
    dataSet= pd.DataFrame(data=d)
    cph = CoxPHFitter()
    cph.fit(dataSet, duration_col='dur', event_col='obsv')
    #cph.fit(df, duration_col='dur', event_col='obsv', formula="fin + wexp + age * prio")
    cph.print_summary() 
    cph.plot()
    
    cph.plot_partial_effects_on_outcome(covariates='Patch Type', values=[2, 1, 0], cmap='coolwarm')
    
    return None


'''
# =============================================================================
#        model  with patch type as categorial COV
           
        -> the model to go 
       
       trial duration ~ Reward Probability + Last Collection Rate + Patch Type
# =============================================================================
'''


#run_CoxReg(E_all,T_TD,all_cov1,all_cov2,patch_type)

#run_CoxReg(E_all,T_GUT,all_cov1,all_cov2,patch_type)         



#factor to percent: 100*Beta-100

'''
# =============================================================================
#     plot survival function

    P(stay in Patch) as a function of time in sec 
# =============================================================================
'''


# kmf.fit(T_all,E_all, label="Stay in patch")
# ax = plt.subplot(111)
# kmf.plot_survival_function(ax=ax,show_censors=True, censor_styles={'ms': 6, 'marker': 's'})


'''

To access the coefficients and the baseline hazard directly, 
you can use params_ and baseline_hazard_ respectively. 
Taking a look at these coefficients for a moment, prio 
(the number of prior arrests) has a coefficient of about 0.09. 
Thus, a one unit increase in prio means the the baseline hazard 
will increase by a factor of exp(0.09)=1.10 - about a 10% increase. 
Recall, in the Cox proportional hazard model, a higher hazard means more at risk of the event occurring. 
The value exp(0.09) is called the hazard ratio, a name that will be clear with another example.

'''
# cph = CoxPHFitter()
# cph.fit(df, duration_col='duration', event_col='event', show_progress=True)
# cph.baseline_hazard_






# #write json file with metadata for each trial and subj
# import json
# a=1
# print('serialization')

# if a==1:
#     myDictObj = { "Task Name":"Human probabilistic foraging", 
#                  "Trial":{"LongName": "Exploration",
#           "Description": "self-initiated switch to next trial = patch leaving",
#           "Levels": {
#              "Exploration": "trial ended before all targets are collected ",
#              "Exploitation": "trial ended after all targets are collected "
#              } }
#             }

# ##convert object to json
# serialized= json.dumps(myDictObj, sort_keys=True, indent=3)
# print(serialized)
# ## now we are gonna convert json to object
# deserialization=json.loads(serialized)
# print(deserialization)

# with open('_beh.json', 'w', encoding='utf-8') as f:
#     json.dump(myDictObj, f, ensure_ascii=False, indent=4)
