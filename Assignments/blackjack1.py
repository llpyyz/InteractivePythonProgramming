"""
Mini-project #6 - Blackjack
Author: David Schonberger
Created 10/29/2014
"""


import simplegui
import random

#canvas dimensions
WIDTH = 950
HEIGHT = 750

#upper left corner for dealer and player hands
DEALER_START_POS = (40, 120)
PLAYER_START_POS = (40, 420)

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

CARD_SPACING = 10

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
hole_card_hidden = True
quit_hand = False
hands_played = 0
wins = 0
loses = 0
winpct = 0.0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}
FULL_SUITS = ('Clubs', 'Spades', 'Hearts', 'Diamonds')
FULL_RANKS = ('Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King')

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
        global hole_card_hidden
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        
        card_back_loc = (CARD_BACK_CENTER[0], CARD_BACK_CENTER[1] )
        
        if pos == DEALER_START_POS and hole_card_hidden:
            canvas.draw_image(card_back, card_back_loc, CARD_BACK_SIZE, [pos[0] + CARD_BACK_CENTER[0], pos[1] + CARD_BACK_CENTER[1]], CARD_SIZE)
        else:
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        
# define hand class
class Hand:
    def __init__(self):
        self.hand = []

    def __str__(self):
        res = ""
        for card in self.hand:
            s = FULL_SUITS[SUITS.index(card.get_suit())]
            r = FULL_RANKS[RANKS.index(card.get_rank())]
            res += r + " of " + s + "; "
        return res

    def add_card(self, card):
        self.hand.append(card)

    def get_value(self):
        #aces == 1 initially
        #if aces in hand, then add 10 to hand value as long as it doesn't bust
        hand_value = 0
        has_aces = False
        for card in self.hand:
            hand_value += VALUES[card.get_rank()]
            if card.get_rank() == 'A':
                has_aces = True
        
        if not has_aces:
            return hand_value
        else:
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
            
    #draws up to 2 rows of five cards for
    #each of delaer and player
    def draw(self, canvas, pos):
        count = 0
        for card in self.hand:
            card.draw(canvas, (pos[0] + (count % 5) * (CARD_SIZE[0] + CARD_SPACING), pos[1] + count // 5 * (CARD_SIZE[0] + CARD_SPACING) ))
            count += 1
        
# define deck class 
class Deck:
    def __init__(self):
        self.deck = [Card(s,r) for s in SUITS for r in RANKS]
        
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck)

    def deal_card(self):
        if len(self.deck) > 0:
            return self.deck.pop(0)
        else:
            print "Error: deck is empty"
            return None
    
    def __str__(self):
        res = ""
        for card in self.deck:
            s = FULL_SUITS[SUITS.index(card.get_suit())]
            r = FULL_RANKS[RANKS.index(card.get_rank())]
            res += r + " of " + s + "\n"
        return res

#helper    
def update_winpct():
    global hands_played, wins, winpct
    winpct = round(100.0 * wins / hands_played, 1)

#define event handlers for buttons
def deal():
    global outcome, in_play, deck, phand, dhand, score 
    global quit_hand, hands_played, loses, wins
    
    if in_play:
        loses += 1
        hands_played += 1
        update_winpct()
        quit_hand = True #flag to post msg to player about losing a pt for quitting mid hand
        
    deck = Deck()
    phand = Hand()
    dhand = Hand()    
    
    
    #shuffle up...
    deck.shuffle()
    
    #and deal!
    phand.add_card(deck.deal_card())
    phand.add_card(deck.deal_card())
    dhand.add_card(deck.deal_card())
    dhand.add_card(deck.deal_card())
    
    in_play = True

def hit():
    global in_play, phand, deck, score, outcome, hands_played 
    global hole_card_hidden, quit_hand, loses
    
    #reset flag if needed
    if quit_hand:
        quit_hand = False
        
    if in_play:
        phand.add_card(deck.deal_card())
        
        if phand.get_value() > 21:
            loses += 1
            hands_played += 1
            update_winpct()
            in_play = False
            hand_over = True
            hole_card_hidden = False
            outcome = "Sorry, you busted! Click 'Deal' to play again."
                
def stand():
    global in_play, phand, dhand, deck, hands_played
    global outcome, hole_card_hidden, quit_hand, wins, loses

    #reset flag if needed
    if quit_hand:
        quit_hand = False
        
    if phand.get_value() <= 21:
        in_play = False
        hole_card_hidden = False
        
        #hit dealer until val >= 17
        while dhand.get_value() < 17:
            dhand.add_card(deck.deal_card())
        
        dval = dhand.get_value()
        if dval > 21:
            outcome = "Dealer busts, you win! Click 'Deal' to play again."
            hands_played += 1
            wins += 1
        else:
            pval = phand.get_value()
            if pval > dval:
                outcome =  "You win! Click 'Deal' to play again."
                hands_played += 1
                wins += 1
            else: 
                if pval == dval:    
                    outcome =  "Tie, dealer wins! Click 'Deal' to play again."
                else:
                    outcome =  "Dealer wins! Click 'Deal' to play again."
                hands_played += 1
                loses += 1
                
        update_winpct()
        
# main draw handler    
def draw(canvas):    
    global phand, dhand, in_play, hole_card_hidden
    global hand_over, outcome, quit_hand 
    global wins, loses, hands_played, winpct
    
    #draw text
    canvas.draw_text("Blackjack", (400, 50), 48, "Black")
    canvas.draw_text("Dealer:", (30, 100), 36, "White")
    canvas.draw_text("Player:", (30, 400), 36, "White")    
    canvas.draw_text("Wins: " + str(wins) + " (" + str(winpct) + "%)" , (600, 450), 36, "White")
    canvas.draw_text("Loses: " + str(loses) , (600, 500), 36, "White")
    canvas.draw_text("Hands played: " + " " + str(hands_played), (600, 550), 36, "White")
    
    
    if in_play:
        hole_card_hidden = True
        if quit_hand:
            outcome = "(Lost a point for quitting hand. Hit or stand?)"
        else:
            outcome = "(Hit or stand?)"
    
    canvas.draw_text(outcome, (150, 400), 24, "Purple")
    
    #draw  hands
    dhand.draw(canvas, DEALER_START_POS)
    phand.draw(canvas, PLAYER_START_POS)
    

def timer_handler():
    global outcome
    outcome = ""
    
# initialization frame
frame = simplegui.create_frame("Blackjack", WIDTH, HEIGHT)
frame.set_canvas_background("Lime")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)
timer = simplegui.create_timer(2000, timer_handler)

# create deck and two hands, then deal initial hands
deck = Deck()
phand = Hand()
dhand = Hand()
deal()
frame.start()
