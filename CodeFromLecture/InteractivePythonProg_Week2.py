#Interactive Python - Week 2

###################################
#Interactive Applications In Python
###################################


#Events:
#1. Input: button, text box, 
#2. Keyboard: key down, key up
#3. Mouse: click, drag
#4. Timer

#Simple event driven program

#CodeSkulptor GUI module
import simplegui

#Event handler
def tick():
    print "Tick!"


#Register handler
timer = simplegui.create_timer(1000, tick)

timer.start()


#Local v global vars

#global v local examples

#num1 is global
num1 = 1
print num1


#num2 is local
def fun():
    num1 = 3
    num2 = num1 + 1
    print num2

fun()


#scope of num1 is entire program

print num1

#scope of num2 is fun() and so underfined outside it
#print num2


#why use local vars?
#--give descriptive name to a quantity
#--avoid computing something multiple times

def fahr2kelvin(fahr):
    celsius = 5.0 / 9.0 * (fahr - 32)
    zero_celsius_in_kelvin = 273.15
    return celsius + zero_celsius_in_kelvin

print fahr2kelvin(32)


#risk/reward of using globals

#risk: consider software system for airliner
# critical piece: flight control system
# non-critical piece: in-flight entertainment system

#Maybe both systems use a var called 'dial'
#Do not want the possibility that changing the
#volume on your headset causes the plane's
#flaps to change!

#example
num = 4


def fun1():
    global num #access global var called num
    num = 5
    
def fun2():
    global num #access global var called num
    num = 6
    

print num
fun1()
print num
fun2()
print num

#global vars are an easy way for event handlers 
#to communicate game information.

#safer method - but they require more sophisticated
#object oriented techniques



#####################################################
#Recommended Program Structure for Simplegui Programs
#####################################################

#1. Define globals (state)
#2. Define helpers
#3. Define classes
#4. Define event handlers
#5. Create a frame
#6. Register event handlers
#7. Start frame and any timers in program

#Example of template:

import simplegui

#1. Define globals (state)
counter = 0

#2. Define helpers
def increment():
    global counter
    counter += 1
    
#3. Define classes

#4. Define event handlers
def tick():
    increment()
    print counter

def buttonpress():
    global counter
    counter = 0

#5. Create a frame
frame = simplegui.create_frame("SimpleGUI Test", 100, 100)

#6. Register event handlers
timer = simplegui.create_timer(1000, tick)
frame.add_button("Click me", buttonpress)

#7. Start frame and any timers in program
frame.start()
timer.start()


########
#Quiz 2a
########

import simplegui
           
x = 5

def c(y):
    return x + y

print c(1)

def a(y):
    global x
    x = x + y
    return y

print a(2)

def d(y):
    y = x + y
    return y

print d(3)

def b(x,y):
    x = x + y
    return x

print b(5,5)

count = 0

def square(x):
    global count
    count += 1
    return x**2

print square(square(square(square(3)))), count



a = 3
b = 6

def f(a):
    c = a + b
    return c

print f(1), a, b

#f = simplegui.create_frame("My Frame", 100, 100)

#frame = simplegui.create_frame("Testing", 200, 200, 300)

#error: frame = simplegui.create_frame(100, 100, 100)


#error: frame = simplegui.create_frame("My Frame", 200, 200, 200, 200)


#########################
#Buttons And Input Fields
#########################


#
#Calculator: v.1 - implement print and swap using frame and buttons
#

import simplegui

#init globals
store = 12
operand = 3

#define fcns that manipulate store and operand
def output():
    print "Store = ", store
    print "Operand = ", operand
    print ""
    
def swap():
    global store, operand
    store, operand = operand, store
    output()


frame = simplegui.create_frame("Calculator", 200, 200)    
frame.add_button("Print", output, 100)
frame.add_button("Swap", swap, 100)
frame.start()

#
#Calculator: v.2 - add mult and div and an input field
# plus convert input to float to allow non-integer operations
#

import simplegui

#init globals
store = 0
operand = 0

#define fcns that manipulate store and operand
def output():
    print "Store = ", store
    print "Operand = ", operand
    print ""
    
def swap():
    global store, operand
    store, operand = operand, store
    output()


def add():
    global store, operand
    store += operand
    output()

    
def subtract():
    global store, operand
    store -= operand
    output()

def multiply():
    global store, operand
    store *= operand
    output()

def divide():
    global store, operand
    store /= operand
    output()    

def operand_input(inp):
    global operand
    operand = float(inp) #convert text to float
    output()
    
frame = simplegui.create_frame("Calculator", 400, 400)    
frame.add_button("Print", output, 100)
frame.add_button("Swap", swap, 100)
frame.add_button("+", add, 100)
frame.add_button("-", subtract, 100)
frame.add_button("*", multiply, 100)
frame.add_button("/", divide, 100)
frame.add_input("Enter operand: ", operand_input, 100)
frame.start()


##########################
#Programming Tips  - Lec 2
##########################



n = 0

def increment():
    global n
    n = n + 1
 
increment()
increment()
increment()
print n

###
n = 0

def assign(x):
    global n
    n = x

assign(2)
print n
assign(15)
print n
assign(7)
print n

##

n = 0

def decrement():
    global n
    n -= 1

x = decrement()

#fcn has no explicit return, so ret val == None
print "x = ",x 

print "n = ", n

###

#Not clear what this codes is doing if you look at what is sent to the console
#One approach is to use print statement inside fcns.

import simplegui

x = 0

def f(n):
    return n ** x

def button_handler():
    global x
    x += 1
    
def input_handler(text):
    print f(float(text))
    
frame = simplegui.create_frame("Example", 200, 200)
frame.add_button("Increment",button_handler)
frame.add_input("Number:", input_handler, 100)
frame.start()


###

########
#Quiz 2b
########


###########
#question 3
###########

#ok
import simplegui
f = simplegui.create_frame("test", 100,100)
f.add_label("My label")

#error
import simplegui
simplegui.create_frame("test", 100, 100)
l1 = simplegui.add_label("Label one")
l2 = simplegui.add_label("Label two")


#error
import simplegui
simplegui.create_frame("test", 100, 100)
simplegui.add_label("My label")

#ok
import simplegui
f = simplegui.create_frame("test", 100, 100)
label = f.add_label("My label")
label.set_text("My new label")


###
# Simple interactive application

import simplegui

# Define globals.

message = "Welcome!"
count = 0

# Define event handlers.

def button_handler():
    """Count number of button presses."""
    global count
    count += 1
    print message,"  You have clicked", count, "times."
    
def input_handler(text):
    """Get text to be displayed."""
    global message, count
	count = 0
    message = text

# Create frame and register event handlers.

frame = simplegui.create_frame("Home", 100, 200)
frame.add_button("Click me", button_handler)
frame.add_input("New message:", input_handler, 100)

# Start frame.

frame.start()