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


#from lifelines import CoxPHFitter
import pandas as pd

#import rm_anova


#sns.set_theme(style="darkgrid")

sns.set_theme(style="white",palette="viridis")



'''
###  directories
'''


datapath=os.getcwd()+'/'

'''
###  info varis
'''

version='random_loc'#'fixed_loc'
number_of_targets=60#40
nBlocks=3
nSubs=range(21,40)

#final sample 
nsubs=[5,8,9,12,13,14,16,17,19,20,21,23,27,28,30,31,33,35,37,38,39,40]
#nsubs=[41,42,43,44,45,46]

'''
###  functions
'''

cox_params={}
cox_params['start']=[]
cox_params['end']=[]
#mk dic to save data on group level
group_dataset={}

key_list=['sub','reward','ITT','trial_dur','patch_leaving','early_break','forced_leaving','exhaustive_search','last_target_RT',
          'nTrials','mean_nTrials_patch_leaving','SD_nTrials_patch_leaving','meanTP_patch_leaving',#target probability when last target was collected 
          'sdTP_patch_leaving',
          'meanTP_forced_leaving','sdTP_forced_leaving','relTP_patch_leaving_low','meanTP_patch_leaving_low',#target probability when last target was collected 
          'sdTP_patch_leaving_low','relTP_patch_leaving_med','meanTP_patch_leaving_med','sdTP_patch_leaving_med','relTP_patch_leaving_high',
          'meanTP_patch_leaving_high','sdTP_patch_leaving_high','total$_patch_leaving','mean$_patch_leaving_low','sd$_patch_leaving_low',
          'mean$_patch_leaving_med','sd$_patch_leaving_med','mean$_patch_leaving_high','sd$_patch_leaving_high','mean_ITT_patch_leaving_low',
          'sd_ITT_patch_leaving_low','mean_ITT_patch_leaving_med','sd_ITT_patch_leaving_med','mean_ITT_patch_leaving_high','sd_ITT_patch_leaving_high',
          'lastITT_patch_leaving_low','2lastITT_patch_leaving_low','3lastITT_patch_leaving_low','lastITT_patch_leaving_med','2lastITT_patch_leaving_med',
          '3lastITT_patch_leaving_med','lastITT_patch_leaving_high',
          '2lastITT_patch_leaving_high',
          '3lastITT_patch_leaving_high',
        'meanCR_patch_leaving_low','sdCR_patch_leaving_low','meanCR_patch_leaving_med','sdCR_patch_leaving_med','meanCR_patch_leaving_high',
        'sdCR_patch_leaving_high','mean_nTrials_patch_leaving_low','sd_nTrials_patch_leaving_low','mean_nTrials_patch_leaving_med','sd_nTrials_patch_leaving_med',
        'mean_nTrials_patch_leaving_high','sd_nTrials_patch_leaving_high','mean_trial_dur_patch_leaving_low','sd_trial_dur_patch_leaving_low',
        'mean_trial_dur_patch_leaving_med','sd_trial_dur_patch_leaving_med','mean_trial_dur_patch_leaving_high','sd_trial_dur_patch_leaving_high',
        'first15_trial_dur_patch_leaving_low','last15_trial_dur_patch_leaving_low','first15_trial_dur_patch_leaving_med','last15_trial_dur_patch_leaving_med','first15_trial_dur_patch_leaving_high',
        'last15_trial_dur_patch_leaving_high','mean$_forced_leaving','sd$_forced_leaving','mean$_patch_leaving','sd$_patch_leaving','meanITT_forced_leaving','sdITT_forced_leaving',
        'meanITT_patch_leaving','sdITT_patch_leaving','meanITT_patch_leaving','sdITT_patch_leaving','meanCR_1half_patch_leaving','meanCR_2half_patch_leaving',
        'sdCR_1half_patch_leaving','sdCR_2half_patch_leaving','meanCR_1half_patch_leaving_low','meanCR_2half_patch_leaving_low',
        'sdCR_1half_patch_leaving_low','sdCR_2half_patch_leaving_low','meanCR_1half_patch_leaving_med','meanCR_2half_patch_leaving_med','sdCR_1half_patch_leaving_med','sdCR_2half_patch_leaving_med',
        'meanCR_1half_patch_leaving_high','meanCR_2half_patch_leaving_high','sdCR_1half_patch_leaving_high','sdCR_2half_patch_leaving_high','lastCR_patch_leaving_low',
        'lastCR_patch_leaving_med','lastCR_patch_leaving_high','GUT_patch_leaving_low','GUT_patch_leaving_med','GUT_patch_leaving_high',
        'lastCR_2_patch_leaving_low','lastCR_3_patch_leaving_low','lastCR_4_patch_leaving_low','lastCR_5_patch_leaving_low',
        'lastCR_2_patch_leaving_med','lastCR_3_patch_leaving_med','lastCR_4_patch_leaving_med','lastCR_5_patch_leaving_med',
        'lastCR_2_patch_leaving_high','lastCR_3_patch_leaving_high','lastCR_4_patch_leaving_high','lastCR_5_patch_leaving_high',
        'lastCR_6_patch_leaving_low','lastCR_7_patch_leaving_low',
        'lastCR_6_patch_leaving_med','lastCR_7_patch_leaving_med',
        'lastCR_6_patch_leaving_high','lastCR_7_patch_leaving_high',
        'list_tri_dur','list_reward','list_gut',
        'travel_time'
        ]


