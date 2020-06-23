# Program name: main.py
# Purpose: For semantic dual task of Ominoise
# Author: Zhihan Yang

# Program description:
# In this experiment, each participant will go through four list of words
# and decide whether each word is a noun. Noun decisions and their
# response times are both recorded. Along with each list, a different
# background noise is played.

from __future__ import absolute_import, division  # must be placed as the first line of code

# >>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>
# TABLE OF CONTENT
# 1. SETUP ENVIRONMENT
# 2. LOAD VARIABLES
# 3. RUN EXPERIMENT
# 4. SAVE DATA
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>

# ============================
# ============================
# SECTION 1: SETUP ENVIRONMENT
# - OPTIONS
# - IMPORTS
# - RECORD PARTICIPANT INFO
# - INSTANTIATE WINDOW
# - INSTANTIATE KEYBOARD, CLOCK, AND TEXT DISPLAY
# ============================
# ============================

# ========== OPTIONS =========

debug_mode_on = True  # in debug mode, the interstimuli durations are shorter

# ========== IMPORTS =========

from psychopy import gui, visual, core
from psychopy.hardware import keyboard

import os
import sys
import time
import json
import numpy as np
import pandas as pd

# ========== RECORD PARTICIPANT INFO =========

expName = "Semantic Dual Task"
expInfo = {'participant_id': ''}

dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)  # open a window that asks for participant ID
if dlg.OK == False:
    core.quit()  # user pressed cancel

# ========== INSTANTIATE WINDOW =========

win = visual.Window(
    size=(1024, 768), fullscr=True, screen=0,
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True,
    units='height')

expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# ========== INSTANTIATE KEYBOARD, CLOCK, AND TEXT DISPLAY ==========

defaultKeyboard = keyboard.Keyboard()
count_down_clock = core.CountdownTimer()
text_on_screen = visual.TextStim(win=win, name='instructions_text',
    text="",
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    languageStyle='LTR',
    depth=0.0);

# ============================
# ============================
# SECTION 2: LOAD VARIABLES
# - LOAD INSTRUCTIONS
# - LOAD NOISE FILES
# - LOAD INTERSTIMULI INTERVALS
# - LOAD WORD LISTS
# - LOAD COUNTER-BALANCING STUFF
# ============================
# ============================

# ========== LOAD INSTRUCTIONS ==========

with open('instructions.json', 'r', encoding='utf-8') as json_f:
    instructions = json.load(json_f)

# ========== LOAD NOISE FILES ==========

# TODO: no noise files available yet
noise_files = [1, 2, 3, 4]

# ========== LOAD WORD LISTS ==========
# load 4 word lists into a list, i.e. [list1, list2, list3, list4]

word_lists_df = pd.read_csv('sdt_word_lists.csv').iloc[:,:4]  # only the first 4 columns are valid, since there are 4 word lists, one per column

word_lists = []  # storing word lists in a list is more convenient for indexing
for col_idx in range(len(word_lists_df.columns)):
    word_lists.append(list(word_lists_df.iloc[:,col_idx]))
    
# ========== LOAD INTERSTIMULI INTERVALS ==========

# notes on dummy word
# Since we want an interstimuli interval between the start
# of each list to the presentation of the first word of that
# list, we need to first present a dummy work (empty string).

num_word_lists = 4
num_words_per_list = 75 + 1  # plus 1 for a dummy word
num_words = num_word_lists * num_words_per_list

if debug_mode_on:
    # use shorter interstimuli interval to speed up debugging
    interstim_interval_lower = 10
    interstim_interval_upper = 20
    interstim_interval_step  = 1
else: 
    interstim_interval_lower = 2500
    interstim_interval_upper = 3500
    interstim_interval_step  = 250

def get_interstim_intervals(how_many):
    choices = np.arange(
        start=interstim_interval_lower, 
        stop=interstim_interval_upper + 1, 
        step=interstim_interval_step
    )
    return np.random.choice(choices, size=how_many)  # sample without replacement

interstim_intervals = get_interstim_intervals(how_many=num_words)

# ========== LOAD COUNTER-BALANCING STUFF ==========

with open('tape.json', 'r') as json_f:
    noises_permutation_idx, wlists_permutation_idx = json.load(json_f)[str(expInfo['participant_id'])].split('/')

