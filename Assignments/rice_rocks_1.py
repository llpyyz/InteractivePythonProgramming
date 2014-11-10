"""
Interactive Python Programming
Week 7: Part I of RiceRocks
http://www.codeskulptor.org/#user38_lJfyZFxwgQrR0Db.py

"""

import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
FRICTION = .005
THRUST_SCALE_FACTOR = 20.0
score = 0
lives = 3
time = 0.5

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

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
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
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
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

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
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
        self.missle_vel_factor = 2.0
        #print "ang: ", self.angle, "forward vec:", self.forward_vec
                
        #pixel offset to grab image with thrusters
        self.thruster_img_offset = 90 
            
    def draw(self,canvas):
        if self.thrust:
            canvas.draw_image(self.image, [self.image_center[0] + self.thruster_img_offset, self.image_center[1]], self.image_size, self.pos , self.image_size, self.angle)
        else:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
    #-update position, wrapping around screen if needed
    #-update velocity, to include friction and also
    #  acceleration when thrusters are on
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
        self.angle_vel = math.pi / 30.0 * direction
    
    #thrusters on/off based on 'up arrow' key down/up
    def thrust_control(self, thrust_flag):
        self.thrust = thrust_flag
        if self.thrust:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()
            
    def shoot(self):
        global a_missile, timer_missile
        init_pos = []
        init_vel = []
        for idx in range(2):
            init_pos.append(self.pos[idx] + self.tip_offset * self.forward_vec[idx])
            init_vel.append(self.vel[idx] + self.forward_vec[idx] * self.missle_vel_factor)
            
        a_missile = Sprite(init_pos, init_vel, 0, 0, missile_image, missile_info, missile_sound)
        timer_missile.start()
        
# Sprite class
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
   
    def draw(self, canvas):
        canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
    
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel

#Draw method for canvas
def draw(canvas):
    global time, lives, score
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    if a_missile:
        a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    if a_missile:
        a_missile.update()
    
    #text for lives remaining and score
    canvas.draw_text("Score: " + str(score), (700, 50), 24, "White")
    canvas.draw_text("Lives: " + str(lives), (30, 50), 24, "White")
            
# timer handler that spawns a rock
def rock_spawner():
    global a_rock
    #random params
    rand_pos = [random.randrange(50, WIDTH - 50), random.randrange(50, HEIGHT - 50)]
    rand_angle = random.random() * 2 * math.pi
    rand_vel = [random.random(), random.random()]
    rand_ang_vel = 2.0 * math.pi / 60 * (random.random() * 2  - 1) 
    
    a_rock = Sprite(rand_pos, rand_vel, rand_angle, rand_ang_vel , asteroid_image, asteroid_info)

def missile_remove():
    global timer_missile, a_missile
    timer_missile.stop()
    a_missile = None
    
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

# initialize a rock
rand_pos = [random.randrange(50, WIDTH - 50), random.randrange(50, HEIGHT - 50)]
rand_angle = random.random() * 2 * math.pi
rand_vel = [random.random(), random.random()]
rand_ang_vel = 2.0 * math.pi / 60 * (random.random() * 2  - 1)  
a_rock = Sprite(rand_pos, rand_vel, rand_angle, rand_ang_vel , asteroid_image, asteroid_info)
    
#initialize the ship
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

#init a missle
a_missile = Sprite([2 * WIDTH / 3, 2 * HEIGHT / 3], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

timer_rock = simplegui.create_timer(1000.0, rock_spawner)
timer_missile = simplegui.create_timer(5000, missile_remove)

# get things rolling
timer_rock.start()
frame.start()