for key in key_list:
   group_dataset['{0}'.format(key)]=[] 
  





'''
write function  that reads out csv file and appends values of interest to a group dictionary 

so data of all subs and runs will be stored in a single dictionary. 

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
        dvXcondition.append(av)
    
    return dvXcondition[0]




def load_file(version,sub,nBlocks,group_dataset,number_of_targets):
    number_of_search_targets=number_of_targets
    sub=sub
    reward=0
    group_dataset['sub'].append(sub)
    
    ITT=[]
    search_dur=[]
    reward=0
    reward2=[]
    trial_type=[]
    search_time=[]
    patchleaving=0
    exhaustivesearch=0
    count_eb=0
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
    fourth_last_low=[]
    fifth_last_low=[]
    sixth_last_low=[]
    seventh_last_low=[]
    
    
    sec_last_med=[]
    third_last_med=[]
    fourth_last_med=[]
    fifth_last_med=[]
    sixth_last_med=[]
    seventh_last_med=[]
    
    sec_last_high=[]
    third_last_high=[]
    fourth_last_high=[]
    fifth_last_high=[]
    sixth_last_high=[]
    seventh_last_high=[]
    
    start=[]
    end=[]
    trial_time=[]
    split_time=[]
    
    last_cr=[]
    start_prob=[]
    
    tp_ex=[]
    tp=[]
    
    itt_low=[]
    itt_med=[]
    itt_high=[]
    
    giving_up_time=[]
    
    mean_travel_time=[]
    search_durs=[]
    n_targets=[]
    n_guts=[]
    
    n_targets_low=[]
    n_targets_med=[]
    n_targets_high=[]
    
    
    #for block in range(nBlocks):
    #intertarget_time=[]
    ICR=[]

    if sub <10:
        df=pd.read_csv(datapath + f'/pilots/random_loc/exp_decay/data/final/final/beh-data-sub00{sub}.csv',sep=",",on_bad_lines='skip')#error_bad_lines=False)#on_bad_lines='skip')#,#,error_bad_lines=False)
                    
                                 # converters={'reward_ons': pd.eval,
                                 # 'responseTime': pd.eval,'search_dur_patch_leaving': pd.eval})
    else:
        df=pd.read_csv(datapath + f'pilots/random_loc/exp_decay/data/final/final/beh-data-sub0{sub}.csv',sep=",",on_bad_lines='skip')#error_bad_lines=False)#on_bad_lines='skip')#,error_bad_lines=False)
    
    # if sub==17:
    #     df = df[:-1]  
    # elif sub==20:
    df = df[:-1]
        
        
    #make strings to list
    
    for ele in range(len(df['reward_ons'])):
        df['reward_ons'][ele]=literal_eval(df['reward_ons'][ele])
        df['detection'][ele]=literal_eval(df['detection'][ele])
        df['reward_prob_next_trial'][ele]=literal_eval(df['reward_prob_next_trial'][ele])
        df['responseTime'][ele]=literal_eval(df['responseTime'][ele])
        
    
        if sub ==22:
             df['search_dur_patch_leaving'][ele]=literal_eval(df['search_dur_patch_leaving'][ele])
        elif sub ==10:
            df['search_dur_patch_leaving'][ele]=literal_eval(df['search_dur_patch_leaving'][ele])
    
    
    #get rid of the last row since the format is messed up
    #df = df[:-1]
    
    reward+=sum(df['reward'])
    nTrials=len(df['fix'])

    group_dataset['nTrials'].append(len(df['fix']))
    #group_dataset['nTrials'].append(nTrials)
   
    
   
    '''
    number of trials is not pre-determined due to the countdown...
    

    '''
    for trial in range(nTrials):
        if trial < nTrials-1:
            travel_time=df['search'][trial+1]-(df['search'][trial]+df['search_dur_patch_leaving'][trial])
            mean_travel_time.append(travel_time)
            sdur=df['search_dur_patch_leaving'][trial]
            print (f'trial{trial} travel time = {travel_time}', {df['trial type'][trial]})
            print (f'trial{trial} search duration = {sdur}', {df['trial type'][trial]})
       
        
        intertarget_time=[]
        
        if df['blank'][trial] <= 300:
            trial_time.append(5)#first 0-5min
            split_time.append(0)
        elif df['blank'][trial] > 300 and df['blank'][trial] <=600:
            trial_time.append(10)#6-10 min
            split_time.append(0)
        elif df['blank'][trial] > 600 and df['blank'][trial] <=900:
            trial_time.append(15)#11-15 min
            split_time.append(0)
        elif df['blank'][trial] > 900 and df['blank'][trial] <=1200:
            trial_time.append(20)#16-20 min
            split_time.append(1)
        elif df['blank'][trial] > 1200 and df['blank'][trial] <=1500:
            trial_time.append(25)#16-20 min
            split_time.append(1)
        elif df['blank'][trial] > 1500: 
            trial_time.append(30)#16-20 min
            split_time.append(1)

         
        
            
        start.append(df['search'][trial])
        end.append(df['end of search'][trial])
        start_prob.append(df['start_prob'][trial])
        #if trial >1:
        euro.append(df['reward'][trial])
        if sub == 20:
            print ('reward',euro[trial])
        if len(df['responseTime'][trial]) >0:
             count_trial+=1
             
        if 'early break' in df['trial type'][trial]:
            trial_type.append(0)
            
        else:
            trial_type.append(1)
            n_targets.append(df['reward'][trial])
            search_durs.append(sdur)
            
        for targ in range(len(df['detection'][trial])):
            #print (f'detection. {targ}')
            
            if targ < len(df['detection'][trial])-1:
                diff=df['detection'][trial][targ+1]-df['detection'][trial][targ]
                intertarget_time.append(diff)
                
            elif targ == len(df['detection'][trial]):
                diff=df['detection'][trial][targ-1]-df['detection'][trial][targ-2]
                intertarget_time.append(diff)
                ICR.append(1/diff)
                
                #print (last_cr)
            #if sub ==20:
                #print ('itt:',diff)
                
                
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
                n_guts.append(df['end of search'][trial]-df['detection'][trial][-1])
                giving_up_time.append(df['end of search'][trial]-df['detection'][trial][-1])
            else:
                giving_up_time.append(np.nan)
                n_guts.append(df['end of search'][trial]-df['search'][trial])
            
            all_det=len(df['responseTime'][trial])
            try:
                detection_last_target=df['responseTime'][trial][all_det-1]
            except IndexError:
                detection_last_target=np.nan
                
            last_targ_det.append(detection_last_target)
            # target_prob_pl=(number_of_search_targets-all_det)/number_of_search_targets
            
            # if sub ==11:
            #     print ('tp',target_prob_pl)
                
            if len (df['reward_prob_next_trial'][trial]) >1:
                tp_pl=df['reward_prob_next_trial'][trial][-2:]
            elif len (df['reward_prob_next_trial'][trial]) >0:
                tp_pl=df['reward_prob_next_trial'][trial][-1:]
            
            tp.append(tp_pl[0])
            
            half=int(math.ceil(len(intertarget_time)/2.0))  
            time_first_half.append(1/np.mean(intertarget_time[0:half]))
            time_second_half.append(1/np.mean(intertarget_time[half:len(intertarget_time)]))
            
            
            quarter=int(math.ceil(len(intertarget_time)/4.0))  
            half=int(math.ceil(len(intertarget_time)/2.0))  
            threequat=quarter+half
            time_first.append(1/np.mean(intertarget_time[0:quarter]))
            time_second.append(1/np.mean(intertarget_time[quarter:half]))#len(intertarget_time)]))
            time_third.append(1/np.mean(intertarget_time[half:threequat]))
            time_fourth.append(1/np.mean(intertarget_time[threequat:len(intertarget_time)]))
    
            
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
            
        
    
        #if len(intertarget_time)>0:
        ITT.append(intertarget_time)
        # else:
        #     ITT.append([np.nan])
            
        quarter=int(math.ceil(len(intertarget_time)/4.0))  
        half=int(math.ceil(len(intertarget_time)/2.0))  
        threequat=quarter+half
        time_first.append(1/np.mean(intertarget_time[0:quarter]))
        time_second.append(1/np.mean(intertarget_time[quarter:half]))#len(intertarget_time)]))
        time_third.append(1/np.mean(intertarget_time[half:threequat]))
        time_fourth.append(1/np.mean(intertarget_time[threequat:len(intertarget_time)]))
        
        if df['start_prob'][trial]==0.5:
            
            if len(intertarget_time)>1:
                
                sec_last_low.append(1/intertarget_time[len(intertarget_time)-2])
                                                 
                if len(intertarget_time)>2:                                
                    
                    third_last_low.append(1/intertarget_time[len(intertarget_time)-3])
                    
                    if len(intertarget_time)>3: 
                        
                         fourth_last_low.append(1/intertarget_time[len(intertarget_time)-4])
                         
                         if len(intertarget_time)>4: 
                             fifth_last_low.append(1/intertarget_time[len(intertarget_time)-5])
                             
                             if len(intertarget_time)>5: 
                        
                                sixth_last_low.append(1/intertarget_time[len(intertarget_time)-6])
                         
                                if len(intertarget_time)>6: 
                                    seventh_last_low.append(1/intertarget_time[len(intertarget_time)-7])
                                    
                                else:seventh_last_low.append(np.nan)
                                
                             else:sixth_last_low.append(np.nan)
                        
                         else:fifth_last_low.append(np.nan)

                    else:fourth_last_low.append(np.nan)
                                                     
                else:third_last_low.append(np.nan)
                
            else:sec_last_low.append(np.nan)
            
        elif df['start_prob'][trial]==0.75:
            
            if len(intertarget_time)>1:
                
                sec_last_med.append(1/intertarget_time[len(intertarget_time)-2])
                                                 
                if len(intertarget_time)>2:                                
                    
                    third_last_med.append(1/intertarget_time[len(intertarget_time)-3])
                    
                    if len(intertarget_time)>3: 
                        
                         fourth_last_med.append(1/intertarget_time[len(intertarget_time)-4])
                         
                         if len(intertarget_time)>4: 
                             fifth_last_med.append(1/intertarget_time[len(intertarget_time)-5])
                             
                             if len(intertarget_time)>5: 
                        
                                sixth_last_med.append(1/intertarget_time[len(intertarget_time)-6])
                         
                                if len(intertarget_time)>6: 
                                    seventh_last_med.append(1/intertarget_time[len(intertarget_time)-7])
                                    
                                else:seventh_last_med.append(np.nan)
                                
                             else:sixth_last_med.append(np.nan)
                        
                         else:fifth_last_med.append(np.nan)

                    else:fourth_last_med.append(np.nan)
              
                                                     
                else:third_last_med.append(np.nan)
                
            else:sec_last_med.append(np.nan)
        
        elif df['start_prob'][trial]==1:
            
            if len(intertarget_time)>1:
                
                sec_last_high.append(1/intertarget_time[len(intertarget_time)-2])
                                                 
                if len(intertarget_time)>2:                                
                    
                    third_last_high.append(1/intertarget_time[len(intertarget_time)-3])
                    
                    if len(intertarget_time)>3: 
                        
                         fourth_last_high.append(1/intertarget_time[len(intertarget_time)-4])
                         
                         if len(intertarget_time)>4: 
                             
                             fifth_last_high.append(1/intertarget_time[len(intertarget_time)-5])
                             
                             if len(intertarget_time)>5: 
                        
                                sixth_last_high.append(1/intertarget_time[len(intertarget_time)-6])
                         
                                if len(intertarget_time)>6: 
                                    seventh_last_high.append(1/intertarget_time[len(intertarget_time)-7])
                                    
                                else:seventh_last_high.append(np.nan)
                                
                             else:sixth_last_high.append(np.nan)
                        
                         else:fifth_last_high.append(np.nan)

                    else:fourth_last_high.append(np.nan)
              
                                                     
                else:third_last_high.append(np.nan)
                
            else:sec_last_high.append(np.nan)
        
              

                               
        
        #group_dataset['trial_dur'].append(search_dur)
  

    print ('###')
    print ('sub %i'%sub)
    
    # print (sec_last)
    # print (third_last)
   
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
    patch_leaving_indis_med=all_indices((0,1,1,0.75),matrix2)  
    patch_leaving_indis_high=all_indices((0,1,1,1.0),matrix2)  

    #get trial indices for 5 min periodes 
    matrix4=list(zip(reward2,search_time,trial_type,start_prob,split_time))
    patch_leaving_indis_low_1half=all_indices((0,1,1,0.5,0),matrix4)  
    patch_leaving_indis_low_2half=all_indices((0,1,1,0.5,1),matrix4)  
    
    patch_leaving_indis_med_1half=all_indices((0,1,1,0.75,0),matrix4)  
    patch_leaving_indis_med_2half=all_indices((0,1,1,0.75,1),matrix4)  
   
    patch_leaving_indis_high_1half=all_indices((0,1,1,1.0,0),matrix4)  
    patch_leaving_indis_high_2half=all_indices((0,1,1,1.0,1),matrix4) 
    
    ITT_patch_leaving=TrialFinder(patch_leaving_indis,ITT)
    ITT_forced_leaving=TrialFinder(forced_leaving_indis,ITT)
    rew_forced_leaving=TrialFinder(forced_leaving_indis,euro)
    rew_patch_leaving=TrialFinder(patch_leaving_indis,euro)
    
    
    '''
            collect values for each prob condi
            
    '''
    rew_patch_leaving_low=TrialFinder(patch_leaving_indis_low,euro)
    rew_patch_leaving_med=TrialFinder(patch_leaving_indis_med,euro)
    rew_patch_leaving_high=TrialFinder(patch_leaving_indis_high,euro)
          
    ITT_patch_leaving_low=TrialFinder(patch_leaving_indis_low,ITT)
    ITT_patch_leaving_med=TrialFinder(patch_leaving_indis_med,ITT)
    ITT_patch_leaving_high=TrialFinder(patch_leaving_indis_high,ITT)
    
    print (ITT_patch_leaving_low)
    tp_patch_leaving_low=TrialFinder(patch_leaving_indis_low,tp)
    tp_patch_leaving_med=TrialFinder(patch_leaving_indis_med,tp)
    tp_patch_leaving_high=TrialFinder(patch_leaving_indis_high,tp)
    
    searchdur_patch_leaving_low=TrialFinder(patch_leaving_indis_low,search_dur)
    if sub==10:
        print (searchdur_patch_leaving_low)
    searchdur_patch_leaving_med=TrialFinder(patch_leaving_indis_med,search_dur)
    searchdur_patch_leaving_high=TrialFinder(patch_leaving_indis_high,search_dur)
    
    last_cr_low=TrialFinder(patch_leaving_indis_low,last_cr)
    last_cr_med=TrialFinder(patch_leaving_indis_med,last_cr)
    last_cr_high=TrialFinder(patch_leaving_indis_high,last_cr)
      
    
    giving_up_time_low=TrialFinder(patch_leaving_indis_low,giving_up_time)
    giving_up_time_med=TrialFinder(patch_leaving_indis_med,giving_up_time)
    giving_up_time_high=TrialFinder(patch_leaving_indis_high,giving_up_time)
    
    #add everything to the dictionary 

    
    try:
        group_dataset['trial_dur'].append(np.nanmedian(search_dur))
    except TypeError:
        group_dataset['trial_dur'].append(pd.isna)
    group_dataset['last_target_RT'].append(last_targ_det)
    group_dataset['patch_leaving'].append(patchleaving)
    group_dataset['early_break'].append(len(early_break_indis))
    group_dataset['reward'].append(reward)
    # ITT=[item for sublist in ITT for item in sublist]
    # group_dataset['ITT'].append(ITT)
    
    group_dataset['travel_time'].append(np.mean(mean_travel_time))
    
    group_dataset['forced_leaving'].append(exhaustivesearch)
    group_dataset['mean_nTrials_patch_leaving'].append(len(patch_leaving_indis))

    
    group_dataset['meanTP_patch_leaving'].append(np.nanmedian(tp))
    group_dataset['sdTP_patch_leaving'].append(np.nanstd(tp))
        
    group_dataset['mean$_patch_leaving'].append(np.nanmedian(rew_patch_leaving))
    group_dataset['total$_patch_leaving'].append(sum(euro))
    group_dataset['sd$_patch_leaving'].append(np.nanstd(rew_patch_leaving))
    ITT_patch_leaving=[item for sublist in ITT_patch_leaving for item in sublist]
    group_dataset['meanITT_patch_leaving'].append(np.nanmedian(ITT_patch_leaving))
    group_dataset['sdITT_patch_leaving'].append(np.nanstd(ITT_patch_leaving))
    
    group_dataset['GUT_patch_leaving_low'].append(np.nanmedian(giving_up_time_low))
    group_dataset['GUT_patch_leaving_med'].append(np.nanmedian(giving_up_time_med))
    group_dataset['GUT_patch_leaving_high'].append(np.nanmedian(giving_up_time_high))
    
    '''
            save for each prob condi
            
    '''
    
    
    group_dataset['lastCR_patch_leaving_low'].append(1/np.nanmean(last_cr_low))
    group_dataset['lastCR_patch_leaving_med'].append(1/np.nanmean(last_cr_med))
    group_dataset['lastCR_patch_leaving_high'].append(1/np.nanmean(last_cr_high))
    
    
    group_dataset['lastITT_patch_leaving_low'].append(np.nanmedian(last_cr_low))
    group_dataset['lastITT_patch_leaving_med'].append(np.nanmedian(last_cr_med))
    group_dataset['lastITT_patch_leaving_high'].append(np.nanmedian(last_cr_high))
    

    group_dataset['mean_nTrials_patch_leaving_low'].append(len(patch_leaving_indis_low))
    group_dataset['mean_trial_dur_patch_leaving_low'].append(np.nanmedian(searchdur_patch_leaving_low))
    
    
    '''
    get trial durations for 5min chunks - is there some kind of learning to leave earlier ?
    '''
    
      
    group_dataset['first15_trial_dur_patch_leaving_low'].append(np.nanmean(TrialFinder(patch_leaving_indis_low_1half,search_dur)))
    group_dataset['last15_trial_dur_patch_leaving_low'].append(np.nanmean(TrialFinder(patch_leaving_indis_low_2half,search_dur)))

    group_dataset['first15_trial_dur_patch_leaving_med'].append(np.nanmean(TrialFinder(patch_leaving_indis_med_1half,search_dur)))
    group_dataset['last15_trial_dur_patch_leaving_med'].append(np.nanmean(TrialFinder(patch_leaving_indis_med_2half,search_dur)))

    group_dataset['first15_trial_dur_patch_leaving_high'].append(np.nanmean(TrialFinder(patch_leaving_indis_high_1half,search_dur)))
    group_dataset['last15_trial_dur_patch_leaving_high'].append(np.nanmean(TrialFinder(patch_leaving_indis_high_2half,search_dur)))


    
    
    
    group_dataset['sd_trial_dur_patch_leaving_low'].append(np.nanstd(searchdur_patch_leaving_low))
    
    group_dataset['mean$_patch_leaving_low'].append(np.nanmedian(rew_patch_leaving_low))
    group_dataset['sd$_patch_leaving_low'].append(np.nanstd(rew_patch_leaving_low))
    ITT_patch_leaving_low = [x for x in ITT_patch_leaving_low if len(x) > 0]
    ITT_patch_leaving_low=[item for sublist in ITT_patch_leaving_low for item in sublist]
    
    group_dataset['mean_ITT_patch_leaving_low'].append(np.nanmedian(ITT_patch_leaving_low))
    group_dataset['sd_ITT_patch_leaving_low'].append(np.nanstd(ITT_patch_leaving_low))#
    
    group_dataset['relTP_patch_leaving_low'].append(np.nanmedian(tp_patch_leaving_low)/0.5)
    group_dataset['meanTP_patch_leaving_low'].append(np.nanmedian(tp_patch_leaving_low))
    group_dataset['sdTP_patch_leaving_low'].append(np.nanstd(tp_patch_leaving_low))
    
    group_dataset['meanCR_patch_leaving_low'].append(1/np.nanmean(ITT_patch_leaving_low))
    group_dataset['sdCR_patch_leaving_low'].append(1/np.nanstd(ITT_patch_leaving_low))
    
    
    
    group_dataset['mean_nTrials_patch_leaving_med'].append(len(patch_leaving_indis_med))
    
    group_dataset['mean_trial_dur_patch_leaving_med'].append(np.nanmedian(searchdur_patch_leaving_med))
    group_dataset['sd_trial_dur_patch_leaving_med'].append(np.nanstd(searchdur_patch_leaving_med))
    
    group_dataset['mean$_patch_leaving_med'].append(np.nanmedian(rew_patch_leaving_med))
    group_dataset['sd$_patch_leaving_med'].append(np.nanstd(rew_patch_leaving_med))
    
    ITT_patch_leaving_med = [x for x in ITT_patch_leaving_med if len(x) > 0]
    ITT_patch_leaving_med=[item for sublist in ITT_patch_leaving_med for item in sublist]
    group_dataset['mean_ITT_patch_leaving_med'].append(np.nanmedian(ITT_patch_leaving_med))
    group_dataset['sd_ITT_patch_leaving_med'].append(np.nanstd(ITT_patch_leaving_med))
    
    group_dataset['relTP_patch_leaving_med'].append(np.nanmedian(tp_patch_leaving_med)/0.75)
    group_dataset['meanTP_patch_leaving_med'].append(np.nanmedian(tp_patch_leaving_med))
    group_dataset['sdTP_patch_leaving_med'].append(np.nanstd(tp_patch_leaving_med))
    
    group_dataset['meanCR_patch_leaving_med'].append(1/np.nanmean(ITT_patch_leaving_med))
    group_dataset['sdCR_patch_leaving_med'].append(1/np.nanstd(ITT_patch_leaving_med))
    
    
    group_dataset['mean_nTrials_patch_leaving_high'].append(len(patch_leaving_indis_high))
    
    group_dataset['mean_trial_dur_patch_leaving_high'].append(np.nanmedian(searchdur_patch_leaving_high))
    group_dataset['sd_trial_dur_patch_leaving_high'].append(np.nanstd(searchdur_patch_leaving_high))
 
    group_dataset['mean$_patch_leaving_high'].append(np.nanmedian(rew_patch_leaving_high))
    group_dataset['sd$_patch_leaving_high'].append(np.nanstd(rew_patch_leaving_high))
    
    ITT_patch_leaving_high = [x for x in ITT_patch_leaving_high if len(x) > 0]
    ITT_patch_leaving_high=[item for sublist in ITT_patch_leaving_high for item in sublist]
    group_dataset['mean_ITT_patch_leaving_high'].append(np.nanmedian(ITT_patch_leaving_high))
    group_dataset['sd_ITT_patch_leaving_high'].append(np.nanstd(ITT_patch_leaving_high))
    
    group_dataset['relTP_patch_leaving_high'].append(np.nanmedian(tp_patch_leaving_high)/1.0)
    group_dataset['meanTP_patch_leaving_high'].append(np.nanmedian(tp_patch_leaving_high))
    group_dataset['sdTP_patch_leaving_high'].append(np.nanstd(tp_patch_leaving_high))
    
    group_dataset['meanCR_patch_leaving_high'].append(1/np.mean(ITT_patch_leaving_high))
    group_dataset['sdCR_patch_leaving_high'].append(1/np.nanstd(ITT_patch_leaving_high))
    

    group_dataset['mean$_forced_leaving'].append(np.nanmedian(rew_forced_leaving))
    group_dataset['sd$_forced_leaving'].append(np.nanstd(rew_forced_leaving))


    group_dataset['meanITT_forced_leaving'].append(np.nanmedian(ITT_forced_leaving))
    group_dataset['sdITT_forced_leaving'].append(np.nanstd(ITT_forced_leaving))

       
    
    group_dataset['lastCR_2_patch_leaving_low'].append(np.nanmean(sec_last_low))
    group_dataset['lastCR_3_patch_leaving_low'].append(np.nanmean(third_last_low))
    group_dataset['lastCR_4_patch_leaving_low'].append(np.nanmean(fourth_last_low))
    group_dataset['lastCR_5_patch_leaving_low'].append(np.nanmean(fifth_last_low))
    group_dataset['lastCR_6_patch_leaving_low'].append(np.nanmean(sixth_last_low))
    group_dataset['lastCR_7_patch_leaving_low'].append(np.nanmean(seventh_last_low))
    
    group_dataset['lastCR_2_patch_leaving_med'].append(np.nanmean(sec_last_med))
    group_dataset['lastCR_3_patch_leaving_med'].append(np.nanmean(third_last_med))
    group_dataset['lastCR_4_patch_leaving_med'].append(np.nanmean(fourth_last_med))
    group_dataset['lastCR_5_patch_leaving_med'].append(np.nanmean(fifth_last_med))
    group_dataset['lastCR_6_patch_leaving_med'].append(np.nanmean(sixth_last_med))
    group_dataset['lastCR_7_patch_leaving_med'].append(np.nanmean(seventh_last_med))
    
    
    group_dataset['lastCR_2_patch_leaving_high'].append(np.nanmean(sec_last_high))
    group_dataset['lastCR_3_patch_leaving_high'].append(np.nanmean(third_last_high))
    group_dataset['lastCR_4_patch_leaving_high'].append(np.nanmean(fourth_last_high))
    group_dataset['lastCR_5_patch_leaving_high'].append(np.nanmean(fifth_last_high))
    group_dataset['lastCR_6_patch_leaving_high'].append(np.nanmean(sixth_last_high))
    group_dataset['lastCR_7_patch_leaving_high'].append(np.nanmean(seventh_last_high))
    
    group_dataset['list_tri_dur'].append(search_durs)
    group_dataset['list_reward'].append(n_targets)
    group_dataset['list_gut'].append(n_guts)

    return group_dataset


'''run analysis'''


#patch_leaving_indis=all_indices((1,1,1),matrix)
#for sub in range(1,14):
for sub in  nsubs:
    load_file(version,sub,nBlocks,group_dataset,number_of_targets)
    


# '''
# check keys, save file if needed
# '''
# # #group_dataset.keys()
# DataSet=pd.DataFrame(group_dataset)
# DataSet.to_csv(datapath+'beh_data_allsubs_young.csv', index=False, header=True)

