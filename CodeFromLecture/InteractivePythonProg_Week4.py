#Interactive Python - Week 3

##### Basics of Lists #####

######
#Lists
######

#create list
l = []
print l

l2 = [1,2,3]

print l2

l3 = ['fruit', 'veggies']
print l3

l4 = [[], [1], ['1'], [1,2,3,4], [['a', 'b']]]

print l4

#access
print len(l)
print l2[0]
print l3[1]
print l4[-1]

l5 = l4[1:3]
print l5


#update - lists are mutable, unlike strings
l2[0] = 4
print l2

###############
#Keyboard Input
###############

#Ex 1 

import simplegui

#init state
current_key = ' '

#event handlers
def keydown(key):
    global current_key
    current_key = chr(key)
    
def keyup(key):
    global current_key
    current_key = ' '
    
def draw(canvas):
    canvas.draw_text(current_key, [10,25], 20, "Red")
    
#create frame
frame = simplegui.create_frame("Echo", 35, 35)

#register handlers
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_draw_handler(draw)

#start frame
frame.start()


#Ex 2
import simplegui

#init globals
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20

ball_pos = [WIDTH / 2, HEIGHT / 2]

#define handlers
def draw(canvas):
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
def keydown(key):
    vel = 4
    if key == simplegui.KEY_MAP["left"]:
        ball_pos[0] -= vel
    elif key == simplegui.KEY_MAP["right"]:
        ball_pos[0] += vel
    elif key == simplegui.KEY_MAP["down"]:
        ball_pos[1] += vel
    elif key == simplegui.KEY_MAP["up"]:
        ball_pos[1] -= vel

#create frame
frame = simplegui.create_frame("Positional ball control", WIDTH, HEIGHT)

#register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)

#start frame
frame.start()



#######
#Motion
#######

#Ex 3

import simplegui

#init globals
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20

init_pos = [WIDTH / 2, HEIGHT / 2]
vel = [0,1]
time = 0

#define handlers
def tick():
    global time
    time += 1
    
def draw(canvas):
    #hold x,y coords of ball pos
    ball_pos = [0,0]
    
    #calc bal pos
    ball_pos[0] = init_pos[0] + time * vel[0]
    ball_pos[1] = init_pos[1] + time * vel[1]
    
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")

#create frame
frame = simplegui.create_frame("Automatic Motion", WIDTH, HEIGHT)

#register handlers
frame.set_draw_handler(draw)
timer = simplegui.create_timer(100, tick)

#start frame
frame.start()
timer.start()

#Ex 4 - motion implicit due to draw fcn refresh rate

import simplegui

#init globals
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20

ball_pos = [WIDTH / 2, HEIGHT / 2]
vel = [0,1] #update 60x per sec, assuming 60Hz refresh rate

#define handlers
def draw(canvas):
    
    #calc bal pos
    ball_pos[0] += vel[0]
    ball_pos[1] += vel[1]
    
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")

#create frame
frame = simplegui.create_frame("Automatic Motion", WIDTH, HEIGHT)

#register handlers
frame.set_draw_handler(draw)

#start frame
frame.start()


###########################
#Collisions and Reflections
###########################

#a ball that bounces off the walls
import simplegui

#init globals
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20

ball_pos = [WIDTH / 2, HEIGHT / 2]
vel = [1,1] #update 60x per sec, assuming 60Hz refresh rate

#define handlers
def draw(canvas):
    
    #calc bal pos
    ball_pos[0] += vel[0]
    ball_pos[1] += vel[1]
    if ball_pos[1] >= HEIGHT - 1 - BALL_RADIUS or ball_pos[1] <= BALL_RADIUS:
        vel[1] *= -1
    if ball_pos[0] >= WIDTH - 1 - BALL_RADIUS or ball_pos[0] <= BALL_RADIUS:
        vel[0] *= -1
    
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")

#create frame
frame = simplegui.create_frame("Automatic Motion", WIDTH, HEIGHT)

#register handlers
frame.set_draw_handler(draw)

#start frame
frame.start()


##### Keyboard Control #####

#################
#Velocity Control
#################


#control ball vel using arrow keys

import simplegui

#init globals
WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
ball_pos = [WIDTH / 2, HEIGHT / 2]
vel = [0,0]

