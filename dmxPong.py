import sys
import os
import pygame, time
import array
import numpy as np
import random
from ola.ClientWrapper import ClientWrapper
################################# DEFINE STUFF AND INITIALIZE #################################
pygame.init()
pygame.font.init()
font = pygame.font.SysFont('Calibri',20)
DISPLAY_W, DISPLAY_H = 480, 270
canvas = pygame.Surface((DISPLAY_W,DISPLAY_H))
window = pygame.display.set_mode(((DISPLAY_W,DISPLAY_H)))
running = True
clock = pygame.time.Clock()
TARGET_FPS = 40
#define menu colors
WHITE = (255,255,255)
BLACK = (0,0,0)
#define dmx colors
dmxWHITE = np.array([255, 255, 255])
dmxBLACK = np.array([0, 0, 0])
dmxRED = np.array([255, 0, 0])
dmxBLUE = np.array([0, 0, 255])
dmxGREEN = np.array([0, 255, 0])
dmxTEAL = np.array([0, 100, 255])
dmxPINK = np.array([255, 0, 75])
#set up game variables
kickoff = False
ballSpeed = 3
ballVel = np.array([0, 0])
paddleVel = 6
decay = 0.5
gameMode = 1
prev_time = time.time()
dt = 0
start = 0
score = np.array([0,0])
FPS = 40
pxlWidth = 8
pxlHeight = 16
intens = 0.5
p1Paddle = float(1)
p2Paddle = float(1)
paddleLength = int(np.rint(pxlWidth*0.25)+1)
ball = np.array([1, (pxlHeight/2)-1])
p1Vel = float(0)
p2Vel = float(0)
upperBound = 1 
lowerBound = (pxlWidth -paddleLength+1)
nextPoint = True
AILVL = 25
#set dmx universe for OLA
universe = 2
gameArray = np.zeros((pxlWidth, pxlHeight), dtype=int)
dmxarray = np.zeros((170, 3), dtype=np.uint8)
def DmxSent(state):
        wrapper.Stop()
def movePaddle(paddle, vel, dt, decay, paddleVel, upperBound, lowerBound):
    movement = (dt *vel *paddleVel)
    paddle = paddle + movement
    vel = decay*vel
    if paddle < upperBound:
        paddle = upperBound
        vel = 0
    if paddle > lowerBound:
        paddle = lowerBound
        vel = 0
    return paddle, vel
def putPaddlesOnGrid(p1Paddle, p2Paddle):
    p1INT = int(p1Paddle)
    p2INT = int(p2Paddle)
    for i in range(0, paddleLength):
        gameArray[(p1INT-i)+1, 0] = 1
        gameArray[(p2INT-i)+1, (pxlHeight-1)] = 2
def moveBall(ball, ballVel, dt, ballSpeed):
    moveX = ballVel[0] * dt *ballSpeed
    moveY = ballVel[1] * dt *ballSpeed
    ball[0] = ball[0] + moveX
    ball[1] = ball[1] + moveY
    return ball
def putBallOnGrid(ball, gameArray):
    gameArray = gameArray
    ballX = int(np.rint(ball[0]))
    ballY = int(np.rint(ball[1]))
    if gameArray[(ballX), (ballY)] == 0:
        gameArray[(ballX), (ballY)] = 3
        collide = 0
    if gameArray[(ballX), (ballY)] == 1:
        collide = 1
    if gameArray[(ballX), (ballY)] == 2:
        collide = 2
    if gameArray[(ballX), (ballY)] == 4:
        collide = 4
    if gameArray[(ballX), (ballY)] == 5:
        collide = 5
    if gameArray[(ballX), (ballY)] == 6:
        collide = 6
    if gameArray[(ballX), (ballY)] == 7:
        collide = 7
    return gameArray, collide
def kickOff():
    i = random.randint(0, 1)
    if i == 0:
        return -1
    if i == 1:
        return 1
def collisionCheck(ball, p1Paddle, p2Paddle, pxlHeight, pxlWidth, paddleLength):
    ballXint = np.rint(ball[0])
    ballYint = np.rint(ball[1])
    ballXtop = np.rint(ball[0]+1)
    ballXbottom = np.rint(ball[0]-1)
    ballYtop = np.rint(ball[1]+1)
    ballYbottom = np.rint(ball[1]-1)
    if ballYbottom <= 0:
        collision = 1
    if ballYtop >= pxlHeight -1:
        collision = 2
    if ballXbottom <= 0:
        collision = 3
    if ballXtop >= pxlWidth -1:
        collision = 4
    else:
        collision = 0
    return collision