# '''
# write to tsv

# '''
# tsv_file= datapath + f"/beh-data-all_subs.csv"

# if not os.path.isfile(tsv_file):
#     data.to_csv(datapath +f"fmri/beh-data-all_subs.csv",
#                 sep=',',index=False,header=True)
# else:
#       with open(tsv_file,'a') as f:
#           data.to_csv(f, header=False,index=False)
 



'''
# =============================================================================
#   OUTLIERS?
# =============================================================================
'''
# d={'sub':nsubs,'n_trial':group_dataset['mean_nTrials_patch_leaving']}
# df=pd.DataFrame(data=d)

# def remove_outliers(df, q=0.01):
#     #remove sub
#     filt_df=df.loc[:,df.columns !='sub']
    
#     #get quantiles
#     low = q
#     high = 1-q
#     quant_df = filt_df.quantile([low, high])
    
#     #filter
#     filt_df = filt_df.apply(lambda x: x[(x>quant_df.loc[low,x.name]) & 
#                                     (x < quant_df.loc[high,x.name])], axis=0)
#     #bring back sub id                            
#     filt_df = pd.concat([df.loc[:,'sub'], filt_df], axis=1)
#     #drop nan
#     #filt_df.dropna(inplace=True)
#     print ('filtered data')
#     print(filt_df['n_trial'].describe())
#     return filt_df

