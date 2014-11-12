"""
Interactive Python Programming
Week 8: Part II of RiceRocks
http://www.codeskulptor.org/#user38_o4ZHtdhR2PTBwM1.py
"""

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
FRICTION = .005
THRUST_SCALE_FACTOR = 10.0
MISSILE_TICKS = 120 #about 2 sec?
POINTS_PER_ROCK = 10
ROCK_SPAWN_INTERVAL = 1000 #spawn a rock every 1 sec
SHIP_ROTATION_SCALE_FACTOR = 60.0
TIME_UNTIL_SOUNDTRACK_RESTART = 170000 #3 min long; restart after 170 sec
ROCK_VEL_SPEEDUP_FACTOR = 0.1 #% increase for rock vel, applied
ROCK_VEL_LOWBND = .5
ROCK_VEL_UPBND = 1.5
TIME_UNTIL_ROCK_SPEEDUP = 15000 #once every this many ms for each life; 
number_of_rock_speedups = 0 #increments by 1 as per TIME_UNTIL_ROCK_SPEEDUP; resets to 0 after life lost
score = 0
lives = 3
time = 0.5
started = False
life_lost = False #set to T when a life is lost

#######################
### ImageInfo class ###
#######################
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

##################
### Art Assets ###
##################

#Created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, MISSILE_TICKS)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot1.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

#######################
##### Helper fcns #####
#######################

#handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)

#check if mouse click inside splash image
#center & size are lists of len 2
def calc_rect_boundary(center, size):
    bounds = []
    for idx1 in range(2):
        for idx2 in range(2):
            bounds.append(center[idx1] - (-1) ** (idx2) * size[idx1] / 2)
            
    return bounds

#check if new rock will be too close to ship
#only allow draw if rock at least 3 radii from ship
def too_close(ship_pos, ship_rad, rock_pos, rock_rad):
    return dist(ship_pos, rock_pos) < ship_rad + 3 * rock_rad

#processing a sprite group
def process_sprite_group(group, canvas):
    for elt in set(group):
        elt.draw(canvas)
        life_expired = elt.update()
        if elt.get_lifespan() and life_expired:
            group.remove(elt)

#check for collisions between a single object
#and a group of objects
def group_collide(sprite_group, other_sprite):
    global explosion_group
    collision_occured = False
    for elt in set(sprite_group):
        if elt.collide(other_sprite):
            sprite_group.remove(elt)
            collision_occured = True
            explosion_group.add(Sprite(elt.get_position(), [0,0], 0, 0 , explosion_image, explosion_info))
            explosion_sound.play()
            break
            
    return collision_occured

#check for collisions between objects in
#each of two groups
def group_group_collide(rocks, missiles):
    number_of_rocks_hit = 0
    for missile in set(missiles):
        if group_collide(rocks, missile):
            number_of_rocks_hit += 1
            missiles.remove(missile)
    return number_of_rocks_hit

def soundtrack_restart():
    global started, soundtrack
    if started:
        soundtrack.rewind()
        soundtrack.play()


##################
### Ship class ###
##################
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.forward_vec = 0
        self.tip_offset = 40
        self.missle_vel_factor = 3.0
                
        #pixel offset to grab image with thrusters
        self.thruster_img_offset = 90 

    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.thruster_img_offset, self.image_center[1]], self.image_size, self.pos , self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
    #-update position, wrapping around screen if needed
    #-update velocity; include friction and
    #  acceleration (when thrusters on)
    #-update angle when ship is rotated
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel
        self.forward_vec = angle_to_vector(self.angle)
        self.vel[0] *= (1 - FRICTION)
        self.vel[1] *= (1 - FRICTION)    
        if self.thrust:
            self.vel[0] += self.forward_vec[0] / THRUST_SCALE_FACTOR
            self.vel[1] += self.forward_vec[1] / THRUST_SCALE_FACTOR
        
        
    def rotate(self, direction):
        """
        Input: direction, a value of +1/-1/0
        
        -direction == +1 -> ship rotates clockwise
        -direction == -1 -> ship rotates counterclockwise
        -direction == 0 -> ship does not rotate
        """
        self.angle_vel = math.pi / SHIP_ROTATION_SCALE_FACTOR * direction
    
    #thrusters on/off based on 'up arrow' key down/up
    def thrust_control(self, thrust_flag):
        self.thrust = thrust_flag
        if self.thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
            
    def shoot(self):
        global missile_group, timer_missile
        init_pos = []
        init_vel = []
        for idx in range(2):
            init_pos.append(self.pos[idx] + self.tip_offset * self.forward_vec[idx])
            init_vel.append(self.vel[idx] + self.forward_vec[idx] * self.missle_vel_factor)
            
        missile_group.add(Sprite(init_pos, init_vel, 0, 0, missile_image, missile_info, missile_sound))

####################
### Sprite class ###
####################
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()

    def get_lifespan(self):
        return self.lifespan
    
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def draw(self, canvas):
        #explosion sprite, used when ship or rock is hit
        if self.animated:
            current_tile_index = (self.age % self.get_lifespan()) // 1
            current_tile_center = [self.image_center[0] +  current_tile_index * self.image_size[0], self.image_center[1]]
            canvas.draw_image(self.image, current_tile_center, self.image_size, self.pos, self.image_size) 
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
    def update(self):
        """
        Output:
        --T/F to indicate that a missile should/should not
        be decommissioned (removed)
        """
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel
        if not self.animated:
            self.age += 1 #for missile sprite
        else:
            self.age += 0.4 #for explosion sprite
            
        if self.lifespan:
            return self.age > self.lifespan
        else:
            return False

    def collide(self, other_sprite):
        """
        Input:
        --other_sprite, the obj to check for a collision
        
        Output:
        --True or False if there is/is not a collision
        """
        dist_between = dist(self.get_position(), other_sprite.get_position())
        radii_sum = self.get_radius() + other_sprite.get_radius()
        if dist_between < radii_sum:
            return True
        else:
            return False
            
