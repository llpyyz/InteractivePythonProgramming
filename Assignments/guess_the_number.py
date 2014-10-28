"""
Guess the number
Interactive Porgramming with Python, Week 2 projectWeek 2
Author: David Schonberger
Date created: 9/30/2014
url: http://www.codeskulptor.org/#user38_tkxVFv5Ydk_0.py
http://www.codeskulptor.org/#user38_EMqCuoNoJq8Lu9y.py

"""

# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

import simplegui
import random
import math

guesses_made = 1
secret_number = -1
range_size = 100
max_guesses = int(math.ceil(math.log(range_size, 2)))

# helper function to start and restart the game
def new_game():
    """
    Start/restart game of guess the number.
    """
    global secret_number, max_guesses, guesses_made
    
    #init/reset secret_number, max_guesses and guesses_made
    secret_number = random.randrange(0,range_size)
    max_guesses = int(math.ceil(math.log(range_size, 2)))
    guesses_made = 0
    print ""
    print "Secret number in range [ 0,",range_size, ") generated."
    print "You have", max_guesses, "attempts to guess the number."
    print "Guess smart!"
    print ""

# define event handlers for control panel
def range100():
    """Event handler for button that changes the range to [0,100) and starts a new game"""
    global range_size
    range_size = 100
    new_game()
    
def range1000():
    """Event handler for button that changes the range to [0,1000) and starts a new game"""
    global range_size
    range_size = 1000
    new_game()
    
def input_guess(guess):
    """
    Event handler invoked when user enters a guess.
    --Checks user guess against secret number
    --Informs user to guess higher or lower is guess incorrect 
    --Tracks number of guesses made so far
    --Starts new game with current range when game is won/lost.
    """
    global guesses_made
    guesses_made += 1
        
    num_guess = int(guess)
    print "Guess #", guesses_made, "was", num_guess
    
    if secret_number < num_guess:
        print "Lower!"
        print "You have", max_guesses - guesses_made, "guesses left."
        print ""
    elif secret_number > num_guess:
        print "Higher!" 
        print "You have", max_guesses - guesses_made, "guesses left."
        print ""
    else:
        print "Correct!", secret_number, "is the secret number."
        print "You took", guesses_made, "guesses."
        print "Well done, you win!"
        print ""
        new_game()
       
    if max_guesses - guesses_made == 0:
        print "The secret number was", secret_number
        print "You did not guess it within ", max_guesses, "guesses."
        print "Unfortunately you did not win this game."
        print "Try again!"
        print ""
        new_game()
                
# create frame
frame = simplegui.create_frame("Guess the number",200,200)

# register event handlers for control elements and start frame
frame.add_input("Your guess:", input_guess, 100)
frame.add_button("Range: 0 - 100", range100)
frame.add_button("Range: 0 - 1000", range1000)

# call new_game 
new_game()