# filt_df=remove_outliers(df, q=0.01)



# #outlier_reward=TrialFinder([5,16],group_dataset['total$_patch_leaving'])
# filt_df['old_n_trial']=group_dataset['mean_nTrials_patch_leaving']
# filt_df['n_trial_high']=group_dataset['mean_nTrials_patch_leaving_high']
# filt_df['n_trial_med']=group_dataset['mean_nTrials_patch_leaving_med']
# filt_df['n_trial_low']=group_dataset['mean_nTrials_patch_leaving_low']

# 'inspect'
# filt_df



'''
    plotting with seaborn
    
'''
# def plotting(l1,label_y,plot_name,subs):
    
#     l2=[[0.5]*len(subs),[0.75]*len(subs),[1]*len(subs)]
#     l1=[item for sublist in l1 for item in sublist]
#     l2=[item for sublist in l2 for item in sublist]
    
#     plotted = sns.boxplot(x=l2, y=l1)
#     plotted.set(xlabel='Start Reward Probability', ylabel=label_y)
#     #https://stackoverflow.com/questions/36578458/how-does-one-insert-statistical-annotations-stars-or-p-values-into-matplotlib
#     # x1, x2 = 0, 1   # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
#     # y, h, col = max(l1) + 0.02, 0.02, 'k'
#     # plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c=col)
#     # plt.text((x1+x2)*.5, y+h, "**", ha='center', va='bottom', color=col)
#     # x1, x2 = 1, 2   # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
#     # y, h, col = max(l1) + 0.04, 0.04, 'k'
#     # plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c=col)
#     # plt.text((x1+x2)*.5, y+h, "**", ha='center', va='bottom', color=col)
#     # x1, x2 = 0, 2   # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
#     # y, h, col = max(l1) + 0.06,0.06, 'k'
#     # plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c=col)
#     # plt.text((x1+x2)*.5, y+h, "**", ha='center', va='bottom', color=col)
    
