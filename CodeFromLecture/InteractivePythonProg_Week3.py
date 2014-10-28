#Interactive Python - Week 3

###############
###############
#Drawing Canvas
###############
###############

###########################
#Lec 1 - Canvas and Drawing
###########################

#example of drawing on canvas

import simplegui

#define draw handler
def draw(canvas):
    canvas.draw_text("Hello!", [100,100], 24, "White")
	
	#draws circle in lower left corner of text
	canvas.draw_circle([100,100], 2 , 2 , "Red") 

#create frame
frame = simplegui.create_frame("Drawing Test" , 300 , 200)

#register draw handler
frame.set_draw_handler(draw)

#start frame
frame.start()

##########################
#Lec 2 - String Processing
##########################

### String Porcessing ###

#String literals
s1 = "That's not funny!"
s2 = "All you can eat churros"
s3 = "t-minus 5 minutes"
print s1, s2 
print s3

#Combining Strings
s4 = "Warren" + ' and ' + "Rixner" + ' are nuts!'
print s4

a = ' and'
s5 = "hello" + a +  ' goodbye'
print s5


#Characters and Slices
print s1[0] #first char
print s1[-1] #last char
print "len of'", s1, "'is", len(s1)

x = 9
print "the first", x, "chars of s1 are",s1[0:x]
print s1[0:5] + s1[5:]

#Converting Strings
s6 = int(100)
print s6
i1 = int(s6)
print i1, "*3 = ", i1 * 3 

print "#####"

def convert_units(val, name):
    res = str(val) + " " + name
    if val > 1 :
        res += "s"
    return res
    
#convert xx.yy into xx dollars and yy cents
def convert(val):
    dollars = int(val)
    cents = round(100 * (val - dollars))
    
    dollars_string = convert_units(dollars, "dollar")
    cents_string = convert_units(cents, "cent")
    
    if dollars == 0 and cents == 0:
        return "Broke!"
    elif dollars == 0:
        return cents_string
    elif cents == 0:
        return dollars_string
    else:
        return dollars_string + " and " + cents_string

print convert(11.23)
print convert(11.20)
print convert(1.12)
print convert(12.01)
print convert(1.01)
print convert(0.01)
print convert(1.00)
print convert(0)
print convert(-1.40)
print convert(12.555555)



############################
#Lec 3 - Interactive Drawing
############################
#Building off of Rixner's interactive program from lec 2:

# interactive app to convert float into dollar and cents
import simplegui

#define global const
value = 3.12

def convert_units(val, name):
    res = str(val) + " " + name
    if val > 1 :
        res += "s"
    return res
    
#convert xx.yy into xx dollars and yy cents
def convert(val):
    dollars = int(val)
    cents = int(round(100 * (val - dollars)))
    
    dollars_string = convert_units(dollars, "dollar")
    cents_string = convert_units(cents, "cent")
    
    if dollars == 0 and cents == 0:
        return "Broke!"
    elif dollars == 0:
        return cents_string
    elif cents == 0:
        return dollars_string
    else:
        return dollars_string + " and " + cents_string


#define draw handler
def draw(canvas):
    canvas.draw_text(convert(value), (50,100), 24, "White")


#define input field handler
def input_handler(text):
    global value
    value = float(text)
    


#create frame
frame = simplegui.create_frame("Converter",300,200)

#register event handlers
frame.set_draw_handler(draw)
frame.add_input("Enter value", input_handler,100)

#start frame
frame.start()


#######
#######
#Timers
#######
#######

###############
#Lec 1 - Timers
###############

#Simple screensaver program

import simplegui
import random

#global state
message = "Python rocks!"
position = [50 , 50]
width = 500
height = 500
interval = 2000 #milliseconds
color = "Red"

#text box handler
def update(text):
    global message
    message = text

def choose_rand_color():
    global color
    #set color randomly to red, green or blue
    rnd = random.randrange(0,3)
    if rnd == 0:
        color = "Red"
    elif rnd == 1:
        color = "Blue"
    else:
        color = "Green"
        
#timer handler
def tick():
    global position, color
    x = random.randrange(0, width)
    y = random.randrange(0, height)
    position[0] = x
    position[1] = y
    choose_rand_color()
    
#canvas draw handler 
def draw(canvas):
    canvas.draw_text(message, position, 36, color)
    
#create frame
frame = simplegui.create_frame("Screensaver", width , height)

#register handlers
text = frame.add_input("Message: ", update, 150)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(interval , tick)

#start frame, timer
frame.start()
timer.start()



#######################################
#Lec 2 - Visualizing Drawing and Timers
#######################################

#Can use viz mode to control drawing, timer, etc and step through
#Good for debugging

#########################
#Lec 3 - Programming Tips
#########################

import simplegui

size = 10
radius = 10

#define handlers

def incr_button_handler():
    """
    Increment size
    """
    global size
    size += 1
    label.set_text("Desired radius:" + str(size))
    

def decr_button_handler():
    """
    Decrement size
    """
    global size
    if size > 1:
        size -= 1
    label.set_text("Desired radius:" + str(size))

def change_circle_handler():
    """
    Change circle radius
    """
    global radius
    radius = size
    radius_label.set_text("Curr radius:" + str(radius))
    
