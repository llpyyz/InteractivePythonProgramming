#Interactive Python - Week 5

################################
##### MouseInput MoreLists #####
################################


### Lec 1 - Mouse Input ###

#imports
import simplegui
import math

#init globals
WIDTH = 450
HEIGHT = 300
BALL_RADIUS = 15

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_color = "Red"

#helper
def distance(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2

#event handler for mouse click
def click(pos):
    global ball_pos, ball_color
    
    if distance(ball_pos, pos) <= BALL_RADIUS ** 2:
        ball_color = "Green"
    else:
        ball_color = "Red"
        
        
    #copy of tuple pos, to avoid possible reference issue later 
    #should we want to modify ball_pos.
    ball_pos = list(pos) 

def draw(canvas):
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "Black", ball_color)
    

#create frame
frame = simplegui.create_frame("Mouse selection", WIDTH, HEIGHT)
frame.set_canvas_background("White")

#register handlers
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

#start frame
frame.start()


############################
### Lec 2 - List Methods ###
############################

#simple task list

import simplegui

tasks = []

#handler for button
def clear():
    while len(tasks) > 0:
        tasks.pop()

#handler for new task
def new(task):
    tasks.append(task)
    
#handler for remove number
def remove_num(tasknum):
    if int(tasknum) >= 1 and int(tasknum) <= len(tasks):
        tasks.pop(int(tasknum) - 1)


#handler for remove name
def remove_name(taskname):
    if taskname in tasks:
        tasks.remove(taskname)
    
#draw handler
def draw(canvas):
    for count in range(0, len(tasks)):
        canvas.draw_text(str(count + 1) + ". " + tasks[count], (20, 30*(count + 1)), 24, "Red")
    
#create frame, register handlers
frame = simplegui.create_frame("Task List", 600, 400)
frame.add_input("New Task:", new, 200)
frame.add_input("Remove task number:", remove_num, 200)
frame.add_input("Remove task:", remove_name, 200)
frame.add_button("Clear All", clear)
frame.set_draw_handler(draw)

#start frame
frame.start()


#############################
### Lec 3 - List Examples ###
#############################

##############################################
#Add multiple balls. click on an existing ball
#and it turns green
##############################################

#imports
import simplegui
import math

#init globals
WIDTH = 450
HEIGHT = 300
BALL_RADIUS = 15

#ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_list = []
ball_color = "Red"

