"""
Rock-paper-scissor-lizard-Spock
Author: David Schonberger
Date created: 9/22/2014
url: http://www.codeskulptor.org/#user37_hH5yilvO8262jaA.py

"""

#Mapping between strings "rock", "paper", "scissors", "lizard", "Spock" and numbers 0-4
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random 

# helper function
def name_to_number(name):
    """
    Converts input string name into the corresponding
    number 0-4. See mapping above.
    """
    
    if name == 'rock':
        return 0
    elif name == 'Spock':
        return 1
    elif name == 'paper':
        return 2
    elif name == 'lizard':
        return 3
    else:
        return 4
    
# helper function
def number_to_name(number):
    """
    Converts input number in range 0-4 to corresponding
    string. See mapping above.
    """
    
    
    if number == 0:
        return 'rock'
    elif number == 1:
        return 'Spock'
    elif number == 2:
        return 'paper'
    elif number == 3:
        return 'lizard'
    else:
        return 'scissors'

#main function
def rpsls(player_choice): 
    """
    Plays a single round of Rock-paper-scissors-lizard-Spock.
    
    Input: string player_choice.
    
    Output: a message showing the player's choice,
    a message showing the computer's random choice, and
    a message indicating who wins or if there is a tie.
    """
    
    #generate random choice for computer
    computer_number = random.randrange(0,5)
    computer_choice = number_to_name(computer_number)
    
    #convert player choice to number
    player_number = name_to_number(player_choice)
    
    print "Player chooses", player_choice
    print "Computer chooses", computer_choice
    
    #Boolean expressions to indicate if computer_number
    #is 1 or 2 spaces clockwise from player_number.
    #In either case, player loses/computer wins.
    #(See the rpsls.pdf dcument from lectures.)
    player_loses1 = (player_number + 1) % 5 == computer_number
    player_loses2 = (player_number + 2) % 5 == computer_number
    player_loses = player_loses1 or player_loses2
    
    if player_number == computer_number:
        print "Player and computer tie!"
    elif player_loses:
        print "Computer wins!"
    else:
        print "Player wins!"
        
    print ""
    

# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

####
"""
Rock-paper-scissor-lizard-Spock
Author: David Schonberger
Date created: 9/22/2014
url: http://www.codeskulptor.org/#user37_hH5yilvO8262jaA.py

"""

#Mapping between strings "rock", "paper", "scissors", "lizard", "Spock" and numbers 0-4
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random 

# helper function
def name_to_number(name):
    """
    Converts input string name into the corresponding
    number 0-4. See mapping above.
    """
    
    if name == 'rock':
        return 0
    elif name == 'Spock':
        return 1
    elif name == 'paper':
        return 2
    elif name == 'lizard':
        return 3
    else:
        return 4
    
# helper function
def number_to_name(number):
    """
    Converts input number in range 0-4 to corresponding
    string. See mapping above.
    """
    
    
    if number == 0:
        return 'rock'
    elif number == 1:
        return 'Spock'
    elif number == 2:
        return 'paper'
    elif number == 3:
        return 'lizard'
    else:
        return 'scissors'

#main function
def rpsls(player_choice): 
    """
    Plays a single round of Rock-paper-scissors-lizard-Spock.
    
    Input: string player_choice.
    
    Output: a message showing the player's choice,
    a message showing the computer's random choice, and
    a message indicating who wins or if there is a tie.
    """
    
    #generate random choice for computer
    computer_number = random.randrange(0,5)
    computer_choice = number_to_name(computer_number)
    
    #convert player choice to number
    player_number = name_to_number(player_choice)
    
    print "Player chooses", player_choice
    print "Computer chooses", computer_choice
    
    #Boolean expressions to indicate if computer_number
    #is 1 or 2 spaces clockwise from player_number.
    #In either case, player loses/computer wins.
    #(See the rpsls.pdf dcument from lectures.)
    player_loses1 = (player_number + 1) % 5 == computer_number
    player_loses2 = (player_number + 2) % 5 == computer_number
    player_loses = player_loses1 or player_loses2
    
    if player_number == computer_number:
        print "Player and computer tie!"
    elif player_loses:
        print "Computer wins!"
    else:
        print "Player wins!"
        
    print ""
    

# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")