#     # y1=0.5*np.mean(group_dataset['meanTP_patch_leaving_low'])
#     # x1=round(30-np.mean(group_dataset['meanTP_patch_leaving_low'])*30)
#     # y2=0.75*np.mean(group_dataset['meanTP_patch_leaving_med'])
#     # x2=round(45-np.mean(group_dataset['meanTP_patch_leaving_med'])*45)
#     # y3=0.75*np.mean(group_dataset['meanTP_patch_leaving_high'])
#     # x3=round(60-np.mean(group_dataset['meanTP_patch_leaving_high'])*60)
#     # plt.scatter(0, y1, marker='o', s=200)
#     # plt.scatter(1, y2, marker='o', s=200)
#     # plt.scatter(2, y3, marker='o', s=200)

    
    
#     sns_plot = plotted.get_figure()
#     #sns_plot.savefig(datapath +f'random_loc/exp_decay/data/final/final/{plot_name}.svg')
#     plt.close()
#     return None

 
# ''' 
#         1.number of trials
# '''
# lst=[group_dataset['mean_nTrials_patch_leaving_low'],
#      group_dataset['mean_nTrials_patch_leaving_med'],
#      group_dataset['mean_nTrials_patch_leaving_high']]

# plotting(lst,'Number of Trials','Ntrials',nsubs)  