#helper
def distance(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2

#event handler for mouse click
def click(pos):
    changed = False
    for ball in ball_list:
        if distance([ball[0], ball[1]], pos) <= BALL_RADIUS ** 2:
            ball[2] = "Green"
            changed = True

    if not changed:
        ball_list.append([pos[0], pos[1], "Red"])

def draw(canvas):
    for ball in ball_list:
        canvas.draw_circle([ball[0], ball[1]], BALL_RADIUS, 1, "Black", ball[2])
    

#create frame
frame = simplegui.create_frame("Mouse selection", WIDTH, HEIGHT)
frame.set_canvas_background("White")

#register handlers
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

#start frame
frame.start()

###################################
#Remove a ball when you click on it
###################################

#imports
import simplegui
import math

#init globals
WIDTH = 450
HEIGHT = 300
BALL_RADIUS = 15

#ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_list = []
ball_color = "Red"

#helper
def distance(p, q):
    return (p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2

#event handler for mouse click
def click(pos):
    remove = []
    for ball in ball_list:
        if distance(ball, pos) <= BALL_RADIUS ** 2:
            remove.append(ball)

    if remove == []:
        ball_list.append(pos)
    else:
        for ball in remove:
            ball_list.pop(ball_list.index(ball))
            
def draw(canvas):
    for ball in ball_list:
        canvas.draw_circle([ball[0], ball[1]], BALL_RADIUS, 1, "Black", ball_color)
    

#create frame
frame = simplegui.create_frame("Mouse selection", WIDTH, HEIGHT)
frame.set_canvas_background("White")

#register handlers
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

#start frame
frame.start()


#########################
### Lec 4 - Iteration ###
#########################

#iterating over lists

#count of odds in list
def count_odd(numbers):
    odd = 0
    for num in numbers:
        if num % 2 == 1:
            odd += 1
    return odd

#check if any odds in list
def check_odd(numbers):
    for num in numbers:
        if num % 2 == 1:
            return True
			
def remove_odd(numbers):
    remove = []
    for num in numbers:
        if num % 2 == 1:
            remove.append(num)
            
    for num in remove:
        numbers.remove(num)
		
def remove_last_odd(numbers):
    has_odd = False
    curr_idx = 0
    odd_idx = -1
    for num in numbers:
        if num % 2 == 1:
            has_odd = True
            odd_idx = curr_idx
        curr_idx += 1
        
    if has_odd:
        numbers.pop(odd_idx)

def run():
    numbers= [1, 7, 2, 34, 8, 7, 2, 5, 14, 22, 93, 48, 76, 15, 7]
    print numbers
    print
    print "This list contains", count_odd(numbers), "odds"
    print
    print "Does", numbers ,"contain any odss?", check_odd(numbers)
    print
    remove_odd(numbers)
    print "After removing all odss via remove_odd() the list is", numbers
    print
    numbers= [1, 7, 2, 34, 8, 7, 2, 5, 14, 22, 93, 48, 76, 15, 7]
    print "After removing all odss via remove_odd2() the list is", remove_odd2(numbers)
    print
    
    numbers= [1, 7, 2, 34, 8, 7, 2, 5, 14, 22, 93, 48, 76, 15, 7]
    remove_last_odd(numbers)
    print "After removing last odd from original, list is", numbers
    print
    
run()


####################################
#####  Dictionaries And Images #####
####################################

############################
### Lec 1 - Dictionaries ###
############################

# Cipher

import simplegui

CIPHER = {'a': 'x', 'b' : 'c', 'c' : 'r', 'd' : 'm', 'e': 'l'}

message = ""

#encode button
def encode():
    emsg = ""
    for ch in message:
        emsg += CIPHER[ch]
    print message, "encodes to", emsg

#decode button
def decode():
    dmsg = ""
    for ch in message:
        for key in CIPHER.keys():
            if ch == CIPHER[key]:
                dmsg += key
    print message, "decodes to", dmsg
    

#update message input
def newmsg(msg):
    global message
    message = msg
    label.set_text(msg)
    
    
#create frame, assign callbacks to handlers
frame = simplegui.create_frame("Cipher", 2, 200, 200)
frame.add_input("Message:", newmsg,  200)
label = frame.add_label("", 200)
frame.add_button("Encode", encode)
frame.add_button("Decode", decode)

#start frame
frame.start()


#version 2 of cipher, using random substitution cipher

# Cipher

import simplegui
import random

CIPHER = {}
LETTERS = "abcdefghijklmnopqrstuvwxyz"

message = ""

def init():
    letter_list = list(LETTERS)
    random.shuffle(letter_list)
    for ch in LETTERS:
        CIPHER[ch] = letter_list.pop()

#encode button
def encode():
    emsg = ""
    for ch in message:
        emsg += CIPHER[ch]
    print message, "encodes to", emsg

#decode button
def decode():
    dmsg = ""
    for ch in message:
        for key in CIPHER.keys():
            if ch == CIPHER[key]:
                dmsg += key
    print message, "decodes to", dmsg
    

#update message input
def newmsg(msg):
    global message
    message = msg
    label.set_text(msg)
    
    
#create frame, assign callbacks to handlers
frame = simplegui.create_frame("Cipher", 2, 200, 200)
frame.add_input("Message:", newmsg,  200)
label = frame.add_label("", 200)
frame.add_button("Encode", encode)
frame.add_button("Decode", decode)
init()

#start frame
frame.start()


######################
### Lec 2 - Images ###
######################

#Dragable magnifier on a map

import simplegui

#1521 x 1818 pix map of native American language
# source - Gutenberg project

image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/gutenberg.jpg")

#Image dimensions
MAP_WIDTH = 1521
MAP_HEIGHT = 1818

#scale factor
SCALE = 3

#canvas size
CAN_WIDTH = MAP_WIDTH // SCALE
CAN_HEIGHT = MAP_HEIGHT // SCALE

#size of magnifier pane and initial center
MAG_SIZE = 120
mag_pos = [CAN_WIDTH // 2 , CAN_HEIGHT // 2]

#handlers
#move magnifier to clicked position
def click(pos):
    global mag_pos
    mag_pos = list(pos)
    
#draw map and magnified region
def draw(canvas):
    #draw map
    canvas.draw_image(image, 
                      [MAP_WIDTH // 2, MAP_HEIGHT // 2], [MAP_WIDTH, MAP_HEIGHT],
                      [CAN_WIDTH // 2, CAN_HEIGHT // 2] , [CAN_WIDTH, CAN_HEIGHT])
    
    #draw magnifier
    map_center = [SCALE * mag_pos[0], SCALE * mag_pos[1]]
    map_rectangle = [MAG_SIZE, MAG_SIZE]
    mag_center = mag_pos
    mag_rectangle = [MAG_SIZE, MAG_SIZE]
    canvas.draw_image(image, map_center, map_rectangle, mag_center, mag_rectangle)
    
#create frame
frame = simplegui.create_frame("Map magnifier" , CAN_WIDTH, CAN_HEIGHT)

#register handlers
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)

#start frame
frame.start()



#####################################
### Lec 3 - Visualizing Iteration ###
#####################################

#
#Example 1
#

#iteration
def square_list1(numbers):
    """
    Input: numbers, a list
    
    Output: result, a list of the squares of numbers
    
    Done via standard interation
    """
    result = []
    for n in numbers:
        result.append(n ** 2)
    return result

#list comprehension - mapping
def square_list2(numbers):
    """
    Input: numbers, a list
    
    Output: result, a list of the squares of numbers
    
    Done via list comprehsnsion
    """
    return [n ** 2 for n in numbers]

print square_list1([4, 5, -2])


#
#Example 2
#
def is_in_range(ball):
    """
    Input: ball, a tuple of two values
    
    Output: True iff both coords of ball are in [0,100]
    """
    return ball[0] >= 0 and ball[0] <= 100 and ball[1] >= 0 and ball[1] <= 100

def balls_in_range1(balls):
    """
    Input: balls, a list of ball 2-tuples
    
    Output: result, a list of balls in range
    
    Calls: is_in_range
    """
    result = []
    for ball in balls:
        if is_in_range(ball):
            result.append(ball)
    return result

#list comprehension - filtering
def balls_in_range2(balls):
    return [ball for ball in balls if is_in_range(ball)]
	
	
balls = [(-5, 40), (30, 20), (70, 140), (60, 50)]
print balls_in_range1(balls)
print balls_in_range2(balls)




################################
### Lec 4 - Programming Tips ###
################################

#about dictionaries

d = {0 : '0', 'one' : '1', 2 : 'two', 4 : 4 == 5, 1.5 : True, '1.5': 'True', True: [['f']]}

d[(1,2)] = (1,2) #works because tuple is immutable so can be a key

#d[[3,4]] = [3,4] #<- list is mutable hence not a hashable type so cant be key

#d[{}] = {} #dict is mutable hence hence not a hashable type so cant be key

d[(3,4)] = {} #however, dict can be a val

for k, v in d.items():
    print k," - " , v



######################
### Lec 5 - Memory ###
######################

import simplegui

#handlers
def new_game():
    global state
    state = 0
    
def buttonclick():
    global state
    if state == 0:
        state = 1
    elif state == 1:
        state = 2
    else:
        state = 1
        
        
def draw(canvas):
    canvas.draw_text(str(state) + " card exposed", [30, 62], 24, "White")
 
#create frame, add buttons
frame = simplegui.create_frame("Memory states", 200, 100)
frame.add_button("Restart", new_game, 200)
frame.add_button("Sim mouse click", buttonclick, 200)

#register handler
frame.set_draw_handler(draw)

#start it up
new_game()
frame.start()



