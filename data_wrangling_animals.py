#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 16 11:27:03 2022

@author: lasseguldener
"""

from __future__ import division
import os
import csv
import numpy as np
import pandas as pd
import math
import glob
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
import natsort

sns.set_theme(style="darkgrid",palette="pastel")

'''
# =============================================================================
# LOAD DATA 
# =============================================================================
'''
wdir=os.getcwd()

'''
# List of parameters of interest

'''
key_list=['nTrial_100%','nTrial_75%','nTrial_50%',
          'mean_nPokes_100%','mean_nPokes_75%','mean_nPokes_50%',
              'mean_reward_100%','mean_reward_75%','mean_reward_50%',
              'mean_trial_dur_100%','mean_trial_dur_75%','mean_trial_dur_50%',
              'mean_rew_Prob_last_poke_100%','mean_rew_Prob_last_poke_75%','mean_rew_Prob_last_poke_50%',
              'mean_CR_last_reward_50%','mean_CR_last_reward_75%','mean_CR_last_reward_100%',
              'mean_GUT_100%','mean_GUT_75%','mean_GUT_50%','session_dur','mean_reward',
              'rel_rew_Prob_last_poke_50%','rel_rew_Prob_last_poke_75%','rel_rew_Prob_last_poke_100%',
              'mean_CR_50%','mean_CR_75%','mean_CR_100%','ITT_last_reward_50%','ITT_last_reward_75%',
              'ITT_last_reward_100%',
              'total$_patch_leaving',
              
              'CR_last_reward_2_50%','CR_last_reward_2_75%','CR_last_reward_2_100%',
              'CR_last_reward_3_50%','CR_last_reward_3_75%','CR_last_reward_3_100%',
              ]



N_days=17
N_animals=8


#function to load animal's data csv file
def load_file(file_name):
    
    data_dict={}
    data_dict['t1']=[]
    data_dict['t2']=[]
    data_dict['dt']=[]
    data_dict['code_side']=[]
    data_dict['code_perf']=[]
    data_dict['c_trial']=[]#trail count
    data_dict['trial_type']=[]#start Prob
    data_dict['c_poke_all']=[]
    data_dict['c_poke_hit']=[]
    data_dict['p']=[]
    data_dict['code_disp']=[]#reward given by dispenser
    
    # opening the CSV file
    with open(file_name, mode ='r')as file:
   
        # reading the CSV file
        csvFile = csv.reader(file)
 
        # displaying the contents of the CSV file
        for counter,lines in enumerate(csvFile):
            if counter > 9:
                data_dict['t1'].append(lines[0]) 
                data_dict['t2'].append(lines[1]) 
                data_dict['dt'].append(lines[2]) 
                data_dict['code_side'].append(lines[3]) 
                data_dict['code_perf'].append(lines[4]) 
                data_dict['c_trial'].append(lines[5]) 
                data_dict['trial_type'].append(lines[6]) 
                data_dict['c_poke_all'].append(lines[7]) 
                data_dict['c_poke_hit'].append(lines[8]) 
                data_dict['p'].append(lines[9]) 
                data_dict['code_disp'].append(lines[10]) 
            #print(lines)
    
    df=pd.DataFrame(data_dict)
    #turn strings into num
    for key in df:
        df[key]=pd.to_numeric(df[key])
    

    return df



'''
# =============================================================================
# find rows of different conditions using index function
# =============================================================================
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



 #this function selects the values of a DV using indices found by all indices   
def TrialFinder(ind,dv): #ind = indices (list), dic=dic with condis for odd and even , dv = dependent variable
    dvXcondition=[]
    

    if len(ind)>0:
        av=np.zeros(shape=(len(ind)))
        av=av.tolist()        

        for i in range(len(ind)):
            av[i] = dv[ind[i]]
        
        dvXcondition=av
    
    else:
        av=np.nan
        dvXcondition=av
    
    return dvXcondition


def itanum(x):
    return format(x,',d').replace(",",".")

'''
# =============================================================================
# calculate means for parameterss of interest for each start probability - this is the interesting part
# =============================================================================
'''

def aggregate_trials(animal_df,key_list):
    
    agg_data={}
    
    for key in key_list:
        average['{0}'.format(key)]=[] 
    
    #get the number of trials
    n_trials=[1]
    count=1

    
    #make a list with 0 and 1; 1 if row is trial's last row
    last_row_of_trial=[0]*len(animal_df['c_trial'])
    first_row_of_trial=[0]*len(animal_df['c_trial'])
    
    first_row_of_hit_trial=[0]*len(animal_df['c_trial'])
    
    for line in range(len(animal_df['c_trial'])):
        
        if line >0: 
            
            #if new trial
            if animal_df['c_trial'][line] != animal_df['c_trial'][line-1]:
                count+=1
                n_trials.append(count)
                
                last_row_of_trial[line-1]=1
                first_row_of_trial[line]=1

                
            else:
                last_row_of_trial[line-1]=0
                first_row_of_trial[line]=0
                
    
    #last element in last_row list is last row of last trial thus needs to be 1 as well
    first_row_of_trial[0]=1
    last_row_of_trial[-1]=1
    
    #sanity check
    if sum(last_row_of_trial) != len(n_trials):
        print ('last row count is off! Please check ...')        


    
   
    '''
    #count n trials for each prob
    
    '''
    #find all the rows that belong to the same trial 
    #find trials for each start prob (i.e., trial type)
    
    index_list_trial={}
    matrix=list(zip(animal_df['c_trial'],animal_df['trial_type']))
    matrix0=list(zip(animal_df['c_trial'],animal_df['code_disp'],animal_df['trial_type']))
    
    
    n_trial_100=0
    n_trial_75=0
    n_trial_50=0
    agg_data['session_dur']=animal_df['t2'][-1:]-animal_df['t1'][0]
    
   
    for trial in n_trials: 
        index_list_trial[f'trial-{trial}-100%']=all_indices((trial,0),matrix)
        index_list_trial[f'hit-trial-{trial}-100%']=all_indices((trial,1,0),matrix0)
        if len(index_list_trial[f'trial-{trial}-100%']) >0:
             n_trial_100+=1
        index_list_trial[f'trial-{trial}-75%']=all_indices((trial,1),matrix) 
        index_list_trial[f'hit-trial-{trial}-75%']=all_indices((trial,1,1),matrix0)
        if len(index_list_trial[f'trial-{trial}-75%']) >0:
             n_trial_75+=1
        index_list_trial[f'trial-{trial}-50%']=all_indices((trial,2),matrix)
        index_list_trial[f'hit-trial-{trial}-50%']=all_indices((trial,1,2),matrix0)
        if len(index_list_trial[f'trial-{trial}-50%']) >0:
             n_trial_50+=1
        
            
    agg_data['nTrial_100%']=n_trial_100
    agg_data['nTrial_75%']=n_trial_75
    agg_data['nTrial_50%']=n_trial_50
    
    '''
    #all pokes
    
    '''
    matrix=list(zip(last_row_of_trial,animal_df['trial_type']))
    matrix2=list(zip(first_row_of_trial,animal_df['trial_type']))

    last_row_100=all_indices((1,0),matrix) 
    last_row_75=all_indices((1,1),matrix) 
    last_row_50=all_indices((1,2),matrix) 
    
    first_row_100=all_indices((1,0),matrix2) 
    first_row_75=all_indices((1,1),matrix2) 
    first_row_50=all_indices((1,2),matrix2) 
    
    c_all_pokes_100=TrialFinder(last_row_100,animal_df['c_poke_all'])
    c_all_pokes_75=TrialFinder(last_row_75,animal_df['c_poke_all'])
    c_all_pokes_50=TrialFinder(last_row_50,animal_df['c_poke_all'])
    

    
    '''
    #mean all pokes 
    
    '''
    agg_data['mean_nPokes_100%']= sum(c_all_pokes_100)/len(c_all_pokes_100)
    agg_data['mean_nPokes_75%']= sum(c_all_pokes_75)/len(c_all_pokes_75)
    agg_data['mean_nPokes_50%']= sum(c_all_pokes_50)/len(c_all_pokes_50)
    
    '''
    #pokes success = reward 
    
    '''
    matrix=list(zip(animal_df['c_trial'],animal_df['code_disp']))
    
    reward_100=[]
    reward_75=[]
    reward_50=[]
    
    agg_data['mean_reward']=sum(animal_df['code_disp'])
    
    for trial in n_trials:
        a=TrialFinder(index_list_trial[f'trial-{trial}-100%'],animal_df['code_disp'])
        if type(a) ==list:#
            #print (f'reward100_trial{trial}',a)
            reward_100.append(a)
        b= TrialFinder(index_list_trial[f'trial-{trial}-75%'],animal_df['code_disp'])
        if type(b) ==list:
            reward_75.append(b)
        c=TrialFinder(index_list_trial[f'trial-{trial}-50%'],animal_df['code_disp'])
        if type(c) == list:
            reward_50.append(c)
    
    #sanity check
    if agg_data['nTrial_100%'] != len(reward_100):
        print ('reward count is off !')
    
    
    reward_100=[item for sublist in reward_100 for item in sublist]
    reward_75=[item for sublist in reward_75 for item in sublist]
    reward_50=[item for sublist in reward_50 for item in sublist]
    
    
    # #claculate mean reward per trial: sum of code_disp / number of trials 
    agg_data['mean_reward_100%']= sum(reward_100)/agg_data['nTrial_100%'] 
    agg_data['mean_reward_75%']= sum(reward_75)/agg_data['nTrial_75%'] 
    agg_data['mean_reward_50%']= sum(reward_50)/agg_data['nTrial_50%'] 
    agg_data['total$_patch_leaving']=sum(reward_100)+sum(reward_75)+sum(reward_50)

    

    '''
    #trial duration
    
    #take the first stamp of trial n and first stamp of trial n+1
    
    
    i.e., last row t2  -  first row t1 
    
    
    '''

    #get time stamp of t1 first row in trial n for each prob condi
    
    first_t1_100=TrialFinder(first_row_100,animal_df['t1'])
    first_t1_75=TrialFinder(first_row_75,animal_df['t1'])
    first_t1_50=TrialFinder(first_row_50,animal_df['t1'])
    
    #get time stamp of t2 last row in trial n for each prob condi
    
    last_t2_100=TrialFinder(last_row_100,animal_df['t2'])
    last_t2_75=TrialFinder(last_row_75,animal_df['t2'])
    last_t2_50=TrialFinder(last_row_50,animal_df['t2'])
    
    #list substraction 
    zip_100=list(zip(last_t2_100,first_t1_100))       
    trial_dur_100=[]
    for t2, t1 in zip_100:
        trial_dur_100.append(t2-t1)
    
    zip_75=list(zip(last_t2_75,first_t1_75))       
    trial_dur_75=[]
    for t2, t1 in zip_75:
        trial_dur_75.append(t2-t1)
        
    zip_50=list(zip(last_t2_50,first_t1_50))       
    trial_dur_50=[]
    for t2, t1 in zip_50:
        trial_dur_50.append(t2-t1)
    

    #sanity check
    if len(trial_dur_100) != agg_data['nTrial_100%']:
         print ('sth is up with the trial durations ...')
    

    agg_data['mean_trial_dur_100%']=np.nanmedian(trial_dur_100)*0.001
    agg_data['mean_trial_dur_75%']=np.nanmedian(trial_dur_75)*0.001
    agg_data['mean_trial_dur_50%']=np.nanmedian(trial_dur_50)*0.001
 
    
    
    '''
    #probability last reward  - take minimal value of trial after removing -1 and 0.0
    
    '''
    last_row_prob_100=[]
    
    for trial in n_trials:
        trial_n=TrialFinder(index_list_trial[f'hit-trial-{trial}-100%'],animal_df['p'])

        if type(trial_n) == list and len(trial_n)>0:
            trial_n=[ele for ele in trial_n if ele > 0]#removes invalid trials i.e., -1.0
            mini=min(trial_n)
            last_row_prob_100.append(mini)
        else:
            last_row_prob_100.append((trial_n))#
            
            
    last_row_prob_75=[]
    
    for trial in n_trials:
        trial_n=TrialFinder(index_list_trial[f'hit-trial-{trial}-75%'],animal_df['p'])
        if type(trial_n) == list and len(trial_n)>0:
            trial_n=[ele for ele in trial_n if ele > 0]
            mini=min(trial_n)
            last_row_prob_75.append(mini)
        else:
            last_row_prob_75.append((trial_n))#v
    
    
    last_row_prob_50=[]
    
    for trial in n_trials:
    
        trial_n=TrialFinder(index_list_trial[f'hit-trial-{trial}-50%'],animal_df['p'])
        if type(trial_n) == list and len(trial_n)>0:
            trial_n=[ele for ele in trial_n if ele > 0]
            mini=min(trial_n)
            last_row_prob_50.append(mini)
        else:
            last_row_prob_50.append((trial_n))#

    
    agg_data['mean_rew_Prob_last_poke_100%']=np.nanmedian(last_row_prob_100)
    agg_data['mean_rew_Prob_last_poke_75%']=np.nanmedian(last_row_prob_75)
    agg_data['mean_rew_Prob_last_poke_50%']=np.nanmedian(last_row_prob_50)

    agg_data['rel_rew_Prob_last_poke_100%']=np.nanmedian(last_row_prob_100)/1
    agg_data['rel_rew_Prob_last_poke_75%']=np.nanmedian(last_row_prob_75)/0.75
    agg_data['rel_rew_Prob_last_poke_50%']=np.nanmedian(last_row_prob_50)/0.5
   
    
    '''
    
    Intertarget times / Collection Rate at patch leaving
    
    '''
    
    last_hit_50=[]
    one_before_last_hit_50=[]
    two_before_last_hit_50=[]
    three_before_last_hit_50=[]
    all_ons_50=[]
    
    last_hit_75=[]
    one_before_last_hit_75=[]
    two_before_last_hit_75=[]
    three_before_last_hit_75=[]
    all_ons_75=[]
    
    last_hit_100=[]
    one_before_last_hit_100=[]
    two_before_last_hit_100=[]
    three_before_last_hit_100=[]
    all_ons_100=[]
    
    two_before_inter_target_times_100  = []
    two_before_inter_target_times_75  = []
    two_before_inter_target_times_50  = []
    
    three_before_inter_target_times_100  = []
    three_before_inter_target_times_75  = []
    three_before_inter_target_times_50  = []
    
    for trial in n_trials:
        
        a=TrialFinder(index_list_trial[f'hit-trial-{trial}-100%'],animal_df['t1'])
        #print (a)
        if type(a) ==list:
            #a.sort()
            if len(a) >1:
                all_ons_100.append(a)
                b=a[-2:]
                last_hit_100.append(max(b))
                one_before_last_hit_100.append(b[0])
                if len(a) >2:
                    two_before_inter_target_times_100.append((a[-2]-a[-3])*0.001)
                    if len(a)>3:
                        three_before_inter_target_times_100.append((a[-3]-a[-4])*0.001)
                 

        
        a=TrialFinder(index_list_trial[f'hit-trial-{trial}-75%'],animal_df['t1'])

        if type(a) ==list:
            #a.sort()
            if len(a) >1:
                all_ons_75.append(a)
                b=a[-2:]
                last_hit_75.append(max(b))
                one_before_last_hit_75.append(b[0]) 
                if len(a) >2:
                    two_before_inter_target_times_75.append((a[-2]-a[-3])*0.001)
                    if len(a)>3:
                        three_before_inter_target_times_75.append((a[-3]-a[-4])*0.001)

                 
        
        a=TrialFinder(index_list_trial[f'hit-trial-{trial}-50%'],animal_df['t1'])

        if type(a) ==list:
            #a.sort()
            if len(a) >1:
                all_ons_50.append(a)
                b=a[-2:]
                last_hit_50.append(max(b))
                one_before_last_hit_50.append(b[0])
                if len(a) >2:
                    two_before_inter_target_times_50.append((a[-2]-a[-3])*0.001)
                    if len(a)>3:
                        three_before_inter_target_times_50.append((a[-3]-a[-4])*0.001)

                 
    #print (len(two_before_last_hit_50))
                
    '''
    #average, last CR 100%, 2 before, 3 before
    '''
    all_ons_100=[item for sublist in all_ons_100 for item in sublist]
    itt_100=[]
    for ele in range(len(all_ons_100)):
        if ele >0:
            itt_100.append((all_ons_100[ele]-all_ons_100[ele-1])*0.001)
            
        
    mean_cr100=list(map(lambda x: 1.0/x,itt_100))
    
    zip_cr100=list(zip(last_hit_100,one_before_last_hit_100))
    last_inter_target_times_100  = []
    
    for lh, obl in zip_cr100:
        last_inter_target_times_100.append((lh-obl)*0.001)

    cr_100=list(map(lambda x: 1.0/x, last_inter_target_times_100))# 1 / Time between the last two rewards 
    
       
    
    '''
    #average and last CR 75%
    
    '''
    all_ons_75=[item for sublist in all_ons_75 for item in sublist]
    itt_75=[]
    for ele in range(len(all_ons_75)):
        if ele >0:
            itt_75.append((all_ons_75[ele]-all_ons_75[ele-1])*0.001)
        
    mean_cr75=list(map(lambda x: 1.0/x,itt_75))

    zip_cr75=list(zip(last_hit_75,one_before_last_hit_75))
    last_inter_target_times_75  = []
    for lh, obl in zip_cr75:
        last_inter_target_times_75.append((lh-obl)*0.001)
    cr_75=list(map(lambda x: 1.0/x, last_inter_target_times_75))
    
   

    
    '''
    #average and last CR 50%
    
    '''
    all_ons_50=[item for sublist in all_ons_50 for item in sublist]
    itt_50=[]
    for ele in range(len(all_ons_50)):
        if ele >0:
            itt_50.append((all_ons_50[ele]-all_ons_50[ele-1])*0.001)
        
    mean_cr50=list(map(lambda x: 1.0/x,itt_50))
 
    zip_cr50=list(zip(last_hit_50,one_before_last_hit_50))
    last_inter_target_times_50  = []
    for lh, obl in zip_cr50:
        last_inter_target_times_50.append((lh-obl)*0.001)
    cr_50=list(map(lambda x: 1.0/x, last_inter_target_times_50))
  

    
    #try:
    agg_data['CR_last_reward_2_50%']=1/np.nanmedian(two_before_inter_target_times_50)#mean_cr50[len(mean_cr50)-2]
    agg_data['CR_last_reward_2_75%']=1/np.nanmedian(two_before_inter_target_times_75)
    agg_data['CR_last_reward_2_100%']=1/np.nanmedian(two_before_inter_target_times_100)
    
    agg_data['CR_last_reward_3_50%']=1/np.nanmedian(three_before_inter_target_times_50)
    agg_data['CR_last_reward_3_75%']=1/np.nanmedian(three_before_inter_target_times_75)
    agg_data['CR_last_reward_3_100%']=1/np.nanmedian(three_before_inter_target_times_100)
    # except IndexError:
    #     agg_data['CR_last_reward_2_50%']=np.nan
    #     agg_data['CR_last_reward_2_75%']=np.nan
    #     agg_data['CR_last_reward_2_100%']=np.nan
        
    #     agg_data['CR_last_reward_3_50%']=np.nan
    #     agg_data['CR_last_reward_3_75%']=np.nan
    #     agg_data['CR_last_reward_3_100%']=np.nan




    agg_data['ITT_last_reward_50%']=np.nanmedian(last_inter_target_times_50)
    agg_data['ITT_last_reward_75%']=np.nanmedian(last_inter_target_times_75)
    agg_data['ITT_last_reward_100%']=np.nanmedian(last_inter_target_times_100)

    agg_data['mean_CR_last_reward_50%']=1/agg_data['ITT_last_reward_50%']
    agg_data['mean_CR_last_reward_75%']=1/agg_data['ITT_last_reward_75%']
    agg_data['mean_CR_last_reward_100%']=1/agg_data['ITT_last_reward_100%']
    # except IndexError: 
    #     agg_data['mean_CR_last_reward_50%']=np.nan#1/agg_data['ITT_last_reward_50%']
    #     agg_data['mean_CR_last_reward_75%']=np.nan#1/agg_data['ITT_last_reward_75%']
    #     agg_data['mean_CR_last_reward_100%']=np.nan#1/agg_data['ITT_last_reward_100%']
 
    
    agg_data['mean_CR_50%']=np.nanmean(mean_cr100)
    agg_data['mean_CR_75%']=np.nanmean(mean_cr75)
    agg_data['mean_CR_100%']=np.nanmean(mean_cr50)
    
   
    
    ''' 
    
    Giving-up Time 
    
    i.e. Time of patch leaving - time of last reward
    
    '''
    hit_trial_100=[]
    hit_trial_50=[]
    hit_trial_75=[]
    
    for trial in n_trials:
        
        trial_n=TrialFinder(index_list_trial[f'trial-{trial}-100%'],animal_df['code_disp'])
        #print (trial_n)
        if type(trial_n)==list:
            #print ('yes')
            if sum(trial_n)!=0:
                hit_trial_100.append(trial)
        
        trial_n=TrialFinder(index_list_trial[f'trial-{trial}-75%'],animal_df['code_disp'])
        #print (trial_n)
        if type(trial_n)==list:
            if sum(trial_n)!=0:
                hit_trial_75.append(trial)
        
        trial_n=TrialFinder(index_list_trial[f'trial-{trial}-50%'],animal_df['code_disp'])
        
        #print (trial_n)
        if type(trial_n)==list:
            if sum(trial_n)!=0:
                hit_trial_50.append(trial)
            
                
    last_hit_t2_100=[]  
    last_hit_t1_100=[]       
    for trial in  hit_trial_100:
                
        t2_hit=TrialFinder(index_list_trial[f'trial-{trial}-100%'],animal_df['t2']) 
        t1_hit=TrialFinder(index_list_trial[f'hit-trial-{trial}-100%'],animal_df['t2']) 
        #print (t2_hit)
        last_hit_t2_100.append(max(t2_hit))
        last_hit_t1_100.append(max(t1_hit))
    zip_gut100=list(zip(last_hit_t2_100,last_hit_t1_100))
    #print ('ZIP',zip_gut100)
    GUT_100=[]
    for t2,hit in zip_gut100:
        GUT_100.append((t2-hit)*0.001)
        
    last_hit_t2_75=[]  
    last_hit_t1_75=[]       
    for trial in  hit_trial_75:
                
        t2_hit=TrialFinder(index_list_trial[f'trial-{trial}-75%'],animal_df['t2']) 
        t1_hit=TrialFinder(index_list_trial[f'hit-trial-{trial}-75%'],animal_df['t2']) 
        #print (t2_hit)
        last_hit_t2_75.append(max(t2_hit))
        last_hit_t1_75.append(max(t1_hit))
    zip_gut75=list(zip(last_hit_t2_75,last_hit_t1_75))
    #print ('ZIP',zip_gut75)
    GUT_75=[]
    for t2,hit in zip_gut75:
        GUT_75.append((t2-hit)*0.001)
    
    last_hit_t2_50=[]  
    last_hit_t1_50=[]       
    for trial in  hit_trial_50:
                
        t2_hit=TrialFinder(index_list_trial[f'trial-{trial}-50%'],animal_df['t2']) 
        t1_hit=TrialFinder(index_list_trial[f'hit-trial-{trial}-50%'],animal_df['t2']) 
        #print (t2_hit)
        last_hit_t2_50.append(max(t2_hit))
        last_hit_t1_50.append(max(t1_hit))
    zip_gut50=list(zip(last_hit_t2_50,last_hit_t1_50))
    #print ('ZIP',zip_gut50)
    GUT_50=[]
    for t2,hit in zip_gut50:
        GUT_50.append((t2-hit)*0.001)
        

    print   (f'GUT 100:{np.nanmean(GUT_100)}')
    print   (f'GUT 75:{np.nanmean(GUT_75)}')
    print   (f'GUT 50:{np.nanmean(GUT_50)}')
    
    agg_data['mean_GUT_100%']=np.nanmedian(GUT_100)
    agg_data['mean_GUT_75%']=np.nanmedian(GUT_75)
    agg_data['mean_GUT_50%']=np.nanmedian(GUT_50)
    
    
    return agg_data    #first_t1_100#agg_data    #c_all_pokes_100#nTrials_prob#index_list_trial





'''
# =============================================================================
# analyze animals day by day 
# =============================================================================

'''


# def remove_outliers(df, q=0.01):
#     upper = df.quantile(1-q)
#     lower = df.quantile(q)
#     mask = (df < upper) & (df > lower)
#     return mask  


all_animals={}

count_animal=0

for animal in range(1,9):
    count_animal+=1
    all_files=[]
    print (f'#####   Gerbil  {count_animal}  ####')
    count_file=0
    
    #load all animal data
    for file in glob.glob(wdir+f'/animal_data/gerbil_beh_data/Foraging_FORa{animal}/*.csv'):
        #print (file)
        all_files.append(file)
        count_file+=1
        
    all_files= natsort.natsorted(all_files)#sorted(all_files,key=lambda x: x.split('_')[2])

    #print (all_files)
    days={}
    average={}
    
    '''
    # 1 ) load animal's data for each day as data frame
    # 2) aggregate data of rows for each trial and condition 
    
    '''
    for day,file in enumerate(all_files):#list with file names
         day+=1
         print (file)
         days[f'day{day}']=load_file(file)
         days[f'day{day}']=aggregate_trials(days[f'day{day}'],key_list)     
             
    all_animals[f'{animal}']=days
    print (f'#####  Gerbil {count_animal} data aggregated of {count_file} days ####')
    
    
    '''
    # AVERAGE across days
    '''
    for key in key_list:
         average['{0}'.format(key)]=[] 
    
    #collect values for each key for each day
    for day in range(len(all_files)):
        for key in average:
            if day > 2:
                average[key].append(all_animals[f'{animal}'][f'day{day}'][key])
    
    #for key in average:
        #print (len(average[key]))

    
    all_animals[f'{animal}']['mean']={key:np.nanmedian(average[key])for key in average}
    
    
    
'''
#=============================================================================
# creat dic with means of all animals 
#=============================================================================V
'''    
animals_dataset={}
for key in key_list:
         animals_dataset['{0}'.format(key)]=[] 
         
 
for animal in range(N_animals):
    animal+=1
    for key in key_list:
        animals_dataset[key].append(all_animals[f'{animal}']['mean'][key])
    
     
  
'''
#=============================================================================V
#   PLOTTING   &   STATISTICS
#=============================================================================

'''
    
  
 
    
def plotting(l1,label_y,plot_name,subs):
    
    l2=[[0.5]*len(subs),[0.75]*len(subs),[1]*len(subs)]
    l1=[item for sublist in l1 for item in sublist]
    l2=[item for sublist in l2 for item in sublist]
    
    plotted = sns.boxplot(x=l2, y=l1)
    plotted.set(xlabel='Start Reward Probability', ylabel=label_y)
    #https://stackoverflow.com/questions/36578458/how-does-one-insert-statistical-annotations-stars-or-p-values-into-matplotlib
    # x1, x2 = 0, 1   # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
    # y, h, col = max(l1) + 0.04, 0.04, 'k'
    # plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c=col)
    # plt.text((x1+x2)*.5, y+h, "**", ha='center', va='bottom', color=col)
    # # x1, x2 = 1, 2   # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
    # y, h, col = max(l1) + 0.6, 0.6, 'k'
    # plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c=col)
    # plt.text((x1+x2)*.5, y+h, "**", ha='center', va='bottom', color=col)
    # x1, x2 = 0, 2   # columns 'Sat' and 'Sun' (first column: 0, see plt.xticks())
    # y, h, col = max(l1) + 0.08,0.08, 'k'
    # plt.plot([x1, x1, x2, x2], [y, y+h, y+h, y], lw=1.5, c=col)
    # plt.text((x1+x2)*.5, y+h, "**", ha='center', va='bottom', color=col)

    sns_plot = plotted.get_figure()
    sns_plot.savefig(wdir +f'/animal_data/{plot_name}.svg')
    plt.close()
    return None

        
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

    #mk dic then pd.dataframe 
    
    d = {av_name: dv, 'patch_type': patch,'sub': sub #'sub':nsubs  
        }
    
    dataSet= pd.DataFrame(data=d)
    
    
    #run anovva using two packages
    print(f'###  single factor rm-ANOVA for {av_name} ###')
    #print(AnovaRM(dataSet, av_name, 'sub', within=['patch_type']).fit())
    res = pg.rm_anova(dv=av_name, within='patch_type', 
                      subject='sub', data=dataSet, detailed=True, correction=True)
    
    
    #res=pg.friedman(dv=av_name, within='patch_type', 
                      #subject='sub', data=dataSet, method="f")
        
    print ('###')
    print (res) 
    #print (res['p-spher'])
    print ('F-value =',res['F'][0])
    # print ('DOF1:',res['ddof1'])
    # print ('DOF2',res['ddof2'])
    if res['p-spher'][0] < 0.05:
        print ('sphericity is violated!')
        print ('###')
        print ('GG-corrected p:')
        print (res['p-GG-corr'])
        if res['p-GG-corr'][0] < 0.05:
             print ('###')
             print ('Post-hoc t-tests (Tuckey)')
             #print(sp.posthoc_ttest(dataSet, val_col=av_name, group_col='patch_type', p_adjust='bonferroni'))
             print (dataSet.pairwise_tukey(dv=av_name, between='patch_type').round(3))

     
    
    
    elif res['p-unc'] [0]<0.05:
        
        print ('p-val:',res['p-unc'][0])
        print ('###')
        print ('Post-hoc t-tests (Tuckey)')
        #print(sp.posthoc_ttest(dataSet, val_col=av_name, group_col='patch_type', p_adjust='bonferroni'))
        print (dataSet.pairwise_tukey(dv=av_name, between='patch_type').round(3))

       
    return res#None
            



'''
# Mean Trial Duration

'''
lst=[animals_dataset['mean_trial_dur_50%'],
      animals_dataset['mean_trial_dur_75%'],
      animals_dataset['mean_trial_dur_100%']]


lst=[group_dataset['mean_trial_dur_patch_leaving_low'],
      group_dataset['mean_trial_dur_patch_leaving_med'],
      group_dataset['mean_trial_dur_patch_leaving_high']]


res=single_rm_anova('mean_trial_dur',lst,30)
#plotting(lst,'Trial Duration in sec','TrialDuration',[1]*N_animals)   
  
'''
# Mean Reward

'''
lst=[animals_dataset['mean_reward_50%'],
      animals_dataset['mean_reward_75%'],
      animals_dataset['mean_reward_100%']]

single_rm_anova('Mean reward at leaving',lst,8)
#plotting(lst,'Mean reward at leaving','avReward',[1]*N_animals)   
  


'''
# Mean Reward Probability last poke 

'''
lst=[animals_dataset['mean_rew_Prob_last_poke_50%'],
      animals_dataset['mean_rew_Prob_last_poke_75%'],
      animals_dataset['mean_rew_Prob_last_poke_100%']]


single_rm_anova('P(reward) at leaving',lst)
 
#plotting(lst,'P reward at leaving','RewardProb_lastPoke',[1]*N_animals)



'''
# Collection rate last poke 

'''

    
lst=[animals_dataset['mean_CR_last_reward_50%'],
      animals_dataset['mean_CR_last_reward_75%'],
      animals_dataset['mean_CR_last_reward_100%']]

single_rm_anova('last ICR',lst,8)

#plotting(lst,'Collection Rate at leaving','CollectionRate_lastPoke',[1]*N_animals)



'''
# Giving-up Time

'''

lst=[animals_dataset['mean_GUT_50%'],
      animals_dataset['mean_GUT_75%'],
      animals_dataset['mean_GUT_100%']]
single_rm_anova('GUT',lst,8)


#plotting(lst,'Giving-up Time','GivingUpTime',[1]*N_animals)


''

lst=[animals_dataset['rel_rew_Prob_last_poke_50%'],
         animals_dataset['rel_rew_Prob_last_poke_75%'],
         animals_dataset['rel_rew_Prob_last_poke_100%']]
single_rm_anova('Relative_Reward_Probability_last_poke',lst)
#plotting(lst,'Relative Reward Probability last poke','RelRewProb_lastPoke',[1]*N_animals)




norm_lst=[]
for l in range(len(lst)):
    xmin = min(lst[l]) 
    xmax=max(lst[l])
    for i, x in enumerate(lst[l]):
        lst[l][i] = (lst[l][i]-np.mean(lst[l]))/ np.std(lst[l])
        norm_lst.append(lst[l])

#     #norm_lst.append(list(map(lambda x: x-min(lst[l])/(max(lst[l])-min(lst[l])),lst[l])))
    
    


'''write csv file wide format'''
means_low=[animals_dataset['mean_GUT_50%']+group_dataset['GUT_patch_leaving_low']]
means_low=[item for sublist in means_low for item in sublist]
means_med=[animals_dataset['mean_GUT_75%']+group_dataset['GUT_patch_leaving_med']]
means_med=[item for sublist in means_med for item in sublist]
means_high=[animals_dataset['mean_GUT_100%']+group_dataset['GUT_patch_leaving_high']]
means_high=[item for sublist in means_high for item in sublist]

species_group=[0]*8+[1]*28
#subj=[1, 2, 3, 4, 5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36]

df = {'50%': means_low, '75%':means_med,'100%':means_high,'subj':subj,
     'species': species_group}
df=pd.DataFrame(data=df)
df.to_csv(os.getcwd()+'/GUT.csv')



'''
#=============================================================================V
#plot ICRs versus MCRs
#=============================================================================V
'''
lst=[animals_dataset['mean_CR_last_reward_50%'],animals_dataset['mean_CR_50%'],
      animals_dataset['mean_CR_last_reward_75%'],animals_dataset['mean_CR_75%'],
      animals_dataset['mean_CR_last_reward_100%'],animals_dataset['mean_CR_100%']]


lst=[group_dataset['lastCR_patch_leaving_low'],group_dataset['meanCR_patch_leaving_low'],
      group_dataset['lastCR_patch_leaving_med'],group_dataset['meanCR_patch_leaving_med'],
      group_dataset['lastCR_patch_leaving_high'],group_dataset['meanCR_patch_leaving_high']]


lst=[group_dataset['lastITT_patch_leaving_low'],group_dataset['GUT_patch_leaving_low'],
      group_dataset['lastITT_patch_leaving_med'],group_dataset['GUT_patch_leaving_med'],
      group_dataset['lastITT_patch_leaving_high'],group_dataset['GUT_patch_leaving_high']]

lst=[animals_dataset['mean_GUT_50%'],animals_dataset['ITT_last_reward_50%'],
      animals_dataset['mean_GUT_75%'],animals_dataset['ITT_last_reward_75%'],
      animals_dataset['mean_GUT_100%'],animals_dataset['ITT_last_reward_100%']]



#def 2x3_rm_anova(av_name,l1,n):

def rm_anova(av_name,l1,n):
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
    types=['ITT']*n+['GUT']*n
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
    
    
    #run anovva using two packages
    print(f'###  2X3 factor rm-ANOVA for {av_name} ###')
    #print(AnovaRM(dataSet, av_name, 'sub', within=['patch_type']).fit())
    res = pg.rm_anova(dv=av_name, within=['patch_type','type'], 
                      subject='sub', data=dataSet, detailed=True, correction=True)
    
    
    # res=pg.friedman(dv=av_name, within=['patch_type','type'], 
    #                   subject='sub', data=dataSet, method="f")
        
    print ('###')
    print (res) 
    #print (res['p-spher'])
    print ('F-value =',res['F'])
    # print ('F-value 2 =',res['F'][1])
    # print ('F-value 3=',res['F'][2])
    print ('DOF1:',res['ddof1'])
    print ('DOF2',res['ddof2'])
    # if res['p-spher'][2] < 0.05:
    #     print ('sphericity is violated !')
    #     print ('###')
    #     print ('GG-corrected p:')
    #     print (res['p-GG-corr'])
    #     if res['p-GG-corr'][2] < 0.05:
    #           print ('###')
    #           print ('Post-hoc t-tests (Tuckey)')
    #           #print(sp.posthoc_ttest(dataSet, val_col=av_name, group_col='patch_type', p_adjust='bonferroni'))
    #print (dataSet.pairwise_tukey(dv=av_name, between='patch_type').round(3))

     
    
    
    # if res['p-unc'] [1]<0.05 or res['p-unc'] [2]<0.05:
        
    #     print ('p-val:',res['p-unc'][2])
    #     print ('###')
    #     print ('Post-hoc t-tests)')
    #     #print(sp.posthoc_ttest(dataSet, val_col=av_name, group_col='patch_type', p_adjust='bonferroni'))
    #     #print (dataSet.pairwise_tukey(dv=av_name, between=['patch_type','type']).round(3))
    posthocs = pg.pairwise_ttests(dv=av_name, within=['patch_type','type'], subject='sub',
                          padjust='fdr_bh', data=dataSet, correction='auto' )
        
        #print(posthocs)

       
    return posthocs#None
            

icr_animals=rm_anova('ICR',lst,23)






# from statsmodels.stats.anova import AnovaRM # 
# import scikit_posthocs as sp



# print(AnovaRM(dataSet, 'Collection rate', 'sub', within=['patch_type', 'CR_Type']).fit())
 
# sp.posthoc_ttest(dataSet, val_col='collection rate', group_col='CR_type', p_adjust='holm')

# '''
# # =============================================================================
# #         Cox Regression  #surivival analysis 
# # =============================================================================
# '''  
 
# from lifelines import KaplanMeierFitter
# from lifelines import CoxPHFitter

# kmf = KaplanMeierFitter()

# def run_CoxReg(observations,duration,cov1,cov2,cov3,cov4):#cov should be list
    
#     d = {'obsv': observations, 'dur': duration,'Reward_Probability': cov1,
#           'Last_Collection_Rate':cov2,'Patch_type':cov3,'Species':cov4}
    
#     dataSet= pd.DataFrame(data=d)
#     dataSet.to_csv(os.getcwd()+'/HG_beh_data_long.csv')
#     cph = CoxPHFitter()
#     cph.fit(dataSet, duration_col='dur', event_col='obsv')
#     cph.fit(dataSet, duration_col='dur', event_col='obsv', formula="c")
#     cph.print_summary() 
#     cph.plot()
    
    
    
#     cph.plot_partial_effects_on_outcome(covariates='Patch_type', values=[0,1,2], cmap='coolwarm')
    
#     cph.plot_partial_effects_on_outcome(covariates='Species', values=[0,1], cmap='coolwarm')
    
#     return None#cph
 
# # =============================================================================
# # # #makee vectors 
# # =============================================================================

# spec=['0']*8+['1']*28
# spec=spec*3
# all_observations=[1]*(108)
# all_dv=animals_dataset['mean_trial_dur_50%']+group_dataset['mean_trial_dur_patch_leaving_low']+animals_dataset['mean_trial_dur_75%']+group_dataset['mean_trial_dur_patch_leaving_low']+animals_dataset['mean_trial_dur_75%']+group_dataset['mean_trial_dur_patch_leaving_high']
# all_cov2=animals_dataset['mean_CR_last_reward_50%']+group_dataset['lastCR_patch_leaving_low']+animals_dataset['mean_CR_last_reward_75%']+group_dataset['lastCR_patch_leaving_med']+animals_dataset['mean_CR_last_reward_100%']+group_dataset['lastCR_patch_leaving_high']
# all_cov1=animals_dataset['rel_rew_Prob_last_poke_50%']+group_dataset['meanTP_patch_leaving_low']+animals_dataset['rel_rew_Prob_last_poke_75%']+group_dataset['meanTP_patch_leaving_med']+animals_dataset['mean_CR_last_reward_100%']+group_dataset['meanTP_patch_leaving_high']
# patch_type=['50%']*36+['75%']*36+['100%']*36

# # #DV = trial durations
# run_CoxReg(all_observations,all_dv,all_cov1,all_cov2,patch_type,spec)   


# d = {'obsv': all_observations, 'dur': all_dv,'species':spec}
# dataSet= pd.DataFrame(data=d)
# cph = CoxPHFitter()
# cph.fit(dataSet, duration_col='dur', event_col='obsv')
# cph.print_summary() 


# # spcies 



# from lifelines import KaplanMeierFitter
# kmf = KaplanMeierFitter()


# '''
# # =============================================================================
# #         determine dependent Variable and covs
# # =============================================================================
        
# '''
# T1 = group_dataset['mean_trial_dur_patch_leaving_low']
# T2 = group_dataset['mean_trial_dur_patch_leaving_med']
# T3 = group_dataset['mean_trial_dur_patch_leaving_high']
# T_TD=T1+T2+T3

# T11 = group_dataset['GUT_patch_leaving_low']
# T21 = group_dataset['GUT_patch_leaving_med']
# T31 = group_dataset['GUT_patch_leaving_high']

# T_GUT=T11+T21+T31

# E_all=[1]*(len(nsubs)*3)#make vector with observed events 
# all_cov1=group_dataset['meanTP_patch_leaving_low']+group_dataset['meanTP_patch_leaving_med']+group_dataset['meanTP_patch_leaving_high']
# all_cov2=group_dataset['lastCR_patch_leaving_low']+group_dataset['lastCR_patch_leaving_med']+group_dataset['lastCR_patch_leaving_high']

# patch_type=[2]*len(nsubs)+[1]*len(nsubs)+[0]*len(nsubs)#Cov3

# ax = plt.subplot(111)
# kmf.fit(T1, label="low")
# kmf.plot(ax=ax,ci_force_lines=False)
# kmf.fit(T2, label="medium")
# kmf.plot(ax=ax,ci_force_lines=False)
# kmf.fit(T3, label="high")
# b=kmf.plot(ax=ax,ci_force_lines=False)
# plt.ylim(0, 1);
# plt.title('Survival function of exploiting a patch for the three display types')

# b.get_figure().savefig(datapath + f'random_loc/exp_decay/data/final/final/KM_low.png')
#plt.close()


