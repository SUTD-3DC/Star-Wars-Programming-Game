from collections import deque
import pygame, eztext
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
green = (0, 155, 0)

# Global settings
control_mode = 'TYPE' # 'KEYPRESS' or 'TYPE'
time_limit = 30 # Time limit that affects Time Bar and Duration countdown

# Use a timer
timer = Timer()

# Use the Movement class to keep track of movements
movement = Movement()

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

AppleThickness = 30
block_size = 10
FPS = 30
direction = "right" 
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Slither')

down_img = ['pictures/lukeMove/Luke_down_stationary.png',
        'pictures/lukeMove/Luke_down_walk_1.png',
        'pictures/lukeMove/Luke_down_walk_2.png']
right_img = ['pictures/lukeMove/Luke_right_stationary.png',
        'pictures/lukeMove/Luke_right_walk_1.png',
        'pictures/lukeMove/Luke_right_walk_2.png']
left_img = ['pictures/lukeMove/Luke_left_stationary.png',
        'pictures/lukeMove/Luke_left_walk_1.png',
        'pictures/lukeMove/Luke_left_walk_2.png']
up_img = ['pictures/lukeMove/Luke_up_stationary.png',
        'pictures/lukeMove/Luke_up_walk_1.png',
        'pictures/lukeMove/Luke_up_walk_2.png']
appleimg = pygame.image.load('pictures/apple.png')

# for run button
btnimg = pygame.image.load('pictures/runbtn.png').convert()
btn_rect = pygame.Rect(850, 550, *btnimg.get_rect().size)

clock = pygame.time.Clock()

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

def done_moving():
    if movement.get_next_move() == 'stationary':
        return True
    return False

def move_left():
    global game_state
    game_state = 'move_left'
    while game_state != 'idle':
        pass

def move_right():
    global game_state
    game_state = 'move_right'
    while game_state != 'idle':
        pass

def move_up():
    global game_state
    game_state = 'move_up'
    while game_state != 'idle':
        pass

def move_down():
    global game_state
    game_state = 'move_down'
    while game_state != 'idle':
        pass

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
    
def randAppleGen():
    randAppleX = round(random.randrange(0, map_width - AppleThickness))#/10.0)*10.0
    randAppleY = round(random.randrange(0, map_height - AppleThickness))#/10.0)*10.0
    return randAppleX, randAppleY
     
def game_intro():

    intro = True
    while intro:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro=False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
                    
        gameDisplay.fill(white)
        message_to_screen("Welcome to the Batcave", black, -100,
                          "medium")
        message_to_screen("Objective of the game is to help the rebel collect death star blueprint",
                          black, -30,"small")
        message_to_screen("Press C to play, P to pause, Q to Quit",
                          black, 30,"small")
        pygame.display.update()
        clock.tick(5)

def rebel(block_size, coords):

    if direction == "right":
        head = pygame.image.load(right_img[0])
        
    if direction == "left":
        head = pygame.image.load(left_img[0])
        
    if direction == "up":
        head = pygame.image.load(up_img[0])
        
    if direction == "down":
        head = pygame.image.load(down_img[0])
        
    gameDisplay.blit(head, coords)
    
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
    global direction, parsing, game_state
    direction = "right"
    gameExit = False
    gameOver = False
    lead_x = map_width - 50
    lead_y = map_height - 50
    lead_x_change = 0
    lead_y_change = 0
    rebelList = []
    rebelLength = 1
    randAppleX, randAppleY = randAppleGen()
    step_count = 0
    pause_duration = 0

    # use get_ticks to time
    timer.set_ticks_func(pygame.time.get_ticks)
    timer.reset()
    
    #eztext
    txtbx=[]
    elemNumber = 15
    ypos=0
    xpos=810
    deltay = 20
    a=['' for i in range(elemNumber)]
    b=['default' for i in range(elemNumber)]
    # Line number to show each line
    # create an input with a max length of 34,
    for i in range(elemNumber):
        txtbx.append(eztext.Input(maxlength=34,
                                color=red,y=ypos,x=xpos,prompt= "{:>2}: ".format(str(i+1))
                                    ))
        ypos+=deltay

    foci=0 #The focus index
    txtbx[foci].focus=True
    txtbx[foci].color=red


    barrier_width = 30
    xlocation = (map_width/2)+ random.randint(-0.2*map_width, 0.2*map_width)
    randomHeight = random.randrange(map_height*0.1,map_height*0.6)

    while not gameExit:
    
        if gameOver == True:
            message_to_screen("Game over", red,
                              y_displace=-50, size = "large")
            message_to_screen("Press C to play again or Q to quit", black,
                              50, size = "medium")
            pygame.display.update()
            
        while gameOver == True:
            
            parser_thread.stop()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameOver = False
                    gameExit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        gameExit = True
                        gameOver = False
                    if event.key == pygame.K_c:
                        gameLoop()

    ############## timer ##########################
        timer.update()
        seconds = timer.get_time() #calculate how many seconds
        #print (seconds) #print how many seconds


