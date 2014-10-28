"""
Interactive Programming in Python
Week 3 Project - Stopwatch Game
Author: David Schonberger
Created: 10/7/2014
Last Modified: 10/7/2014
url: http://www.codeskulptor.org/#user38_MkRvplqRBrMZaxX.py
"""

import simplegui

#global variables
tenths_count = 0
stop_count = 0 #number of stops made (while stopwatch running)
successes = 0 #number of times stopped on whole second, i.e. tenths == 0
is_stopwatch_running = False

##################
# Helper functions
##################
def format(t):
    """
    Converts time in tenths of seconds 
    into formatted string A:BC.D.
    Works correctly up to 59:59.9
    """
    t = t % 36000 #roll over to 0:00.0 at 1 hour mark
    tenths_digit = t % 10
    seconds_digit = (t // 10) % 10
    tens_digit = (t // 100) % 6
    minutes_digit = t // 600
    return str(minutes_digit) + ":" + str(tens_digit)+str(seconds_digit) + "." + str(tenths_digit)

def update_score():
    """
    Increments stop_count unconditionally
    Increment stop_count iff stopwatch was 
    initially running and 'Stop' button was
    pushed on a whole number of seconds
    """
    global stop_count, successes
    stop_count += 1
    if tenths_count % 10 == 0:
        successes += 1

######################################################
# Event handlers for buttons; "Start", "Stop", "Reset"
######################################################
def start_button_handler():
    global is_stopwatch_running
    timer.start()
    is_stopwatch_running = True

def stop_button_handler():
    global is_stopwatch_running
    timer.stop()
    #update score
    if is_stopwatch_running: 
        update_score()
        
    is_stopwatch_running = False

def reset_button_handler():
    global tenths_count, stop_count, successes
    timer.stop()
    tenths_count = 0
    stop_count = 0
    successes = 0

###############################################
# Event handler for timer with 0.1 sec interval
###############################################
def tick():
    global tenths_count
    tenths_count += 1

##############
# Draw handler
##############
def draw(canvas):
    """
    Draw formatted stopwatch A:BC.D
    Draw game score 'successes / attempts'
    Draw success percent
    """
    canvas.draw_text(format(tenths_count), (105,170) , 36,  "White")
    
    game_scoring = str(successes) + "/" + str(stop_count)
    if successes == 0:
        success_pct = 0
    else:
        success_pct = 1.0 *  successes / stop_count
    success_pct_str  = str(round(success_pct * 100.0, 1))
    
    canvas.draw_text(game_scoring, (250,20), 24, "Red")
    canvas.draw_text("(Success %: " + success_pct_str + ")", (120,60), 24, "Blue")
    

##############
# Create frame
##############
frame = simplegui.create_frame("Stopwatch Game" , 300 , 300)

#########################
# Register event handlers
#########################
timer = simplegui.create_timer(100, tick) #0.1 sec per tick
frame.set_draw_handler(draw)
frame.add_button("Start" , start_button_handler)
frame.add_button("Stop" , stop_button_handler)
frame.add_button("Reset" , reset_button_handler)

#############
# Start frame
#############
frame.start()

"""print format(0)
print format(1)
print format(11)
print format(111)
print format(301)
print format(599)
print format(600)
print format(601)
print format(1199)
print format(1200)
print format(1201)
print format(1247)
print format(1547)
print format(2999)
print format(321)
print format(613)
"""