#define handlers
def draw(canvas):
    ball_pos[0] += vel[0]
    ball_pos[1] += vel[1]
    
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")
    
def keydown(key):
    acc = 1
    if key == simplegui.KEY_MAP["left"]:
        vel[0] -= acc
    elif key == simplegui.KEY_MAP["right"]:
        vel[0] += acc
    elif key == simplegui.KEY_MAP["down"]:
        vel[1] += acc
    elif key == simplegui.KEY_MAP["up"]:
        vel[1] -= acc
        
    print ball_pos, vel

#create frame
frame = simplegui.create_frame("Positional ball control", WIDTH, HEIGHT)

#register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)

#start frame
frame.start()



###############################
#Visualizing lists and mutation
###############################

a = [4,5,6]
b = [4,5,6]

print "Example 1:"
print "original a", a, "original b", b
print
print "are they the same thing?", a is b
print

a[1] = 20
print "new a", a, "new b", b

print "Example 2:"
a = [4,5,6]
b = a

print "original a", a, "original b", b
print
print "are they the same thing?", a is b
print

a[1] = 20
print "new a", a, "new b", b

print "Example 3:"
a = [4,5,6]
b = list(a)

print "original a", a, "original b", b
print
print "are they the same thing?", a is b
print

a[1] = 20
print "new a", a, "new b", b



a = [4,5,6]

def mutate_part(x):
    a[1] = x
    
def assign_whole(x):
    a = x
    
def assign_whole_global(x):
    global a
    a = x
    
mutate_part(100)

assign_whole(200)

assign_whole_global(300)


#####################
#Programming tips - 4
#####################

#what is and is not mutable?

print 1 is 1 #T

print 1.0 is 1.0 #T

print True is True #T

print "abc" is "abc" #T

print [4,5,6] is [4,5,6] #F

print 1 is 1.0 #F

print 1 is int(1.0) #T

print (4,5,6) is (4,5,6) #F


a = [4,5,6]
a[1] = 100
print a

b = (4,5,6)
b[1] = 100 #tuple not mutable, so this is an error
print b







#####
#Pong
#####







###############
### Quizzes ###
###############


#question 6, quiz 4b
a = ["green", "blue", "white", "black"]
b = a
c = list(a)
d = c
a[3] = "red"
c[2] = a[1]
b = a[1 : 3]
b[1] = c[2]

print a
print b
print c
print d
print

c[0] = "cyan"
print a
print b
print c
print d
print

d[1] = "magenta"
print a
print b
print c
print d
print

b[0] = "peach"
print a
print b
print c
print d
print

a[2] = "puce"
print a
print b
print c
print d
print


#####


#
#question 8
#

import simplegui

#init globals
WIDTH = 1000
HEIGHT = 1000
pos = [10,10]
vel = [0, 0]
acc = [0,0]
ACC_INC = (0.0001, 0.0001)
pos_list = [pos]

#define handlers
def draw(canvas):
    global pos_list
    canvas.draw_circle(pos, 2, 2, "White")        
    pos[0] += vel[0]
    pos[1] += vel[1]
    vel[0] += acc[0]
    vel[1] += acc[1]
    acc[0] += ACC_INC[0]
    acc[1] += ACC_INC[1]
    pos_list.append(pos)
    print len(pos_list)
    for idx in range(0, len(pos_list)):
        canvas.draw_polyline(pos_list[:idx + 1], 5, "Red")

    
#create frame
frame = simplegui.create_frame("Positional ball control", WIDTH, HEIGHT)

#register handlers
frame.set_draw_handler(draw)


#start frame
frame.start()

#
#questions 9
#

import simplegui

#init state
count = 5
key_count = 0 

#event handlers
def keydown(key):
    global count, key_count
    count *= 2
    key_count += 1
    print count, key_count
    
def keyup(key):
    global count, key_count
    count -= 3
    key_count += 1
    print count, key_count
    
#def draw(canvas):
#    canvas.draw_text(key_count, [10,25], 20, "Red")
    
#create frame
frame = simplegui.create_frame("Echo", 35, 35)

#register handlers
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
#frame.set_draw_handler(draw)

#start frame
frame.start()
