#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 22 23:39:44 2022

@author: lasseguldener
"""


from __future__ import division

'''
###    FORAGING SFB C02 - WP1.1
###    generate onset files for GLM
'''

import os
import numpy as np
import pandas as pd
import pathlib 
from pathlib import Path
from ast import literal_eval


datapath=Path(Path.cwd())



def get_onsets(sub,n_block,
               dic,keys,
               condition,
               start_prob):
    
    print (f'block-0{n_block+1}')
    global subs_path
    subs_path=datapath / f'human_foraging/data/beh/sub-{sub}/'
    df=pd.read_csv(subs_path / f"beh-data_sub-0{sub}_block-0{n_block}.tsv",sep='\t',error_bad_lines=False)
    
    for ele in range(len(df['reward_ons'])):
        df['reward_ons'][ele]=literal_eval(df['reward_ons'][ele])
        df['detection'][ele]=literal_eval(df['detection'][ele])
        df['reward_prob_next_target'][ele]=literal_eval(df['reward_prob_next_target'][ele])
        df['responseTime'][ele]=literal_eval(df['responseTime'][ele])
    
    
    '''
    by condition
    
    '''
    GUT=list()
    ons_pre_patch_leaving=list()
    dur_pre_patch_leaving=list()
    #ones_pre_patch_leaving=list()
    
    ons_search=[]
    ons_detection=[]
    ons_patch_leaving=[]
      
    dur_search=[]
    dur_detection=[]
    dur_patch_leaving=[]

    
    ones=[]

    if len(df['detection'][len(df)-1]) == 0:
    
    
        n_rows=len(df)-1
        
    else:n_rows=len(df)

    for row in range(n_rows):
    
        if df['trial type'][row]==condition:
            print (row)
            
            if len(df['detection'][row])!=0:
                if start_prob==0:
                
                    if len(df['reward_ons'][row])>0:#if they found at least one search target
                        
                        
                        for i,a in zip(df['detection'][row],df['reward_ons'][row]):
                            diff=float(a)-float(i)
                            dur_detection.append(diff)
                        for ele in range(len(df['detection'][row])):
                            ons_detection.append(df['detection'][row][ele])
                    
                        
                        if df['search_dur_patch_leaving'][row] > 10.0: #those trials in which subj spend more than 10 sec searching
                        
                            pre_ons=df['end of search'][row] - 10
                            GUT.append(df['end of search'][row]-df['reward_ons'][row][-1:][0])
                            print (pre_ons)
                            ons_pre_patch_leaving.append(pre_ons)
                            dur_pre_patch_leaving.append(0.1)
                        
                        
                            for i,a in zip(df['detection'][row],df['reward_ons'][row]):
                                diff=float(a)-float(i)
                                dur_detection.append(diff)
                            for ele in range(len(df['detection'][row])):
                                ons_detection.append(df['detection'][row][ele])
                        
                        elif len(df['reward_ons'][row])==0:
                                
            
                            diff=float(df['end of search'][row])-float(df['detection'][row][0])
                            dur_detection.append(diff)
                            ons_detection.append(df['detection'][row][0])
            
                   
                            
                        ons_search.append(df['search'][row])
                        dur_search.append(df['search_dur_patch_leaving'][row])
                        ones.append(1)
                        
                        ons_patch_leaving.append(df['end of search'][row])
                        dur_patch_leaving.append(1.0)
                    
                elif df['start_prob'][row]==start_prob:
                    
             
                    
                    if len(df['reward_ons'][row])>0:
                        
                        for i,a in zip(df['detection'][row],df['reward_ons'][row]):
                            diff=float(a)-float(i)
                            dur_detection.append(diff)
                        for ele in range(len(df['detection'][row])):
                            ons_detection.append(df['detection'][row][ele])
                    
                    elif len(df['reward_ons'][row])==0:
                        
                        diff=float(df['end of search'][row])-float(df['detection'][row][0])
                        dur_detection.append(diff)
                        ons_detection.append(df['detection'][row][0])
           
                            
                    ons_search.append(df['search'][row])
                    dur_search.append(df['search_dur_patch_leaving'][row])
                    ones.append(1)
                    
                    ons_patch_leaving.append(df['end of search'][row])
                    dur_patch_leaving.append(1.0)
                    
  
    '''
    onsets for GLM: search display onset
        
    '''
    onse=[1]*len(ons_search)
    zip_=list(zip(ons_search,dur_search,onse))
    d1=pd.DataFrame(zip_)
    print (d1)
    dic[keys[0]].append(d1)
    
    
    onse=[1]*len(ons_detection)
    zip_=list(zip(ons_detection,dur_detection,onse))
    d2=pd.DataFrame(zip_)
    dic[keys[1]].append(d2)
    
    
    onse=[1]*len(ons_patch_leaving)
    zip_=list(zip(ons_patch_leaving,dur_patch_leaving,onse))
    d3=pd.DataFrame(zip_)
    dic[keys[2]].append(d3)
    
    onse=[1]*len(ons_pre_patch_leaving)
    zip_=list(zip(ons_pre_patch_leaving,dur_pre_patch_leaving,onse))
    d4=pd.DataFrame(zip_)
    dic[keys[3]].append(d4)

    return all_onsets#all_ds1,all_ds_2,all_ds_3,all_ds_4


ons_keys=['search','detection','patch_leaving','pre_patch_leaving']
    
for sub in  [6,7,8,9,10,11,12]:
    
    for condition in ['full search', 'early break']:
    
        for prob in [0,0.5,0.75,1]:
            
            all_onsets=dict()
            all_onsets['search']=[]
            all_onsets['detection']=[]
            all_onsets['patch_leaving']=[]
            all_onsets['pre_patch_leaving']=[]
            
            for block in [0,1,2,3,4,5]:
                '''
                get onsets, save in df for each block and save in condition dic
                '''
                get_onsets(sub,block,all_onsets,ons_keys,condition,prob)
                
            
            '''
            save onset files for each block
            '''

            # if prob !=0:
            #     for key in list(all_onsets.keys()):
            #         all_onsets[key][block].to_csv(datapath + f"/human_foraging/data/beh/sub-{sub}/onsets_{key}_{c}_{prob}_block0{block+1}.txt", sep='\t',index=False, header=False)

            #     # all_onsets['pre_patch_leaving'][block].to_csv(datapath + f"/human_foraging/data/beh/sub-{sub}/onsets_pre_patch_leaving_{key}_{c}_{prob}_block0{block+1}.txt", sep='\t',index=False, header=False)
            #     # all_onsets['patch_leaving'][block].to_csv(datapath + f"/human_foraging/data/beh/sub-{sub}/onsets_patch_leaving_{key}_{c}_{prob}_block0{block+1}.txt", sep='\t',index=False, header=False)
            #     # all_onsets['search'][block].to_csv(datapath + f"/human_foraging/data/beh/sub-{sub}/onsets_search_{key}_{c}_{prob}_block0{block+1}.txt", sep='\t',index=False, header=False)
            #     # all_onsets['detection'][block].to_csv(datapath + f"/human_foraging/data/beh/sub-{sub}/onsets_detection_{key}_{c}_{prob}_block0{block+1}.txt", sep='\t',index=False, header=False)
            # else :
            #     for key in list(all_onsets.keys()):
            #         all_onsets[key][block].to_csv(datapath + f"/human_foraging/data/beh/sub-{sub}/onsets_{key}_{c}_block0{block+1}.txt", sep='\t',index=False, header=False)
            
                # all_onsets['pre_patch_leaving'][block].to_csv(datapath + f"/human_foraging/data/beh/sub-{sub}/onsets_pre_patch_leaving_{key}_{c}_block0{block+1}.txt", sep='\t',index=False, header=False)
                # all_onsets['patch_leaving'][block].to_csv(datapath + f"/human_foraging/data/beh/sub-{sub}/onsets_patch_leaving_{key}_{c}_block0{block+1}.txt", sep='\t',index=False, header=False)
                # all_onsets['search'][block].to_csv(datapath + f"/human_foraging/data/beh/sub-{sub}/onsets_search_{key}_{c}_block0{block+1}.txt", sep='\t',index=False, header=False)
                # all_onsets['detection'][block].to_csv(datapath + f"/human_foraging/data/beh/sub-{sub}/onsets_detection_{condi}_block0{block+1}.txt", sep='\t',index=False, header=False)
            

                
            '''
            add 10*60 / 20*60 sec. to onset column in the second and third block
            to adjust the timing when nii.gz are merged in time 
            
            '''
            for key in list(all_onsets.keys()):
                if len(all_onsets[key][1]) >0:
                    all_onsets[key][1][0]= all_onsets[key][1][0]+(10*60)#add 10 minutes in block 2
                if len(all_onsets[key][2]) >0:
                    all_onsets[key][2][0]= all_onsets[key][2][0]+(20*60)#add 20 minutes in block 3
                if len(all_onsets[key][4]) >0:
                    all_onsets[key][4][0]= all_onsets[key][4][0]+(10*60)# ... block 4
                if len(all_onsets[key][5]) >0:
                    all_onsets[key][5][0]= all_onsets[key][5][0]+(20*60)# ... block 5
                    
            
                '''
                concatenate first 30 minutes 
                '''
                merged_1=pd.concat(all_onsets[key][0:3])
                merged_2=pd.concat(all_onsets[key][4:6])
                # merged_1=merged_1.reset_index()
                # merged_1=merged_1.reset_index()
            
                # '''
                # do some cleaning
                # '''
                #merged_1 = merged_1[merged_1[1] < np.mean(merged_1[1])+(2*np.std(merged_1[1]))]  
                #merged_2 = merged_2[merged_2[1] < np.mean(merged_2[1])+(2*np.std(merged_2[1]))]  
                
                '''
                write text file in 3 column format for FSL
                
                '''
                if prob !=0:
                    if condition =='early break':
                        c='early_break'
                    else:
                        c ='full_search'
                    merged_1.to_csv(subs_path / f"onsets_{key}_{prob}_{c}_1half.txt", sep='\t',index=False, header=False)
                    merged_2.to_csv(subs_path / f"onsets_{key}_{prob}_{c}_2half.txt", sep='\t',index=False, header=False)
                else:
                    if condition =='early break':
                        c='early_break'
                    else:
                        c ='full_search'
                    merged_1.to_csv(subs_path / f"onsets_{key}_{c}_1half.txt", sep='\t',index=False, header=False)#across all reward probs
                    merged_2.to_csv(subs_path / f"onsets_{key}_{c}_2half.txt", sep='\t',index=False, header=False)
      
            
                
