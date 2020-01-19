######################################
#Names:Sanjay,Darren,Daniel
#Date:12/17/2019
#File Name:Game Summative Map Thing
#Description:Map of Crystalnite
######################################

import pygame

pygame.init()
width = 800
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


while playGame:
    pygame.display.update()
    for event in pygame.event.get():  

#Inventory
        pygame.event.clear()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:

        
            pygame.draw.rect(gameWindow,DARKGREY,(0,0,width,height))

            inventory = font2.render("Inventory",1,RED,)
            gameWindow.blit(inventory,(320,100))

            pygame.draw.rect(gameWindow,BLACK,(150,150,500,500))
            box1 = pygame.draw.rect(gameWindow,WHITE,(180,170,75,75))
            box2 = pygame.draw.rect(gameWindow,WHITE,(300,170,75,75))
            box3 = pygame.draw.rect(gameWindow,WHITE,(420,170,75,75))
            box4 = pygame.draw.rect(gameWindow,WHITE,(540,170,75,75))
            box5 = pygame.draw.rect(gameWindow,WHITE,(180,270,75,75))
            box6 = pygame.draw.rect(gameWindow,WHITE,(300,270,75,75))
            box7 = pygame.draw.rect(gameWindow,WHITE,(420,270,75,75))
            box8 = pygame.draw.rect(gameWindow,WHITE,(540,270,75,75))
            box9 = pygame.draw.rect(gameWindow,WHITE,(180,370,75,75))
            box10 = pygame.draw.rect(gameWindow,WHITE,(300,370,75,75))
            box11 = pygame.draw.rect(gameWindow,WHITE,(420,370,75,75))
            box12 = pygame.draw.rect(gameWindow,WHITE,(540,370,75,75))
            box13 = pygame.draw.rect(gameWindow,WHITE,(180,470,75,75))
            box14 = pygame.draw.rect(gameWindow,WHITE,(300,470,75,75))
            box15 = pygame.draw.rect(gameWindow,WHITE,(420,470,75,75))
            box16 = pygame.draw.rect(gameWindow,WHITE,(540,470,75,75))

        if event.type == pygame.MOUSEBUTTONDOWN:
                print (" pressed mouse button  :",event.button)
        elif event.type == pygame.MOUSEBUTTONUP:
                print ("released mouse button  :",event.button)
        elif event.type == pygame.MOUSEMOTION:
                print (" current mouse location:",pygame.mouse.get_pos())

        elif keys[pygame.K_ESCAPE]:

            gameWindow.fill(GREEN)
        


