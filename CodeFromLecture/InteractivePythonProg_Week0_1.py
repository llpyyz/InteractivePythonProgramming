#Interactive Python - Week 0

#########################################################
#Arithmetic expressions - numbers, operators, expressions
#########################################################

print 3, -1, 3.14159, -2.8

#two types of numbers int() and float()

print type(3), type(3.14159), type(3.0)

#convert between int and float

print int(3.14149), int(-2.8)

print float(2)

#float has about 15 digits of accuracy

print 4.5348709676829765789379612067506457765897693480943 #accuracy lost in print out

#arithmetic operators
print 1+2, 3-4, 5*6, 11/6, 2**5 

#Division: int/int does integer division, thus

print 11/6 #prints 1

print -11/6 #prints -2, uses the division algorithm forcing nonneg remainder
# -11 = -2 * 6 + 1, so the remainder is between 0 and 5

#If at least one number is a decimal, the result is floating point

print 1.0/2, 5/6.0, 7.8/2.3

#Expressions - number or arithmetic op applied to one or more expressions

print 2 #number
print 2+3 #binary op applied to two expressions
print -4 #unary op applied to expression

#Precedence of operations determined by usual rule from arithmetic: PEMDAS

print 1 + 2 - 3/4 * 5 ** 6 #same as 1  2 - 0 * 5 ** 6 -> 3 - 0 * 15625 -> 3 - 0 -> 3

##########################
#Variables and Assignments
##########################

#Placeholder
#Valid names: letters, numbers and underscores 
#starts with letter or underscore
#case sensitive
#Convention in Python: multiple words joined with _

my_name = "David"
print my_name

my_age = 47
print my_age

my_age = my_age + 1
print my_age

my_age += 1
print my_age

magic_pill = 30
print my_age - magic_pill

my_grandpa = 75
print my_grandpa - 2 * magic_pill

#Temperature examples

#Convert F to C: C = 5/9 * (F - 32)

temp_F = 32
temp_C = 5.0/9 *(temp_F - 32)
print temp_C

#Convert C to F: F = 9/5* C + 32
temp_C = 10
temp_F = 9.0 / 5 * temp_C + 32


##########
#Functions
##########

#Computes area of triangle
def triangle_area(base, height):
    return (1.0 / 2.0 * base * height)

a1 = triangle_area(2,3)
a2 = triangle_area(5,7)
print a1, a2

#converts Fahrenhit to Celsius
def fahrenheit_to_celsius(temp_f):
    return 5.0 / 9.0 *(temp_f - 32)

f1 = fahrenheit_to_celsius(32)
f2 = fahrenheit_to_celsius(212)
print f1, f2

#converts Celsius to Fahrenheit
def celsius_to_fahrenheit(temp_c):
    return 9.0 / 5.0 * temp_c + 32

c1 = celsius_to_fahrenheit(0)
c2 = celsius_to_fahrenheit(100)
print c1, c2

#converts Fahrenhit to Kelvin
def fahrenheit_to_kelvin(temp_f):
    return fahrenheit_to_celsius(temp_f) + 273.15

k1 = fahrenheit_to_kelvin(32)
k2 = fahrenheit_to_kelvin(212)
print k1, k2

#print hello world
def hello():
    print "Hello world!"

hello()
h = hello()
print h #h == None

import math
def root(b, a, c):
    """
    Returns a root of quadratic fcn ax^2 + bx + c = 0
    """
    return (-b + math.sqrt(b ** 2 - 4 * a * c))/(2 * a)

r = root(1,0,-1) #error since fcn sets a = 0. Use Vizmode to step through and find problem!
print r




#######################
#Logic and Conditionals
#######################

#Logic 
a = True
b = False
c = True
d = True
print a ,b
print not a, a and b, a or b
print (a and b) or (c and not d)

#Comparison operators
a = 7 > 3
print a

x = 5
y = 8
b = x >= y
print b

c = "Hello" == 'Hello'
print c

d = "Hello" == 'hello'
print d

print "###"

#####Conditionals#####

###Example 1###

def greet(friend, money):
    if friend and money > 20:
        print "Hi!"
        money = money - 20
    elif friend:
        print "Hello"
    else:
        print "Ha ha"
        money = money + 10

    return money

money = 15

money = greet(True, money)
print "Money:", money
print ""

money = greet(False, money)
print "Money:", money
print ""

money = greet(True, money)
print "Money:", money
print ""

###Example 2###

def is_leap_year(year):
    """
    Return true if 'year' is a leap year, else false
    """
    if(year % 400) == 0:
        return True
    elif (year % 100) == 0:
        return False
    elif (year % 4) == 0:
        return True
    else:
        return False

year = 2006
ly = is_leap_year(year)
if ly:
    print year, "is a leap year"
else:
    print year, "is not a leap year"


###Programming tips###

#Make sure functions and vars are defined and not misspelled
def volume_cube(side):
    return side ** 3

s = 2
print "Volume of cube with side", s, "is", volume_cube(s), "."

print "###"

#Remember to import needed modules
import random
def random_dice():
    die1 = random.randrange(1,7)
    die2 = random.randrange(1,7)
    return die1 + die2

print "sum of two random dice", random_dice()
print "sum of two random dice", random_dice()
print "sum of two random dice", random_dice()

print "###"

#Remember names are case sensitive: 
#Make sure to use correct name for constants such as pi
import math
def volume_sphere(radius):
    return 4.0 / 3.0 * math.pi * radius ** 3

r = 2
print "Volume of sphere with radius", r, "is", volume_sphere(r)

print "###"

#Can't multiply string by float
def area_triangle(base, height):
    return 0.5 * base * height

b = "5" #string
h = "2+2" #string
#print "Area of triangle with base", b, "and height", h, "is", area_triangle(b,h)

b = 5
h = 2+2
print "Area of triangle with base", b, "and height", h, "is", area_triangle(b,h)

print "###"

#Use doc strings to describe inputs, output, and purpose
#Use comments to describe how it works
def area_triangle_sss(side1,side2,side3):
    """
    Returns area of triangle given all sides
    """
    
    #Heron's formula
    semi_perim = (side1 + side2 + side3)/2.0
    return math.sqrt(semi_perim * 
                     (semi_perim - side1) * 
                     (semi_perim - side2) * 
                     (semi_perim - side3))

side1 = 3
side2 = 4
side3 = 5
print "area of triangle with sides", side1, side2, side3, "is", area_triangle_sss(side1, side2, side3)
