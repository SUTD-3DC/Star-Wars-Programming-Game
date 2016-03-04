#batman is the best
from collections import deque
import pygame, ezpztext
import time
import random
import threading
import traceback
import pygame
import os
import sys
from pygame import *
from pygame.locals import *

from Movement import Movement
from Hole import Hole
from Timer import Timer
import ParserThread
import util

pygame.init()

level = 9
numOfLevels = 10
rebelScore = 0

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0, 255, 0)
yellow = (255, 255, 0)
grey = (96, 125, 139)
orange = (255, 87, 34)

# default colour for text editor font
txtfont_default = white
txtfont_focus = green

# Global settings
control_mode = 'TYPE' # 'KEYPRESS' or 'TYPE'
time_limit = 20 # Time limit that affects Time Bar and Duration countdown

# Use a timer
timer = Timer()

# Use the Movement class to keep track of movements
movement = Movement(1)

# Game state
game_state = 'idle'
parsing = False

#textbox
txtbx = ezpztext.Textbox(lines=14, default_color=txtfont_default,
            focus_color=txtfont_focus, maxlength=28, y=60, x=840)

for i in range(len(txtbx.txtbx)):
    txtbx.txtbx[i].prompt = "{:>2}: ".format(i + 1)

# Use ParserThread to create a separate thread for parsing user code
parser_thread = ParserThread.Thread()

map_width = 800
map_height = 600
status_bar = 40
display_width = map_width +400
display_height = map_height + status_bar

lead_x = 750
lead_y = 540
lead_direction = 'down'
blueprintCollected = False
blueprintExist = False
rebelScore = 0

BlueprintThickness = 30
block_size = 10
FPS = 30
gameDisplay = pygame.display.set_mode((display_width,display_height))
##gameDisplay = pygame.display.set_mode((display_width,display_height),FULLSCREEN)
pygame.display.set_caption('Star Wars: A programming education game')

wallpaper_img = util.load_image('wallpaper/Wallpaper.png')
text_editor_img = util.load_image('pictures/right panel/Text editor.png')
maps = ['pictures/Map/warm_up.png',
           'pictures/Map/Map_0.png','pictures/Map/Map_4.png','pictures/Map/Balcony_map.png',
           'pictures/Map/Map_1.png','pictures/Map/SU.png','pictures/Map/Map_3.png',
           'pictures/Map/Map_5.png','pictures/Map/docking_bay.png','pictures/Map/Last_level_map_space.png']

map_img = [util.load_image(m) for m in maps]

lukeUpStationary = util.load_image('pictures/lukeMove/Luke_up_stationary.png')
lukeUpWalk1 = util.load_image('pictures/lukeMove/Luke_up_walk_1.png')
lukeUpWalk2 = util.load_image('pictures/lukeMove/Luke_up_walk_2.png')
lukeDownStationary = util.load_image('pictures/lukeMove/Luke_down_stationary.png')
lukeDownWalk1 = util.load_image('pictures/lukeMove/Luke_down_walk_1.png')
lukeDownWalk2 = util.load_image('pictures/lukeMove/Luke_down_walk_2.png')
lukeRightStationary = util.load_image('pictures/lukeMove/Luke_right_stationary.png')
lukeRightWalk = util.load_image('pictures/lukeMove/Luke_right_walk_1.png')
lukeLeftStationary = util.load_image('pictures/lukeMove/Luke_left_stationary.png')
lukeLeftWalk = util.load_image('pictures/lukeMove/Luke_left_walk_1.png')

reyUpStationary = util.load_image('pictures/reyMove/Rey_up_stationary.png')
reyUpWalk1 = util.load_image('pictures/reyMove/Rey_up_walk_1.png')
reyUpWalk2 = util.load_image('pictures/reyMove/Rey_up_walk_2.png')
reyDownStationary = util.load_image('pictures/reyMove/Rey_down_stationary.png')
reyDownWalk1 = util.load_image('pictures/reyMove/Rey_down_walk_1.png')
reyDownWalk2 = util.load_image('pictures/reyMove/Rey_down_walk_2.png')
reyRightStationary = util.load_image('pictures/reyMove/Rey_right_stationary.png')
reyRightWalk1 = util.load_image('pictures/reyMove/Rey_right_walk_1.png')
reyRightWalk2 = util.load_image('pictures/reyMove/Rey_right_walk_2.png')
reyLeftStationary = util.load_image('pictures/reyMove/Rey_left_walk_1.png')
reyLeftWalk1 = util.load_image('pictures/reyMove/Rey_left_walk_1.png')
reyLeftWalk2 = util.load_image('pictures/reyMove/Rey_left_walk_2.png')

finnUpStationary = util.load_image('pictures/finnMove/Finn_up_stationary.png')
finnUpWalk1 = util.load_image('pictures/finnMove/Finn_up_walk_1.png')
finnUpWalk2 = util.load_image('pictures/finnMove/Finn_up_walk_2.png')
finnDownStationary = util.load_image('pictures/finnMove/Finn_down_stationary.png')
finnDownWalk1 = util.load_image('pictures/finnMove/Finn_down_walk_1.png')
finnDownWalk2 = util.load_image('pictures/finnMove/Finn_down_walk_2.png')
finnRightStationary = util.load_image('pictures/finnMove/Finn_right_stationary.png')
finnRightWalk1 = util.load_image('pictures/finnMove/Finn_right_walk_1.png')
finnRightWalk2 = util.load_image('pictures/finnMove/Finn_right_walk_2.png')
finnLeftStationary = util.load_image('pictures/finnMove/Finn_left_stationary.png')
finnLeftWalk1 = util.load_image('pictures/finnMove/Finn_left_walk_1.png')
finnLeftWalk2 = util.load_image('pictures/finnMove/Finn_left_walk_2.png')