''' 
        2. Trial duration
'''
lst=[group_dataset['mean_trial_dur_patch_leaving_low'],
      group_dataset['mean_trial_dur_patch_leaving_med'],
      group_dataset['mean_trial_dur_patch_leaving_high']]

#plotting(lst,'Trial Duration in sec','TrialDur',nsubs)  


# ''' 
#         3. $$$ Reward
# '''
lst=[group_dataset['mean$_patch_leaving_low'],
      group_dataset['mean$_patch_leaving_med'],
      group_dataset['mean$_patch_leaving_high']]

# plotting(lst,'Mean Earnings in Cents per Patch','Reward',nsubs)  

''' 
        4. Target Probability
'''
lst=[group_dataset['meanTP_patch_leaving_low'],
      group_dataset['meanTP_patch_leaving_med'],
      group_dataset['meanTP_patch_leaving_high']]

#plotting(lst,'P reward at leaving','TP',nsubs) 


# ''' 
#         5. ITT
# '''
# lst=[group_dataset['mean_ITT_patch_leaving_low'],
#       group_dataset['mean_ITT_patch_leaving_med'],
#       group_dataset['mean_ITT_patch_leaving_high']]

# plotting(lst,'Mean Intertarget Time in sec','ITT',nsubs) 


''' 
# =============================================================================
#         6. Collection Rate - does CR drop according to marginal value theory below average CR before patch leaving?
# =============================================================================
'''