with open('integer_2_noise_order.json', 'r') as json_f:
    noise_order = json.load(json_f)[noises_permutation_idx]
    
with open('letter_2_word_list_order.json', 'r') as json_f:
    wlist_order = json.load(json_f)[wlists_permutation_idx]

# ============================
# ============================
# SECTION 3: RUN EXPERIMENT
# - DISPLAY INSTRUCTIONS
# - RUN EXPERIMENT LOOP
# ============================
# ============================

num_rounds = 4
noun_resps = []
reaction_times = []

# ========== DISPLAY INSTRUCTIONS ==========

def display_until_space(txt):
    
    if txt == "N/A":
        return
    
    text_on_screen.setText(txt)
    text_on_screen.height = 0.03
    text_on_screen.setAutoDraw(True)
    win.flip()

    while True:
        if defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        elif defaultKeyboard.getKeys(keyList=["space"]):
            break

    text_on_screen.setAutoDraw(False)
    win.flip()

display_until_space(instructions["welcome"])
display_until_space(instructions["before_practice"])

# ========== RUN EXPERIMENT LOOP ==========
 
resp_timer = core.Clock()
    
for i in range(num_rounds):
    
    display_until_space(instructions[f"before_block_{i+1}"])

    # specify the word list and noise file to be presented this round
    noise_idx, wlist_idx = noise_order[i], wlist_order[i]
    noise_file, word_list = noise_files[noise_idx], word_lists[wlist_idx]
    
    # TODO: add real noise files here
    print('Playing noise {}'.format(noise_file))

    # loop over the word list one word at a time
    # the earliest word in each list is a dummy word, because we want an interstimuli interval before the first presented word
    for j, word in enumerate([''] + word_list):
        
        if word == '':  # in case the word is a dummy word, we don't want to record any data about it
            is_dummy = True
        else:
            is_dummy = False
        
        # present the word and record the start time
        
        text_on_screen.setText(word)
        text_on_screen.setAutoDraw(True)
        # resp_start_time = win.getFutureFlipTime(clock=resp_timer)  returns negative time elapsed sometimes; therefore not used
        win.flip()
        resp_start_time = time.time()
        
        # By definition, an interstimuli interval describes the duration between
        # the current word and the upcoming word.
        
        interstim_interval = interstim_intervals[i * num_words_per_list + j]
        noun_button_pressed = 0
        
        count_down_clock.reset(interstim_interval / 1000)  # countdown starts from here
        while count_down_clock.getTime() > 0:
           
            if defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            elif defaultKeyboard.getKeys(keyList=["space"]) and (not noun_button_pressed):  # the 2nd condition prevents logging the noun button response twice for one word
                # TODO: modify this if-statement for button box
                noun_button_pressed = 1
                resp_end_time = time.time() #resp_timer.getTime()
                
        # stop presenting the word
                  
        text_on_screen.setAutoDraw(False) 
        win.flip()
        
        ##### record data #####
        
        if not is_dummy:
            
            noun_resps.append(noun_button_pressed)
            
            if noun_button_pressed:  # ensure that resp_end_time has been updated
                reaction_times.append(resp_end_time - resp_start_time)
            else:
                reaction_times.append(-1)  # if the noun button was not pressed, an impossible reaction time is appended
            
            ##### debug #####
            
            if debug_mode_on:
                print(noun_resps[-1])
                print(reaction_times[-1])

    display_until_space(instructions[f"after_block_{i+1}"])

# ============================
# ============================
# SECTION 4: SAVE DATA
# ============================
# ============================

##### save data first #####

_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)
    
filename = _thisDir + os.sep + u'data/%s' % (expInfo['participant_id']) + '.csv'

noun_resps, reaction_times = map(np.array, [noun_resps, reaction_times])
array = np.hstack([noun_resps.reshape(-1, 1), reaction_times.reshape(-1, 1)])
df = pd.DataFrame(array)
df.columns = ['resp', 'reaction_time']
df.to_csv(filename)

##### display thank you message #####

display_until_space(instructions['after_experiment'])
    
# Flip one final time so any remaining win.callOnFlip()
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

win.close()
core.quit()
