### IMPORT LIBRAIRES & DEPENDENCIES ###
import pygame as pg # imports pygame library under name pg
import random # imports random library
import os # impors operating system library
import time # imports time library
from settings import * # imports all methods and attributes froms settings library

### A CLASS FOR THE WALL SPRITES ###
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # a method to initialise this sprite
        self.groups = [game.all_sprites, game.all_walls] # defines groups to be apart of
        pg.sprite.Sprite.__init__(self, self.groups) # initialise the sprite withing the pygame framework
        self.game = game # stores game class locally
        self.image = pg.Surface((tile_length, tile_length)) # creates a square surface
        #self.image = WALL_TILE # sets surface to be wall graphic
        self.image.fill(BLUE) # sets surface colour to blue
        self.rect = self.image.get_rect() # gets rect of surface
        self.x = x # stores x as self variable
        self.y = y # stores y as self variable
        self.rect.x = x * tile_length # places the sprite in the correct x location
        self.rect.y = y * tile_length # places the sprite in the correct y location

### A CLASS FOR THE PLAYER SPRITE ###
class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # a method to initialise this sprite
        self.groups = [game.all_sprites, game.player] # defines groups for Player to be part of
        pg.sprite.Sprite.__init__(self, self.groups)  # initialise the sprite within the pygame framework for given groups
        self.game = game # stores game class locally
        #self.image = pg.Surface((tile_length - 4, tile_length - 4))  # creates a square surface # legacy - uses image now
        #self.image.fill(YELLOW) # sets surface colour to yellow # legacy - uses image now
        self.image = PAC_CLOSED # sets image to the closed mouth pacman image
        self.image_rot = 0 # orients sprite in correct direction (horizontal)
        self.image = pg.transform.rotate(self.image, self.image_rot) # roates sprite to defined orientation
        self.rect = self.image.get_rect() # gets rect of surface
        self.x = x # stores x as self variable
        self.y = y # stores y as self variable
        self.rect.x = x * tile_length + 2 # places the sprite in the correct location horizontaly
        self.rect.y = y * tile_length + 2 # places the sprite in the correct location vertically
        self.h_speed = 0 # initialises speed variables
        self.v_speed = 0

    def check_for_x_wall_collision(self):
        # a method to check for collisons with walls when travelling horizontally
        for wall in self.game.all_walls: # takes each wall sprite individually
            if self.rect.colliderect(wall.rect): # checks whether the sprite has collided with that particular wall
                if self.h_speed > 0: # if the sprite was moving right:
                    self.rect.right = wall.rect.left # the sprite is returned left
                if self.h_speed < 0: # if the sprite was moving left:
                    self.rect.left = wall.rect.right # the sprite is returned right

    def check_for_y_wall_collision(self):
        # a method to check for collisons with walls when travelling verticaly
        for wall in self.game.all_walls: # takes each wall sprite individually
            if self.rect.colliderect(wall.rect): # checks whether the sprite has collided with that particular wall
                if self.v_speed < 0: # if the sprite was moving up:
                    self.rect.top = wall.rect.bottom # the sprite is returned down
                if self.v_speed > 0: # if the sprite was moving down:
                    self.rect.bottom = wall.rect.top # the sprite is returned left

    def check_for_dot_collision(self):
        # a method used to check for collions with white dots
        for dot in self.game.all_dots: # take each heart individually
            if self.rect.colliderect(dot.rect): # checks for collision between player and heart
                dot.kill() # removes heart from map
                DOT_FX.play() # play eating effect
                self.game.dot_score += 1 # increments lives by 1
                self.image = PAC_OPEN # opens pacman mouth
                self.image_changed = True # declares image is not default
                self.time_changed = time.time() # denotes time when mouth of sprite opened

    def check_for_heart_collision(self):
        # a method used to check for colisions with hearts
        for heart in self.game.all_hearts: # take each dot individually
            if self.rect.colliderect(heart.rect): # checks for collision between player and dot
                heart.kill() # removes dot from map
                HEART_FX.play() # play effect
                self.game.life_count += 1 # increments score by 1

    def check_for_ghost_collision(self):
        # a method used to check for colisions with ghosts
        for ghost in self.game.all_ghosts: # take each ghost individually
            if self.rect.colliderect(ghost.rect): # if player collided with that ghost
                DEATH_FX.play() # play death sound
                if GOD_MODE == False: # if able to die (default)
                    self.game.playing = False # terminate gameplay
                    self.game.running = False # kill session

    def update(self):
        # a method used to update this sprite
        keystate = pg.key.get_pressed() # creates list of booleans representing pressed keys (TRUE if has been pressed, else FALSE)
        if keystate[pg.K_LEFT] or keystate[pg.K_a]: # if player pressed Left Arrow or a key
            self.h_speed = - player_max_speed # player moves left
            #self.image_rot = 180
        elif keystate[pg.K_RIGHT] or keystate[pg.K_d]: # if player pressed Right Arrow or d key
            self.h_speed = player_max_speed # player moves right
            #self.image_rot = 0
        if keystate[pg.K_DOWN] or keystate[pg.K_s]: # if player pressed Up Arrow or s key
            self.v_speed = player_max_speed # player moves up
            #self.image_rot = 90
        elif keystate[pg.K_UP] or keystate[pg.K_w]: # if player pressed Down Arrow or d key
            self.v_speed = - player_max_speed # player moves down
            #self.image_rot = 270
        if self.image == PAC_OPEN: # if mouth open
            if time.time() - self.time_changed > 0.25: # if has been open for more than quarter a second
                self.image = PAC_CLOSED # reset image
        if self.h_speed == 0 and self.v_speed == 0:
            self.image_rot = 0
        #self.image = pg.transform.rotate(self.image, self.image_rot)


        if ((keystate[pg.K_LEFT] == False) and (keystate[pg.K_a] == False)) and ((keystate[pg.K_RIGHT] == False) and (keystate[pg.K_d] == False)):