###################### END GAME CONDITIONS: Out of bound detection, Timelimit ###########################
        if lead_x > map_width - block_size or lead_x < 0 or lead_y > map_height - block_size \
            or lead_y<0:
            gameOver = True

####################### UPDATES PLAYER LOCATION ################################
        lead_x += lead_x_change
        lead_y += lead_y_change

####################### displaying it on screen ################################
        gameDisplay.fill(white)
        pygame.draw.line(gameDisplay,black,(map_width,display_height),(map_width,0), 2)#draw boundary for user to type code
        pygame.draw.line(gameDisplay,black,(0,map_height),(map_width,map_height), 2)#draw boundary for status bar
        gameDisplay.blit(appleimg, (randAppleX, randAppleY))
##        snakeHead = []
##        snakeHead.append(lead_x)
##        snakeHead.append(lead_y)
##        snakeList.append(snakeHead)
        rebel(block_size, (lead_x, lead_y))
        status(rebelLength - 1, time_limit,seconds)
        barrier(xlocation,randomHeight, barrier_width)
        
        
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
        if lead_x >= randAppleX and lead_x <= randAppleX + AppleThickness or lead_x + block_size >= randAppleX and lead_x + block_size <= randAppleX + AppleThickness:
            if lead_y >= randAppleY and lead_y <= randAppleY + AppleThickness:
                randAppleX, randAppleY = randAppleGen()
                rebelLength+=1
                
            elif lead_y + block_size >= randAppleY and lead_y + block_size <= randAppleY + AppleThickness:
                randAppleX, randAppleY = randAppleGen()
                rebelLength+=1

        clock.tick(30)

    ######################### Player controls - Keypress or Typed text #########################

        events = pygame.event.get()

        # to quit game
        for event in events:
            if event.type == pygame.QUIT:
                gameExit = True
        
        if control_mode == 'TYPE':
            # eztext
            # events for txtbx
            for i in range(elemNumber):
                # update txtbx and get return val
                a[i]=txtbx[i].update(None) #Add cursor to indicate where you are typing add (lose ability to type 'cursor')
                a[i]=txtbx[i].update(events)
                if i==foci:
                    txtbx[i].focus=True
                    txtbx[i].color=red
                else:
                    txtbx[i].focus=False
                    txtbx[i].color=black
                    
                # blit txtbx[i] on the screen
                txtbx[i].draw(gameDisplay)
                

            #Changing the focus to the next element 
            #every time enter is pressed
            for i in range(elemNumber):
                if a[i] != None:
                    txtbx[i].focus=False
                    txtbx[i].color=black
                    txtbx[(i+1)%elemNumber].focus=True
                    txtbx[(i+1)%elemNumber].color=red
                    foci=(i+1)%elemNumber

        elif control_mode == 'KEYPRESS':
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        lead_x_change = -block_size
                        step_count += 1
                        lead_y_change = 0
                        direction = "left"
                    elif event.key == pygame.K_RIGHT:
                        lead_x_change = block_size
                        step_count += 1
                        lead_y_change = 0
                        direction = "right"
                    elif event.key == pygame.K_UP:
                        lead_y_change = -block_size
                        step_count += 1
                        lead_x_change = 0
                        direction = "up"
                    elif event.key == pygame.K_DOWN:
                        lead_y_change = block_size
                        step_count += 1
                        lead_x_change = 0
                        direction = "down"
                    elif event.key == pygame.K_p:
                        pause()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        lead_x_change = 0
                        step_count = 0
                        lead_y_change = 0
                        direction = "left"
                    elif event.key == pygame.K_RIGHT:
                        lead_x_change = 0
                        step_count = 0
                        lead_y_change = 0
                        direction = "right"
                    elif event.key == pygame.K_UP:
                        lead_y_change = 0
                        step_count = 0
                        lead_x_change = 0
                        direction = "up"
                    elif event.key == pygame.K_DOWN:
                        lead_y_change = 0
                        step_count = 0
                        lead_x_change = 0
                        direction = "down"

        # Use the Movement class to keep track of moves.
        if control_mode == 'TYPE':
            next_move = movement.get_next_move()

            if next_move == 'stationary':
                lead_x_change = 0
                lead_y_change = 0
            elif next_move == 'up':
                direction = 'up'
                lead_x_change = 0
                lead_y_change = -block_size
            elif next_move == 'down':
                direction = 'down'
                lead_x_change = 0
                lead_y_change = block_size
            elif next_move == 'left':
                direction = 'left'
                lead_x_change = -block_size
                lead_y_change = 0
            elif next_move == 'right':
                direction = 'right'
                lead_x_change = block_size
                lead_y_change = 0

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

                    code_list = []
                    for i in range(elemNumber):
                        line = txtbx[i].value
                        if line != '':
                            if line[-1] == '|':
                                line = line[:-1]
                            code_list.append(line)

                    code = '\n'.join(code_list)

                    code = code.replace('self.', '')

                    parser_thread.start(parser_func, code)

                    for i in range(elemNumber):
                        txtbx[i].value = ''
                        txtbx[i].color = black

                    foci = 0


        pygame.display.update()


    parser_thread.stop()
    pygame.quit()
    quit()

game_intro()
gameLoop()

