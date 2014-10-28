# Implementation of classic arcade game Pong

import simplegui
import random

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
BALL_VEL_INC_FACTOR = 1.1

ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0,0]
paddle1_vel = 0
paddle2_vel = 0
paddle1_pos = HEIGHT * 1.0 / 2
paddle2_pos = HEIGHT * 1.0 / 2

score1 = 0
score2 = 0

# initialize ball_pos and ball_vel for new ball in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    vel_hor = (-1) ** (int(direction == LEFT)) * random.randrange(2,4)
    vel_vert = -random.randrange(1,3)
    ball_vel = [vel_hor, vel_vert]
    
# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    paddle1_pos = HEIGHT * 1.0 / 2
    paddle2_pos = HEIGHT * 1.0 / 2
    rnd_dir = random.random()
    if rnd_dir <= 0.5:
        direction = RIGHT
    else:
        direction = LEFT
    spawn_ball(direction)
    
def draw(canvas):
    global score1, score2, paddle1_pos
    global paddle2_pos, ball_pos, ball_vel
    global paddle1_vel, paddle2_vel, count
    
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    #bounce off top and bottom walls
    if ball_pos[1] >= HEIGHT - 1 - BALL_RADIUS or ball_pos[1] <= BALL_RADIUS:
        ball_vel[1] *= -1        
    
    #Check gutters:
    #deflect ball back into play if paddle in positio
    #else score point for other player
    right_gutter = WIDTH - 1 - BALL_RADIUS - PAD_WIDTH
    left_gutter = BALL_RADIUS + PAD_WIDTH
    if ball_pos[0] >= right_gutter:
        if paddle2_pos >= ball_pos[1] - HALF_PAD_HEIGHT and paddle2_pos <= ball_pos[1] + HALF_PAD_HEIGHT:
            ball_vel[0] *= -BALL_VEL_INC_FACTOR
            ball_vel[1] *= BALL_VEL_INC_FACTOR
        else:
            score1 += 1
            spawn_ball(LEFT)
    elif ball_pos[0] <= left_gutter:
        if paddle1_pos >= ball_pos[1] - HALF_PAD_HEIGHT and paddle1_pos <= ball_pos[1] + HALF_PAD_HEIGHT:
            ball_vel[0] *= -BALL_VEL_INC_FACTOR
            ball_vel[1] *= BALL_VEL_INC_FACTOR
        else:
            score2 += 1
            spawn_ball(RIGHT)
        
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "Red", "White")

    # update paddle 1 vertical position; keep paddle on the screen
    if paddle1_vel <= 0:
        paddle1_pos = max(paddle1_pos + paddle1_vel, HALF_PAD_HEIGHT)
    else:
        paddle1_pos = min(paddle1_pos + paddle1_vel, HEIGHT - 1 - HALF_PAD_HEIGHT)
        
    # draw paddle 1
    pad1_ul = [0,paddle1_pos - HALF_PAD_HEIGHT]
    pad1_ur = [PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT]
    pad1_lr = [PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT]
    pad1_ll = [0, paddle1_pos + HALF_PAD_HEIGHT]
    canvas.draw_polygon([pad1_ul, pad1_ur, pad1_lr, pad1_ll], 1, 'Blue', 'White')
    
    #update paddle 2; keep on screen
    if paddle2_vel <= 0:
        paddle2_pos = max(paddle2_pos + paddle2_vel, HALF_PAD_HEIGHT)
    else:
        paddle2_pos = min(paddle2_pos + paddle2_vel, HEIGHT - 1 - HALF_PAD_HEIGHT)
    
    # draw paddle 2    
    pad2_ul = [WIDTH - 1 - PAD_WIDTH , paddle2_pos - HALF_PAD_HEIGHT]
    pad2_ur = [WIDTH - 1 , paddle2_pos - HALF_PAD_HEIGHT]
    pad2_lr = [WIDTH - 1 , paddle2_pos + HALF_PAD_HEIGHT]
    pad2_ll = [WIDTH - 1 - PAD_WIDTH , paddle2_pos + HALF_PAD_HEIGHT]
    canvas.draw_polygon([pad2_ul, pad2_ur, pad2_lr, pad2_ll], 1, 'Blue', 'White')
    
    # draw scores
    if score1 > score2:
        col1 = "Red"
        col2 = "Blue"
    elif score1 < score2:
        col1 = "Blue"
        col2 = "Red"
    else:
        col1 = "Green"
        col2 = "Green"
    canvas.draw_text(str(score1), (200, 50), 36, col1)    
    canvas.draw_text(str(score2), (400, 50), 36, col2)    
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel  = -2
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel  = 2 
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel  = -2
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel  = 2
   
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]:
        paddle1_vel  = 0
    elif key == simplegui.KEY_MAP["up"] or key == simplegui.KEY_MAP["down"]:
        paddle2_vel  = 0

def restart_buttonpress():
    new_game()

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)

#register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", restart_buttonpress)

# start frame
new_game()
frame.start()
