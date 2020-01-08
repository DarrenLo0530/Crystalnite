######################################
#Names:Sanjay,Darren,Daniel
#Date:12/17/2019
#File Name:Game Summative Map Thing
#Description:Map of Crystalnite
######################################

import pygame

pygame.init()
width = 600
height = 600
gameWindow = pygame.display.set_mode((width,height)) #Screen Size

#Colours
BLACK =(0,0,0)
BLUE =(0,0,255)
RED =(255,0,0)
DARKGREY =(69,69,69)
DARKERGREY = (77,77,77)
WHITE = (255,250,240)
NAVY = (16,78,139)
LIGHTBLUE = (100,149,237)
GREEN = (0,255,0)
font = pygame.font.SysFont("Courier New Bold",18)
font2 = pygame.font.SysFont("Impact", 42)
font3 = pygame.font.SysFont("comicsans",24)
outline = 0

#-----------------------------------------------------------------------------#
#MAIN PROGRAM#
#-----------------------------------------------------------------------------#
playGame = True

gameWindow.fill(GREEN)
#gameWindow.fill(GREEN)
while playGame:
    pygame.display.update()

#Inventory
    pygame.event.clear()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        
        print("left pressed")
        pygame.draw.rect(gameWindow,BLACK,(100,100,320,300))
        pygame.draw.rect(gameWindow,WHITE,(130,120,50,50))
        pygame.draw.rect(gameWindow,WHITE,(200,120,50,50))
        pygame.draw.rect(gameWindow,WHITE,(270,120,50,50))
        pygame.draw.rect(gameWindow,WHITE,(340,120,50,50))
        pygame.draw.rect(gameWindow,WHITE,(130,190,50,50))
        pygame.draw.rect(gameWindow,WHITE,(200,190,50,50))
        pygame.draw.rect(gameWindow,WHITE,(270,190,50,50))
        pygame.draw.rect(gameWindow,WHITE,(340,190,50,50))
        pygame.draw.rect(gameWindow,WHITE,(130,260,50,50))
        pygame.draw.rect(gameWindow,WHITE,(200,260,50,50))
        pygame.draw.rect(gameWindow,WHITE,(270,260,50,50))
        pygame.draw.rect(gameWindow,WHITE,(340,260,50,50))
        pygame.draw.rect(gameWindow,WHITE,(130,330,50,50))
        pygame.draw.rect(gameWindow,WHITE,(200,330,50,50))
        pygame.draw.rect(gameWindow,WHITE,(270,330,50,50))
        pygame.draw.rect(gameWindow,WHITE,(340,330,50,50))
        

    elif keys[pygame.K_ESCAPE]:

        print("esc pressed")
        gameWindow.fill(GREEN)
        