def putBoundariesOnGrid(gameArray, pxlHeight, pxlWidth):
    gameArray = gameArray
    for i in range(0, pxlHeight-1):
        gameArray[0, i] = 4
    for i in range(0, pxlHeight-1):
        gameArray[pxlWidth-1, i] = 5
    for i in range(0, pxlWidth):
        gameArray[i, 0] = 6
    for i in range(0, pxlWidth):
        gameArray[i, pxlHeight-1] = 7
    return gameArray
def collision(ball, ballVel, gameArray, collide, ballSpeed, dt, score, nextPoint):
    ballX = int(np.rint(ball[0]))
    ballY = int(np.rint(ball[1]))
    if collide == 1:
        moveX = -1*(ballVel[0] * dt *ballSpeed)
        moveY = -1*(ballVel[1] * dt *ballSpeed)
        ball[0] = ball[0] + moveX
        ball[1] = ball[1] + moveY
        ballVel[1] = 1
        ball[1] = 2
        collide = 0
    if collide == 2:
        moveX = -1*(ballVel[0] * dt *ballSpeed)
        moveY = -1*(ballVel[1] * dt *ballSpeed)
        ball[0] = ball[0] + moveX
        ball[1] = ball[1] + moveY
        ballVel[1] = -1
        ball[1] = pxlHeight -2
        collide = 0
    if collide == 4:
        moveX = -2*(ballVel[0] * dt *ballSpeed)
        moveY = -2*(ballVel[1] * dt *ballSpeed)
        ball[0] = ball[0] + moveX
        ball[1] = ball[1] + moveY
        ballVel[0] = 1
        gameArray[0, ballY] = 3
        collide = 0
    if collide == 5:
        moveX = -2*(ballVel[0] * dt *ballSpeed)
        moveY = -2*(ballVel[1] * dt *ballSpeed)
        ball[0] = ball[0] + moveX
        ball[1] = ball[1] + moveY
        ballVel[0] = -1
        gameArray[pxlWidth-1, ballY] = 3
        collide = 0
    if collide == 6:
        score[1] += 1
        collide = 0
        nextPoint = True
    if collide == 7:
        score[0] += 1
        collide = 0
        nextPoint = True
    return collide, ball, ballVel, gameArray, score, nextPoint
def p2AI(ball, p2Paddle, p2Vel, AILVL):
    if ball[0] > p2Paddle:
        p2Vel = 0.01*AILVL
    if ball[0] < p2Paddle:
        p2Vel = -0.01*AILVL
    return p2Vel
