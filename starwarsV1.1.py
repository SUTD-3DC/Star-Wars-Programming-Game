from collections import deque
import pygame, eztext
import time
import random

pygame.init()

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0, 155, 0)

# Global settings
control_mode = 'KEYPRESS' # 'KEYPRESS' or 'TYPE'
time_limit = 15 # Time limit that affects Time Bar and Duration countdown

map_width = 800
map_height = 600
status_bar = 40
display_width = map_width +400
display_height = map_height + status_bar

time_limit = 60
AppleThickness = 30
block_size = 10
FPS = 30
direction = "right" 
gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Slither')

down_img = ['pictures/stationary.png','pictures/Luke_down_walk_1.png','pictures/Luke_down_walk_2.png']
right_img = ['pictures/right_stationary.png','pictures/Luke_right_walk_1.png','pictures/Luke_right_walk_2.png']
left_img = ['pictures/left_stationary.png','pictures/Luke_left_walk_1.png','pictures/Luke_left_walk_2.png']
up_img = ['pictures/up_stationary.png','pictures/Luke_up_walk_1.png','pictures/Luke_up_walk_2.png']
appleimg = pygame.image.load('pictures/apple.png')
clock = pygame.time.Clock()

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

def barrier(xlocation,randomHeight, barrier_width):
    pygame.draw.rect(gameDisplay,black, [xlocation, randomHeight, barrier_width, barrier_width])

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
        message_to_screen("Objective of the game is to help the snake eat apple",
                          black, -30,"small")
        message_to_screen("Press C to play, P to pause, Q to Quit",
                          black, 30,"small")
        pygame.display.update()
        clock.tick(5)

def snake(block_size, coords):

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
    global direction
    direction = "right"
    gameExit = False
    gameOver = False
    lead_x = map_width - 50
    lead_y = map_height - 50
    lead_x_change = 0
    lead_y_change = 0
    snakeList = []
    snakeLength = 1
    randAppleX, randAppleY = randAppleGen()
    step_count = 0
    pause_duration = 0

    #Buffer to hold the moves
    move_buffer = []
    move_hash = hash(tuple(move_buffer))
    
    #eztext
    txtbx=[]
    elemNumber = 32
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

    start_ticks=pygame.time.get_ticks() #starter tick
    
    while not gameExit:
    
        if gameOver == True:
            message_to_screen("Game over", red,
                              y_displace=-50, size = "large")
            message_to_screen("Press C to play again or Q to quit", black,
                              50, size = "medium")
            pygame.display.update()
            
        while gameOver == True:
            
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
        seconds=(pygame.time.get_ticks()-start_ticks+pause_duration)/1000.0 #calculate how many seconds
        #print (seconds) #print how many seconds


    ######################### Player controls - Keypress or Typed text #########################
        
        if control_mode == 'TYPE':
            # eztext
            # events for txtbx
            for i in range(elemNumber):
                # update txtbx and get return val
                a[i]=txtbx[i].update(None) #Add cursor to indicate where you are typing add (lose ability to type 'cursor')
                a[i]=txtbx[i].update(pygame.event.get())
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
                    b[i]=a[i]
                    if b[i]=="self.movedown()":
                        lead_y_change = block_size
                        step_count +=1
                        direction = "down"
                        move_buffer.append(direction) # Store text into buffer
                    elif b[i]=="self.moveup()":
                        lead_y_change = -block_size
                        step_count +=1
                        direction = "up"
                        move_buffer.append(direction)
                    elif b[i]=="self.moveright()":
                        lead_x_change = block_size
                        step_count +=1
                        direction = "right"
                        move_buffer.append(direction)
                    elif b[i]=="self.moveleft()":
                        lead_x_change = -block_size
                        step_count +=1
                        direction = "left"
                        move_buffer.append(direction)
                    txtbx[i].focus=False
                    txtbx[i].color=black
                    txtbx[(i+1)%elemNumber].focus=True
                    txtbx[(i+1)%elemNumber].color=red
                    foci=(i+1)%elemNumber

            if hash(tuple(move_buffer)) != move_hash: # Prints buffer iff it has changed
                move_hash = hash(tuple(move_buffer))
                print move_buffer

        elif control_mode == 'KEYPRESS':
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameExit = True
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
        

###################### END GAME CONDITIONS: Out of bound detection, Timelimit ###########################
        if lead_x > map_width - block_size or lead_x < 0 or lead_y > map_height - block_size \
            or lead_y<0 or seconds > time_limit:
            gameOver = True

####################### UPDATES PLAYER LOCATION ################################
        lead_x += lead_x_change
        lead_y += lead_y_change

####################### POP first item from move buffer ###################################
        if move_buffer != []:
            move_process = move_buffer.pop(0)
            lead_x_change = 0
            lead_y_change = 0
            step_count = 0

####################### displaying it on screen ################################
        gameDisplay.fill(white)
        pygame.draw.line(gameDisplay,black,(map_width,display_height),(map_width,0), 2)#draw boundary for user to type code
        pygame.draw.line(gameDisplay,black,(0,map_height),(map_width,map_height), 2)#draw boundary for status bar
        gameDisplay.blit(appleimg, (randAppleX, randAppleY))
##        snakeHead = []
##        snakeHead.append(lead_x)
##        snakeHead.append(lead_y)
##        snakeList.append(snakeHead)
        snake(block_size, (lead_x, lead_y))
        status(snakeLength - 1, time_limit,seconds)
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
                snakeLength+=1
                
            elif lead_y + block_size >= randAppleY and lead_y + block_size <= randAppleY + AppleThickness:
                randAppleX, randAppleY = randAppleGen()
                snakeLength+=1

        clock.tick(30)
        
        pygame.display.update()


    pygame.quit()
    quit()

game_intro()
gameLoop()
