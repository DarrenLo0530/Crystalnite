#########################################
# File Name: 
# Description:  
# Author: ICS2O
# Date: 15/01/2018
#########################################
import pygame
from random import randint

pygame.init()
HEIGHT = 600
WIDTH  = 800
gameWindow=pygame.display.set_mode((WIDTH,HEIGHT))

BLACK = (  0,  0,  0)
WHITE = (255,255,255)
STEP = 6
shift = 8

#---------------------------------------#
#   functions                           #
#---------------------------------------#
def redrawGameWindow():
    gameWindow.blit(background, (0,0))
    gameWindow.blit(heart, (heartX,heartY))
    gameWindow.blit(vertical, (verticalX, verticalY))
    gameWindow.blit(vertical2, (verticalX2, verticalY2))
    gameWindow.blit(vertical3, (verticalX3, verticalY3))
    gameWindow.blit(vertical4, (verticalX4, verticalY4))
    gameWindow.blit(vertical5, (verticalX5, verticalY5))


    pygame.display.update()

#---------------------------------------#
#   main program                        #
#---------------------------------------#    

background = pygame.image.load("outer_space.jpg")

vertical = pygame.image.load("white obstacle.png")
verticalRect = vertical.get_rect()
verticalW = verticalRect.width
verticalH = verticalRect.height
verticalX = randint (30,200)
verticalY = randint (260,300)

vertical2 = pygame.image.load("white obstacle.png")
verticalRect2 = vertical.get_rect()
verticalW2 = verticalRect.width
verticalH2 = verticalRect.height
verticalX2 = randint (70,120)
verticalY2 = randint (340,500)

vertical3 = pygame.image.load("white obstacle.png")
verticalRect3 = vertical.get_rect()
verticalW3 = verticalRect.width
verticalH3 = verticalRect.height
verticalX3 = randint (70,120)
verticalY3 = randint (340,500)

vertical4 = pygame.image.load("white obstacle.png")
verticalRect4 = vertical.get_rect()
verticalW4 = verticalRect.width
verticalH4 = verticalRect.height
verticalX4 = randint (70,120)
verticalY4 = randint (340,500)

vertical5 = pygame.image.load("white obstacle.png")
verticalRect5 = vertical.get_rect()
verticalW5 = verticalRect.width
verticalH5 = verticalRect.height
verticalX5 = randint (70,120)
verticalY5 = randint (340,500)
 
heart = pygame.image.load("crystal.png")
heartRect = heart.get_rect()
heartW = heartRect.width
heartH = heartRect.height
heartX = 450
heartY = 450

print ("Hit ESC to end the program.")
clock = pygame.time.Clock()
FPS = 30
num = 0

#---------------------------------------#
inPlay = True
while inPlay:              
    redrawGameWindow()
    clock.tick(FPS)
    
    pygame.event.clear()                  
    keys = pygame.key.get_pressed()                                         
    if keys[pygame.K_ESCAPE]:           
        inPlay = False
    if keys[pygame.K_LEFT]:
        heartX = heartX - STEP
    if keys[pygame.K_RIGHT]:
        heartX = heartX + STEP
    if keys[pygame.K_UP]:
        heartY = heartY - STEP
    if keys[pygame.K_DOWN]:
        heartY = heartY + STEP

    if (verticalX < 950) and (verticalX2 < 950) and (verticalX3 < 950):
            verticalX += shift * 0.9
            verticalX2 += shift * 0.6
            verticalX3 += shift * 0.7
    elif (verticalX >= 950) and (verticalX2 < 950) and (verticalX3 < 950):
            verticalX = -150
            verticalX += shift * 0.9
            verticalX2 += shift * 0.6
            verticalX3 += shift * 0.7
    elif (verticalX < 950) and (verticalX2 >= 950) and (verticalX3 < 950):
            verticalX += shift * 0.9
            verticalX2 = -150
            verticalX2 += shift * 0.6
            verticalX3 += shift * 0.7
    elif (verticalX < 950) and (verticalX2 < 950) and (verticalX3 >= 950):
            verticalX += shift * 0.9
            verticalX2 += shift * 0.6
            verticalX3 = -150
            verticalX3 += shift * 0.7
        
    heartRect = pygame.Rect(heartX,heartY,heartW,heartH)
    verticalRect = pygame.Rect(verticalX,verticalY,verticalW,verticalH)
    verticalRect2 = pygame.Rect(verticalX2,verticalY2,verticalW2,verticalH2)
    verticalRect3 = pygame.Rect(verticalX3,verticalY3,verticalW3,verticalH3)
    verticalRect4 = pygame.Rect(verticalX4,verticalY4,verticalW4,verticalH4)
    verticalRect5 = pygame.Rect(verticalX5,verticalY5,verticalW5,verticalH5)

    if verticalRect.colliderect(heartRect):
        num += 1
        print ("Collision"),num,("detected!")
    if verticalRect2.colliderect(heartRect):
        num += 1
        print ("Collision"),num,("detected!")
    if verticalRect3.colliderect(heartRect):
        num += 1
        print ("Collision"),num,("detected!")
    if verticalRect4.colliderect(heartRect):
        num += 1
        print ("Collision"),num,("detected!")
    if verticalRect5.colliderect(heartRect):
        num += 1
        print ("Collision"),num,("detected!")

#---------------------------------------#     
pygame.quit()
    
