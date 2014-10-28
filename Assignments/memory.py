"""
Interactive Programming in Python - Memory card game
"""
import simplegui
import random

#globals
deck = range(8) + range(8)
exposed = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
state = 0
card1 = -1
card2 = -1
turns = 0

# helper function to initialize globals
def new_game():
    global state, deck, exposed
    state = 0
    deck = range(8) + range(8)
    exposed = [False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False]
    random.shuffle(deck)
     
# define event handlers
def mouseclick(pos):
    global state, card1, card2, turns
    #game state logic
    if pos[1] >= 0 and pos[1] <= 100 and pos[0] >=0 and pos[0] <= 800: #check in bounds
        card_num = pos[0] // 50
        if not exposed[card_num]:
            if state == 0: #start of game
                exposed[card_num] = True
                card1 = card_num
                state = 1
            elif state == 1: #one card exposed
                if not exposed[card_num]:
                    exposed[card_num] = True
                    card2 = card_num
                    state = 2
            else: #two cards exposed
                state = 1
                turns += 1
                exposed[card_num] = True
                if deck[card1] != deck[card2]: #if no match -> hide the other two
                    exposed[card1] = False
                    exposed[card2] = False    
                card1 = card_num
                                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global turns
    label.set_text("Turns = " + str(turns))
    offset = 0
    for card in deck:
        if exposed[offset]:
            canvas.draw_text(str(card), (15 + offset*50, 60), 36, "White")
        else:
            canvas.draw_polygon([[0 + offset * 50, 0], [49 + offset * 50, 0], [49 + offset * 50, 100], [0 + offset * 50, 100]], 2, 'Purple', 'Green')
        offset += 1

# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Reset", new_game)
label = frame.add_label("Turns = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()
