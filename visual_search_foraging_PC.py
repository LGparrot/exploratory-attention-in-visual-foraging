#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Lasse 

"""


from psychopy import visual, core, event, gui, data, monitors, logging
from psychopy.hardware import joystick
globalClock = core.Clock()
logging.setDefaultClock(globalClock)
import sys
import os
import numpy as np
import random
import pandas as pd
import csv
import json
import glob
import time
from math import e
import json
from datetime import datetime
logging.console.setLevel(logging.CRITICAL)
from pathlib  import Path



''' 
screen parameters 

'''

#from screeninfo import get_monitors
#bash:  xdpyinfo | grep dimensions



 
'''
# =============================================================================
# subject info
# =============================================================================
 '''
#sub=3
#age=0
#gender='w'
#vision=0

date=data.getDateStr()
training=True
reward_count=[]
'''
# =============================================================================
# Monitors used for displays - adjust these params to your machine!
# =============================================================================
 '''
#Prisma scanner 
#my mac 
width = 2560 
height = 1600
#width = 1440#2560 
#height = 900#1600

#basement K010 three booth
#width=1920
#height=1080


'5min intro + training'


#logFile
logging.LogFile()


''' 
# =============================================================================
# get current working directory and create folders  
# =============================================================================

'''

wdir=os.getcwd()
exp_folder = Path(wdir+"/human_foraging/")
data_folder = Path(wdir+"/human_foraging/data/")
subInfo_folder= Path(wdir+"/human_foraging/subjInfo/")
allfolders=[exp_folder,data_folder,subInfo_folder]




for fd in allfolders:
    if not os.path.exists(fd):
        os.makedirs(fd)



''' 
# =============================================================================
# PARAMETERS #### 
# =============================================================================
'''

stim_color = 'white'
fixation_color = 'black'
bg_color = 'black'

ppd = 20#factor to mult pix size


stim_height = 20
frameRate= 1/60.0
fr=1/60.0


horizontal_start = -35 # horiz dimension of the grid
horizontal_end = 35 # 

vertical_start = -20 #vertical limits -20
vertical_end = 20 # 20

jitter_offset_list = np.linspace(-0.25, 0.25, 10)#[-0.2, 0, 0.2] # offset of jitter 

stim_size=20
number_of_search_targets = 40 # number of targets 
number_of_distractors = 120 # number of distractors
visual_grid = [26,24] # the grid on which the targets and distractors will be sitting ()
if visual_grid[0]*visual_grid[1] < number_of_distractors+number_of_search_targets:
    sys.exit("Number of targets and distractors is higher than number of grid cells")

timerDuration = 0.5#for the target fixation
#maxdur=30#108000*frameRate#1800=30min
maxdur=600
n_blocks=6 # number of runs /search periods of 10 min. each

#mk cb list for the target probability a trial starts with
start_probability=[1]*100+[0.75]*100+[0.5]*100




'''

predefine target identity 

'''
#stim_dir=Path(os.getcwd()+"/Desktop/Lasse/stimuli/")
stim_dir=Path(os.getcwd()+"/stimuli/")
reward_image=stim_dir / "5cent.png"
target_image=stim_dir / "circle.png"

distractor_image0=stim_dir / "square.png"
distractor_image1=stim_dir / "square2.png"
distractor_image2=stim_dir / "circle2.png"



all_stim=[target_image,distractor_image0,distractor_image1,distractor_image2]
random.shuffle(all_stim)

all_dist=[]
target_img=[]

for img in range(len(all_stim)):
    if img <1:
        target_img.append(all_stim[img])
        #del all_stim[img]
    else:all_dist.append(all_stim[img])

print (f'target in main exp. = {target_img[0]}')
if target_img[0] == target_image:
    target='blue_circle'
elif target_img[0] == distractor_image2:
    target='green_circle'
elif target_img[0] == distractor_image0:
    target='green_square'
elif target_img[0] == distractor_image1:
    target='blue_square'

'''

training stimuli

'''
target_image2=stim_dir / "circle3.png"
distractor_image0_2=stim_dir / "square3.png"
distractor_image1_2=stim_dir / "square4.png"
distractor_image2_2=stim_dir / "circle4.png"



all_stim_training=[target_image2,distractor_image0_2,distractor_image1_2,distractor_image2_2]
random.shuffle(all_stim_training)
all_dist_training=[]
target_img_training=[]
for img in range(len(all_stim_training)):
    if img <1:
        target_img_training.append(all_stim_training[img])
        #del all_stim[img]
    else:all_dist_training.append(all_stim_training[img])
    
print (f'target for training = {target_img_training[0]}')  
    
'''    
# =============================================================================
# Instructions
# =============================================================================
'''   
def show_intro(win):

    instructions=[(f'''Vielen Dank für deine Teilnahme! \n\n\n 
    Im folgenden Experiment hast du die Gelegenheit, Geld zu verdienen! 
    Drücken die rechte Maustaste um fortzufahren.
    ''')]#%(number_of_search_targets)]

    text2=(u'''Wenn du bereit bist, kann es losgehen. 
    Jetzt folgen die zwei Probedurchläufe. Suche dabei nach Objekten, die mit dem gezeigten Objekt in Farbe und Form übereinstimmen.\n\n\n
    Wie im späteren Experiment, kannst du jederzeit zu einem neuen Display wechseln, wenn die Suche zu mühsam wird.\n\n\nDu wechselst zum nächsten Display, indem du die rechte Maustaste drückst.\n\n\n
    Drücke die Leertaste, wenn du bereit bist zu starten.''')

    mouse = event.Mouse()
    intro = visual.TextStim(win, text='LOREM IPSE',pos=[0,0], units='pix',color='white',height=20)
    
    for key in instructions:
        intro.text=key

        intro.draw()
        mouse.setVisible(False)
        win.flip()
        buttons, times = mouse.getPressed(getTime=True)
        while buttons == [0,0,0]:
            buttons, times = mouse.getPressed(getTime=True)
            if buttons == [1, 0, 0] or buttons == [0, 0, 1]:
                break
        times = mouse.clickReset()
        event.clearEvents()
        
    example_target= visual.ImageStim(win, pos=(0,95),image=target_img_training[0],contrast=1, size=(20,20))
    example_target.draw()
    intro.text=text2
    intro.height=20
    intro.draw()
    mouse.setVisible(False)
    event.clearEvents()
    win.flip()
    times = mouse.clickReset()
    button, times = mouse.getPressed(getTime = True)
    keypress = event.waitKeys(keyList=['space','t', 'escape'])
    
    if keypress[0] == 'escape':
        core.quit()
        
    return None 
 
        
def show_intro2(win,trial):
    mouse = event.Mouse()
    intro = visual.TextStim(win, text=(f'''Nach %i Probedurchgängen bist du jetzt fit für das eigentliche Experiment. Suche ab jetzt nach dem oben abgebildeten Objekt.\n\n\nDrücke die Leertaste, dann t, um zu starten.''')%trial,
                                        pos=[0,0], units='pix',color='white',height=20)
    example_target= visual.ImageStim(win, pos=(0,100),image=target_img[0],contrast=1, size=(20,20))
    example_target.draw()
    intro.draw()
    mouse.setVisible(False)
    win.flip()
    keypress = event.waitKeys(keyList=['space', 'escape'])
    
    if keypress[0] == 'escape':
        core.quit()
    return None 


def do_break(win,text):
    mouse = event.Mouse()
    break_text2 = visual.TextStim(win, text=text, pos=[0, -100], units='pix',color='white')
    break_text2.draw()
    mouse.setVisible(False)
    win.flip()
    keypress = event.waitKeys(keyList=['space', 'escape'])
    if keypress[0] == 'escape':
        core.quit()
    
    return None 

def quit_task(win,
              sub,
              n_Blocks,
              date,subs_path,rewardcount):
     
    #give feedback about current score 
    
    # scores=[]
    
    # for block in range(n_Blocks):
    #     df = pd.read_csv(subs_path/f"beh-data-sub{sub}-block{block}.csv",converters={'reward':eval},sep=',')
    #     results=list(map(int, df['reward']))
    #     scores.append(sum(results))
    
    gewinn=sum(rewardcount)/20.0
    print ('Versuchsperson hat',gewinn,' Euro gewonnen')


    df1={}
    df1['Gewinn']=gewinn
    df1['age']=age
    df1['gender']=gender
    df1['vision']=vision
    df1['ID']=sub
    df1 = pd.DataFrame(data=df1,index=[0])
    df1.to_csv(subInfo_folder /f"subj{sub}_info_{date}.csv",sep=',',index=False,header=True)
    
    end_text = visual.TextStim(win, text=(f'''Die Suchzeit ist vorbei! Du hast einen Gewinn von {gewinn} Euro.\n\n Vielen Dank für deine Teilnahme!'''), 
                                          pos=[0, 0], 
                                          units='pix',
                                          color='white')
    end_text.draw()
    win.flip()
    core.wait(5)
    win.close()
    core.quit()
    
    return None 

def write_json(entry_list,
               fname,
               condi,
               sub,
               target_type):
    
    now = datetime.now()
    
    
    if condi:
            
        entry = { "Task Name":"Human probabilistic foraging", 
                 "Task Description":"Conjunct Foraging - collect all items that have same color and shape",
                 "InstitutionName":"Otto-von-Guericke-University",
                 "InstitutionalDepartmentName":"Department of Psychology",
                 "Code Author":"Lasse Gueldener",
                 "Trial Type":{"LongName": "Exploration", "Date & Time":now.strftime("%d/%m/%Y %H:%M:%S"),
          "Trial Description": "self-initiated switch to next trial bev= patch leaving",
          "Levels": {
             "Exploration": "trial ended before all targets were collected ",
             "Exploitation": "trial ended after all targets were collected ",
             "Search Target":target_type,
             } }
            }
    else:
        
        entry = { "Task Name":"Human probabilistic foraging", 
                 "Task Description":"Conjunct Foraging - all items that have same color and shape",
                 "InstitutionName":"Otto-von-Guericke-University",
                 "InstitutionalDepartmentName":"Department of Psychology",
                 "Code Author":"Lasse Gueldener",
                 "Trial":{"LongName": "Exploitation",  "Date & Time":now.strftime("%d/%m/%Y %H:%M:%S"),
          "Trial Description": "forced switch to next trial after all targets are collected = exhaustive search",
          "Levels": {
             "Exploration": "trial ended before all targets were collected ",
             "Exploitation": "trial ended after all targets were collected ",
             "Search Target":target_type,
             
             } }
            }
    
    entry_list.append(entry)

    with open(fname, mode='w') as f:
        f.write(json.dumps(entry_list, indent=2))

    
    return None

'''
use this to ensure correct format of final file 
'''
def collect_responses(fix,
                      blank,
                      search, 
                      detection,
                      trial_type,
                      rt,
                      searchtime,
                      rewardons,
                      search_dur,
                      search_end,
                      reward,
                      reward_p,
                      start_prob
                      ):
    
    trial_column = pd.DataFrame({'fix' : [fix], 
                              'blank' : [blank],
                              'search' : [search],
                              'detection' : [detection],
                              'trial type' : [trial_type],
                              'responseTime' : [rt],
                              'searchTime' : [searchtime],
                              'reward_ons' : [rewardons],
                              'search_dur_patch_leaving':[search_dur],
                              'end of search':[search_end],
                              'reward':[reward],
                              'reward_prob_next_target':[reward_p],
                              'start_prob':[start_prob]
                              })
    return trial_column 


'''
# =============================================================================
#     Start with GUI to collect subj info
# =============================================================================
'''
def sub_info():
    expName = 'human_foraging'
    expVar = {'SubjID': '', 
              'Initials': '', 
              'Gender':['Female', 'Male','Other'], 
              'Age': '', 
              'Vision':['normal','korrigiert mit Brille'],
              'Handedness':['rechts', 'links','beide'],
              'Include practice?': True, 
              'Fullscreen mode?': True, 
              }

    dlg = gui.DlgFromDict(expVar, title = expName)
    
    if not dlg.OK: 
        core.quit()
    else:
        expVar['Date'] = data.getDateStr()
        global date
        date = expVar['Date']
        global sub
        sub=int(expVar['SubjID'])
        global fullscr
        fullscr=expVar['Fullscreen mode?']
        
        expinfo=pd.DataFrame([expVar])
        #expinfo.to_csv(subInfo_folder + 'subj%s'%expVar['SubjID']+'_info_%s'%expVar['Date']+'.csv',sep=',',index=False,header=True)
        expinfo.to_csv(subInfo_folder / f"subj{expVar['SubjID']}_info_{expVar['Date']}.csv",sep=',',index=False,header=True)
        
    return expinfo, sub 

'''
# =============================================================================
#   Trial function
# =============================================================================
'''
def run_trial(win,
              block,
              sub,
              training,
              trial,
              early_break,
              onset_clock,
              search_countdown,
              start,
              maxdur,
              reward_count,
              start_probability,
              positions_mouse,
              positions_time,
              json_list,ons,
              durs,
              events, 
              block_column,
              all_stim_pos,
              all_stim_pos_time,
              positions_target,
              ):
                
    '''mk sub folder'''
    global subs_path
    subs_path= data_folder / f"beh/sub-{sub}/"
    if not os.path.exists(subs_path):
        os.makedirs(subs_path)
        
    if not training:

        draw_from=[0]*75+[1]*25 # assumes 100 trial max per block
        
        random.shuffle(draw_from)
        if random.choice(draw_from) ==0:
            early_break = False
        else:early_break = True
        
    else:early_break = False

    '''
    #create dictionary to collect onsets, RTs etc. 
    
    '''
    onsets={}
    onsets['fix']=0
    onsets['blank']=0
    onsets['search']=0
    onsets['detection']=[]
    onsets['trial type']='full search'
    onsets['responseTime']=[]
    onsets['searchTime']=0
    onsets['reward_ons']=[]
    onsets['search_dur_patch_leaving']=[]
    onsets['end of search']=0
    onsets['reward']=0
    onsets['reward_prob_next_target']=[]
    onsets['start_prob']=0
    all_ends=[]

    

    condi=True
    '''
    # =============================================================================
    # initiate all components.
    
    '''
    fixation = visual.ShapeStim(win,
                                pos=(0.,0.),
                                units= 'height',
                                vertices = ((0, -0.025), (0, 0.025), (0,0), (-0.025,0), (0.025, 0)),
                                lineWidth = 3,
                                closeShape = False,
                                lineColor = 'white')

    
    feedback = visual.TextStim(win, pos=[0, 0], units='pix',height=20,color='white')
    
    clock= visual.TextStim(win, pos=[-390, -430],units='pix',height=20,color='white')#430
    

    
    collection_count=0
    gain= visual.TextStim(win, pos=[390, -430], units='pix',height=20,color='white') #430

    end_message = visual.TextStim(win, text=u'Die Zeit für die Suche ist abgelaufen!', pos=[0, 0], units='pix',height=20,color='black')
    
    if training:
        
        mouse_point = visual.Circle(win, radius=4, pos=(0, 0), edges=100, lineColor='blue',
                                      fillColor='blue')
        
        mouse_rect  = visual.Rect(win, 25, 25, pos=(0,0), lineColor='blue', fillColor=None)
    
    else:
        mouse_point = visual.Circle(win, radius=4, pos=(0, 0), edges=100, lineColor='red',
                                      fillColor='red')
        
        mouse_rect  = visual.Rect(win, 25, 25, pos=(0,0), lineColor='red', fillColor=None)
        

    all_targ_pos=[]
    all_dis_pos=[]
    all_rem_pos=[]
    all_targ_pos=[]
    all_dis_pos=[]
    
    '''
    # make lists with random target and 
    distractor positions for reconfiguartion after a target was detected 
    '''
    for pos_list in range(number_of_search_targets):

        #shift=[0.25,0.5,0.75,1,1.25,1.5,1.75,2]
        shift= np.random.uniform(low=0.25, high=0.5, size=(50,))
        horiz = np.linspace(horizontal_start, horizontal_end, (visual_grid[0]))
        vertical = np.linspace(vertical_start, vertical_end, (visual_grid[1]))

        jitterX = random.choice(shift)
        jitterY = random.choice(shift)
        stim_grid_pos = [[h,v] for h in horiz for v in vertical]
        # allocate where the targets and distractors are placed. remaining positions are kept empty 
        target_positions = []   
        target_positions = random.sample(stim_grid_pos,k=number_of_search_targets)
        stim_grid_pos1 = []
        stim_grid_pos1 = [ele for ele in stim_grid_pos if ele not in target_positions] 
        distractor_positions = []
        distractor_positions = random.sample(stim_grid_pos1,k=number_of_distractors+number_of_search_targets)
        remaining_positions = []
        remaining_positions = [ele for ele in stim_grid_pos1 if ele not in distractor_positions] 
            
                    
        for ele in range(len(distractor_positions)):
            jitterX = random.choice(shift)
            jitterY = random.choice(shift)
            distractor_positions[ele][0] += jitterX
            distractor_positions[ele][1] += jitterY
    
        for ele in range(len(target_positions)):
            jitterX = random.choice(shift)
            jitterY = random.choice(shift)
            target_positions[ele][0] += jitterX
            target_positions[ele][1] += jitterY
            
        all_targ_pos.append(target_positions)
        all_dis_pos.append(distractor_positions)
        

      
  
    '''
    # make lists with random target and 
    distractor positions the display starts with 
    
    '''
    shift= np.random.uniform(low=0.25, high=0.5, size=(50,))
    horiz = np.linspace(horizontal_start, horizontal_end, (visual_grid[0]))
    vertical = np.linspace(vertical_start, vertical_end, (visual_grid[1]))

    jitterX = random.choice(shift)
    jitterY = random.choice(shift)
    
    stim_grid_pos = [[h,v] for h in horiz for v in vertical]

    
    # allocate where the targets and distractors are placed. remaining positions are kept empty 
    target_positions = []   
    target_positions = random.sample(stim_grid_pos,k=number_of_search_targets)
    stim_grid_pos1 = []
    stim_grid_pos1 = [ele for ele in stim_grid_pos if ele not in target_positions] 
    distractor_positions = []
    distractor_positions = random.sample(stim_grid_pos1,k=number_of_distractors)
    remaining_positions = []
    remaining_positions = [ele for ele in stim_grid_pos1 if ele not in distractor_positions] 

    
    for ele in range(len(distractor_positions)):
        jitterX = random.choice(shift)
        jitterY = random.choice(shift)
        distractor_positions[ele][0] += jitterX
        distractor_positions[ele][1] += jitterY
    
    for ele in range(len(target_positions)):
        jitterX = random.choice(shift)
        jitterY = random.choice(shift)
        target_positions[ele][0] += jitterX
        target_positions[ele][1] += jitterY
      
    all_stim = []
    target_rect =[]
    targ_stim = []
    reward_stim = []

    for i in range(0,len(target_positions)):
        
        
        target_rect.append(visual.Rect(win, 12,12,pos=(target_positions[i][0]*ppd,  target_positions[i][1]*ppd),lineColor='pink',
                                  fillColor='silver')) # or jitter the rect to the same amount as the target
        
        jittered_position = [ target_positions[i][0]+random.choice(jitter_offset_list), 
                              target_positions[i][1]+random.choice(jitter_offset_list)]
        
        if training:
            targ_stim.append(visual.ImageStim(win, pos=target_rect[i].pos,image=target_img_training[0],contrast=1, size=(stim_size,stim_size)))
               

        
        else:
            targ_stim.append(visual.ImageStim(win, pos=target_rect[i].pos,image=target_img[0],contrast=1, size=(stim_size,stim_size)))
               

    
    distractor_rect = []
    distractor_stim = []
    dist_color=['blue','green']
    
    for i in range(0,len(distractor_positions)):
        
        color=random.choice(dist_color)

        
        distractor_rect.append(visual.Rect(win, 12,12,pos=(distractor_positions[i][0]*ppd, distractor_positions[i][1]*ppd), lineColor='pink',
                                  fillColor='blue'))
        
        jittered_position = [distractor_positions[i][0]+random.choice(jitter_offset_list), 
                              distractor_positions[i][1]+random.choice(jitter_offset_list)]
        
        jittered_position_deg = [jittered_position[0]*ppd, jittered_position[1]*ppd]
        
        if training:
            distractor_stim.append(visual.ImageStim(win, pos=(distractor_positions[i][0]*ppd,distractor_positions[i][1]*ppd),
                                                image=random.choice(all_dist_training),contrast=1, size=(stim_size,stim_size)))
        

           
        else: 
            distractor_stim.append(visual.ImageStim(win, pos=(distractor_positions[i][0]*ppd,distractor_positions[i][1]*ppd),
                                                image=random.choice(all_dist),contrast=1, size=(stim_size,stim_size)))
        

                
    other_rect = []
    for i in range(0,len(remaining_positions)):

        other_rect.append(visual.Rect(win, 12,12,pos=(remaining_positions[i][0]*ppd,remaining_positions[i][1]*ppd), lineColor='pink',
                                  fillColor='yellow'))
    
    all_rects = target_rect+distractor_rect+other_rect
    all_stim = targ_stim+distractor_stim
    
    task_finished = visual.TextStim(win, text=u'Alle Zielreize wurden gefunden', 
                                        pos = (0,0), 
                                        color=stim_color, height=stim_height)

    
    # the mouse tracking 
    mouse = event.Mouse(win=win)
    mouse_pos = mouse.getPos()
    mouse_point.setPos(mouse_pos)
    new_mouse_rect_pos = [mouse_pos[0], mouse_pos[1]]# always X pix below
    mouse_rect.setPos(new_mouse_rect_pos)

    # initialize clocks 
    timer = core.CountdownTimer(0.1) # initiate the timer that will record how long participants looked at the target
    trial_timer=core.CountdownTimer()
    
    #set a time limit for fixation and blank
    
    maxSearch=frameRate*120#4620
    #maximal 
    search_dur=core.CountdownTimer(10800*fr)#3min max search time 
    
    trial_timer.add(maxSearch)

    
    # create boolean for trials that stop early (control condition)
    #early_break=False 
    random.shuffle(start_probability)
    start_prob=start_probability[0] 
    onsets['start_prob']=start_prob
    
    del start_probability[0]
    
    target_limit=random.randint(1,3)

    
    '''
    deactivate targets according to the start prob 
    
    '''
    
    if start_prob !=1:
        
        actual_num_of_targ=round(number_of_search_targets*start_prob)
        index=number_of_search_targets-actual_num_of_targ
        distractor_stim=distractor_stim+targ_stim[:index]
        del targ_stim[:index]
        del target_rect[:index]
        
    else:actual_num_of_targ=number_of_search_targets
    
    print ('### NEW TRIAL  ###')
    print ('                  ')
    print (f'number of targets the trial starts with: {len(targ_stim)}')
    
    '''
    # start stimulus presentation
    
    '''
    event.clearEvents()
    
    '''
    #FIXATION
    
    '''
    frameN = -1
    break_count=0
    
    while trial_timer.getTime() > maxSearch-frameRate*60: 
        frameN += 1
        fixation.draw()
        #if not joy:
        mouse.setVisible(False)   
        
        if not training:
            clock.text='Verbleibende Suchzeit: %.2f Minuten'%(search_countdown.getTime()/60.0)
            clock.draw()
            gain.text='Aktueller Gewinn: %.2f Euro'%(sum(reward_count)/100.0)
            gain.draw()
        win.flip()
        if frameN ==0:
            onsets['fix']=onset_clock.getTime()
            
        '''
        # quit search if time is up - search duration in patch leaving trials = nan! 
                    
        '''
        if onset_clock.getTime() - start == maxdur:
            
            onsets['end of search']=onset_clock.getTime()
            
            onsets['search_dur_patch_leaving']=np.nan
       
            break

    frameN = -1
    
    '''    
    #BLANK
    '''
    while trial_timer.getTime() <= maxSearch-frameRate*60  and  trial_timer.getTime() > maxSearch - 120*frameRate:
        frameN += 1
        mouse.setVisible(False)
        #show clock and earnings only in the mainexp
        if not training:
            clock.text='Verbleibende Suchzeit: %.2f Minuten'%(search_countdown.getTime()/60.0)
            clock.draw()
            gain.text='Aktueller Gewinn: %.2f Euro'%(sum(reward_count)/100.0)#10 cents now 
            gain.draw()
            
        #win.flip()
        win.update()
        if frameN ==0:
            onsets['blank']=onset_clock.getTime()
        
        '''
        # quit search if time is up - search duration in patch leaving trials = nan! 
                    
        '''
    
        if onset_clock.getTime() - start == maxdur:
            
            onsets['end of search']=onset_clock.getTime()
            onsets['search_dur_patch_leaving']=np.nan
       
            break

    frameN = -1  
      
    #recenter mouse with search onset
    mouse.setPos(newPos=(0,0))
    
    '''
    #SEARCH DISPLAY
    
    '''
    buttons, keys = mouse.getPressed(getTime=True)
    
    while search_dur.getTime() >0 and buttons == [0,0,0]:
        
        buttons, keys = mouse.getPressed(getTime=True)
        
        frameN+=1
        
        if frameN==0:
            
            beginn=time.time()
            onsetTime=onset_clock.getTime()
            onsets['search']=onsetTime
            
        
        '''
        # quit search if time is up - search duration in patch leaving trials = nan! 
                    
        '''    
        if onset_clock.getTime() - start >= maxdur:
            
            onsets['end of search']=onset_clock.getTime()
            onsets['search_dur_patch_leaving']=time.time()-beginn
            
            break

   
        [st_d.draw() for st_d in distractor_stim]
        [st_d.draw() for st_d in targ_stim]
        
        mouse_pos = mouse.getPos()
        new_mouse_rect_pos = [mouse_pos[0], mouse_pos[1]]
        mouse_rect.setPos(new_mouse_rect_pos)
        mouse_rect.draw()
        mouse_point.setPos(mouse_pos)
        
        mouse_rect.draw()
        mouse_point.draw()
            
            
        '''save mouse positions and time '''
        if not training:
        
            current_time = onset_clock.getTime()#time.strftime("%H:%M:%S", t)
            positions_mouse.append(mouse_pos)
            positions_time.append(current_time)

            
        '''
        # for normal search:
        set the position of the mouse to the mouse_rect.
        
        '''
        
        if not training:
            clock.text='Verbleibende Suchzeit: %.2f Minuten'%(search_countdown.getTime()/60.0)
            clock.draw()
            gain.text='Aktueller Gewinn: %.2f Euro'%(sum(reward_count)/100.0)
            gain.draw() 
            
            
        win.flip()

        keys = event.getKeys(keyList=['escape'])
        if 'escape' in keys:
                core.quit()
                win.close()
                
        
        if buttons == [1,0,0] or buttons == [0, 0, 1]:
            #all_ends.append(onset_clock.getTime())
            onsets['end of search']=onset_clock.getTime()
            onsets['search_dur_patch_leaving']=time.time() - beginn
            
            break 

        count=-1
 
        
        for n, i in enumerate(targ_stim):

            if i.contains(mouse_pos):
                positions_target.append(targ_stim[n])
                #target_activate=core.CountdownTimer(0.33)
                #reward_count+=5
                if not training:
                    reward_count.append(5)
                collection_count+=1
                break_count+=1
                

                print (f'reward_count={sum(reward_count)}')
                currTime=trial_timer.getTime() 
                detectionTime=onset_clock.getTime()
                onsets['responseTime'].append(detectionTime - onsetTime)
                onsets['detection'].append(detectionTime)
                timer.getTime()
                targ_stim[n].size=(stim_size,stim_size)
                
                #test boolean "Training" - if true, use different stimuli
                if training: 
                    targ_stim[n].setImage(target_img_training[0])
                else:
                    targ_stim[n].setImage(target_img[0])
                    
                core.wait(frameRate*48)
    
                targ_stim[n].size=(45,45)
                targ_stim[n].setImage(reward_image)
    
                [st_d.draw() for st_d in distractor_stim]
                [st_d.draw() for st_d in targ_stim]
    
                if not training:
                    clock.text='Verbleibende Suchzeit: %.2f Minuten'%(search_countdown.getTime()/60.0)
                    clock.draw()
                    
                    '''
                    # quit search if time is up - search duration in patch leaving trials = nan! 
                    
                    '''
                    if onset_clock.getTime() - start == maxdur:
                        
                        onsets['end of search ']=onset_clock.getTime()
                        onsets['search_dur_patch_leaving']=np.nan
                        
                        break
                    
                    gain.text='Aktueller Gewinn: %.2f Euro'%(sum(reward_count)/100.0)
                    gain.draw()
                    
                win.flip()
                onsets['reward_ons'].append(onset_clock.getTime())
                core.wait(frameRate*48)
                
                if early_break:
                    #print ('yes, early break')
                    onsets['trial type']='early break'
                    if break_count == target_limit:
                        all_ends.append(onset_clock.getTime())
                        onsets['end of search']=all_ends[0]
                        #task_finished.text='Die Suche ist vorzeitig beendet!'
                        search_time= all_ends[0] - onsetTime
                        #print ('full searchtime:',search_time)
                        onsets['searchTime']=search_time
                        win.flip()
                        core.wait(0.1)
                        break
                    
                reward_offset=trial_timer.getTime() 
                targ_stim[n].size=(stim_size,stim_size)

                if training:
                    
                     targ_stim[n].setImage(target_img_training[0])
                     
                     del targ_stim[n]
                     del target_rect[n]
                     
                else:
                    targ_stim[n].setImage(target_img[0])
                    
                    '''
                    deactivate targets that has been collected + additional number according to exp decay func 
                    
                    # A*e**((-n-1)/5) -> see Lottem et al. 
                    
                    - A = start probability 
                    
                    - e = eulers number 
                    
                    - n = number of performed pokes = I use collected rewards   
                    
                    - this gives the remaining target probability
                    
                    
                    '''

                    
                    potenz=(-(collection_count-1)/5)
                    
                    decay_func=start_prob*e**potenz
                    
                    #print (f'start probability = {start_prob}')
                    #print (f'remaining probability = {decay_func}')
                    
                    #calculate number of deleted and remaining targets 
                    remaining_targets=round(decay_func*actual_num_of_targ)#actual_num instead of number_of_search_targets # would only be ok if start prop = 1
                    deleted_targets=abs(len(targ_stim) - remaining_targets)
                    onsets['reward_prob_next_target'].append(decay_func)
                    
                    #print (f'current number of targets: {len(targ_stim)}')
                    #print (f'number of remaining targets in the next trial: {remaining_targets}')
    
                    if deleted_targets < len(targ_stim):
    
                        distractor_stim=distractor_stim+targ_stim[:deleted_targets]
                        
                        del targ_stim[:deleted_targets]
                        del target_rect[:deleted_targets]
                    
                    else:
    
                        distractor_stim=distractor_stim+targ_stim[:len(targ_stim)-1]
                            
                        del targ_stim[:len(targ_stim)-1]
                        del target_rect[:len(targ_stim)-1]
                    
    
                                    
                    print (f'number of to be deleted targets: {deleted_targets}')
                    print (f'number of remaining targets: {len(targ_stim)}')
                
                '''re-draw everything again after a target was collected '''
                
                #randomize target positions 
                random.shuffle(all_targ_pos[n])
                random.shuffle(all_dis_pos[n])
                
                #set new positions for all objects after target has been collected 
                stim_time=onset_clock.getTime()
                for ele in range(len(distractor_stim)):
                    distractor_stim[ele].pos=((all_dis_pos[n][ele][0]+random.choice(jitter_offset_list))*ppd,(all_dis_pos[n][ele][1]+random.choice(jitter_offset_list))*ppd)
                    distractor_stim[ele].draw()
                    all_stim_pos.append(distractor_stim[ele].pos)
                    all_stim_pos_time.append(onset_clock.getTime())
                   
    
                for ele in range(len(targ_stim)):
                    targ_stim[ele].pos=((all_targ_pos[n][ele][0]+random.choice(jitter_offset_list))*ppd,(all_targ_pos[n][ele][1]+random.choice(jitter_offset_list))*ppd)
                    positions_target.append(all_targ_pos[n])
                    targ_stim[ele].draw()
                    positions_target.append(targ_stim[ele])
                    
                if not training:
                    clock.text='Verbleibende Suchzeit: %.2f Minuten'%(search_countdown.getTime()/60.0)
                    clock.draw()
                    
                    '''
                    # quit search if time is up - search duration in patch leaving trials = nan! 
                    
                    '''
                    if onset_clock.getTime() - start >= maxdur:
                        
                        onsets['search_dur_patch_leaving']=np.nan
                        onsets['end of search']=onset_clock.getTime()
                        
                        break
                    
                    gain.text='Aktueller Gewinn: %.2f Euro'%(sum(reward_count)/100.0)
                    gain.draw()
                
                    
                event.clearEvents()
                
                win.flip()

        else:
            timer.reset(timerDuration)
            
        if early_break:
            #print ('yes, early break')
            onsets['trial type']='early break'
            if break_count == target_limit:
                all_ends.append(onset_clock.getTime())
                onsets['end of search']=all_ends[0]
                onsets['search_dur_patch_leaving']=time.time() - beginn
                #task_finished.text='Die Suche ist vorzeitig beendet!'
                search_time= all_ends[0] - onsetTime
                #print ('full searchtime:',search_time)
                onsets['searchTime']=search_time
                win.flip()
                core.wait(0.1)
                break

        if len(targ_stim) == 0:
            condi=False
            task_finished.draw()
            all_ends.append(onset_clock.getTime())
            end=onset_clock.getTime()
            onsets['end of search']=all_ends[0]
            onsets['searchTime']=end - beginn
            task_finished.draw()
            break
        else:
            condi=True
            
    
    if training:    
        if trial ==2:
            feedback.text=u'Das Training ist nun beendet. Sage der Testleitung, wenn du bereit bist, zu starten.'
            feedback.draw()
            win.flip()
            keypress = event.waitKeys(keyList=['space', 'escape'])
            if 'escape' in keypress:
                core.quit()
                win.close()
                
    else:
        '''save onsets, search times, and rewards after training only '''
        onsets['reward']=len(onsets['detection'])
        df=collect_responses(onsets['fix'],
                                        onsets['blank'],
                                        onsets['search'],
                                        onsets['detection'],
                                        onsets['trial type'],
                                        onsets['responseTime'],
                                        onsets['searchTime'],
                                        onsets['reward_ons'],
                                        onsets['search_dur_patch_leaving'],
                                        onsets['end of search'],
                                        onsets['reward'],
                                        onsets['reward_prob_next_target'],
                                        onsets['start_prob']
                                        )
        
        tsv_file=subs_path /f"beh-data_sub-0{sub}_block-0{block}.tsv"
        if not os.path.isfile(tsv_file):
            df.to_csv(subs_path/f"beh-data_sub-0{sub}_block-0{block}.tsv", sep='\t', index=False)
        else:
             with open(tsv_file,'a') as f:
                df.to_csv(f, header=False,index=False,sep='\t')

    return  None
                              



        
def run_experiment(n_training,max_dur):
    
    ons=[]
    durs=[]
    events=[]
    block_column=[]
    json_list=[]
    #breaks=
    sub_info()
    #fullscr=True
    if fullscr:
        win = visual.Window([width,height],monitor="testMonitor", screen=1,units="pix", color=bg_color, fullscr=True)
    
    else:
        win = visual.Window([width,height],monitor="testMonitor", units="pix", color=bg_color,fullscr=False,screen=1)
    
    show_intro(win)

    
    if n_training >0:
        early_break =False
        onset_clock = core.Clock()
        onset_clock.reset() 
        training=True
        search_countdown=core.CountdownTimer(max_dur)
        start=onset_clock.getTime()
        
        for block in range(0,1):
            
            mouse_tracking={}
            mouse_tracking['positions_mouse']=[] 
            mouse_tracking['time_of_mp']=[] 
            
            all_stim_pos={}
            all_stim_pos['time']=[]
            all_stim_pos['pos']=[]
            
            targ_stim_pos={}
            targ_stim_pos['targ_pos']=[]
            targ_stim_pos['targ_pos_time']=[]

                
            for tr in range(n_training):
                    run_trial(win,
                              block,
                              sub,
                              training,
                              tr,early_break,
                              onset_clock,
                              search_countdown,
                              start,
                              max_dur,
                              reward_count,
                              start_probability,
                              mouse_tracking['positions_mouse'],
                              mouse_tracking['time_of_mp'],
                              json_list,
                              ons,
                              durs,
                              events,
                              block_column,
                              all_stim_pos['pos'],
                              all_stim_pos['time'],
                              targ_stim_pos['targ_pos']
                              )
        training=False
        
    else:
        training=False

    count=0
    block_count=0
    count+=1
    
    if count==1: 
        show_intro2(win,n_training)

    n=1

    for block in range(n_blocks):


        '''
        use a dict to save mouse tracking data (time and positons)
        
        lists are huge so append after each trial 
        but write to file at the end of the exp. 
        
        '''
        mouse_tracking={}
        mouse_tracking['positions_mouse']=[] 
        mouse_tracking['time_of_mp']=[] 
        
        all_stim_pos={}
        all_stim_pos['time']=[]
        all_stim_pos['pos']=[]
        
        targ_stim_pos={}
        targ_stim_pos['targ_pos']=[]
        targ_stim_pos['targ_pos_time']=[]
        
        block_count+=1
        onset_clock = core.Clock()
        onset_clock.reset() 
        early_break = False 
        


        
        if block > 0:
            #win.flip()
            #core.wait(2)# give it some time to store all the data after a block 
     
                   
            do_break(win,f'Kurze Pause? Es folgen noch {(n_blocks+1)-block_count} Durchgänge mit jeweils 10 Minuten Zeit für die Suche. Teile der Testleitung mit, wenn du bereit bist, das Experiment fortzusetzen.')
            #keypress = event.waitKeys(keyList=['t'])
            

        keypress = event.waitKeys(keyList=['t'])
            
        if keypress[0] == 't':
            


            start=onset_clock.getTime()
            search_countdown=core.CountdownTimer(max_dur)
            while search_countdown.getTime() > 0:
                
                run_trial(win,
                          block,
                          sub,
                          training,
                          n,early_break,
                          onset_clock,
                          search_countdown,
                          start,
                          max_dur,
                          reward_count,
                          start_probability,
                          mouse_tracking['positions_mouse'],
                          mouse_tracking['time_of_mp'],
                          json_list,
                          ons,
                          durs,
                          events,
                          block_column,
                          all_stim_pos['pos'],
                          all_stim_pos['time'],
                          targ_stim_pos['targ_pos'],
                          )
                
                if onset_clock.getTime() - start == max_dur:
                    break
                
            win.flip()
            core.wait(2)# give it some time to store all the data after a block 
     

            '''save mouse tracking at the end of each block'''
        
            #mouse_file=subs_path/f"mouse-tracking-sub{sub}-block{block}.csv"
            #data=pd.DataFrame(list(zip(mouse_tracking['positions_mouse'],mouse_tracking['time_of_mp'])),columns=['location', 'time'])
            
            #if not os.path.isfile(mouse_file):
                #data.to_csv(subs_path /f"mouse-tracking-sub{sub}-block{block}.csv",
                            #sep=',',index=False,header=True)
            
                
            #else:
                #with open(mouse_file, 'a') as f:
                    #data.to_csv(f, header=False,index=False,sep=',')
                    
                    
            ''' save obj locations '''
            
            #stim_loc_file=subs_path/f"obj-location-sub{sub}-block{block}.csv"
            #data=pd.DataFrame(list(zip(all_stim_pos['pos'],all_stim_pos['time'])),columns=['location', 'time'])
            
            #if not os.path.isfile(stim_loc_file):
                #data.to_csv(subs_path/f"obj-location-sub{sub}-block{block}.csv",
                            #sep=',',index=False,header=True)
                
            #else:
                #with open(stim_loc_file, 'a') as f:
                    #data.to_csv(f, header=False,index=False,sep=',')
      
                



    win.flip()
    core.wait(2)

    quit_task(win,
              sub,
              n_blocks,
              date,
              subs_path,reward_count)

    return None


'''
# =============================================================================
# 
# run the experiment via function
# 
# run_experiment(n_training, maximal duration,mouse_tracking)
# 
# =============================================================================
'''

run_experiment(2,maxdur)
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