# if the player hasn't pressed Left Arrow, a key, Right arrow, and d key
            if self.h_speed > 0: # if moving right
                self.h_speed -= player_deceleration_rate # decrease speed
            else: # moving left
                self.h_speed += player_deceleration_rate # increase speed
        if ((keystate[pg.K_UP] == False) and (keystate[pg.K_w] == False)) and ((keystate[pg.K_DOWN] == False) and (keystate[pg.K_s] == False)):
# if the player hasn't pressed Up Arrow, w key, Down arrow, and s key
            if self.v_speed > 0: # if moving up
                self.v_speed -= player_deceleration_rate # decrease speed
            else: # moving down
                self.v_speed += player_deceleration_rate # increase speed

        self.temp_h_speed = self.h_speed # temporary horizontal speed
        self.temp_v_speed = self.v_speed # temporary vertical speed

        self.v_speed = 0 # vertical speed set to 0 to remove chance of affecting horizontal wall collision check
        self.rect.x += self.h_speed # moves horizontaly
        self.check_for_x_wall_collision() # checks for horizontal wall collisions
        self.h_speed = 0 # horizontal speed set to 0 to remove chance of affecting vertical wall collision check
        self.v_speed = self.temp_v_speed # restores vertical speed
        self.rect.y += self.v_speed # moves verticaly
        self.check_for_y_wall_collision() # checks for vertical wall collisions
        self.h_speed = self.temp_h_speed # restores horizontal speed

        self.check_for_dot_collision() # runs dot collison check method
        self.check_for_heart_collision() # runs heart collision check method
        self.check_for_ghost_collision() # runs ghost colliosn check method

