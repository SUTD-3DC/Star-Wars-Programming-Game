#batman is the best
from collections import deque
import pygame, ezpztext
import time
import random
import threading
import traceback

from Movement import Movement
from Hole import Hole
from Timer import Timer
import ParserThread

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0, 255, 0)
yellow = (255, 255, 0)
grey = (96, 125, 139)

# default colour for text editor font
txtfont_default = white
txtfont_focus = green

# Global settings
control_mode = 'TYPE' # 'KEYPRESS' or 'TYPE'
time_limit = 50 # Time limit that affects Time Bar and Duration countdown

# Use a timer
timer = Timer()

# Use the Movement class to keep track of movements
movement = Movement(1)

# Game state
game_state = 'idle'
parsing = False


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

BlueprintThickness = 30
block_size = 10
FPS = 30
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Star Wars: A programming education game')

wallpaper_img = 'wallpaper/Wallpaper.png'
text_editor_img = 'pictures/right panel/Text editor.png'
map_img = ['pictures/Map/Map_1.png','pictures/Map/Map_2.png',
           'pictures/Map/Test map.png']

lukeUpStationary = pygame.image.load('pictures/lukeMove/Luke_up_stationary.png')
lukeUpWalk1 = pygame.image.load('pictures/lukeMove/Luke_up_walk_1.png')
lukeUpWalk2 = pygame.image.load('pictures/lukeMove/Luke_up_walk_2.png')
lukeDownStationary = pygame.image.load('pictures/lukeMove/Luke_down_stationary.png')
lukeDownWalk1 = pygame.image.load('pictures/lukeMove/Luke_down_walk_1.png')
lukeDownWalk2 = pygame.image.load('pictures/lukeMove/Luke_down_walk_2.png')
lukeRightStationary = pygame.image.load('pictures/lukeMove/Luke_right_stationary.png')
lukeRightWalk = pygame.image.load('pictures/lukeMove/Luke_right_walk_1.png')
lukeLeftStationary = pygame.image.load('pictures/lukeMove/Luke_left_stationary.png')
lukeLeftWalk = pygame.image.load('pictures/lukeMove/Luke_left_walk_1.png')

lukeMoveUp = [lukeUpWalk1, lukeUpWalk2, lukeUpStationary]
lukeMoveDown = [lukeDownWalk1, lukeDownWalk2, lukeDownStationary]
lukeMoveRight = [lukeRightStationary, lukeRightWalk, lukeRightStationary]
lukeMoveLeft = [lukeLeftStationary, lukeLeftWalk, lukeLeftStationary]
lukeMove = [lukeMoveUp, lukeMoveDown, lukeMoveRight, lukeMoveLeft]

blueprint_img = pygame.image.load('pictures/Blueprint.png')

# holes
holes = [Hole(gameDisplay, (750, 420)),
         Hole(gameDisplay, (630, 420))]

# for run button
btnimg = pygame.image.load('pictures/runbtn.png').convert_alpha()
btn_rect = pygame.Rect(1075, 590, *btnimg.get_rect().size)

clock = pygame.time.Clock()

smallfont = pygame.font.Font('diehund.ttf', 28)
medfont = pygame.font.Font('diehund.ttf', 50)
largefont = pygame.font.Font('diehund.ttf', 80)

#sounds
collectSaber = pygame.mixer.Sound("sounds/saberswing2.wav")
pressC = pygame.mixer.Sound("sounds/start.wav")
wallbang = pygame.mixer.Sound("sounds/wallbang.ogg")

def done_moving():
    if movement.get_next_move() == 'stationary':
        return True
    return False

def move(direction, steps):
    global game_state
    game_state = direction

    while True:
        if game_state == 'idle':
            steps -= 1
            if steps <= 0: break
            game_state = direction

moveUp = lambda steps = 1: move('move_up', steps)
moveDown = lambda steps = 1: move('move_down', steps)
moveLeft = lambda steps = 1: move('move_left', steps)
moveRight = lambda steps = 1: move('move_right', steps)

jumpUp = lambda : move('jump_up', 2)
jumpDown = lambda : move('jump_down', 2)
jumpLeft = lambda : move('jump_left', 2)
jumpRight = lambda : move('jump_right', 2)

def holeInFront():
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

def parser_func(code):
    try:
        exec(code)
    except SystemExit:
        print "exit from loop."
    except:
        traceback.print_exc()
    finally:
        parsing = False

