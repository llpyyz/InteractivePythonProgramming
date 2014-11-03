#Interactive Python - Week 6

###################
##### Classes #####
###################


### Lec 1 - Object-oriented programming - 1 ###

#####Classes: Example 1#####

class Character:
    def __init__(self, name, initial_health):
        self.name = name
        self.health = initial_health
        self.inventory = []
        
    def __str__(self):
        s = "Name: " + self.name
        s += " Health: " + str(self.health)
        s += " Inventory: " + str(self.inventory)
        return s
    
    def grab(self, item):
        self.inventory.append(item)
        
    def get_health(self):
        return self.health
    
def example():
    me = Character("David", 20)
    print str(me)
    me.grab("rock")
    me.grab("paper")
    print str(me)
    print "Health: ", me.get_health()
    

example()


### Lec 2 - Object-oriented programming - 2 ###

#####Classes: Example 2#####

#Classes: Example 2
import simplegui
import random
import math

width = 600
height = 400

#Ball traits
radius = 20
color = "White"
reflect_count = 0

#helper fcn
def dot(v, w):
    return v[0] * w[0] + v[1] * w[1]
    
    
class RectangularDomain:
    
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.border = 2
        
    #return if bounding circle inside domain
    def inside(self, center , radius):
        x_inbounds = center[0] > radius + self.border and center[0] < self.width - radius - self.border
        y_inbounds = center[1] > radius + self.border and center[1] < self.height - radius - self.border
        return x_inbounds and y_inbounds
        
    #return unit normal to domain boundary point nearest center
    def normal(self, center):
        left = center[0]
        right = self.width - center[0]
        top = center[1]
        bottom = self.height - center[1]
        if left < min(right, top, bottom):
            return (1,0)
        elif right < min(left, top, bottom):
            return (-1,0)
        elif top < min(left, right, bottom):
            return (0,1)
        elif bottom < min(left, right, top):
            return (0, -1)
        
    #return random location
    def random_pos(self, radius):
        x = random.randrange(radius, self.width - radius - self.border)
        y = random.randrange(radius, self.hright - radius - self.border)
        return [x,y]
    
    #Draw boundary of domain
    def draw(self, canvas):
        canvas.draw_polygon([[0 , 0], 
                             [self.width, 0], 
                             [self.width, self.height], 
                             [0, self.height]], 2 * self.border,
                            "Red")

        
class CircularDomain:
    
    def __init__(self, center ,radius):
        self.center = center
        self.radius = radius
        self.border = 2
        
    # return if bounding circle is inside the domain    
    def inside(self, center, radius):
        delta_x = center[0] - self.center[0]
        delta_y = center[1] - self.center[1]
        delta_r2 = delta_x ** 2 + delta_y ** 2
        return delta_r2 < (self.radius - radius - self.border) ** 2
    
    # return a unit normal to the domain boundary point nearest center
    def normal(self, center):
        delta_x = center[0] - self.center[0]
        delta_y = center[1] - self.center[1]
        delta_r = math.sqrt(delta_x ** 2 + delta_y ** 2)
        print
        print "dx", delta_x
        print "dy", delta_y
        print "dr", delta_r
        print [delta_x / delta_r, delta_y / delta_r]
        print
        return [delta_x / delta_r, delta_y / delta_r]
    
    # return random location
    def random_pos(self, radius):
        rand_radius = random.random()* (self.radius - radius - self.border)
        rand_theta = random.random() * 2 * math.pi
        x = rand_radius * math.cos(rand_theta) + self.center[0]
        y = rand_radius * math.sin(rand_theta) + self.center[1]
        return [x,y]
    
    # Draw boundary of domain
    def draw(self, canvas):
        canvas.draw_circle(self.center, self.radius, 2 * self.border, "Red")
        

