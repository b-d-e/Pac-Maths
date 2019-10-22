### IMPORT LIBRAIRES & DEPENDENCIES ###
import pygame as pg # imports the pygame library under the name 'pg'
import random  # imports the random library
from datetime import datetime # imports datetime method from datetime library
import time # imports time library
import sys # imports system library
from settings import * # imports all attributes and methods from settings library
from sprites import * # imports all attributes and methods from sprites library

### A CLASS FOR THE START SPLASH SCREEN ###
class Startup:
    def __init__(self):
        # a method to initialise this class
        pg.init() # initialises the pygame module
        pg.mixer.init() # initialise sound playback within pygame
        if FULLSCREEN == False: # by default this is false
            self.screen = pg.display.set_mode((WIDTH, HEIGHT)) # sets dimensions of the pygame screen
        else: # for the potential use of fullscreen mode
            self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN) # sets dimensions to fill current windows display resolution
        pg.display.set_caption("PacMaths Start Screen!") # sets the title of the window
        self.game_icon = pg.image.load(os.path.join(IMG_DIR, 'logo.png')) # loads the window icon
        pg.display.set_icon(self.game_icon) # sets the pygame window icon to a pacman character image
        self.clock = pg.time.Clock() # makes a game clock
        self.running = True # starts the game running (essentially indicates initialisation is complete)

    def new(self):
        # a method to start a new screen using this class, called the first time it is run
        pg.mixer.music.load(os.path.join(SND_DIR, 'startup_msc.wav')) # load game music
        pg.mixer.music.set_volume(1) # sets the volume of the music channel in the pygame mixer
        if MUTE == False: # if volume is on in settings, by default
            pg.mixer.music.play(-1) # play game music on infinite loop
        f = open(os.path.join(S_DIR, "Highscore.txt"), "r") # loads high score file from scr directory in read mode
        self.last_hs = f.read() #reads contents of high score and stores it as a variable
        f.close() # closes high score file
        self.run() # starts the main loop of the class

    def run(self):
        # a method used to execute the main loop for the start screen
        self.playing = True # playing the game
        while self.playing: # while playing the game
            self.clock.tick(FPS) # iterates clock at the frames per second rate
            self.draw() # draws content to screen
            self.check_key_press() # checks for key press

    def draw(self):
        # a method used to draw content to the screen
        self.screen.fill(BLACK) # draws a black background
        self.draw_text("PACMATHS", YELLOW, 75, FONTS[1], WIDTH/2, 45) # write title
        self.draw_text(("High Score: " + self.last_hs), WHITE, 35, FONTS[0], WIDTH/2, 100) # write high score
        self.draw_text("Press any key to start", WHITE, 40, FONTS[0], WIDTH/2, HEIGHT/2-60) # write instruction 1
        self.draw_text("Collect all of the dots using WASD to move.", WHITE, 20, FONTS[0], WIDTH/2, HEIGHT/2 + 60) # write instruction 2
        self.draw_text("Then answer as many questions as you can.", WHITE, 20, FONTS[0], WIDTH/2, HEIGHT/2 + 90) # write instruction 3

        pg.display.flip() # updates screen with new graphics

    def check_key_press(self):
        # a method used to check whether any keys have been pressed since the last time it was called
        for event in pg.event.get(): # for every event that has occured
            if event.type == pg.KEYUP: # if key up occurs
                self.playing = False # stops startup class from playing
                self.running = False # stop startup class from running
            elif event.type == pg.QUIT: # if event is clicking 'x'
                pg.quit() # closes the pygame window
                sys.exit() # shuts down python in a controlled manner

    def draw_text(self, text, colour, size, font, x, y):
        # a method used to draw a string of text to a location on the screen in a specified format
        font = pg.font.Font(font, size) # calls the Pygame font class
        text_surf = font.render(text, True, colour) # renders the txt within that font
        text_rect = text_surf.get_rect() # gets the rect for that font
        text_rect.centerx = x # positions the text at the specified x coordinate
        text_rect.centery = y # positions the text at the specified y coordinate
        self.screen.blit(text_surf, text_rect) # blits the text to the screen surface

