#batman is the best
from collections import deque
import pygame, ezpztext
import time
import random
import threading
import traceback

from Movement import Movement
from Timer import Timer
import ParserThread

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0, 255, 0)
yellow = (255, 255, 0)

# default colour for text editor font
txtfont_default = white
txtfont_focus = green

# Global settings
control_mode = 'TYPE' # 'KEYPRESS' or 'TYPE'
time_limit = 30 # Time limit that affects Time Bar and Duration countdown

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

BlueprintThickness = 30
block_size = 10
FPS = 30
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Slither')

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

blueprint_img = pygame.image.load('pictures/apple.png')

# for run button
btnimg = pygame.image.load('pictures/runbtn.png').convert_alpha()
btn_rect = pygame.Rect(1075, 590, *btnimg.get_rect().size)

clock = pygame.time.Clock()

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

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

def parser_func(code):
    try:
        exec(code)
    except SystemExit:
        print "exit from loop."
    except:
        traceback.print_exc()
    finally:
        parsing = False

def barrier(xlocation,randomHeight, barrier_width):
    pygame.draw.rect(gameDisplay,black, [xlocation, randomHeight, barrier_width, barrier_width])

def winGrid(xlocation, ylocation, grid_width):
    pygame.draw.rect(gameDisplay,yellow, [xlocation, ylocation, grid_width, grid_width])

def pause():

    paused = True
    timer.pause()
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
                    timer.unpause()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    quit()

        clock.tick(5)
        
def status(score,set_time,elapse_time):
    text = smallfont.render("Score: " + str(score), True, black)
    gameDisplay.blit(text,[0,map_height])

    if(elapse_time>set_time):
        elapse_time=set_time
    pygame.draw.rect(gameDisplay,red, [map_width/2, map_height+2, map_width*(set_time-elapse_time)/(2*set_time), status_bar])
    pygame.draw.line(gameDisplay,black,(map_width/2-2,map_height),(map_width/2-2,display_height), 4)
    text2 = smallfont.render("Time left", True, black)
    gameDisplay.blit(text2,[3*map_width/4,map_height])
    
def randBlueprintGen():
##    randBlueprintX = round(random.randrange(0, map_width - AppleThickness))#/10.0)*10.0
##    randBlueprintY = round(random.randrange(0, map_height - AppleThickness))#/10.0)*10.0
    randBlueprintX = 180
    randBlueprintY = 180
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


def rebel_move(direction, playerX, playerY, xChange, yChange, rebelScore, time_limit, seconds, xlocation, randomHeight, barrier_width,
               randBlueprintX, randBlueprintY):

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
            barrier(xlocation, randomHeight, barrier_width)
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

def gameLoop():
    global parsing, game_state, game_map, text_editor, elemNumber, txtbx
    gameWon = False
    gameExit = False
    gameOver = False
    player = lukeDownStationary
    lead_x = 750
    lead_y = 540
    lead_x_change = 0
    lead_y_change = 0
    rebelScore = 0
    randBlueprintX, randBlueprintY = randBlueprintGen()
    step_count = 0
    pause_duration = 0

    # use get_ticks to time
    timer.set_ticks_func(pygame.time.get_ticks)
    timer.reset()
    
    #textbox
    txtbx = ezpztext.Textbox(lines=14, default_color=txtfont_default,
                focus_color=txtfont_focus, maxlength=34, y=60, x=840)

    for i in range(len(txtbx.txtbx)):
        txtbx.txtbx[i].prompt = "{:>2}: ".format(i + 1)

    barrier_width = 30
    xlocation = (map_width/2)+ random.randint(-0.2*map_width, 0.2*map_width)
    randomHeight = random.randrange(map_height*0.1,map_height*0.6)

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
            message_to_screen("Press C to play again or Q to quit", black,
                              50, size = "medium")
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
        timer.update()
        seconds = timer.get_time() #calculate how many seconds
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
        gameDisplay.blit(blueprint_img, (randBlueprintX, randBlueprintY))
        gameDisplay.blit(player, (lead_x, lead_y))
        status(rebelScore, time_limit,seconds)
        barrier(xlocation,randomHeight, barrier_width)
        winGrid(win_xlocation, win_ylocation, win_width)
        
        
####################### barrier collision detection #############################
        if randomHeight + barrier_width > lead_y and lead_y + block_size > randomHeight:
            if lead_x - (block_size/2) < xlocation + barrier_width and lead_x > xlocation + barrier_width/2:
                lead_x += block_size
            if lead_x + (3*block_size/2) > xlocation and lead_x < xlocation + barrier_width/2:
                lead_x -= block_size
        elif xlocation + barrier_width > lead_x and lead_x + block_size > xlocation:
            if lead_y - (block_size/2) < randomHeight + barrier_width and lead_y > randomHeight + barrier_width/2:
                lead_y += block_size
            if lead_y + (3*block_size/2) > randomHeight and lead_y < randomHeight + barrier_width/2:
                lead_y -= block_size
        
######################## when apple have been collected ###########################
        if lead_x >= randBlueprintX and lead_x <= randBlueprintX + BlueprintThickness or lead_x + block_size >= randBlueprintX and lead_x + block_size <= randBlueprintX + BlueprintThickness:
            if lead_y >= randBlueprintY and lead_y <= randBlueprintY + BlueprintThickness:
                randBlueprintX, randBlueprintY = randBlueprintGen()
                rebelScore+=1
                
            elif lead_y + block_size >= randBlueprintY and lead_y + block_size <= randBlueprintY + BlueprintThickness:
                randBlueprintX, randBlueprintY = randBlueprintGen()
                rebelScore+=1

        clock.tick(30)

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
            elif next_move == 'up':
                lead_x, lead_y, player = rebel_move(0, lead_x, lead_y, 0, -10, rebelScore, time_limit, seconds, xlocation, randomHeight,
                                                    barrier_width, randBlueprintX, randBlueprintY)
            elif next_move == 'down':
                lead_x, lead_y, player = rebel_move(1, lead_x, lead_y, 0, 10, rebelScore, time_limit, seconds, xlocation, randomHeight,
                                                    barrier_width, randBlueprintX, randBlueprintY)
            elif next_move == 'left':
                lead_x, lead_y, player = rebel_move(3, lead_x, lead_y, -10, 0, rebelScore, time_limit, seconds, xlocation, randomHeight,
                                                    barrier_width, randBlueprintX, randBlueprintY)
            elif next_move == 'right':
                lead_x, lead_y, player = rebel_move(2, lead_x, lead_y, 10, 0, rebelScore, time_limit, seconds, xlocation, randomHeight,
                                                    barrier_width, randBlueprintX, randBlueprintY)

        if parsing:
            if game_state == 'move_left':
                movement.add_move('left');
                game_state = 'moving'
            elif game_state == 'move_right':
                movement.add_move('right');
                game_state = 'moving'
            elif game_state == 'move_up':
                movement.add_move('up');
                game_state = 'moving'
            elif game_state == 'move_down':
                movement.add_move('down');
                game_state = 'moving'
            elif game_state == 'moving':
                if done_moving():
                    game_state = 'idle'

        # run code button
        gameDisplay.blit(btnimg, btn_rect)
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if btn_rect.collidepoint(pygame.mouse.get_pos()):
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

