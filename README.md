#  DATA AVAILABILITY     
We did not pre-register any part of the reported study procedures nor any of the conducted analyses prior to conducting the research. 

The human and animal behavioral data is deposited at OSF: https://osf.io/fexgb/?view_only=b3b16acc786f497db13881ae5aa99b6d

The conditions of our ethics approval do not permit public archiving of anonymized fMRI data. 
Readers seeking access to the data should contact the me.


#  STIMULUS PRESENTATION
Note: written for python 3.6, tested on 3.8, psychopy is needed - https://www.psychopy.org/download.html)

  1) download stimuli/
  2) run visual_search_foraging.py 


#  USER GUIDE - Data wrangling & analysis of the behavioral data  
Note: written for python 3.6, runs on 3.9< with a few changes 

  1) data_wrangling.py                - aggregates raw behavioral data to means and calculates parameters relevant for further analysis.
  2) wrangling_animal_data.py         - does the same for the animal data.
  3) rm_anova.py                      - functions to conduct repeated measure ANOVAS mostly using lib pingouin.   
  4) data_cleaning.py                 - function to clean data. 



  
