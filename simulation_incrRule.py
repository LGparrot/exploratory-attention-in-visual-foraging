#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 16:45:56 2024

@author: parrot
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from scipy.stats import bootstrap





'''
take the residence times as well as the intital rewards and simulate the number of rewards.
'''
def simulate_rewards(staying_times, initial_rewards):
    caught_rewards = []
    for time in staying_times:
        # Randomly select an initial number of rewards from the environments
        initial_reward = np.random.choice(initial_rewards)
        # Simulate the number of rewards caught based on staying time and initial rewards
        # This is a placeholder for your simulation logic
        rewards = simulate_catching_logic(time, initial_reward)
        caught_rewards.append(rewards)
    return np.array(caught_rewards)


#null model - assuming a simple proportional relation
def simulate_catching_logic(time, initial_reward):
    # Placeholder for the actual simulation logic
    # For example, a simple logic might be proportional to the staying time
    return time * initial_reward / 100  # Adjust this formula as needed




'''
then regressed the residence times on the simulated number of reward captures
'''



for sub in range(len(group_dataset_fmri['list_tri_dur'])):#for each subject
    subj_slopes=[]
    for n in range(100):#100 simulations of reward encounters if relation was random
        staying_times = np.array(group_dataset_fmri['list_tri_dur'][sub])
        initial_rewards = np.array([40,30,20 ])#number of active targets in a patch 
        # Simulate the rewards caught based on staying times
        simulated_rewards = simulate_rewards(staying_times, initial_rewards)
        
        
        
        # Fit the linear regression model to the simulated data
        model = LinearRegression()
        model.fit(simulated_rewards.reshape(-1, 1), staying_times)#(x,y)
        
        # Obtain the slope (coefficient) and intercept
        slope = model.coef_[0]
        subj_slopes.append(slope)
        intercept = model.intercept_

    simulated_slopes.append(subj_slopes)


simulated_slopes=[item for sublist in simulated_slopes for item in sublist]


'''
recombination via boostrapping
'''
data = (simulated_slopes,)
bootstrap_ci = bootstrap(data, np.median, confidence_level=0.95,n_resamples=100000,
                         random_state=1, method='percentile')



'''
plot slopes for simulated data

'''

#data1 = simulated_slopes  # First distribution
data1 = bootstrap_ci.bootstrap_distribution  # Second distribution

# Determine the number of bins
num_bins_1 = int(np.sqrt(len(data1)))

# Generate histogram for the data
hist1, bins1 = np.histogram(data1, bins=num_bins_1)


# Plot the histogramss
plt.hist(data1, bins=bins1, alpha=0.5, label='simulated slopes', color='blue', edgecolor='black')
#plt.hist(data2, bins='auto', alpha=0.5, label='real slopes', color='green', edgecolor='black')
plt.xlim(2.1, 2.2)
plt.ylim(0, 1300)
plt.axvline(x = np.percentile(data1, 99), color = 'r', label = f'99th percentile = {round(np.percentile(data1, 99),3)}')
plt.xlabel('Slopes obtained with simulated data')
plt.ylabel('Counts')
# Add a legend to the plot
plt.legend(loc='upper right')

# Display the plot
plt.show()





'''
repeat the same for the animal data

resDurs is imported from data wrangling of animal data

'''



'''
get animals' residences time into the right format 
(list with list, listing animals as elements that contain a llist of their residence times trial by trial)
Then seperate longGUT from shortGUT animals 

'''

time_ani_short={}
animals=indices_short_g
for key in animals:
    time_ani[key]=[]
for animal in indices_short_g:
    for count,day in enumerate(resDurs):
        for row in day:
            if count >0:
                if row[1]==animal:
                    time_ani_short[animal].append(row[0])

resDurs_short=[]
for key in time_ani:
    resDurs_short.append(time_ani[key])
    
    
    
time_ani_long={}
animals=indices_long_g
for key in animals:
    time_ani[key]=[]
for animal in indices_long_g:
    for count,day in enumerate(resDurs):
        for row in day:
            if count >0:
                if row[1]==animal:
                    time_ani_long[animal].append(row[0])

resDurs_long=[]
for key in time_ani:
    resDurs_long.append(time_ani[key])
        
 
all_Durs=[resDurs_long,resDurs_short]
    
'''
now do the reg based on simulated data for both sub-groups
'''
for resDurs in all_Durs:  
    
    simulated_slopes_animals=[]
    for animal in range(len(resDurs)):#for experimental session (397)
        animals_slopes=[]
        for n in range(100):#100 simulations of reward encounters if relation was random
            staying_times = np.array(resDurs[animal])
            initial_rewards = np.array([20,15,10])#number of active targets in a patch 
            # Simulate the rewards caught based on staying times
            simulated_rewards = simulate_rewards(staying_times, initial_rewards)
            
            
            
            # Fit the linear regression model to the simulated data
            model = LinearRegression()
            model.fit(simulated_rewards.reshape(-1, 1), staying_times)#(x,y)
            
            # Obtain the slope (coefficient) and intercept
            slope = model.coef_[0]
            animals_slopes.append(slope)
            intercept = model.intercept_
    
        simulated_slopes_animals.append(animals_slopes)
    
    
    simulated_slopes_animals=[item for sublist in simulated_slopes_animals for item in sublist]
    
    
    '''
    boostrap
    '''
    data2 = (simulated_slopes_animals,)
    bootstrap_ci_ani = bootstrap(data2, np.median, confidence_level=0.95,n_resamples=100000,
                             random_state=1, method='percentile')
    
    #data1 = simulated_slopes  # First distribution
    data_ani = bootstrap_ci_ani.bootstrap_distribution  # Second distribution
    
    # Determine the number of bins
    num_bins_ani = int(np.sqrt(len(data_ani)))
    
    # Generate histogram for the data
    hist_ani, bins_ani = np.histogram(data_ani, bins=num_bins_ani)
    
    
    
    
    '''
    visualize
    '''
    # Plot the histogramss
    plt.hist(data_ani, bins=bins_ani, alpha=0.5, label='simulated slopes', color='blue', edgecolor='black')
    #plt.hist(data2, bins='auto', alpha=0.5, label='real slopes', color='green', edgecolor='black')
    plt.xlim(5.7, 6.3)
    plt.ylim(0, 2500)
    plt.axvline(x = np.percentile(data_ani, 99), color = 'r', label = f'99th percentile = {round(np.percentile(data_ani, 99),3)}')
    plt.xlabel('Slopes obtained with simulated data')
    plt.ylabel('Counts')
    # Add a legend to the plot
    plt.legend(loc='upper right')
    
    # Display the plot
    plt.show()