################################# GAME LOOP ##########################
while running:
    # Limit framerate
    clock.tick(FPS)
    # Compute delta time
    now = time.time()
    dt = now - prev_time
    prev_time = now
    #start the point
    if nextPoint == True:
        ball = [1, (pxlHeight/2)-1]
    if kickoff == True:
        if start == 1 or start == 2:
            if nextPoint == True:
                ballVel[1] = kickOff()
                ballVel[0] = 1
                kickoff = False
                nextPoint = False
    #move paddles
    p1Paddle, p1Vel = movePaddle(p1Paddle, p1Vel, dt, decay, paddleVel, upperBound, lowerBound)
    p2Paddle, p2Vel = movePaddle(p2Paddle, p2Vel, dt, decay, paddleVel, upperBound, lowerBound)
    ball = moveBall(ball, ballVel, dt, ballSpeed)
    #move the player 2 paddle if we're in 1 player mode
    if gameMode == 1:
        p2Vel = p2AI(ball, p2Paddle, p2Vel, AILVL)
    #reset game array
    gameArray.fill(0)
    #draw boundaries on game array
    gameArray = putBoundariesOnGrid(gameArray, pxlHeight, pxlWidth)
    #draw paddles
    putPaddlesOnGrid(p1Paddle, p2Paddle)
    #put ball on grid if there is no collision
    gameArray, collide = putBallOnGrid(ball, gameArray)
    #handle collission
    if collide != 0:
        collide, ball, ballVel, gameArray, score, nextPoint = collision(ball, ballVel, gameArray, collide, ballSpeed, dt, score, nextPoint)
    
    ################################# CHECK PLAYER INPUT #################################
    #for keys we want to hold down
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        p1Vel = -1
    if keys[pygame.K_DOWN]:
        p1Vel = 1
    if keys[pygame.K_w]:
        p2Vel = -1
    if keys[pygame.K_s]:
        p2Vel = 1
    #for keys we want to tap
    for event in pygame.event.get():
        #check if we want to quit
        if event.type == pygame.QUIT:
            running = False
        #check input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start = gameMode
            if event.key == pygame.K_LEFT:
                if gameMode == 2 and start == 0:
                    gameMode = 1
            if event.key == pygame.K_RIGHT:
                if gameMode == 1 and start == 0:
                    gameMode = 2
            if event.key == pygame.K_SPACE:
                kickoff = True
            #check intensity input
            if event.key == pygame.K_1:
                intens = 0.1
            if event.key == pygame.K_2:
                intens = 0.2
            if event.key == pygame.K_3:
                intens = 0.3
            if event.key == pygame.K_4:
                intens = 0.4
            if event.key == pygame.K_5:
                intens = 0.5
            if event.key == pygame.K_6:
                intens = 0.6
            if event.key == pygame.K_7:
                intens = 0.7
            if event.key == pygame.K_8:
                intens = 0.8
            if event.key == pygame.K_9:
                intens = 0.9
            if event.key == pygame.K_0:
                intens = 1
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        
    ################################# SET UP MENU #################################
    fps_text = font.render("FPS: " +str(round(clock.get_fps(),2)), False, (255,255,255))
    intens_text = font.render("| Press Space to Start | Intensity: " +str(intens*100), False, (255,255,255))
    if start == 0 and gameMode == 1:
        modeSelect = font.render(">1 Player | 2 Player", False, (255,255,255))
    if start == 0 and gameMode == 2:
        modeSelect = font.render("1 Player | >2 Player", False, (255,255,255))
    if start != 0:
        scoreDisplay = font.render(str(score[0]) + " | " + str(score[1]), False, (255,255,255))
    ###################################### UPDATE DMX ##########################################
    #get gameArray ready for dmx conversion
    convertarray = gameArray.flatten()
    #set the colors for head tail and food
    col1LVL = dmxTEAL*intens
    col1LVL = np.rint(col1LVL)
    col2LVL = dmxPINK*intens
    col2LVL = np.rint(col2LVL)
    col3LVL = dmxGREEN*intens
    col3LVL = np.rint(col3LVL)
    #put colors into dmxarray
    for i in range(0,pxlHeight*pxlWidth):
        if convertarray[i] == 0:
            dmxarray[i] = dmxBLACK
        if convertarray[i] == 1:
            dmxarray[i] = col1LVL
        if convertarray[i] == 2:
            dmxarray[i] = col2LVL
        if convertarray[i] == 3:
            dmxarray[i] = col3LVL
        if convertarray[i] == 4:
            dmxarray[i] = dmxBLACK
        if convertarray[i] == 5:
            dmxarray[i] = dmxBLACK
        if convertarray[i] == 6:
            dmxarray[i] = dmxBLACK
        if convertarray[i] == 7:
            dmxarray[i] = dmxBLACK
    #use ola to send dmx frame
    dmxpacket = dmxarray.tobytes()
    data = array.array('B', dmxpacket)
    wrapper = ClientWrapper()
    client = wrapper.Client()
    client.SendDmx(universe, data, DmxSent)
    wrapper.Run()
    ################################# UPDATE WINDOW AND DISPLAY ################################
    canvas.fill((0, 0, 0))
    canvas.blit(fps_text, (0, 0))
    canvas.blit(intens_text, (150, 0))
    if start == 0:
        canvas.blit(modeSelect, (50, DISPLAY_H/2))
    if start != 0:
        canvas.blit(scoreDisplay, (DISPLAY_W/2, DISPLAY_H/2))
    #debug prints
    #print(gameArray)
    #print(p1Vel)
    #print(p1Paddle)
    #print(ballVel)
    #print(collision)
    ################################# RENDER WINDOW ################################
    window.blit(canvas, (0,0))
    pygame.display.update()