renUpStationary = util.load_image('pictures/renMove/Ren_up.png')
renDownStationary = util.load_image('pictures/renMove/Ren_down.png')
renRightStationary = util.load_image('pictures/renMove/Ren_right.png')
renLeftStationary = util.load_image('pictures/renMove/Ren_left.png')

darthUpStationary = util.load_image('pictures/darthMove/Darth_up.png')
darthDownStationary = util.load_image('pictures/darthMove/Darth_down.png')
darthRightStationary = util.load_image('pictures/darthMove/Darth_right.png')
darthLeftStationary = util.load_image('pictures/darthMove/Darth_left.png')

stormtUpStationary = util.load_image('pictures/stormtMove/StormT_up.png')
stormtDownStationary = util.load_image('pictures/stormtMove/StormT_down.png')
stormtRightStationary = util.load_image('pictures/stormtMove/StormT_right.png')
stormtLeftStationary = util.load_image('pictures/stormtMove/StormT_left.png')

mFalconStationary = util.load_image('pictures/milleniumFalcon/mFalcon_stationary.png')
mFalconThrusterSmall = util.load_image('pictures/milleniumFalcon/mFalcon_thruster_small.png')
mFalconThrusterBig = util.load_image('pictures/milleniumFalcon/mFalcon_thruster_big.png')

reyMoveUp = [reyUpWalk1, reyUpWalk2, reyUpStationary]
reyMoveDown = [reyDownWalk1, reyDownWalk2, reyDownStationary]
reyMoveRight = [reyRightWalk1, reyRightWalk2, reyRightStationary]
reyMoveLeft = [reyLeftWalk1, reyLeftWalk2, reyLeftStationary]

lukeMoveUp = [lukeUpWalk1, lukeUpWalk2, lukeUpStationary]
lukeMoveDown = [lukeDownWalk1, lukeDownWalk2, lukeDownStationary]
lukeMoveRight = [lukeRightStationary, lukeRightWalk, lukeRightStationary]
lukeMoveLeft = [lukeLeftStationary, lukeLeftWalk, lukeLeftStationary]

finnMoveUp = [finnUpWalk1, finnUpWalk2, finnUpStationary]
finnMoveDown = [finnDownWalk1, finnDownWalk2, finnDownStationary]
finnMoveRight = [finnRightWalk1, finnRightWalk2, finnRightStationary]
finnMoveLeft = [finnLeftWalk1, finnLeftWalk2, finnLeftStationary]

renMoveUp = [renUpStationary, renUpStationary, renUpStationary]
renMoveDown = [renDownStationary, renDownStationary, renDownStationary]
renMoveRight = [renRightStationary, renRightStationary, renRightStationary]
renMoveLeft = [renLeftStationary, renLeftStationary, renLeftStationary]

darthMoveUp = [darthUpStationary, darthUpStationary, darthUpStationary]
darthMoveDown = [darthDownStationary, darthDownStationary, darthDownStationary]
darthMoveRight = [darthRightStationary, darthRightStationary, darthRightStationary]
darthMoveLeft = [darthLeftStationary, darthLeftStationary, darthLeftStationary]

stormtMoveUp = [stormtUpStationary, stormtUpStationary, stormtUpStationary]
stormtMoveDown = [stormtDownStationary, stormtDownStationary, stormtDownStationary]
stormtMoveRight = [stormtRightStationary, stormtRightStationary, stormtRightStationary]
stormtMoveLeft = [stormtLeftStationary, stormtLeftStationary, stormtLeftStationary]

mFalconFireUp = [mFalconStationary, mFalconThrusterSmall, mFalconStationary, mFalconThrusterSmall,
                 mFalconThrusterBig, mFalconStationary, mFalconThrusterSmall, mFalconThrusterBig,
                 mFalconThrusterSmall, mFalconThrusterBig, mFalconThrusterBig, mFalconThrusterBig]
blueprint_img = util.load_image('pictures/Blueprint.png')

# holes
holes = []

trooper_LOS = pygame.Rect(420, 210, 30, 30)

# for run button
btnimg = util.load_image('pictures/runbtn.png')
btn_rect = pygame.Rect(1075, 590, *btnimg.get_rect().size)

clock = pygame.time.Clock()

smallfont = pygame.font.Font('diehund.ttf', 30)
medfont = pygame.font.Font('diehund.ttf', 40)
largefont = pygame.font.Font('diehund.ttf', 80)

#sounds
collectSaber = pygame.mixer.Sound("sounds/saberswing2.wav")
pressC = pygame.mixer.Sound("sounds/start.wav")
wallbang = pygame.mixer.Sound("sounds/wallbang.ogg")