# #wide format
# hal1 = group_dataset['meanCR_patch_leaving_low']+group_dataset['meanCR_patch_leaving_med']+group_dataset['meanCR_patch_leaving_high']
# hal1=[float(i) for i in hal1 ]
# hal2 =group_dataset['lastCR_patch_leaving_low']+group_dataset['lastCR_patch_leaving_med']+group_dataset['lastCR_patch_leaving_high']
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

p1=[]
p075=[]
p05=[]
all_p=[p1,p075,p05]
ps=[1,0.75,0.5]
for count, prob in enumerate(ps, 0):
    print(count, prob)
    for r in range(1,14):
        star_prob=prob
        potenz=(-(r-1)/5)
        decay_func=star_prob*e**potenz
        all_p[count].append(decay_func)
        
        
df = pd.DataFrame(np.c_[all_p[0], all_p[1],all_p[2]]) # modified @Elliots dataframe production
ax = sns.lineplot(data=df, dashes=[(2, 2), (2, 2),(2, 2)])
plt.legend(labels=["1","0.75","0.5"])
ax.set(xlabel='Number of obtained rewards', ylabel='Reward Probability')
sns_plot = ax.get_figure()
# y1=0.5*np.mean(group_dataset['meanTP_patch_leaving_low'])
# x1=round(30-np.mean(group_dataset['meanTP_patch_leaving_low'])*30)
# y2=0.75*np.mean(group_dataset['meanTP_patch_leaving_med'])
# x2=round(45-np.mean(group_dataset['meanTP_patch_leaving_med'])*45)
# y3=0.75*np.mean(group_dataset['meanTP_patch_leaving_high'])
# x3=round(60-np.mean(group_dataset['meanTP_patch_leaving_high'])*60)
# plt.scatter(x3, y3, marker='o', s=200)
# plt.scatter(x2, y2, marker='o', s=200)
# plt.scatter(x1, y1, marker='o', s=200)
#sns_plot.savefig(datapath +f'random_loc/exp_decay/data/final/final/Prob-decay.svg')