class Ball:
    def __init__(self, radius, color, domain):
        self.radius = radius
        self.color = color
        self.domain = domain
        
        self.pos = self.domain.random_pos(self.radius)
        self.vel = [random.random() + 0.1 , random.random() + 0.1]
        print "init pos:", self.pos, "init vel:", self.vel
        print
        
        
    #Bounce
    def reflect(self):
        global reflect_count
        reflect_count += 1
        norm = self.domain.normal(self.pos)
        norm_length = dot(self.vel, norm)
        print "#####"
        print "Before reflect #", reflect_count
        print "norm:", norm
        print "vel: ", self.vel
        print "norm len:", norm_length
        print
        self.vel[0] = self.vel[0] - 2 * norm_length * norm[0]
        self.vel[1] = self.vel[1] - 2 * norm_length * norm[1]
        print
        print "After reflect" 
        print " pos:", self.pos
        print "vel:", self.vel
        print "#####"
        
    #Update ball pos
    def update(self):
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        if not self.domain.inside(self.pos, self.radius):
            self.reflect()
            
    #draw
    def draw(self, canvas):
        canvas.draw_circle(self.pos, self.radius, 1,
                           self.color, self.color)

#generic update code for ball physics        
def draw(canvas):
    ball.update()
    field.draw(canvas)
    ball.draw(canvas)
    
#field = RectangularDomain(width, height)
field = CircularDomain([width / 2, height / 2], 180)
ball = Ball(radius, color, field)

frame = simplegui.create_frame("Ball physics", width, height)

frame.set_draw_handler(draw)

frame.start()



### Lec 3 - Working with objects ###

#Particle class examle used to simulate diffusion of molecules

import simplegui
import random

#global constants
WIDTH = 600
HEIGHT = 400
PARTICLE_RADIUS = 5
COLOR_LIST = ["Red", "Green", "Blue", "White"]
DIRECTION_LIST = [[1,0], [0,1], [-1,0], [0, -1]]

#definition of Particle class
class Particle:
    
    #initializer
    def __init__(self, position, color):
        self.position = position
        self.color = color
        
    #update particle position
    def move(self, offset):
        self.position[0] += offset[0]
        self.position[1] += offset[1]
        
    #draw method for particles
    def draw(self, canvas):
        canvas.draw_circle(self.position, PARTICLE_RADIUS, 1, self.color, self.color)
        
        
    #string method for particles
    def __str__(self):
        return "Particle with position " + str(self.position) + " and color " + self.color
                
#draw handler
def draw(canvas):

    for p in particle_list:
        p.move(random.choice(DIRECTION_LIST))
        
    for p in particle_list:
        p.draw(canvas)
        
#create frame, register handler
frame = simplegui.create_frame("Particle simulator", WIDTH, HEIGHT)
frame.set_draw_handler(draw)

#create list of particles
particle_list = []
for i in range(10):
    p = Particle([WIDTH / 2, HEIGHT / 2], random.choice(COLOR_LIST))
    particle_list.append(p)
    #print p

#start frame
frame.start()





### Lec 4 - Classes for Blackjack ###

###################
##### Quiz 6a #####
###################

class BankAccount:
    def __init__(self, initial_balance):
        """Creates an account with the given balance."""
        self.balance = initial_balance
        self.fees = 0
       
    def deposit(self, amount):
        """Deposits the amount into the account."""
        self.balance += amount
       
    def withdraw(self, amount):
        """
        Withdraws the amount from the account.  Each withdrawal resulting in a
        negative balance also deducts a penalty fee of 5 dollars from the balance.
        """
        self.balance -= amount
        if self.balance < 0:
            self.balance -= 5
            self.fees += 5
       
    def get_balance(self):
        """Returns the current balance in the account."""
        return self.balance
       
    def get_fees(self):
        """Returns the total fees ever deducted from the account."""
        return self.fees
    
    
my_account = BankAccount(10)
my_account.withdraw(5)
my_account.deposit(10)
my_account.withdraw(5)
my_account.withdraw(15)
my_account.deposit(20)
my_account.withdraw(5) 
my_account.deposit(10)
my_account.deposit(20)
my_account.withdraw(15)
my_account.deposit(30)
my_account.withdraw(10)
my_account.withdraw(15)
my_account.deposit(10)
my_account.withdraw(50) 
my_account.deposit(30)
my_account.withdraw(15)
my_account.deposit(10)
my_account.withdraw(5) 
my_account.deposit(20)
my_account.withdraw(15)
my_account.deposit(10)
my_account.deposit(30)
my_account.withdraw(25) 
my_account.withdraw(5)
my_account.deposit(10)
my_account.withdraw(15)
my_account.deposit(10)
my_account.withdraw(10) 
my_account.withdraw(15)
my_account.deposit(10)
my_account.deposit(30)
my_account.withdraw(25) 
my_account.withdraw(10)
my_account.deposit(20)
my_account.deposit(10)
my_account.withdraw(5) 
my_account.withdraw(15)
my_account.deposit(10)
my_account.withdraw(5) 
my_account.withdraw(15)
my_account.deposit(10)
my_account.withdraw(5) 
print my_account.get_balance(), my_account.get_fees()