def loadLevel(level):
    position=[[360,570],[180,180],[0,450],[30,270],[750,540],[360,30],[420,30],[60,330],[30,270],[30,270]]
    levelXList = [[510,0,0],[0,180,360,180,360,600,360,450],[0,120,270,420,690,540,390,240,0],
                  [0,0,0,30,780,780],[0,30,780,0,420,180,510,180,300,420,510,30,180,510,630],[0,0,60,390],
             [0,0,270,330,360,450,450,450,450,450,750],
             [0,0,360,600,240,480,720,0,0],[0,0,0,30],[0,0,0,30]]
    levelYList = [[360,0,180],[0,0,120,450,390,0,240,0],[0,0,0,0,0,150,270,390,510],[0,30,300,570,30,300],
                  [0,570,0,0,0,480,480,30,30,60,60,210,180,180,210],
                  [0,90,270,0],
                  [0,90,120,120,240,0,120,270,420,540,60],
                  [0,180,180,180,270,270,240,390,300],[0,60,300,570],[0,60,300,570]]
    widthlist = [[300,810,270],[180,240,60,630,450,210,240,150],
                 [120,150,150,150,120,150,150,150,240],[600,30,30,780,30,30],
                 [30,780,30,390,780,120,120,120,90,90,120,150,120,120,180],
                 [360,60,300,420],
                 [420,240,60,90,60,360,270,180,270,360,60],
                 [810,180,60,60,60,60,90,810,60],[810,30,30,780],[810,30,30,780]]
    heightlist=[[240,180,420],[600,120,60,150,60,390,90,180],
                [420,300,180,60,600,450,330,210,90],[60,240,270,30,240,270],
                [600,30,570,60,60,90,90,120,90,60,90,120,210,210,120],
                [90,510,330,600],
                [90,390,360,90,360,90,90,90,90,60,480],
                [180,120,120,120,120,120,150,210,90],[60,210,300,30]
                ,[60,210,300,30]]
    win_width = [30,30,120,30,30,30,30,30,30,60]
    win_height = [240,30,30,30,30,30,30,60,510,120]
    win_xyCoordinates = [[780,180],[420,0],[570,0],[780,270],[390,0],[360,570],
                         [420,570],[780,180],[780,60],[510,240]]
    holeCoords = [[],[[570,180],[570,210]],[],[[390,0],[390,30],[390,60],[390,90],[390,120],[390,150],[390,180],[390,210],[390,240],[390,270]
                                               ,[390,300],[390,330],[390,360],[390,390],[390,420],[390,450],[390,480],[390,510],[390,540],[390,570]]
                  ,[],[[360,150],[360,300],[360,420]],[],[],[[180,210],[180,240],[210,450],[210,480],[210,510],[360,270],[360,270],[360,270],[360,300],[360,330],[570,150],
                                [570,180],[570,210],[510,390],[510,420]],[]]

    stormTCoords = [[],[],[],[],[],[],[330,210],[],[],[]]
    vader_face = [0,0,1,2,2,0,0,1,1,3] # 0-Down, 1-Left, 2- Up, 3-Right
    blueprint_xy = [[],[],[],[],[120,150],[],[],[],[],[]]
    return [position[level][0],position[level][1],levelXList[level],levelYList[level],widthlist[level],heightlist[level],win_width[level],win_height[level],\
            win_xyCoordinates[level][0],win_xyCoordinates[level][1],holeCoords[level], vader_face[level],blueprint_xy[level],stormTCoords[level]]

def done_moving():
    if movement.get_next_move() == 'stationary':
        return True
    return False

class Player:

    def __init__(self):
        self.moveUp = lambda steps = 1: self.move('move_up', steps)
        self.moveDown = lambda steps = 1: self.move('move_down', steps)
        self.moveLeft = lambda steps = 1: self.move('move_left', steps)
        self.moveRight = lambda steps = 1: self.move('move_right', steps)

        self.jumpUp = lambda steps = 1: self.move('jump_up', steps)
        self.jumpDown = lambda steps = 1: self.move('jump_down', steps)
        self.jumpLeft = lambda steps = 1: self.move('jump_left', steps)
        self.jumpRight = lambda steps = 1: self.move('jump_right', steps)

    def move(self, direction, steps):
        global game_state
        game_state = direction

        while True:
            if game_state == 'gameover':
                game_state = 'idle' # reset game_state
            if game_state == 'idle':
                steps -= 1
                if steps <= 0: break
                game_state = direction

    def holeInFront(self):
        for hole in holes:
            player_rect = pygame.Rect(lead_x, lead_y, 30, 30)
            collide_direction = hole.collides(player_rect)
            print player_rect
            print 'psuedo_holes', collide_direction
            print 'lead_direction', lead_direction
            # if lead_direction == collide_direction: return True
            if lead_direction == collide_direction:
                print True
                return True
        print False
        return False

this_is_impossible_to_be_screwed_up = Player()

def parser_func(code):
    global game_state
    try:
        exec(code)
    except SystemExit:
        print "exit from loop."
    except:
        traceback.print_exc()
        game_state = 'error'
    finally:
        parsing = False