### A CLASS FOR THE GAMEPLAY PHASE OF THE PRODUCT ###
class Game:
    def __init__(self):
        # a method used to initialise this class
        pg.init() # initialises the pygame module
        pg.mixer.init() # initialise sound playback within pygame
        if FULLSCREEN == False: # by default this is false
            self.screen = pg.display.set_mode((WIDTH, HEIGHT)) # sets dimensions of the pygame screen
        else: # for the potential use of fullscreen mode
            self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN) # sets dimensions to fill current windows display resolution
        pg.display.set_caption("PacMaths Game!") # sets the title of the window
        self.game_icon = pg.image.load(os.path.join(IMG_DIR, 'logo.png')) # loads the window icon
        pg.display.set_icon(self.game_icon) # sets the icon of the pygame window to the pacman logo
        self.clock = pg.time.Clock() # makes a game clock
        self.running = True # starts the game running

    def new(self):
        # a method to start a new instance of the game
        # creates sprite groups
        self.all_sprites = pg.sprite.Group() # the group all sprites will be in
        self.all_walls = pg.sprite.Group() # a special group for wall items
        self.all_ghosts = pg.sprite.Group() # a special group for ghost sprites
        self.all_dots = pg.sprite.Group() # a special group for dot sprites
        self.all_hearts = pg.sprite.Group() # a special group for heart sprites
        self.player = pg.sprite.Group() # a special group to hold only the player sprite

        # loads powerup images
        self.dot_image = pg.image.load(os.path.join(IMG_DIR, 'white_dot.png')) # loads image for dots
        self.heart_image = pg.image.load(os.path.join(IMG_DIR, 'heart.png')) # loads image for hearts
        self.dot_image = pg.transform.scale(self.dot_image, (13, 13)) # resizes dot_image
        self.heart_image = pg.transform.scale(self.heart_image, (25, 25)) # resizes heart_image

        # initialises key counter variables
        self.num_dots = 0 # initialises the total number of dots that are shown on screen
        self.dot_score = 0 # initialises score
        self.life_count = 0 # initialises lives

        # loads and plays music
        pg.mixer.music.load(os.path.join(SND_DIR, 'game_msc.wav')) # load game music file
        pg.mixer.music.set_volume(0.6) # sets volume of music channel in pygame mixer
        if MUTE == False: # if not set to mute
            pg.mixer.music.play(-1) # play game music on infinite loop
        self.read_map_file() # calls method to read map from storage
        self.create_map() # reads method to generate the game map from the map file
        self.run() # runs the game

    def run(self):
        # a method to run the main Game loop
        self.playing = True # playing the game
        while self.playing: # while playing the game
            self.clock.tick(FPS) # iterates clock
            self.events() # check for events
            self.update() # runs all update procedures
            self.draw() # draws content to screen

    def update(self):
        # a method to reguarly update the main Game loop
        self.all_sprites.update() # runs update procedure for every sprite in all_sprites
        # check for all dots collected
        if self.dot_score == self.num_dots: # if all dots have been collected
                if GOD_MODE == False: # if not in debug 'god' mode - this a mode for testing purposes which prevents the player from dying in the game phase
                    self.playing = False # terminate gameplay
                    self.running = False # kill session
        # write frame rate for debugging purposes
        if DEBUG == True: # if debugging
            pg.display.set_caption(str(self.clock.get_fps())) # write current fps to title

    def events(self):
        # a method check for events
        for event in pg.event.get(): # for every event that has occured
            # check for clicking 'x' to close window
            if event.type == pg.QUIT: # if event is clicking 'x'
                pg.quit() # quits pygame
                sys.exit() # smoothly exits python

    def draw(self):
        # a method used to draw content to the screen
        self.screen.fill(BLACK) # draws a black background
        self.all_walls.draw(self.screen) # draws walls on top of the background
        self.all_dots.draw(self.screen) # draws dots on top of the background and walls
        self.all_hearts.draw(self.screen) # draws hearts on top of the background, walls and dots
        self.all_ghosts.draw(self.screen) # draws ghosts on top of the background, walls, dots and hearts
        self.player.draw(self.screen) # draws player on top of the background, walls, dots, hearts and ghosts
        self.draw_text(("Score: " + str(self.dot_score)), WHITE, 30, FONTS[1], 1, 24) # draws text
        for i in range(self.life_count): # for the number of lives currently accumulated
            heart = Heart(self, 13 - i, 24) # draw a heart at the bottom of the screen
        # self.draw_text("PACMATHS", YELLOW, 30, FONTS[1], 5, 0)

        pg.display.flip() # updates screen with new graphics

    def read_map_file(self):
        # a method used to read the map file and format it into an executable format
        f = open(map_file, 'r') # opens the map file in read mode
        self.map_string = f.read() # takes the contents of the map and saves it to a string
        f.close() # closes the map file
        self.map_array = self.map_string.splitlines() # splits string into array at new line break
        for i in range(len(self.map_array)): # takes each item (line from file)
            self.map_array[i] = list(self.map_array[i]) # splits it further into individual characters within a 2 dimensional array

    def create_map(self):
        # a method used to take the map data and draw the map sprites onto the screen
        for y in range(0, len(self.map_array)): # takes each line of the map
            for x in range(0, len(self.map_array[y])): # takes each character from that line
                if self.map_array[y][x] == "w": # if character represents wall
                    wall = Wall(self, x, y) # spawn wall in that location
                elif self.map_array[y][x] == "p": # if character represents player
                    player = Player(self, x, y) # spwan player in that location
                elif (self.map_array[y][x] == "1" or self.map_array[y][x] == "2" or self.map_array[y][x] == "3" or self.map_array[y][x] == "4"):
                # if character represents ghost
                    ghost = Ghost(self, x, y, self.map_array[y][x]) # spawn that particular ghost in that location
                    dot = Dot(self, x, y) # spawn dot in that location
                    self.num_dots += 1 # adds one to the total number of dots drawn
                elif self.map_array[y][x] == "0": # if character represents dot
                    dot = Dot(self, x, y) # spawn dot in that location
                    self.num_dots += 1 # adds one to the total number of dots drawn
                elif self.map_array[y][x] == "h": # if character represents heart
                    heart = Heart(self, x, y) # spawn heart in that location

    def draw_text(self, text, colour, size, font, x, y):
        # a method used to draw a string of text to a location on the screen in a specified format
        font = pg.font.Font(font, size) # calls the Pygame font class
        text_surf = font.render(text, True, colour) # renders the txt within that font
        text_rect = text_surf.get_rect() # gets the rect for that font
        text_rect.x = x * tile_length # positions the text at the specified x coordinate
        text_rect.y = y * tile_length # positions the text at the specified y coordinate
        self.screen.blit(text_surf, text_rect) # blits the text to the screen surface


