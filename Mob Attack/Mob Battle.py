# Zombie - Gravity
# Book - Shoots squares
# Slime - Shoots circles
# Necromancer - 
from random import randint
import pygame
pygame.init()
class randomProjectiles:
    def __init__(self, mobType, numberOfProjectiles, projX, projY, projLength, projWidth, shift, direction):
        self.mobType = mobType
        self.numberOfProjectiles = randint(40, 60)
        self.projX = randint(0, 800)
        self.projY = randint(125, 600)
        self.projLength = projLength
        self.projWidth = projWidth
        self.shift = randint(1, 2)
        self.direction = randint(0, 3)

    def createProjectile(self):
        pygame.draw.rect(gameWindow, white, (self.projX, self.projY, self.projLength, self.projWidth), 0)
        if self.direction == 0:
            self.projX += self.shift
        if self.direction == 1:
            self.projX -= self.shift
        if self.direction == 2:
            self.projY += self.shift
        if self.direction == 3:
            self.projY -= self.shift
                
def getHealth(totalHealth, damage, heal, backBarX, backBarY, backBarLength, backBarWidth, backBarColor, barColor):
    pygame.draw.rect(gameWindow, backBarColor, (backBarX, backBarY, backBarLength, backBarWidth), 0) # Back Bar
    newHealth = totalHealth + heal - damage
    if newHealth >= 100:
        newHealth = 100
    pygame.draw.rect(gameWindow, barColor, (backBarX, backBarY, newHealth * 3, backBarWidth), 0) # Front Bar
    totalHealth = newHealth
    
    font = pygame.font.SysFont(None, 40)
    playerDisplay = font.render(str(totalHealth) + "/100", 1, barColor)
    playerText = font.render("PLAYER HEALTH", 1, barColor)
    gameWindow.blit(playerDisplay, (150, 70))
    gameWindow.blit(playerText, (90, 20))
    


xPos = 400
yPos = 300
shift = 2
black = (0, 0, 0)
red = (255, 0, 0)
darkRed = (139, 0, 0)
lightBlack = (20, 20, 20)
white = (255, 255, 255)
purple = (127, 0, 255)
emptyList = []
gameWindow = pygame.display.set_mode((800, 600))
gameWindow.fill(black)
inPlay = True

image = pygame.image.load("Heart Crystal.png")
newImage = pygame.transform.scale(image, (30, 30))

totalHealth = 100
damage = 0
heal = 0

#mobHealth =
#mobDamage =

number = randint(40, 50)
for i in range(number):
    zombie = randomProjectiles(0, True, True, True, 15, 15, True, True)
    emptyList.append(zombie)

while inPlay:
    gameWindow.fill(black)
    pygame.draw.rect(gameWindow, white, (5, 125, 790, 470), 5) 
    gameWindow.blit(newImage, (xPos, yPos))
    for i in emptyList:
        zombie.createProjectile()
    getHealth(totalHealth, damage, heal, 50, 100, 300, 10, darkRed, red)
    pygame.display.update()
    pygame.time.delay(5)    

    pygame.event.clear()
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        xPos -= shift

        if xPos <= 10:
            xPos = 10

    if keys[pygame.K_RIGHT]:
        xPos += shift

        if xPos >= 760:
            xPos = 760

    if keys[pygame.K_UP]:
        yPos -= shift

        if yPos <= 130:
            yPos = 130

    if keys[pygame.K_DOWN]:
        yPos += shift

        if yPos >= 560:
            yPos = 560

    

    
    

                