def barrier(xlocation,ylocation, barrier_width, barrier_height):
    pygame.draw.rect(gameDisplay,black, [xlocation, ylocation, barrier_width, barrier_height])

def winGrid(xlocation, ylocation, grid_width):
    pygame.draw.rect(gameDisplay,yellow, [xlocation, ylocation, grid_width, grid_width])

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

def status(score,set_time,elapse_time):
    text = smallfont.render("Score: " + str(score), True, black)
    gameDisplay.blit(text,[15,map_height])

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
    pygame.mixer.music.load("sounds/intro - star wars main theme.ogg")
    pygame.mixer.music.play(0)
    intro = True

    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    intro=False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()


##        message_to_screen("Star Wars", black, -100,
##                          "medium")
##        message_to_screen("A programming education game",
##                          black, -30,"small")
##        message_to_screen("Press C to play, P to pause, Q to Quit",
##                          black, 30,"small")
        gameDisplay.fill(white)
        wp = pygame.image.load(wallpaper_img)
        gameDisplay.blit(wp, (0,0))
        pygame.display.update()
        clock.tick(5)


def rebel_move(direction, playerX, playerY, xChange, yChange, rebelScore, time_limit, seconds, xlocation, ylocation, barrier_width,barrier_height,randBlueprintX, randBlueprintY):

    global game_map
    image = None
    for img in lukeMove[direction]:

        playerX += xChange
        playerY += yChange

        for i in range(2):
            gameDisplay.fill(white)
            gameDisplay.blit(game_map, (0,0))
            gameDisplay.blit(text_editor, (map_width,0))
            pygame.draw.line(gameDisplay,black,(map_width,display_height),(map_width,0), 2)#draw boundary for user to type code
            pygame.draw.line(gameDisplay,black,(0,map_height),(map_width,map_height), 2)#draw boundary for status bar
            status(rebelScore, time_limit,seconds)
            #if level one
            game_map=pygame.image.load(map_img[1]);

            if blueprintCollected == False:
                #barrier(xlocation, randomHeight, barrier_width)
                gameDisplay.blit(blueprint_img, (randBlueprintX, randBlueprintY))

            gameDisplay.blit(btnimg, btn_rect)
            gameDisplay.blit(img, (playerX, playerY))
            image = img

            txtbx.draw(gameDisplay)
            pygame.display.update()
            clock.tick(60)

    return playerX, playerY, image


def rebel_jump(direction, playerX, playerY, xChange, yChange, rebelScore, time_limit, seconds, xlocation, ylocation, barrier_width,barrier_height,randBlueprintX, randBlueprintY):

    global game_map
    image = None

    if direction == 2 or 3:

        for img in lukeMove[direction]:

            playerX += xChange
            playerY += yChange

            for i in range(2):
                gameDisplay.fill(white)
                gameDisplay.blit(game_map, (0,0))
                gameDisplay.blit(text_editor, (map_width,0))
                pygame.draw.line(gameDisplay,black,(map_width,display_height),(map_width,0), 2)#draw boundary for user to type code
                pygame.draw.line(gameDisplay,black,(0,map_height),(map_width,map_height), 2)#draw boundary for status bar
                status(rebelScore, time_limit,seconds)
                #if level one
                game_map=pygame.image.load(map_img[1]);

                if blueprintCollected == False:
                    #barrier(xlocation, randomHeight, barrier_width)
                    gameDisplay.blit(blueprint_img, (randBlueprintX, randBlueprintY))

                gameDisplay.blit(btnimg, btn_rect)
                gameDisplay.blit(img, (playerX, playerY))
                image = img

                txtbx.draw(gameDisplay)
                pygame.display.update()
                clock.tick(60)

    return playerX, playerY, image



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

#def loadLevelOne():
#    #load map
#    #level 1 barriers
#    #borders (x, y, width, height)
#    global xlist,ylist,widthlist,heightlist
#    xlist = [0,29,780,0,420,180,510,180,300,420,510,30,180,510,630]
#    ylist = [600,600,569,59,59,569,569,149,119,119,149,329,389,389,329]
#    widthlist=[29,781,30,389,784,119,119,119,89,89,119,149,119,119,149]
#    heightlist=[600,31,569,59,59,89,89,123,95,60,89,119,209,209,119]
    #barrier(0,600,29,600) #left border
    #barrier(29,600,781,31)#bottom
    #barrier(780,569, 30,569)#right
    #barrier(0,59,389,59)# top part 1
    #barrier(420,59, 784,59)# top part 2
    #barrier(180,569,119,89)# bottom left extrusion
    #barrier(510,569, 119,89)# bottom right
    #barrier(180,149, 119,123)# top left extrusion part 1
    #barrier(300,119, 89,95)# top left extrusion part 2
    #barrier(420,119, 89,60)# top right extrusion part 1
    #barrier(510,149, 119,89)# top right extrusion part 2
    #barrier(30,329, 149,119)# left extrusion part 1
    #barrier(180,389, 119,209)# left extrusion part 2
    #barrier(510,389, 119,209)# right extrusion part 1
    #barrier(630,329, 149,119)# right extrusion part 2