############
#TiledImages
############



### Lec 1 - Tiled images ###


#some test code
# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        pass	# create Hand object

    def __str__(self):
        pass	# return a string representation of a hand

    def add_card(self, card):
        pass	# add a card object to a hand

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        pass	# compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        pass	# draw a hand on the canvas, use the draw method for cards
 
        
# define deck class 
class Deck:
    def __init__(self):
        pass	# create a Deck object

    def shuffle(self):
        # shuffle the deck 
        pass    # use random.shuffle()

    def deal_card(self):
        pass	# deal a card object from the deck
    
    def __str__(self):
        pass	# return a string representing the deck



#define event handlers for buttons
def deal():
    global outcome, in_play

    # your code goes here
    
    in_play = True

def hit():
    pass	# replace with your code below
 
    # if the hand is in play, hit the player
   
    # if busted, assign a message to outcome, update in_play and score
       
def stand():
    pass	# replace with your code below
   
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more

    # assign a message to outcome, update in_play and score

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    
    card = Card("S", "A")
    card.draw(canvas, [300, 300])


# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()


### Lec 2 - Visualizing objects ###

#Example 1 - mutation and aliasing
class Point1:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
    def set_x(self, newx):
        self.x = newx
        
    def get_x(self):
        return self.x
    
    
    
p = Point1(4,5)
q = Point1(4,5)
r = p

print p.get_x()
print q.get_x()
print r.get_x()

p.set_x(10)

print p.get_x()
print q.get_x()
print r.get_x()


#Example 2 - aliasing using a list (hidden state)
class Point2:
    def __init__(self, coordinates):
        self.coords = coordinates
        
    def set_coord(self, index, value):
        self.coords[index] = value
        
    def get_coord(self, index):
        return self.coords[index]
    
    
    
coordinates = [4,5] #coordinates is a ref to the list, so when passed to constructor, both p and q ref this list
p = Point2(coordinates)
q = Point2(coordinates)
r = Point2([4,5])

p.set_coord(0, 10)
coordinates[0] = 6

print p.get_coord(0)
print q.get_coord(0)
print r.get_coord(0)


#Example 3 - no shared state between objects
class Point3:
    def __init__(self, coordinates):
        self.coords = list(coordinates)
        
    def set_coord(self, index, value):
        self.coords[index] = value
        
    def get_coord(self, index):
        return self.coords[index]
    
    
    
c = [4,5]
p = Point3(c)
q = Point3(c)
r = Point3([4,5])

p.set_coord(0, 10)

print p.get_coord(0)
print q.get_coord(0)
print r.get_coord(0) #p and q now look like r in terms of their refs to internal lists

### Lec 3 - Programming tips ###


### Lec 4 - Blackjack ###


### quiz 6b ###
def list_extend_many(lists):
    """Returns a list that is the concatenation of all the lists in the given list-of-lists."""
    result = []
    for l in lists:
        result.extend(l)
    return result

l = [[1,2], [3,4,5] , [6]]
l2 = [[1,2,3]]
print list_extend_many(l), l
print list_extend_many(l2), l2
print


def list_extend_many2(lists):
    result = []
    i = 0
    while i < len(lists): 
        result += lists[i]
        i += 1
    return result

l = [[1,2], [3,4,5] , [6]]
l2 = [[1,2,3]]
print list_extend_many2(l), l
print list_extend_many2(l2), l2
print


def list_extend_many3(lists):
    result = []
    for i in range(len(lists)):
        result.extend(lists[i])
    return result

l = [[1,2], [3,4,5] , [6]]
l2 = [[1,2,3]]
print list_extend_many3(l), l
print list_extend_many3(l2), l2
print

def list_extend_many4(lists):
    result = []
    while len(lists) > 0:
        result.extend(lists.pop(0))
    return result

l = [[1,2], [3,4,5] , [6]]
l2 = [[1,2,3]]
print list_extend_many4(l), l
print list_extend_many4(l2), l2
print


### prime number sieve ###


