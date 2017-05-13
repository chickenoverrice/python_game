#http://www.codeskulptor.org/#user40_7y6Jg8SnYToOINh.py

# Implementation of classic arcade game Pong

import simplegui
import random
import math

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
LEFT_PAD_POS = (HEIGHT - PAD_HEIGHT) / 2
RIGHT_PAD_POS = (HEIGHT - PAD_HEIGHT) / 2
paddle1_vel = 0
paddle2_vel = 0
ball_vel = [1.0, 1.0]
ball_pos = [WIDTH / 2, HEIGHT / 2]
LEFT_SCORE = 0
RIGHT_SCORE = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_vel # these are vectors stored as lists
    if direction == LEFT:
        ball_vel[0] = -ball_vel[0]
        ball_vel[0] = (ball_vel[0] / math.fabs(ball_vel[0])) * random.randrange(120, 240) / 60.0                                             
    if direction == RIGHT:
        ball_vel[1] = -ball_vel[1]
        ball_vel[1] = (ball_vel[1] / math.fabs(ball_vel[1])) * random.randrange(60, 180) / 60.0

        

# define event handlers
def new_game():
    global LEFT_PAD_POS, RIGHT_PAD_POS, paddle1_vel, paddle2_vel  # these are numbers
    global LEFT_SCORE, RIGHT_SCORE  # these are ints
    global ball_vel, ball_pos
    LEFT_PAD_POS = (HEIGHT - PAD_HEIGHT) / 2
    RIGHT_PAD_POS = (HEIGHT - PAD_HEIGHT) / 2
    LEFT_SCORE = 0
    RIGHT_SCORE = 0
    paddle1_vel = 0
    paddle2_vel = 0
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    if random.randint(0, 1) == 0:
        spawn_ball(RIGHT)
    else:
        spawn_ball(LEFT)

    
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel,paddle1_vel, paddle2_vel
    global LEFT_PAD_POS, RIGHT_PAD_POS, LEFT_SCORE, RIGHT_SCORE
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    if ball_pos[1] < BALL_RADIUS or ball_pos[1] > HEIGHT - BALL_RADIUS:
        spawn_ball(RIGHT)
    if ball_pos[0] >= WIDTH - PAD_WIDTH - BALL_RADIUS or ball_pos[0] <= BALL_RADIUS + PAD_WIDTH:
        spawn_ball(LEFT)
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White")
    
    # update paddle's vertical position, keep paddle on the screen
    LEFT_PAD_POS += paddle1_vel
    if LEFT_PAD_POS <= 1:
        LEFT_PAD_POS = 1
        paddle1_vel = 0
    if LEFT_PAD_POS >= HEIGHT - PAD_HEIGHT:
        LEFT_PAD_POS = HEIGHT - PAD_HEIGHT
        paddle1_vel = 0
    RIGHT_PAD_POS += paddle2_vel
    if RIGHT_PAD_POS < 1:
        RIGHT_PAD_POS = 1
        paddle2_vel = 0
    if RIGHT_PAD_POS >= HEIGHT - PAD_HEIGHT:
        RIGHT_PAD_POS = HEIGHT - PAD_HEIGHT
        paddle2_vel = 0
        
    # draw paddles
    canvas.draw_line([0, LEFT_PAD_POS], [PAD_WIDTH, LEFT_PAD_POS], 1, "White")
    canvas.draw_line([0, LEFT_PAD_POS + PAD_HEIGHT], [PAD_WIDTH, LEFT_PAD_POS + PAD_HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, RIGHT_PAD_POS], [WIDTH, RIGHT_PAD_POS], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, RIGHT_PAD_POS + PAD_HEIGHT], [WIDTH, RIGHT_PAD_POS + PAD_HEIGHT], 1, "White")
    
    # determine whether paddle and ball collide   
    if ball_pos[0] <= (BALL_RADIUS + PAD_WIDTH):
        if ball_pos[1] < LEFT_PAD_POS or ball_pos[1] > (LEFT_PAD_POS + PAD_HEIGHT):
            RIGHT_SCORE += 1
    if ball_pos[0] >= (WIDTH - PAD_WIDTH - BALL_RADIUS):
        if ball_pos[1] < RIGHT_PAD_POS or ball_pos[1] > (RIGHT_PAD_POS + PAD_HEIGHT):
            LEFT_SCORE += 1
                        
    # draw scores
    canvas.draw_text(str(LEFT_SCORE), (250, 50), 20, "White")
    canvas.draw_text(str(RIGHT_SCORE), (340, 50), 20, "White")

        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel -= 2        
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel += 2        
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel -= 2        
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel += 2
                                       
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP['w']:
        paddle1_vel += 2        
    if key == simplegui.KEY_MAP['s']:
        paddle1_vel -= 2        
    if key == simplegui.KEY_MAP['up']:
        paddle2_vel += 2        
    if key == simplegui.KEY_MAP['down']:
        paddle2_vel -= 2
    
def button_newgame():
    new_game()


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button('New Game', button_newgame, 100)


# start frame
new_game()
frame.start()