'''
# =============================================================================
# t-tests trial dur = low < med and high p <.001
# =============================================================================

'''



# rm_anova.single_rm_anova('Mean Trial Duration',[group_dataset['mean_trial_dur_patch_leaving_low'],
#                 group_dataset['mean_trial_dur_patch_leaving_med'],
#                 group_dataset['mean_trial_dur_patch_leaving_high']],len(nsubs))   


# '''
#       target probability

# '''
# rm_anova.single_rm_anova('Target Probability',[group_dataset['meanTP_patch_leaving_low'], 
#                group_dataset['meanTP_patch_leaving_med'],
#                group_dataset['meanTP_patch_leaving_high']],len(nsubs))



# rm_anova.single_rm_anova('Target Probability',[group_dataset['relTP_patch_leaving_low'], 
#                group_dataset['relTP_patch_leaving_med'],
#                group_dataset['relTP_patch_leaving_high']],len(nsubs))

# '''
#         reward

# '''

# rm_anova.single_rm_anova('Mean Reward',[group_dataset['mean$_patch_leaving_low'], 
#                                 group_dataset['mean$_patch_leaving_med'],
#                                 group_dataset['mean$_patch_leaving_high']],len(nsubs))


# '''
#         ITT

# '''

# rm_anova.single_rm_anova('ITT',[group_dataset['mean_ITT_patch_leaving_low'], 
#                                 group_dataset['mean_ITT_patch_leaving_med'],
#                                 group_dataset['mean_ITT_patch_leaving_high']],len(nsubs))




# '''
#         Giving Up Time

# '''

# rm_anova.single_rm_anova('Giving Up Time',[group_dataset['GUT_patch_leaving_low'], 
#                                 group_dataset['GUT_patch_leaving_med'],
#                                 group_dataset['GUT_patch_leaving_high']],len(nsubs))