def display_error():
    global game_state, rebelScore
    rebelScore -= 5
    paused = True
    message_to_screen("CODE ERROR", red,
                      y_displace=-50, size = "large")
    message_to_screen("Press C to play again", orange,
                      50, size = "medium")
    message_to_screen("or Q to quit", orange,
                      100, size = "medium")
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        clock.tick(5)
    game_state = 'idle'
    pygame.mixer.music.stop()
    pressC.play()
    gameLoop()


def barrier(xlocation,ylocation, barrier_width, barrier_height):
    pygame.draw.rect(gameDisplay,black, [xlocation, ylocation, barrier_width, barrier_height])

def pause():
    paused = True
    message_to_screen("Paused", black, -100, size = "large")
    message_to_screen("Press c to continue", black, 25, size = "small")
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        clock.tick(5)

def helpInstructions(level):
    csmallfont = pygame.font.Font('diehund.ttf', 15)
    csmallfont.set_italic(True);
    
    xsmallfont = pygame.font.Font('diehund.ttf', 15)
    xsmallfont.set_underline(True)
    xsmallfont.set_bold(True)
    gameDisplay.blit(xsmallfont.render("Tips:", True, white),\
                         [835, 375])
    xsmallfont.set_underline(False)
    xsmallfont.set_bold(False)

    # 9 Lines max
    helpMessage = {0 : ["Commands to move your player", # Learn move
                        "c      self.moveUp()",
                        "c      self.moveRight()",
                        "",
                        "You can put in parameters, eg",
                        "to move right 4 steps",
                        "c      self.moveRight(4)"],
                   1 : ["Commands to move your player", # Learn move
                        "c      self.moveUp()",
                        "c      self.moveRight()",
                        "c      self.moveDown()",
                        "c      self.moveLeft()",
                        "",
                        "Python is indentation and case ",
                        "sensitive!",
                        "It could be the source of your bugs"],
                   1 : ["Commands to move your player", # Learn move
                        "c      self.moveUp()",
                        "c      self.moveRight()",
                        "c      self.moveDown()",
                        "c      self.moveLeft()",
                        "",
                        "Python is indentation and case ",
                        "sensitive!",
                        "It could be the source of your bugs"],
                   2 : ["Loops can ease your pain of coding", # Learn basic loop
                        "lines of the same thing.",
                        "c      x = 0",
                        "c      while x < 5 :",
                        "c          self.moveRight()",
                        "c          self.moveLeft()",
                        "c          x = x + 1",
                        "'self' represents the object you are",
                        " controling, in this case the player."],
                   3 : ["The Death Star Blueprint earns you points",
                        "",
                        "Here are some useful actions to use", # Learn condition check
                        "c      if self.holeInFront() :",
                        "c          self.jumpRight()",
                        "",
                        "Don't forget how to use the loops!",
                        "c      while x < 5 :",
                        "c          self.jumpUp()"],
                   4 : ["If you didn't realize, If and While", # Example conditions 1
                        "statements require conditions.",
                        "",
                        "c      x = 0",
                        "c      while x < 5 :",
                        "c          self.moveUp()",
                        "c          if x == 3",
                        "c              self.moveLeft()",
                        ""],
                   5 : ["I avoid getting detected by infrared sensor",
                        "",
                        "Use less than(<), more than(>) or" # Example conditions 2
                        "equal to(==), within a condition",
                        "check.",
                        "c      while <condtion> :",
                        "c          <do stuff>",
                        "c      if <condition> :",
                        "c          <do stuff>"],
                   6 : ["Let's see how quickly you can get", # Test!
                        "this over and done with",
                        "",
                        "c      x = <value>",
                        "c      while <condtion> :",
                        "c          <do stuff>",
                        "c      if <condition> :",
                        "c          <do stuff>",
                        ""],
                   7 : ["Condtitions result in either True",
                        "or False.",
                        "Try assigning 'True' as the x value",
                        "",
                        "c      x = <value>",
                        "c      while <condtion> :",
                        "c          <do stuff>",
                        "c      if <condition> :",
                        "c          <do stuff>"],
                   8 : ["You may have heard of an infinite",
                        "loop. 'break' is your friend, but",
                        "where is it used?",
                        "",
                        "c      x = <value>",
                        "c      while <condtion> :",
                        "c          <do stuff>",
                        "c      if <condition> :",
                        "c          <do stuff>"],
                   9 : ["Hop onto the Millenium Falcon and",
                        "escape!",
                        "Holes will randomly appear on the",
                        "so try putting if-statement in ",
                        "a loop"]}
    for lineNumber in range(len(helpMessage[level])):
        isCode = False
        if len(helpMessage[level][lineNumber]) > 0:
            if helpMessage[level][lineNumber][0] == 'c':
                helpMessage[level][lineNumber] = helpMessage[level][lineNumber][1:];
                isCode = True;

        if isCode:
            gameDisplay.blit(csmallfont.render(helpMessage[level][lineNumber], True, grey),\
                             [835, 395+lineNumber*xsmallfont.get_linesize()])
        else:
            gameDisplay.blit(xsmallfont.render(helpMessage[level][lineNumber], True, white),\
                             [835, 395+lineNumber*xsmallfont.get_linesize()])