### A CLASS FOR THE GHOST SPRITE ###
class Ghost(pg.sprite.Sprite):
    def __init__(self, game, x, y, type):
        # a method used to initialise this sprite
        self.groups = [game.all_sprites, game.all_ghosts] # list of groups for the ghost to be a part of
        pg.sprite.Sprite.__init__(self, self.groups)  # initialise the sprite within the pygame framework
        self.game = game # saves game within class
        self.type = int(type) # saves type as integer within class
        #self.image = pg.Surface((tile_length - 4, tile_length - 4))  # creates a square surface
        if self.type == 1: # if the colour attribute is red
            #colour = RED # set colour to red
            self.image = BLINKY
        elif self.type == 2: # if the colour attribute is cyan
            #colour = CYAN # set colour to cyan
            self.image = PINKY
        elif self.type == 3: # if the colour attribute is orange
            #colour = ORANGE # set colour to orange
            self.image = INKY
        else: # if the colour is pink
            #colour = PINK # set colour attribute to pink
            self.image = CLYDE
        #self.image.fill(colour) # fills rect with that colour
        self.rect = self.image.get_rect() # generates pygame rect from surface
        self.x = x # saves x start position within class
        self.y = y # saves y start position within class
        self.rect.x = x * tile_length + 2 # places the sprite in the correct x location (centraly)
        self.rect.y = y * tile_length + 2 # places the sprite in the correct y location (centraly)
        self.speed = random.randrange(ghost_min_speed * 10, ghost_max_speed * 10, 2)/2
        #generates random speed of ghost within given range
        self.h_speed = 0 # initialises horizontal speed
        self.v_speed = 0 # initialises vertical speed
        self.has_collided = False # variable to inform update procedure whether to change direction
        self.dir = random.choice(["v","h"]) # chooses the start direction randomly
        if self.dir == "v": # if vertical
            self.v_speed = random.choice([-1,1]) * self.speed # chooses up or down randomly
        else: # if horizontal
            self.h_speed = random.choice([-1,1]) * self.speed # choses left or right randomly

    def check_for_ghost_collision(self):
        # a method used to check whether a ghost has hit another ghost
        for ghost in self.game.all_ghosts: # iterates through each of the other ghosts from the ghost group
            if self.rect.colliderect(ghost) and self != ghost: # if hit ghost
                self.h_speed *= -1 # opposite horizontal
                self.v_speed *= -1 # opposite vertical

    def check_for_x_wall_collision(self):
        # a method used to check for a collision with a wall whilst travelling horizonatally
        for wall in self.game.all_walls: # takes each wall sprite individually
            if self.rect.colliderect(wall.rect): # checks whether the sprite has collided with that particular wall
                if self.h_speed > 0: # if the sprite was moving right:
                    self.rect.right = wall.rect.left # the sprite is moved back left
                if self.h_speed < 0: # if the sprite was moving left:
                    self.rect.left = wall.rect.right # the sprite is moved back right
                self.has_collided = True # declare a collision occured to the update section

    def check_for_y_wall_collision(self):
        # a method used to check for a collision with a wall whilst travelling vertically
        for wall in self.game.all_walls: # takes each wall sprite individually
            if self.rect.colliderect(wall.rect): # checks whether the sprite has collided with that particular wall
                if self.v_speed < 0: # if the sprite was moving up:
                    self.rect.top = wall.rect.bottom # the sprite is moved back down
                if self.v_speed > 0: # m if the sprite was moving down:
                    self.rect.bottom = wall.rect.top # the sprite is moved back left
                self.has_collided = True # declare a collision occured to the update section

    def update(self):
        # a method used to update this sprite
        if self.has_collided == True: # if has collided with wall
            self.has_collided = False # reset has_collided boolean to false so statement not retriggered
            if self.v_speed != 0: # if moving verticaly
                self.v_speed = 0 # stop moving verticaly
                self.h_speed = random.choice([1,  -1]) * self.speed # randomly pick left or right to move
            else: # moving horizontaly
                self.h_speed = 0 # stop moving horizontaly
                self.v_speed = random.choice([1, -1]) * self.speed # randomly pick up or down to move

        self.rect.x += self.h_speed # move rect horizontally
        self.rect.y += self.v_speed # move rect verticaly
        if self.h_speed != 0: # if moving horizontally
            self.check_for_x_wall_collision() # check for a horizontal collison
        else: # if moving vertically
            self.check_for_y_wall_collision() # check for a vertical collision
        self.check_for_ghost_collision() # check to see if has hit another ghost

### A CLASS FOR THE DOT SPRITE ###
class Dot(pg.sprite.Sprite):
    def __init__(self, game, x, y):
            # a method used to intialise the sprite
            self.groups = [game.all_sprites, game.all_dots] # list of groups for the ghost to be a part of
            pg.sprite.Sprite.__init__(self, self.groups)  # initialise the sprite within the pygame framework
            self.game = game # saves game within class
            self.image = self.game.dot_image # sets image of dot to preloaded png
            self.rect = self.image.get_rect() # gets rect of that image
            self.x = x # stores x as self variable
            self.y = y # stores y as self variable
            self.rect.x = self.x * tile_length + 7.5 # positions rect horizontally
            self.rect.y = self.y * tile_length + 7.5 # positions rect vertically

### A CLASS FOR THE HEART SPRITE ###
class Heart(pg.sprite.Sprite):
    def __init__(self, game, x, y):
            # a method used to intialise the sprite
            self.groups = [game.all_sprites, game.all_hearts] # list of groups for the ghost to be a part of
            pg.sprite.Sprite.__init__(self, self.groups)  # initialise the sprite within the pygame framework
            self.game = game # saves class which called as variable
            self.image = self.game.heart_image # sets image of heart to preloaded png
            self.rect = self.image.get_rect() # gets rect of image
            self.x = x # stores x as self variable
            self.y = y # stores y as self variable
            self.rect.x = self.x * tile_length + 5 # positions rect horizontaly
            self.rect.y = self.y * tile_length + 5 # postions rect vertically
