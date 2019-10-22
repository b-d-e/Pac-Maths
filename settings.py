### IMPORT LIBRAIRES & DEPENDENCIES ###
import os # imports the operating system library
import pygame as pg # imports pygame library under name pg


### KEY SETTINGS AND CONSTANTS ###
# master execution setting
MASTER = True # a master executing boolean (code runs when true)

# debug settings
DEBUG = False # terminal feedback provided when True
GOD_MODE = False # cannot die when True - for testing purposes in the game phase
MUTE = False # sound does not play when True

# experimental features
FULLSCREEN = False # fullscreen game window when True
SCALER = 1 # scales all items up to a different size - not properly implemented

# define window dimensions
WIDTH = 480 * SCALER # 15 tiles
HEIGHT = 800 * SCALER # 25 tiles

# game fonts
FONTS = ['arial.ttf', 'CRACKMAN.ttf']

# directory constants - relative to current working directory
IMG_DIR = str(os.getcwd())+"//Img" # answer directory
SND_DIR = str(os.getcwd())+"//Snd" # sound directory
Q_DIR = str(os.getcwd())+"//Qsn" # question directory
S_DIR = str(os.getcwd())+"//Scr" # score directory

# file specification
map_file = 'map.txt'

# load images
PAC_CLOSED = pg.image.load(os.path.join(IMG_DIR, 'pacman-closed.png')) # pacman mouth closed image
PAC_CLOSED = pg.transform.scale(PAC_CLOSED, (28, 28)) # sizes correcly
PAC_OPEN = pg.image.load(os.path.join(IMG_DIR, 'pacman-open.png')) # pacman mouth open image
PAC_OPEN = pg.transform.scale(PAC_OPEN, (28, 28)) # sizes correctly
WALL_TILE = pg.image.load(os.path.join(IMG_DIR, 'wall.png')) # wall tile image (not used)
WALL_TILE = pg.transform.scale(WALL_TILE, (32, 32)) # sizes correctly
BLINKY = pg.image.load(os.path.join(IMG_DIR, 'blinky.png')) # ghost image
BLINKY = pg.transform.scale(BLINKY, (32, 32)) # sizes correctly
PINKY = pg.image.load(os.path.join(IMG_DIR, 'pinky.png')) # ghost image
PINKY = pg.transform.scale(PINKY, (32, 32)) # sizes correctly
INKY = pg.image.load(os.path.join(IMG_DIR, 'inky.png')) # ghost image
INKY = pg.transform.scale(INKY, (32, 32)) # sizes correctly
CLYDE = pg.image.load(os.path.join(IMG_DIR, 'clyde.png')) # ghost image
CLYDE = pg.transform.scale(CLYDE, (32, 32)) # sizes correctly

# LOAD SOUND FX
pg.mixer.init() # initialises pygame mixer so that sounds can be loaded
CORRECT_FX = pg.mixer.Sound(os.path.join(SND_DIR, 'correct_fx.wav')) # answer correct fx
INCORRECT_FX = pg.mixer.Sound(os.path.join(SND_DIR, 'incorrect_fx.wav')) # answer incorrect fx
DOT_FX = pg.mixer.Sound(os.path.join(SND_DIR, 'eat_fx.wav')) # dot eating fx
HEART_FX = pg.mixer.Sound(os.path.join(SND_DIR, 'heart_fx.wav')) # heart eating fx
DEATH_FX = pg.mixer.Sound(os.path.join(SND_DIR, 'die_fx.wav')) # player death fx

# define refresh rate
FPS = 30 # runs at 30 frames per second

# define colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
PINK = (255, 0, 144)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)
DGREEN = (0, 190, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255 ,0)

# define game map dimensions
tile_length = 32 * SCALER # primarly for game phase as made of regular sized tiles

# define physics constant
player_max_speed = 8
player_deceleration_rate = 0.5
ghost_max_speed = 1
ghost_min_speed = 0.5