def status(score,set_time,elapse_time):
    text = smallfont.render("Score:          " + str(score), True, black)
    gameDisplay.blit(text,[55,map_height])

    if(elapse_time>set_time):
        elapse_time=set_time
    pygame.draw.rect(gameDisplay,red, [map_width/2, map_height+2, map_width*(set_time-elapse_time)/(2*set_time), status_bar])
    pygame.draw.line(gameDisplay,black,(map_width/2-2,map_height),(map_width/2-2,display_height), 4)
    text2 = smallfont.render("Time left", True, black)
    gameDisplay.blit(text2,[3*map_width/4-15,map_height])

def randBlueprintGen():
    randBlueprintX = 120
    randBlueprintY = 150
    return randBlueprintX, randBlueprintY

def game_intro():
    global characterMove
    pygame.mixer.music.load("sounds/intro - star wars main theme.ogg")
    pygame.mixer.music.play(0)
    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    characterMove = [renMoveUp, renMoveDown, renMoveRight, renMoveLeft]
                    intro=False
                if event.key == pygame.K_s:
                    characterMove = [stormtMoveUp, stormtMoveDown, stormtMoveRight, stormtMoveLeft]
                    intro=False
                if event.key == pygame.K_t:
                    characterMove = [lukeMoveUp, lukeMoveDown, lukeMoveRight, lukeMoveLeft]
                    intro=False
                if event.key == pygame.K_d:
                    characterMove = [darthMoveUp, darthMoveDown, darthMoveRight, darthMoveLeft]
                    intro=False
                if event.key == pygame.K_m:
                    characterMove = [finnMoveUp, finnMoveDown, finnMoveRight, finnMoveLeft]
                    intro=False
                if event.key == pygame.K_f:
                    characterMove = [reyMoveUp, reyMoveDown, reyMoveRight, reyMoveLeft]
                    intro=False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        gameDisplay.fill(white)
        wp = wallpaper_img
        wp = pygame.transform.scale(wp,(display_width,display_height))
        gameDisplay.blit(wp, (0,0))
        pygame.display.update()
        clock.tick(5)


def rebel_move(direction, playerX, playerY, xChange, yChange, rebelScore, time_limit, seconds, xlocation, ylocation, barrier_width,barrier_height,randBlueprintX, randBlueprintY):

    global game_map
    image = None
    for img in characterMove[direction]:

        playerX += xChange
        playerY += yChange

        gameDisplay.fill(white)
        gameDisplay.blit(game_map, (0,0))
        gameDisplay.blit(text_editor, (map_width,0))
        pygame.draw.line(gameDisplay,black,(map_width,display_height),(map_width,0), 2)#draw boundary for user to type code
        pygame.draw.line(gameDisplay,black,(0,map_height),(map_width,map_height), 2)#draw boundary for status bar
        status(rebelScore, time_limit,seconds)
        #if level one
        game_map=map_img[level]
        if (blueprintCollected == False) and blueprintExist:
            gameDisplay.blit(blueprint_img, (randBlueprintX, randBlueprintY))

        gameDisplay.blit(btnimg, btn_rect)
        draw_holes()
        gameDisplay.blit(img, (playerX, playerY))
        if level == 9:
            gameDisplay.blit(mFalconStationary, (510, 225))

        image = img

        txtbx.draw(gameDisplay)
        helpInstructions(level)
        pygame.display.update()
        clock.tick(10)

    return playerX, playerY, image


def rebel_jump(direction, playerX, playerY, xChange, yChange, rebelScore, time_limit, seconds, xlocation, ylocation, barrier_width,barrier_height,randBlueprintX, randBlueprintY):

    global game_map
    image = None

    img = characterMove[direction][-1] # get stationary img

    for j in range(6):

        # hardcoding storm trooper line of sight
        player_rect = pygame.Rect(playerX, playerY, 30, 30)
        if player_rect.colliderect(trooper_LOS) and level == 6:
            break

        playerX += xChange

        if direction == 2 or direction == 3:
            if j < 3:
                playerY -= abs(xChange)
            else:
                playerY += abs(xChange)
        elif direction == 0:
            if j < 4:
                playerY -= int(1.7*abs(yChange))
            else:
                playerY += int(0.4*abs(yChange))
        elif direction == 1:
            if j < 2:
                playerY -= int(0.4*abs(yChange))
            else:
                playerY += int(1.7*abs(yChange))

        gameDisplay.fill(white)
        gameDisplay.blit(game_map, (0,0))
        gameDisplay.blit(text_editor, (map_width,0))
        pygame.draw.line(gameDisplay,black,(map_width,display_height),(map_width,0), 2)#draw boundary for user to type code
        pygame.draw.line(gameDisplay,black,(0,map_height),(map_width,map_height), 2)#draw boundary for status bar
        status(rebelScore, time_limit,seconds)
        #if level one
        game_map=map_img[level]

        if (blueprintCollected == False) and blueprintExist:
            #barrier(xlocation, randomHeight, barrier_width)
            gameDisplay.blit(blueprint_img, (randBlueprintX, randBlueprintY))

        #for checking hole position
##            for hole in holes:
##                hole.draw()
        gameDisplay.blit(btnimg, btn_rect)
        draw_holes()
        gameDisplay.blit(img, (playerX, playerY))
        if level == 9:
            gameDisplay.blit(mFalconStationary, (510, 225))

        image = img

        txtbx.draw(gameDisplay)
        helpInstructions(level)
        pygame.display.update()
        clock.tick(15)

    return playerX, playerY, image