##############################        
### Draw method for canvas ###
##############################
def draw(canvas):
    global time, lives, score, rock_group, missile_group, started, soundtrack, number_of_rock_speedups, my_ship, life_lost, explosion_group
    
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    
    
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
    else:
        #redraw ship when space permits
        if life_lost:
            too_close_to_rock = False
            for rock in rock_group:
                if too_close(my_ship.get_position(), my_ship.get_radius(), rock.get_position(), rock.get_radius()):
                    too_close_to_rock = True
                    break
                    
            if not too_close_to_rock:
                pos = my_ship.get_position()
                my_ship = None
                my_ship = Ship(pos, [0, 0], 0, ship_image, ship_info)
                my_ship.draw(canvas)
                life_lost = False
                
        #redraw ship unconditionally        
        else:
            my_ship.draw(canvas)
            my_ship.update()
            
        process_sprite_group(rock_group, canvas)
        process_sprite_group(missile_group, canvas)
            
        if not life_lost and group_collide(rock_group, my_ship):
            lives -= 1
            life_lost = True
            number_of_rock_speedups = 0 #reset for next life
                    
        score += POINTS_PER_ROCK * group_group_collide(rock_group, missile_group)
        
        #check for game over
        if lives == 0 and started:
            timer_rock.stop()
            soundtrack.rewind()
            started = False
            rock_group = set([])
            missile_group = set([])
            
    if len(explosion_group) > 0:
        process_sprite_group(explosion_group, canvas)
        
    #text for lives remaining and score
    canvas.draw_text("Score: " + str(score), (650, 50), 24, "White")
    canvas.draw_text("Lives: " + str(lives), (30, 50), 24, "White")

def rock_spawner():
    """
    timer handler for rock spawn
    """
    global rock_group, my_ship
    if len(rock_group) < 12:
        #rand params
        rand_pos = [random.randrange(50, WIDTH - 50), random.randrange(50, HEIGHT - 50)]
        rand_angle = random.random() * 2 * math.pi
        vel_x = random.random() * (ROCK_VEL_UPBND - ROCK_VEL_LOWBND) + ROCK_VEL_LOWBND
        vel_x *= (-1) ** (random.random() <= 0.5) * (1 + ROCK_VEL_SPEEDUP_FACTOR * number_of_rock_speedups)
        vel_y = random.random() * (ROCK_VEL_UPBND - ROCK_VEL_LOWBND) + ROCK_VEL_LOWBND
        vel_y *= (-1) ** (random.random() <= 0.5) * (1 + ROCK_VEL_SPEEDUP_FACTOR * number_of_rock_speedups)
        rand_vel = [vel_x, vel_y]        
        rand_ang_vel = 2.0 * math.pi / 60 * (random.random() * 2  - 1)
        
        #make new rock if not too close to ship
        if not too_close(my_ship.get_position(), my_ship.get_radius(), rand_pos, asteroid_info.get_radius()):
            rock_group.add(Sprite(rand_pos, rand_vel, rand_angle, rand_ang_vel , asteroid_image, asteroid_info))

def mouse_handler(pos):
    """
    Input: pos, the position of the mouse click
    
    -Detect mouse click on opening splash screen 
    -Signals (re)start of game
    """
    global started, splash_info, lives, score, my_ship, soundtrack
    
    [xmin, xmax, ymin, ymax] = calc_rect_boundary([WIDTH / 2, HEIGHT / 2], splash_info.get_size())
    x_cond = pos[0] > xmin and pos[0] <= xmax
    y_cond = pos[1] > ymin and pos[1] <= ymax
    started = (x_cond and y_cond)
    
    if started:
        lives = 3
        score = 0
        my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
        timer_rock.start()
        timer_rock_speedup.start()
        timer_soundtrack.start()
        soundtrack.play()
        
#Make game more challenging: 
#the longer the current life lasts, the higher the velocity 
#of new rocks spawned 
def rock_speedup():
    global number_of_rock_speedups
    number_of_rock_speedups += 1

#keydown and keyup handlers:
#left arrow: rotate counterclockwise; right arrow: rotate clockwise
#up arrow: thrust control
#spacebar: fire missle
def keydown(key):
    global my_ship
    if key == simplegui.KEY_MAP["left"]:
        my_ship.rotate(-1)
    elif key == simplegui.KEY_MAP["right"]:
        my_ship.rotate(1)
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrust_control(True)
    elif key == simplegui.KEY_MAP["space"]:
        my_ship.shoot()
        
def keyup(key):
    global my_ship
    if key == simplegui.KEY_MAP["left"] or key == simplegui.KEY_MAP["right"]:
        my_ship.rotate(0)
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.thrust_control(False)

# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize an empty rock set
rock_group = set([])    

#initialize the ship
my_ship = None

#init empty missle set
missile_group = set([])

#init empty set of explosion sprites
explosion_group = set([])

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_mouseclick_handler(mouse_handler)

timer_rock = simplegui.create_timer(ROCK_SPAWN_INTERVAL, rock_spawner)
timer_soundtrack = simplegui.create_timer(TIME_UNTIL_SOUNDTRACK_RESTART, soundtrack_restart)
timer_rock_speedup = simplegui.create_timer(TIME_UNTIL_ROCK_SPEEDUP, rock_speedup)

# get things rolling
frame.start()