### A CLASS FOR THE QUESTION PHASE OF THE PRODUCT ###
class Questions:
    def __init__(self):
        # a method used to initialise the question class
        pg.init() # initialises the pygame module
        pg.mixer.init() # initialise sound playback within pygame
        if FULLSCREEN == False: # by default this is false
            self.screen = pg.display.set_mode((WIDTH, HEIGHT)) # sets dimensions of the pygame screen
        else: # for the potential use of fullscreen mode
            self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN) # sets dimensions to fill current windows display resolution
        pg.display.set_caption("PacMaths Questions!") # sets the title of the window
        self.clock = pg.time.Clock() # makes a game clock
        self.running = True # starts the game running

    def new(self):
        # a method used to create a new instance of this class
        # creates sprite groups
        self.all_hearts = pg.sprite.Group() # a special group for heart sprites
        self.heart_image = pg.image.load(os.path.join(IMG_DIR, 'heart.png')) # loads image for hearts
        self.heart_image = pg.transform.scale(self.heart_image, (40, 40)) # resizes heart_image

        # loads & plays music
        pg.mixer.music.load(os.path.join(SND_DIR, 'question_msc.wav')) # load question music
        if MUTE == False: # if music set to muted
            pg.mixer.music.play(-1) # play question music on infinite loop

        # initialises key variables
        self.timer = g.dot_score # import timer from game class
        self.o_timer = self.timer # make record of the original timer value
        self.lives = g.life_count # import lives from game class
        self.last_time = pg.time.get_ticks() # initial tick

        self.bg_colour = BLACK # sets background variable to black
        self.bg_num = 0 # 0 is black, 1 is green, 2 is red
        self.new_bg = False # sets a new background boolean to False - the bg does not need changing
        self.bg_changed = True # sets a background change complete indicator to False - the background has not yet changed
        self.feedback_response = False # sets the feedback response boolean to false - the game is not currently giving feedback
        self.question_score = 0 # initialises the question score at 0

        self.current_question = "" # initialises a string containing the current question as empty
        self.current_answer = "" # initialises a string containing the current answer as empty
        self.current_category = -1 # initialises a variable indicating the current category of question being asked. Not currently asking a question so it is initialised to -1 (i.e. not asking)
        self.category_scores = [0,0,0,0] # individual score for each category: addition, subtraction, multiplication, division
        self.new_question = True # indicates a new question should be loaded
        self.selected_answer = -1 # a variable containing the index of the current answer selected
        self.actual_answer = -1 # a variable containing the index of the actual answer
        self.read_files() # calls the read files method for questions and answers to be read from file
        self.run() # runs the main loop

    def run(self):
        # a method used to run the main Question loop
        self.playing = True # playing the game
        while self.playing: # while playing the game
            self.clock.tick(FPS) # iterates clock
            self.events() # check for events
            self.update() # runs all update procedures
            self.draw() # draws content to screen

    def events(self):
        # a method used to check for events
        for event in pg.event.get(): # for every event that has occured
            # check for clicking 'x' to close window
            if event.type == pg.QUIT: # if event is clicking 'x'
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN: # if a mouse key has been pressed (any of 3)
                if event.button == 1: #left
                    x = pg.mouse.get_pos()[0] # get x coordinate of click
                    y = pg.mouse.get_pos()[1] # get y coordinate of click
                    if self.feedback_response == False:
                        if (x>=40)and (x<=230) and (y>=250) and (y<=425): # if in region of box 1
                            self.selected_answer = 0 # set index of answer to box 1
                        else: # stops unnessarilary running of following code
                            if (x>=250) and (x<=440) and (y>=250) and (y<=425): # if in region of box 2
                                self.selected_answer = 1 # set index of answer to box 2
                            else: # stops unnessarilary running of following code
                                if (x>=40)and (x<=230) and (y>=450) and (y<=625): # if in region of box 3
                                    self.selected_answer = 2 # set index of answer to box 3
                                else: # stops unnessarilary running of following code
                                    if (x>=250) and (x<=440) and (y>=450) and (y<=625): # if in region of box 4
                                        self.selected_answer = 3 # set index of answer to box 4
                    if self.feedback_response == True: # if giving feedback
                        if event.type == pg.MOUSEBUTTONDOWN: # check if user has clicked anywhere
                            self.feedback_response = False # if so, stop giving feedback
                            self.new_question = True # and then load the next question
                    if DEBUG == True: # if debugging
                        print(self.selected_answer) # print what the user selected

    def update(self):
        # a method used to continually update the class as it executes
        if (self.timer < 0.1) or (self.lives < 0 and self.new_question == True): # if the timer has run out or lives have run out & question answered incorrectly:
        # note that the timer value is 0.1 not 0 as due to it's variable length there is no way to gauntee this line will execute while the timer is 0
        # hence the check value is slightly above 0 and a comparactive operator is used to check - this prevents underflow of the timer
            self.playing = False # stops the playing of the question class
            self.running = False # stops the running of the question class
        else: # if Question phase still in progress i.e. not yet failed
            self.current_time = pg.time.get_ticks() # gets time now, for future comparative reference
            if ((self.current_time - self.last_time) / 100 > 1) and (self.feedback_response == False): # checks if required interval has passed and if not giving feedback
                self.timer -= 0.1 # decrements timer
                self.last_time = self.current_time # updates last time value with current time
            # write frame rate for debugging purposes
            if DEBUG == True: # if debugging
                pg.display.set_caption(str(self.clock.get_fps())) # write current fps to title
            if self.new_question == True: # if new question needs to be picked
                try: # attempts to get lowest category scrore
                    self.current_category = random.choice(self.get_lowest(self.category_scores)) # generate worst category indexes to indicate which category the user is performing least well in.
                except: # as a failsafe (sometimes above line does not work, this line will randomly pick a category)
                    self.current_category = random.choice([0,1,2,3]) # randomly picks one of the question categories
                q_data = random.choice(self.QandA[self.current_category]) # randomly picks q&a for worst category[s] for the current user – these are the categories for which the user has the lowest score
                self.current_question = q_data[0] # sets question
                self.current_answer = q_data[1] # sets answer
                self.mult_answers = self.pick_answers(self.current_answer) # randomly pick answers and shuffle
                if DEBUG == True: # if debuggine mode is on
                    print(self.mult_answers) # prints the set of answers to the terminal
                self.new_question = False # made False until answered correctly
            if self.selected_answer == self.actual_answer: # if the clicked the correct box
                self.answer_correct() # runs the answer correct method
            elif self.selected_answer != -1: # if they clicked an incorrect box
                    self.answer_incorrect() # runs the answer incorrect method

    def draw(self):
        # a method used to draw content onto the screen in the Question phase
        # the first section handles the background colour changing in response to correct/incorrect answers
        if self.new_bg == True: # if temp bg in progress
            if self.bg_changed == False: # if not yet changed
                if self.bg_num == 0: # if background should be black
                    self.bg_colour = BLACK # set black
                elif self.bg_num == 1: # if background should be green
                    self.bg_colour = DGREEN # set green
                elif self.bg_num == 2: # if background should be red
                    self.bg_colour = RED # set red
                self.time_changed = time.time() # get current time
                self.bg_changed = True # declare background has changed
            if time.time() - self.time_changed > 0.5: # if half a second has passed since changed
                self.bg_colour = BLACK # revert to black
                self.new_bg = False # temporary background no longer in progress
        self.screen.fill(self.bg_colour) # draws a black background
        self.draw_text("QUESTIONS", YELLOW, 75, FONTS[1], WIDTH/2, 45) # draws title text at top of screen
        # self.draw_text(str(self.timer), RED, 100, FONTS[1], 0.75, 6) ######
        pg.draw.rect(self.screen, WHITE, pg.Rect(40, 90, ((self.timer/self.o_timer)*400), 20), 0) # draws timer as time remaining proportional to the original time
        for i in range(self.lives): # for the number of lives currently accumulated
            self.screen.blit(self.heart_image, ((WIDTH/2)-20, (20+(1.5*i))*tile_length)) # draws a heart image at the bottom of the screen
        # draw question
        pg.draw.rect(self.screen, BLUE, pg.Rect(40, 140, WIDTH-80, 80), 0) # question box
        self.draw_text(self.current_question, WHITE, 80, FONTS[0], WIDTH/2, 180) # question text
        # draw answers
        pg.draw.rect(self.screen, RED, pg.Rect(40, 250, 190, 175), 0) # box 1
        pg.draw.rect(self.screen, PINK, pg.Rect(250, 250, 190, 175), 0) # box 2
        pg.draw.rect(self.screen, CYAN, pg.Rect(40, 450, 190, 175), 0) # box 3
        pg.draw.rect(self.screen, ORANGE, pg.Rect(250, 450, 190, 175), 0) # box 4
        self.draw_text(self.mult_answers[0], BLACK, 50, FONTS[0], 135, 337.5) # answer text 1
        self.draw_text(self.mult_answers[1], BLACK, 50, FONTS[0], 345, 337.5) # answer text 2
        self.draw_text(self.mult_answers[2], BLACK, 50, FONTS[0], 135, 537.5) # answer text 3
        self.draw_text(self.mult_answers[3], BLACK, 50, FONTS[0], 345, 537.5) # answer text 4
        if self.feedback_response == True: # if giving feedback to the user
            pg.draw.rect(self.screen, YELLOW, pg.Rect(20, 300, 440, 100), 0) # yellow outline
            pg.draw.rect(self.screen, WHITE, pg.Rect(30, 310, 420, 80), 0) # white box
            self.draw_text(("The correct answer was "+str(self.current_answer)), BLACK, 30, FONTS[0], 240, 350) # black feedback text containing correct answer
            self.draw_text("Click anywhere to dismiss feedback", WHITE, 20, FONTS[0], 240, 650) # informative label

        pg.display.flip() # updates screen with new graphics

    def draw_text(self, text, colour, size, font, x, y):
        # a metod used to draw a string of text to a location on the screen in a specified format
        font = pg.font.Font(font, size) # calls the Pygame font class
        text_surf = font.render(text, True, colour) # renders the txt within that font
        text_rect = text_surf.get_rect() # gets the rect for that font
        text_rect.centerx = x # positions the text at the specified x coordinate
        text_rect.centery = y # positions the text at the specified y coordinate
        self.screen.blit(text_surf, text_rect) # blits the text to the screen surface

    def read_files(self):
        # a method used to import all the questions and answers.
        # import of addition questions and answers
        f = open(os.path.join(Q_DIR, "AddQ.txt"), "rb")  # opens addition questions
        AddQ = f.read().splitlines() # reads into array
        f.close # closes file
        f = open(os.path.join(Q_DIR, "AddA.txt"), "rb") # opens addition answers
        AddA = f.read().splitlines() # reads into array
        f.close # closes file
        #import of subtraction questions and answers, as above
        f = open(os.path.join(Q_DIR, "SubQ.txt"), "rb")
        SubQ = f.read().splitlines()
        f.close
        f = open(os.path.join(Q_DIR, "SubA.txt"), "rb")
        SubA = f.read().splitlines()
        f.close
        #import of multiplication questions and answers, as above
        f = open(os.path.join(Q_DIR, "MultQ.txt"), "rb")
        MultQ = f.read().splitlines()
        f.close
        f = open(os.path.join(Q_DIR, "MultA.txt"), "rb")
        MultA = f.read().splitlines()
        f.close
        #import of subtraction questions and answers, as above
        f = open(os.path.join(Q_DIR, "DivQ.txt"), "rb")
        DivQ = f.read().splitlines()
        f.close
        f = open(os.path.join(Q_DIR, "DivA.txt"), "rb")
        DivA = f.read().splitlines()
        f.close()
        # now take arrays containing composite questions and answers and combine into 4 2d arrays formatted as [[q1,a1],[q2,a2],[q3,a3]]
        add = self.make_2d(AddQ, AddA) # combines addition q&a
        sub = self.make_2d(SubQ, SubA) # combines subtraction q&a
        mult = self.make_2d(MultQ, MultA) # combines multiplication q&a
        div = self.make_2d(DivQ, DivA) # combines division q&a
        self.QandA = [add,sub,mult,div] # makes a master 3 dimensional array using the 4 2d arrays
        if DEBUG == True: # if debuging
            print(self.QandA) # prints master array to terminal

    def make_2d(self, a, b):
        # a method used to make two arrays into a two dimensional array in the format [[q1,a1],[q2,a2],[q3,a3]]
        length = len(a) # gets number of questions
        result = [] # initialises result 2d array
        for i in range(0, length-1): # iterates through each item in each array
            result.append([a[i],b[i]]) # combines corresponding index items
        return result # returns new 2d array

    def get_lowest(self, a):
        # a method used to return the indexes for lowest values from an array
        x = 9999999999 # running lowest value, subject to change if a new lowest is found
        # initialised as a high value so that every other value is properly compared
        for item in a: # check each
            if item<x: # if lower than current lowest
                x = item # becomes new lowest
        results = [] # lowest index array
        for i in range(len(a)):
            if a[i] == x: # checks each result to see if it is one of lowest - this is done to know if the running lowest needs to be replaced with this new value
                results.append(i) # if so adds to array
        return results # returns index of lowest values

    def pick_answers(self, correct):
        # a method used to pick 4 different multiple choice answers, including the correct one, and return them in a random order
        answers = [correct] # starts array
        while len(answers) < 4: # while list not full
            a = random.choice(self.QandA[self.current_category])[1] # randomly picks answer
            if a not in answers: # checks it hasnt already been chosen
                answers.append(a) # adds to list
        shuffled_answers = [] # new shuffle array
        while len(shuffled_answers)<4: # whilst not all answers added to shuffled array
            choice = random.choice(answers) # picks randomly
            if choice not in shuffled_answers: # if not done already
                shuffled_answers.append(choice) # adds to shuffled array
        self.actual_answer = shuffled_answers.index(self.current_answer) # stores the index of the correct answer to the question for future reference
        if DEBUG == True: # if debugging
            print(self.actual_answer) # prints the index of the answer to the terminal
        return shuffled_answers # returns result

    def answer_correct(self):
        # a method used when the user picks a correct response
        CORRECT_FX.play() # play answer correct sound
        self.bg_num = 1 # set bg to green
        self.new_bg = True # declare temporary background in progress
        self.bg_changed = False # declare colour not changed yet
        self.selected_answer = -1 # reset selected answer
        self.question_score += 1 # increment question score
        self.category_scores[self.current_category] += 1 # increment score for that category
        self.new_question = True # load new question
        if DEBUG == True: # if debugging
            print("Correct answer") # prints response to terminal
            print(self.category_scores) # prints scores for each question category to terminal

    def answer_incorrect(self):
        # a method used when the user picks an incorrect answer
        INCORRECT_FX.play() # play answer incorrect sound
        self.bg_num = 2 # set bg to red
        self.new_bg = True # declare temporary background in progress
        self.bg_changed = False # declare colour not changed yet
        self.feedback_response = True
        self.selected_answer = -1 # reset selected answer
        self.lives -= 1 # decrement lives
        self.category_scores[self.current_category] -= 1 # increment score for that category
        if DEBUG == True: # if debugging
            print("Incorrect answer") # prints response to terminal
            print(self.category_scores) # prints scores for each question category to terminal