def draw_handler(canvas):
    canvas.draw_circle((100 , 100) , radius , 5 , "Red")
    

#create frame
frame = simplegui.create_frame("Draw Circle" , 200, 200)
label = frame.add_label("Desired radius:" + str(size))
frame.add_button("Increase" , incr_button_handler)
frame.add_button("Decrease" , decr_button_handler)
radius_label = frame.add_label("Curr radius:" + str(radius))
frame.add_button("Change circle", change_circle_handler)
frame.set_draw_handler(draw_handler)

#start frame
frame.start()


########
#Quiz 3a
########


###########
#Question 9
###########
import simplegui

#canvas draw handler 
def draw(canvas):
    canvas.draw_circle((90, 200), 20, 10, "White")
    canvas.draw_circle((210, 200), 20, 10, "White")
    canvas.draw_line((50, 180), (250, 180), 40, "Red")
    canvas.draw_line((55, 170), (90, 120), 5, "Red")
    canvas.draw_line((90, 120), (130, 120), 5, "Red")
    canvas.draw_line((180, 108), (180, 160), 140, "Red")
    
    
#create frame
frame = simplegui.create_frame("Screensaver", 300, 300)

#register handlers

frame.set_draw_handler(draw)

#start frame
frame.start()


########
#quiz 3b
########

###########
#question 2
###########

import simplegui

count = 10

def tick():
    global count
    print count, "calls left"
    count -= 1
    if count == 0:
        timer.stop()
        print "goodbye"
    

#register handlers
timer = simplegui.create_timer(1000 , tick)

#start frame, timer

timer.start()


#
#question 3
#

import simplegui

count = 10

def tick():
    global count
    print count, "calls left"
    count -= 1
    if count == 0:
        timer.stop()
        print "goodbye"
        count = 10
    

#register handlers
timer = simplegui.create_timer(1000, tick)

#start frame, timer

timer.start()

timer.stop()

timer = simplegui.create_timer(100, tick)
timer.start()


#
#question 4
#

import simplegui

def tick():
    print "timer1 running"
    
def tick2():
    print "timer2 running"

def tick3():
    print "timer3 running"

#register handlers, start timers
timer1 = simplegui.create_timer(1000, tick)
timer1.start()

timer2 = simplegui.create_timer(500, tick2)
timer2.start()

timer3 = simplegui.create_timer(200, tick3)
timer3.start()

print timer1.is_running()
print timer2.is_running()
print timer3.is_running()

#
#question 7
#

# Takes input n and computes sqrt(n) via Newtons method

import simplegui

# global state

result = 1
iteration = 0
max_iterations = 10

# helper functions

def init(start):
    """Initializes n."""
    global n
    n = start
    print "Input is", n
    
def get_next(current):
    """???  Part of mystery computation."""
    return 0.5 * (current + n / current)

# timer callback

def update():
    """???  Part of mystery computation."""
    global iteration, result
    iteration += 1
    # Stop iterating after max_iterations
    if iteration >= max_iterations:
        timer.stop()
        print "Output is", result
    else:
        result = get_next(result)

# register event handlers

timer = simplegui.create_timer(1, update)

# start program
init(10001)
timer.start()


#
#question 8
#

# Mystery computation in Python
# Takes input n and computes output named result

import simplegui

# global state
n = 219
max = -1
# timer callback

def update():
    """Calc next number in sequence"""
    global n, max
    if n > max:
        max = n
    if n == 1:
        print str(n)
        timer.stop()
        print ""
        print "max = ", max
    elif n % 2 == 0:
        print str(n) + ", "
        n /= 2
    else:
        print str(n) + ", "
        n = 3 * n + 1
       
# register event handlers

timer = simplegui.create_timer(100, update)

# start program
#init(n)
timer.start()


#
#question 9 code
#

# animation of explosion using 2D sprite sheet

import simplegui

# load 81 frame sprite sheer for explosion - image generated by phaedy explosion generator, source is hasgraphics.com
EXPLOSION_CENTER = [50, 50]
EXPLOSION_SIZE = [100, 100]
EXPLOSION_DIM = [9, 9]
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/explosion.hasgraphics.png")

# create timer that iterates current_sprite_center through sprite
time = 0

# define draw handler
def draw(canvas):
    global time
    explosion_index = [time % EXPLOSION_DIM[0], (time // EXPLOSION_DIM[0]) % EXPLOSION_DIM[1]]
    canvas.draw_image(explosion_image, 
                    [EXPLOSION_CENTER[0] + explosion_index[0] * EXPLOSION_SIZE[0], 
                     EXPLOSION_CENTER[1] + explosion_index[1] * EXPLOSION_SIZE[1]], 
                     EXPLOSION_SIZE, EXPLOSION_CENTER, EXPLOSION_SIZE)
    time += 1

        
# create frame and size frame based on 100x100 pixel sprite
f = simplegui.create_frame("Asteroid sprite", EXPLOSION_SIZE[0], EXPLOSION_SIZE[1])

# set draw handler and canvas background using custom HTML color
f.set_draw_handler(draw)
f.set_canvas_background("Blue")

# start animation
f.start()
