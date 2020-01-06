# item -> weapons and potions
# Healing potions can heal during and outside of battle, on player turn
# Speed potion increase movement during and outside of battle, on player turn
# Strength potion adds more damage during battle, on player turn
import pygame

pygame.init()
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
shift = 5
gameWindow = pygame.display.set_mode((800, 600))
gameWindow.fill(black)
health = 100
inPlay = True
# Health
# Health Bar
pygame.draw.rect(gameWindow, red, (350, 75, 200, 10), 0)

# Health Number
font = pygame.font.SysFont(None, 40)
healthNum = font.render(str(health) + "/100", 1, red)
gameWindow.blit(healthNum, (230, 70))

# "Health"
healthText = font.render("HEALTH", 1, red)
gameWindow.blit(healthText, (350, 20))

# Attack
pygame.draw.rect(gameWindow, red, (50, 500, 150, 75), 0)

# Item
pygame.draw.rect(gameWindow, blue, (325, 500, 150, 75), 0)

# Run
pygame.draw.rect(gameWindow, green, (600, 500, 150, 75), 0)

#Misc.
attackText = font.render("ATTACK", 1, white)
itemText = font.render("ITEM", 1, white)
runText = font.render("RUN", 1, white)
branch = 0
while inPlay:
    for event in pygame.event.get():
        
        x, y = pygame.mouse.get_pos()
        if (50 <= x <= 200) and (500 <= y <= 575) and (event.type == pygame.MOUSEBUTTONDOWN):
            branch = 1
        elif (325 <= x <= 475) and (500 <= y <= 575) and (event.type == pygame.MOUSEBUTTONDOWN):
            branch = 2
        elif (600 <= x <= 750) and (500 <= y <= 575) and (event.type == pygame.MOUSEBUTTONDOWN):
            branch = 3
        else:
            pygame.draw.rect(gameWindow, red, (50, 500, 150, 75), 0)
            pygame.draw.rect(gameWindow, blue, (325, 500, 150, 75), 0)
            pygame.draw.rect(gameWindow, green, (600, 500, 150, 75), 0)
        
        if branch == 1:
            gameWindow.fill(black)
            gameWindow.blit(attackText, (200, 200))
        elif branch == 2:
            gameWindow.fill(black)
            gameWindow.blit(itemText, (200, 200))
        elif branch == 3:
            gameWindow.fill(black)
            gameWindow.blit(runText, (200, 200))
            inPlay = False
        else:
            continue        
    pygame.display.update()
pygame.quit()