def gameLoop():
    global parsing, game_state, text_editor, elemNumber, \
    txtbx,xlist,ylist,widthlist,heightlist, game_map, blueprintCollected
    global lead_x, lead_y, lead_direction
    gameWon = False
    gameExit = False
    gameOver = False
    leftCollision = False
    rightCollision = False
    topCollision = False
    bottomCollision = False
    player = lukeDownStationary
    lead_x_change = 0
    lead_y_change = 0
    rebelScore = 0
    randBlueprintX, randBlueprintY = randBlueprintGen()
    step_count = 0
    pause_duration = 0


    timerStart=False
    seconds=0

    # use get_ticks to time
    #timer.reset()

    #textbox
    txtbx = ezpztext.Textbox(lines=14, default_color=txtfont_default,
                focus_color=txtfont_focus, maxlength=34, y=60, x=840)

    for i in range(len(txtbx.txtbx)):
        txtbx.txtbx[i].prompt = "{:>2}: ".format(i + 1)

    barrier_width = 30
    barrier_height = 30
    xlocation = (map_width/2)+ random.randint(-0.2*map_width, 0.2*map_width)
    ylocation = random.randrange(map_height*0.1,map_height*0.6)

    # WinGrid - size and location for win state to be triggered
    win_width = 30
    win_xlocation = 390
    win_ylocation = 0

    dvlist = ["sounds/darth vader - die1.wav","sounds/darth vader - i have you now.wav","sounds/darth vaer - breath.wav","sounds/darth vader - thisistheend.wav"]
    playonce = 0
    if playonce == 0:
        pygame.mixer.music.load("sounds/level 1 - throne room.ogg")
        pygame.mixer.music.play(0)
        playonce = 1

    while not gameExit:

        if gameWon == True:
            #-----sounds
            pygame.mixer.music.stop()
            pygame.mixer.music.load("sounds/lose - imperial march.ogg")
            pygame.mixer.music.play(0)
            #-----sounds
            message_to_screen("You won!", red,
                              y_displace=-50, size = "large")
            message_to_screen("Press C to play again or Q to quit", black,
                              50, size = "medium")
            pygame.display.update()

        elif gameOver == True:
            randnumb = random.randint(0,len(dvlist)-1)
            #-----sounds
            pygame.mixer.music.stop()
            pygame.mixer.music.load("sounds/lose - imperial march.ogg")
            pygame.mixer.music.play(0)
            pygame.mixer.Sound(dvlist[randnumb]).play()
            #-----sounds
            message_to_screen("Game over", red,
                              y_displace=-50, size = "large")
            message_to_screen("Press C to play again", grey,
                              50, size = "small")
            message_to_screen("or Q to quit", grey,
                              100, size = "small")
            pygame.display.update()

        while gameOver == True or gameWon == True:

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
        if 0 < (lead_y+(block_size/2)) and (lead_y+(block_size/2)) < win_ylocation+win_width and \
            win_xlocation < (lead_x+(block_size/2)) and (lead_x+(block_size/2)) < win_xlocation+win_width:
            gameWon = True;

###################### END GAME CONDITIONS: Out of bound detection, Timelimit ###########################
        if lead_x > map_width - block_size or lead_x < 0 or lead_y > map_height - block_size \
            or lead_y<0:
            gameOver = True


####################### UPDATES PLAYER LOCATION ################################
        # lead_x += lead_x_change
        # lead_y += lead_y_change