def mfalcon_fly(rebelScore, time_limit, seconds, randBlueprintX, randBlueprintY):

    global game_map

    # millenium falcon initial coordinates: 510, 225
    mFalconX = 510
    mFalconY = 225

    for i in range(len(mFalconFireUp) + 100):

        if i > 11:
            index = 11
            mFalconX += 5
        else:
            index = i

        for j in range(2):
            gameDisplay.fill(white)
            gameDisplay.blit(game_map, (0,0))
            draw_holes()
            gameDisplay.blit(mFalconFireUp[index], (mFalconX, mFalconY))
            gameDisplay.blit(text_editor, (map_width,0))
            pygame.draw.line(gameDisplay,black,(map_width,display_height),(map_width,0), 2)#draw boundary for user to type code
            pygame.draw.line(gameDisplay,black,(0,map_height),(map_width,map_height), 2)#draw boundary for status bar
            status(rebelScore, time_limit,seconds)
            helpInstructions(level)
            #if level one
            game_map=map_img[level]

            if (not blueprintCollected) and blueprintExist:
                gameDisplay.blit(blueprint_img, (randBlueprintX, randBlueprintY))
            gameDisplay.blit(btnimg, btn_rect)


            txtbx.draw(gameDisplay)
            helpInstructions(level)
            pygame.display.update()

            if index != 11:
                clock.tick(10)

def place_random_holes():
    del holes[:]
    if level == 9:
        possible_locs = range(3, 20, 2)
    else:
        possible_locs = range(3, 25, 2)
    vertical_locs = random.randint(6, 12)
    for i in range (8): # number of columns of holes
        x = random.randrange(3, 16, 2)
        y = random.randrange(6, 12)
        make_hole_columns(x * 30, y * 30, random.choice((2, 3)))

def make_hole_columns(x, y, height):
    for i in range(height):
        holes.append(Hole(gameDisplay, (x, y + (i * 30))))

def draw_holes():
    if level == numOfLevels - 1: # only draw holes for last level
        for hole in holes:
            hole.draw()

def crashed_into_wall(lead_x, lead_y, xlist, ylist, widthlist, heightlist):
    player_rect = pygame.Rect(lead_x, lead_y, 30, 30)
    for i in range(len(xlist)):
        wall = pygame.Rect(xlist[i], ylist[i], widthlist[i], heightlist[i])
        if wall.colliderect(player_rect): return True
    return False

def linecount_to_score(n):
    return txtbx.lines - n

