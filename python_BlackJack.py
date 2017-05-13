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
        self.hand_card = []	# create Hand object

    def __str__(self):
        ans = ""
        for i in range(len(self.hand_card)):
            ans += str(self.hand_card[i])
        return ans	# return a string representation of a hand

    def add_card(self, card):
        new_card = Card(card.get_suit(), card.get_rank())
        self.hand_card.append(new_card)	# add a card object to a hand
        
    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        sum = 0
        num_of_ace = 0
        for i in range(len(self.hand_card)):
            if self.hand_card[i].get_rank() == 'A':
                num_of_ace += 1
            sum = sum + VALUES.get(self.hand_card[i].get_rank())
        if num_of_ace == 1 and (sum + 10) < 21:
            sum += 10
        return sum
            
            # compute the value of the hand, see Blackjack video
   
    def draw(self, canvas, pos):
        for i in range(len(self.hand_card)):
                # draw a hand on the canvas, use the draw method for cards
            card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.hand_card[i].rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.hand_card[i].suit))
            canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
            pos[0] += CARD_SIZE[0]
            
# define deck class 
class Deck:
    def __init__(self):
        self.deck_card = []	# create a Deck object
        for i in range(len(SUITS)):
            for j in range(len(RANKS)):
                self.deck_card.append(Card(SUITS[i], RANKS[j]))
                
    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck_card)
        # use random.shuffle()

    def deal_card(self):
        a = self.deck_card.pop()
        b = Card(a.get_suit(), a.get_rank())
        return b	# deal a card object from the deck
    
    def __str__(self):
        ans = ""
        for i in range(len(self.deck_card)):
            ans += str(self.deck_card[i])
        return ans	# return a string representing the deck

player_hand = Hand()
dealer_hand = Hand()
deck = Deck()

#define event handlers for buttons
def deal():
    global score, outcome, in_play, deck, player_hand, dealer_hand
    
    if in_play == False:
        in_play = True
        outcome = 'Hit or Stand?'
        deck.shuffle()
        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
        player_hand.add_card(deck.deal_card())
        dealer_hand.add_card(deck.deal_card())
    else:
        outcome = 'You lose. New deal?'
        score -= 1
        in_play = False
        
def hit():
    global score, outcome, in_play
    if in_play == True:      # if the hand is in play, hit the player
        player_hand.add_card(deck.deal_card())
        if player_hand.get_value() < 21:
            outcome = 'Hit or Stand?'
        if player_hand.get_value() > 21:      # if busted, assign a message to outcome, update in_play and score
            outcome = 'You have busted. New deal?'
            in_play = False
            score -= 1
        
def stand():
    global score, outcome, in_play
    if in_play == False:
        outcome = 'Game is over. New deal?'
    if in_play == True:  # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        if dealer_hand.get_value() < 17:
            dealer_hand.add_card(deck.deal_card())
        if dealer_hand.get_value() > 21:
            outcome = 'Dealer has busted. New deal?'
            score += 1
        elif dealer_hand.get_value() >= player_hand.get_value():
            outcome = 'You lose. New deal?'
            score -= 1
        else:
            outcome = 'You win. New deal?'
            score += 1
    in_play = False

# draw handler    
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    canvas.draw_text('BlackJack', [200, 70], 40, 'black')
    canvas.draw_text('Player', [150,170], 30, 'white')
    canvas.draw_text('Dealer', [150, 420], 30, 'white')
    player_hand.draw(canvas,[100,200])
    dealer_hand.draw(canvas,[100,450])
    canvas.draw_text(outcome, [330, 170], 22, 'white')
    canvas.draw_text('SCORE: ' + str(score), [450, 90], 20, 'white')
    if in_play == True:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                      [100 + CARD_CENTER[0], 450 + CARD_CENTER[1]], CARD_BACK_SIZE)
        
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


# remember to review the gradic rubric