####################### displaying it on screen ################################
        gameDisplay.fill(white)
        game_map=pygame.image.load(map_img[1]);
        text_editor=pygame.image.load(text_editor_img);
        gameDisplay.blit(game_map, (0,0))
        gameDisplay.blit(text_editor, (map_width,0))
        pygame.draw.line(gameDisplay,black,(map_width,display_height),(map_width,0), 2) #draw boundary for user to type code
        pygame.draw.line(gameDisplay,black,(0,map_height),(map_width,map_height), 2) #draw boundary for status bar

        gameDisplay.blit(player, (lead_x, lead_y))
        status(rebelScore, time_limit,seconds)
        #winGrid(win_xlocation, win_ylocation, win_width)

        #if level 1:
        xlist = [0,29,780,0,420,180,510,180,300,420,510,30,180,510,630]
        ylist = [0,569,0,0,0,480,480,30,30,60,60,210,180,180,210]
        widthlist=[29,781,30,389,784,119,119,119,89,89,119,149,119,119,190]
        heightlist=[600,31,569,59,59,89,89,123,95,60,89,119,209,209,119]#load level one barriers


####################### barrier collision detection #############################

        for i in range(0,len(xlist)):
            ylocation = ylist[i]
            xlocation = xlist[i]
            barrier_height = heightlist[i]
            barrier_width = widthlist[i]
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




######################## when apple have been collected ###########################
        if blueprintCollected == False:
            gameDisplay.blit(blueprint_img, (randBlueprintX, randBlueprintY))
            if lead_x >= randBlueprintX and lead_x <= randBlueprintX + BlueprintThickness or lead_x + block_size >= randBlueprintX and lead_x + block_size <= randBlueprintX + BlueprintThickness:
                if lead_y >= randBlueprintY and lead_y <= randBlueprintY + BlueprintThickness:
                    randBlueprintX, randBlueprintY = randBlueprintGen()
                    rebelScore+=1
                    blueprintCollected = True

                elif lead_y + block_size >= randBlueprintY and lead_y + block_size <= randBlueprintY + BlueprintThickness:
                    randBlueprintX, randBlueprintY = randBlueprintGen()
                    rebelScore+=1
                    blueprintCollected = True

        clock.tick(30)

        holes[0].draw()
        holes[1].draw()

    ######################### Player controls - Keypress or Typed text #########################

        events = pygame.event.get()

        # to quit game
        for event in events:
            if event.type == pygame.QUIT:
                gameExit = True

        # Use the Movement class to keep track of moves.
        if control_mode == 'TYPE':
            next_move = movement.get_next_move()

            # 0: up, 1: down, 2: right, 3: left
            if next_move == 'stationary':
                lead_x_change = 0
                lead_y_change = 0
            elif next_move == 'move_up':
                if topCollision:
                    lead_x, lead_y, player = rebel_move(0, lead_x, lead_y, 0, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)
                    topCollision = False
                else:
                    lead_x, lead_y, player = rebel_move(0, lead_x, lead_y, 0, -10, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)
            elif next_move == 'move_down':
                if bottomCollision:
                    lead_x, lead_y, player = rebel_move(1, lead_x, lead_y, 0, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)
                    bottomCollision = False
                else:
                    lead_x, lead_y, player = rebel_move(1, lead_x, lead_y, 0, 10, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)

            elif next_move == 'move_left':
                if leftCollision:
                    lead_x, lead_y, player = rebel_move(3, lead_x, lead_y, 0, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)
                    leftCollision = False
                else:
                    lead_x, lead_y, player = rebel_move(3, lead_x, lead_y, -10, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)

            elif next_move == 'move_right':

                if rightCollision:
                    lead_x, lead_y, player = rebel_move(2, lead_x, lead_y, 0, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)
                    rightCollision = False
                else:
                    lead_x, lead_y, player = rebel_move(2, lead_x, lead_y, 10, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)

            elif next_move == 'jump_left':

                if leftCollision:
                    lead_x, lead_y, player = rebel_move(3, lead_x, lead_y, 0, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)
                    leftCollision = False
                else:
                    lead_x, lead_y, player = rebel_move(3, lead_x, lead_y, -10, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)

            elif next_move == 'jump_right':

                if rightCollision:
                    lead_x, lead_y, player = rebel_move(2, lead_x, lead_y, 0, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)
                    rightCollision = False
                else:
                    lead_x, lead_y, player = rebel_move(2, lead_x, lead_y, 10, 0, rebelScore, time_limit, seconds, xlocation, ylocation,
                                                    barrier_width, barrier_height, randBlueprintX, randBlueprintY)

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
                if btn_rect.collidepoint(pygame.mouse.get_pos()):
                    if timerStart==False:
                        timer.set_ticks_func(pygame.time.get_ticks)
                        timer.reset()
                        timerStart=True
                    parsing = True

                    code = txtbx.get_text()
                    code = code.replace('self.', '')
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