### A CLASS FOR THE LEADERBOARD PHASE OF THE PRODUCT ###
class Leaderboard:
    def __init__(self):
        # a method used to initialise the class
        pg.init() # initialises the pygame module
        pg.mixer.init() # initialise sound playback within pygame
        if FULLSCREEN == False: # by default this is false
            self.screen = pg.display.set_mode((WIDTH, HEIGHT)) # sets dimensions of the pygame screen
        else: # for the potential use of fullscreen mode
            self.screen = pg.display.set_mode((0, 0), pg.FULLSCREEN) # sets dimensions to fill current windows display resolution
        pg.display.set_caption("PacMaths Leaderboard!") # sets the title of the window
        self.game_icon = pg.image.load(os.path.join(IMG_DIR, 'logo.png')) # loads in the window icon
        pg.display.set_icon(self.game_icon) # sets the pygame window icon to a pacman character image
        self.clock = pg.time.Clock() # makes a game clock
        self.running = True # starts the game running

    def new(self):
        # a method used to start a new instance of the leaderboard class
        self.enter_name = True # signals the player needs to enter their name
        self.file_read = False # boolean to indicate whether the leaderboard has been read from file yet
        self.username = "" # the username value, initialised to a blank string
        self.leaderboard = [] # a blank intialised leaderboard array
        pg.mixer.music.fadeout(2) # fades out quetion music
        #pg.mixer.music.stop() # stops question music
        DEATH_FX.play() # play death sound to signal end of Question phase
        self.run() # calls the run method

    def run(self):
        # a method used to run the main Leaderboard loop that controls this phase of the product
        self.playing = True # playing the game
        while self.playing: # while playing the game
            self.clock.tick(FPS) # iterates clock
            self.events() # check for events
            self.update() # runs all update procedures
            self.draw() # draws content to screen


    def events(self):
        # a method used to check for events
        for event in pg.event.get(): # for every event that has occured
            # check for clicking 'x' to close window
            if event.type == pg.QUIT: # if event is clicking 'x'
                pg.quit() # quits the pygame window
                sys.exit() # smoothly quits the python instance
            # the following code if used to enter the username value
            if self.enter_name == True: # if still need to enter name
                #check for keyboard input
                if event.type == pg.KEYUP: # if a key has been pressed (and lifted backup)
                    if pg.key.name(event.key).isalpha() and len(pg.key.name(event.key)) == 1: #check if the user pressed an alphabet character, and that only one key was pressed
                        if pg.key.get_mods() and (pg.KMOD_CAPS or pg.KMOD_SHIFT): #check for cap locks or shift key
                            self.username += pg.key.name(event.key).upper() #add onto username using uppercase letter
                        else:
                            self.username += pg.key.name(event.key).lower() #add onto username using lowercase letter
                    if event.key == pg.K_BACKSPACE: #check if backspace was pressed
                        self.username = self.username[:-1] #take off the last letter of the username
                    if event.key == pg.K_SPACE: #check if space bar was pressed
                        self.username += ' ' #add a space to username
                    if len(self.username) > 12: #check if username goes over length limit
                        self.username = self.username[:-1] #take off last letter of the username so it is the right length
                    if (event.key == pg.K_RETURN) and (self.username != ""): # check if user has pressed enter
                        self.enter_name = False # end input of username

    def update(self):
        # a method used to update this class while it is executing
        if self.enter_name == False: # if finished entering name
            if self.file_read == False: # if leaderboard needs to be loaded
                f = open(os.path.join(S_DIR, "Leaderboard.txt"), "r") # open leaderboard file in read mode
                raw_leaderboard = f.read().splitlines() # read data of the leaderboard rankings, names and scores into array, splitting items by line
                f.close # close the file to protect integrity
                f = open(os.path.join(S_DIR, "Leaderboard.txt"), "a") # open leaderboard file in append mode
                f.write(self.username+"\n") # write username with a new line after it
                f.write(str(q.question_score)+"\n") # write score with a new line after it
                f.close # close the file to protect integrity
                i = 0 # iterator
                while i < (len(raw_leaderboard)): # while leaderboard not yet fully formatted
                    temp_array = [raw_leaderboard[i], raw_leaderboard[i+1]] # add name and corresponding score to 1d array
                    self.leaderboard.append(temp_array) # make that 1d array an element in the 2d scores array
                    i = i + 2 # iterates by 2
                self.leaderboard.append([self.username, q.question_score]) # adds user's name and score to end of array
                self.leaderboard = self.bubble_sort(self.leaderboard) # sorts array
                if DEBUG == True:
                    print(self.leaderboard) # prints for testing purposes
                f = open(os.path.join(S_DIR, "Highscore.txt"), "r") # opens high score file in read mode
                if q.question_score > int(f.read()): # if high score beaten
                    f.close() # closes file
                    f = open(os.path.join(S_DIR, "Highscore.txt"), "w") # reopens in write mode
                    f.write(str(q.question_score)) # writes new high score
                f.close() # closes file
                self.file_read = True # stops this if statement from returning true and executing again
                pg.mixer.music.load(os.path.join(SND_DIR, 'leaderboard_fx.wav')) # load game music
                if MUTE == False: # if not muted
                    pg.mixer.music.play() # play music once

    def draw(self):
        # a method used to draw content to the screen
        self.screen.fill(BLACK) # draws a black background
        self.draw_text("LEADERBOARD", YELLOW, 60, FONTS[1], WIDTH/2, 45) # draws title text in pacman font
        if self.enter_name == True: # if entering their name
            pg.draw.rect(self.screen, WHITE, pg.Rect(20, 300, 440, 100), 0) # draws white box for name entry
            self.draw_text("Enter your name:", WHITE, 40, FONTS[0], 240, 250) # draws informative label
            self.draw_text(self.username, BLACK, 50, FONTS[0], 240, 350) # draws informative label
        else:
            for i in range(0,len(self.leaderboard)): # for each item in leaderboard
                if i < 10: # until 10 items been drawn
                    pg.draw.rect(self.screen, WHITE, pg.Rect(20, (90+65*i), 55, 55), 0) # draw number boxes
                    pg.draw.rect(self.screen, WHITE, pg.Rect(85, (90+65*i), 285, 55), 0) # draw names boxes
                    pg.draw.rect(self.screen, WHITE, pg.Rect(380, (90+65*i), 80, 55), 0) # draw scores boxes
                    self.draw_text(str((i+1)), BLACK, 46, FONTS[0], 48, ((90+65*i)+(55/2))) # draw number text
                    self.draw_text(self.leaderboard[i][0], BLACK, 46, FONTS[0], 228, ((90+65*i)+(55/2))) # draw name text
                    self.draw_text(str(self.leaderboard[i][1]), BLACK, 46, FONTS[0], 420, ((90+65*i)+(55/2))) # draw score text - the score that this corresponding player attained when they played the game
        pg.display.flip() # flips display

    def draw_text(self, text, colour, size, font, x, y):
        # a method used to draw a string of text to a location on the screen in a specified format
        font = pg.font.Font(font, size) # calls the Pygame font class
        text_surf = font.render(text, True, colour) # renders the txt within that font
        text_rect = text_surf.get_rect() # gets the rect for that font
        text_rect.centerx = x # positions the text at the specified x coordinate
        text_rect.centery = y # positions the text at the specified y coordinate
        self.screen.blit(text_surf, text_rect) # blits the text to the screen surface

    def bubble_sort(self, arr): # arr takes input of an array
        # a method used to sort the leaderboar by order of score
        for loopernum in range(len(arr)-1,0,-1): # makes it run the maximum number of passes to sort
            for i in range(loopernum): # takes each item
                if int(arr[i][1])<int(arr[i+1][1]): # if score of item is bigger than that of item that comes after it in the array
                    temp = arr[i] # stores value from array as temporary variable
                    arr[i] = arr[i+1] # next item goes to current item in the array
                    arr[i+1] = temp # next item in the array becomes temporary variable
        return arr # returns the sorted array

### MASTER GAME LOOP ###
# this handles the linking of the 4 different stages of the game.
while MASTER == True:
    s = Startup() # instantiate startup calss under the variable with name 's'
    while s.running == True: # while startup is running
        s.new() # start new startup
    g = Game() # instantiate game class under the variable with name 'g'
    while g.running == True: # while game is running
        g.new() # start new game
    q = Questions() # instantiate question class under the variable with name 'q'
    while q.running == True: # whilst questions are running
        q.new() # start new questions
    l = Leaderboard() # instantiate leaderboard class under the variable with name 'l'
    while l.running == True: # whilst leaderboard is running
        l.new() # starts new leaderboard