def text_objects(text,color,size):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    elif size == "medium":
        textSurface = medfont.render(text, True, color)
    elif size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen(msg,color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects(msg, color, size)
    textRect.center = (map_width / 2), (map_height / 2) + y_displace
    gameDisplay.blit(textSurf, textRect)



def gameLoop():
    global parsing, game_state, text_editor, elemNumber, level,txtbx, game_map, blueprintCollected, characterMove,numOfLevels, rebelScore
    global lead_x, lead_y, lead_direction,holes,blueprintExist
    gameWon = False
    gameExit = False
    gameOver = False
    leftCollision = False
    rightCollision = False
    topCollision = False
    bottomCollision = False
    player = characterMove[1][2]
    [lead_x,lead_y,xlist,ylist,widthlist,heightlist,win_width,win_height,win_xlocation,win_ylocation,holeCoords,vadarOrientation,blueprint,stormT] = loadLevel(level)
    
    lead_x_change = 0
    lead_y_change = 0
    randBlueprintX = 0
    randBlueprintY = 0
    blueprintExist = False
    if(len(blueprint)>0):
        blueprintExist = True
        randBlueprintX = blueprint[0]
        randBlueprintY = blueprint[1]
    
    step_count = 0
    pause_duration = 0
    code_lines = 0
    movement.reset()

    timerStart=False
    seconds=0
    del holes[:]
    for i in range(len(holeCoords)):
        holes.append(Hole(gameDisplay, (holeCoords[i][0], holeCoords[i][1])))
    # use get_ticks to time
    #timer.reset()

    barrier_width = 30
    barrier_height = 30
    xlocation = (map_width/2)+ random.randint(-0.2*map_width, 0.2*map_width)
    ylocation = random.randrange(map_height*0.1,map_height*0.6)

    dvlist = ["sounds/darth vader - die1.wav","sounds/darth vader - i have you now.wav","sounds/darth vaer - breath.wav","sounds/darth vader - thisistheend.wav"]
    playonce = 0
    if playonce == 0:
        pygame.mixer.music.load("sounds/level 1 - throne room.ogg")
        pygame.mixer.music.play(0)
        playonce = 1

    while not gameExit:
        if gameWon == True:
            rebelScore += linecount_to_score(code_lines)
            #-----sounds
            pygame.mixer.music.stop()
            pygame.mixer.music.load("sounds/lose - imperial march.ogg")
            pygame.mixer.music.play(0)
            #-----sounds
            if level == 9:
                message_to_screen("Congratulations!", green,
                                  y_displace=-150, size = "large")
                message_to_screen("Your Score is " + str(rebelScore), green,
                                  y_displace=-50, size = "medium")
                message_to_screen("Press C to proceed", orange,
                                  50, size = "small")
                message_to_screen("or Q to quit", orange,
                                  100, size = "small")
            else:
                message_to_screen("Level cleared!", green,
                                  y_displace=-50, size = "large")
                message_to_screen("Press C to proceed", orange,
                                  50, size = "small")
                message_to_screen("or Q to quit", orange,
                                  100, size = "small")

            level = (level+1)%numOfLevels

            pygame.display.update()

        elif gameOver == True:
            rebelScore -= 5
            randnumb = random.randint(0,len(dvlist)-1)
            #-----sounds
            pygame.mixer.music.stop()
            pygame.mixer.music.load("sounds/lose - imperial march.ogg")
            pygame.mixer.music.play(0)
            pygame.mixer.Sound(dvlist[randnumb]).play()
            #-----sounds
            message_to_screen("GAME OVER", red,
                              y_displace=-50, size = "large")
            message_to_screen("Press C to play again", orange,
                              50, size = "medium")
            message_to_screen("or Q to quit", orange,
                              100, size = "medium")
            #----- displays
            if vadarOrientation == 0:
                gameDisplay.blit(darthDownStationary, (win_xlocation, win_ylocation))
            elif vadarOrientation == 2:
                gameDisplay.blit(darthUpStationary, (win_xlocation, win_ylocation))
            elif vadarOrientation == 1:
                gameDisplay.blit(darthLeftStationary, (win_xlocation, win_ylocation))
            else:
                gameDisplay.blit(darthRightStationary, (win_xlocation, win_ylocation))
            pygame.display.update()

        while gameOver == True or gameWon == True:
            game_state = 'gameover'
            parser_thread.stop()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameWon = False
                    gameOver = False
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameWon = False
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        game_state = 'idle'
                        gameWon= False
                        pygame.mixer.music.stop()
                        pressC.play()
                        gameLoop()
                        

    ############## timer ##########################
        if timerStart:
            timer.update()
            seconds = timer.get_time() #calculate how many seconds
            if (time_limit - seconds)<=0:
                gameOver=True
            #print (seconds) #print how many seconds

###################### WIN GAME CONDITIONS: Lands on the exit grid ###########################
        win_rect = pygame.Rect(win_xlocation, win_ylocation, win_width, win_height)
        player_rect = pygame.Rect(lead_x, lead_y, 30, 30)
        if win_rect.colliderect(player_rect):
            gameWon = True
            if level == 9:
                mfalcon_fly(rebelScore, time_limit, seconds, randBlueprintX, randBlueprintY)

###################### END GAME CONDITIONS: Out of bound detection, Timelimit ###########################
        if lead_x > map_width - block_size or lead_x < 0 or lead_y > map_height - block_size \
            or lead_y<0:
            gameOver = True

        if game_state == 'error':
            display_error()


####################### UPDATES PLAYER LOCATION ################################
        # lead_x += lead_x_change
        # lead_y += lead_y_change

####################### displaying it on screen ################################
        gameDisplay.fill(white)
        game_map=map_img[level]
        text_editor=text_editor_img
        gameDisplay.blit(game_map, (0,0))
        gameDisplay.blit(text_editor, (map_width,0))
        pygame.draw.line(gameDisplay,black,(map_width,display_height),(map_width,0), 2) #draw boundary for user to type code
        pygame.draw.line(gameDisplay,black,(0,map_height),(map_width,map_height), 2) #draw boundary for status bar
        if not gameWon:
            gameDisplay.blit(player, (lead_x, lead_y))
        status(rebelScore, time_limit,seconds)
        helpInstructions(level)

        if level == numOfLevels - 1:
            draw_holes()
        if level == 9 and not gameWon:
            gameDisplay.blit(mFalconStationary, (510, 225))
        if(len(stormT)>0):
            gameDisplay.blit(stormtRightStationary, (stormT[0], stormT[1]))


####################### barrier collision detection #############################

        for i in range(0,len(xlist)):
            ylocation = ylist[i]
            xlocation = xlist[i]
            barrier_height = heightlist[i]
            barrier_width = widthlist[i]
            #for debugging:
            #pygame.draw.rect(gameDisplay,red,[xlocation,ylocation,barrier_width,barrier_height])
            if ylocation + barrier_height > lead_y and lead_y + block_size > ylocation:
                if lead_x - (block_size/2) < xlocation + barrier_width and lead_x > xlocation + barrier_width/2:
                    leftCollision = True
                if lead_x + (4*block_size) > xlocation and lead_x < xlocation + barrier_width/2:
                    rightCollision = True
            elif xlocation + barrier_width > lead_x and lead_x + block_size > xlocation:
                if lead_y - (block_size/2) < ylocation + barrier_height and lead_y > ylocation + barrier_height/2:
                    topCollision = True
                if lead_y + (4*block_size) > ylocation and lead_y < ylocation + barrier_height/2:
                    bottomCollision = True




######################## when blueprint have been collected ###########################
        if (blueprintCollected == False) and blueprintExist:
            gameDisplay.blit(blueprint_img, (randBlueprintX, randBlueprintY))
            if lead_x >= randBlueprintX and lead_x <= randBlueprintX + BlueprintThickness or lead_x + block_size >= randBlueprintX and \
               lead_x + block_size <= randBlueprintX + BlueprintThickness:
                if lead_y >= randBlueprintY and lead_y <= randBlueprintY + BlueprintThickness:
                    rebelScore+=20
                    blueprintCollected = True

                elif lead_y + block_size >= randBlueprintY and lead_y + block_size <= randBlueprintY + BlueprintThickness:
                    rebelScore+=20
                    blueprintCollected = True

        clock.tick(30)
            ##for checking holes in map
##        for hole in holes:
##            hole.draw()

    ######################### Player controls - Keypress or Typed text #########################

        events = pygame.event.get()

        # to quit game
        for event in events:
            if event.type == pygame.QUIT:
                gameExit = True

        # Use the Movement class to keep track of moves.
        if control_mode == 'TYPE':
            next_move = movement.get_next_move()
            # print "next_move", next_move
            # print "left collision", leftCollision
            # print "right collision", rightCollision
            # print "top collision", topCollision
            # print "btm collision", bottomCollision

            # 0: up, 1: down, 2: right, 3: left
            if next_move == 'stationary':
                lead_x_change = 0
                lead_y_change = 0
            elif next_move == 'move_up':
                if topCollision:
                    lead_x, lead_y, player = rebel_move(0, lead_x, lead_y, 0, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)
                    # topCollision = False
                else:
                    lead_x, lead_y, player = rebel_move(0, lead_x, lead_y, 0, -10, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)

            elif next_move == 'move_down':
                if bottomCollision:
                    lead_x, lead_y, player = rebel_move(1, lead_x, lead_y, 0, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)
                    # bottomCollision = False
                else:
                    lead_x, lead_y, player = rebel_move(1, lead_x, lead_y, 0, 10, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)

            elif next_move == 'move_left':
                if leftCollision:
                    lead_x, lead_y, player = rebel_move(3, lead_x, lead_y, 0, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)
                    # leftCollision = False
                else:
                    lead_x, lead_y, player = rebel_move(3, lead_x, lead_y, -10, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)

            elif next_move == 'move_right':

                if rightCollision:
                    lead_x, lead_y, player = rebel_move(2, lead_x, lead_y, 0, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)
                    # rightCollision = False
                else:
                    lead_x, lead_y, player = rebel_move(2, lead_x, lead_y, 10, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)

            elif next_move == 'jump_up':
                if topCollision:
                    lead_x, lead_y, player = rebel_jump(0, lead_x, lead_y, 0, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)
                    # topCollision = False
                else:
                    lead_x, lead_y, player = rebel_jump(0, lead_x, lead_y, 0, -10, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)

            elif next_move == 'jump_down':
                if bottomCollision:
                    lead_x, lead_y, player = rebel_jump(1, lead_x, lead_y, 0, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)
                    # bottomCollision = False
                else:
                    lead_x, lead_y, player = rebel_jump(1, lead_x, lead_y, 0, 10, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)

            elif next_move == 'jump_left':

                if leftCollision:
                    lead_x, lead_y, player = rebel_jump(3, lead_x, lead_y, 0, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)
                    # leftCollision = False
                else:
                    lead_x, lead_y, player = rebel_jump(3, lead_x, lead_y, -10, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)

            elif next_move == 'jump_right':

                if rightCollision:
                    lead_x, lead_y, player = rebel_jump(2, lead_x, lead_y, 0, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)
                    # rightCollision = False
                else:
                    lead_x, lead_y, player = rebel_jump(2, lead_x, lead_y, 10, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)

            # reset all collision state after moving (although right now it resets even when not moving)
            topCollision = False
            bottomCollision = False
            leftCollision = False
            rightCollision = False

        if crashed_into_wall(lead_x, lead_y, xlist, ylist, widthlist, heightlist):
            gameOver = True

        # hardcoding storm trooper line of sight
        player_rect = pygame.Rect(lead_x, lead_y, 30, 30)
        if level == 6 and player_rect.colliderect(trooper_LOS):
            gameOver = True
                    
        # check if player is on a hole
        for hole in holes:
            player_rect = pygame.Rect(lead_x, lead_y, 30, 30)
            collide_direction = hole.collides(player_rect)
            if collide_direction == 'exact':
                gameOver = True

        if parsing:
            movement_state = game_state[:4]
            direction = game_state[5:]
            if movement_state == 'jump' or movement_state == 'move':
                movement.add_move(game_state)
                lead_direction = direction
                game_state = 'moving'
            elif game_state == 'moving' and done_moving():
                game_state = 'idle'

        # run code button
        gameDisplay.blit(btnimg, btn_rect)
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                print pygame.mouse.get_pos()
                if btn_rect.collidepoint(pygame.mouse.get_pos()):
                    if timerStart==False:
                        timer.set_ticks_func(pygame.time.get_ticks)
                        timer.reset()
                        timerStart=True

                    if level == numOfLevels - 1:
                        place_random_holes()

                    parsing = True

                    code = txtbx.get_text()
                    code = code.replace('self', 'this_is_impossible_to_be_screwed_up')
                    code_lines += txtbx.get_linecount()
                    parser_thread.start(parser_func, code)
                    txtbx.clear()
        
        txtbx.update(events)
        txtbx.draw(gameDisplay)
        pygame.display.update()


    parser_thread.stop()
    pygame.quit()
    quit()

game_intro()
gameLoop()

