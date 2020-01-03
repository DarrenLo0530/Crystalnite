########################################################################
#File Name: CrystalNite.py
#Description: A cool RPG
#Authors: Darren Lo, Daniel Zhang and Sanjary Rajendran
#Date: Dec 16, 2019
#######################################################################
#pylint: disable = E1101

import pygame
from math import floor, ceil


#Initialization
pygame.init()
WIDTH = 1400
HEIGHT = 900
display = pygame.display.set_mode((WIDTH, HEIGHT))

#Colours
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (238, 232, 170)
WATER_BLUE = (0, 0, 130)
EDGE = (255, 255, 0)

#Map Information
GRID_DIST_TOP = 25
GRID_WIDTH = 40
GRID_HEIGHT = 30
SQUARE_SIZE = 25
moveableSpaces = [".", "/", ","]
tileDict = {
    "#" : pygame.transform.scale(pygame.image.load("treeArt.png"), (25, 25)),
    "." : pygame.transform.scale(pygame.image.load("grassArt.png"), (25, 25)), 
    "/" : pygame.transform.scale(pygame.image.load("pathArt.png"), (25, 25)), 
    "%" : pygame.transform.scale(pygame.image.load("waterArt.png"), (25, 25)),
    "-" : pygame.transform.scale(pygame.image.load("waterEdgeArt.png"), (25, 25))
}

#Code to load the map
def getMap(areaNumber, areas):
    mapGrid = []
    with open(areas[areaNumber], "r") as mapFile:
        for line in mapFile:
            mapGrid.append(list(line.strip("\n")))
    return mapGrid

def drawMap(grid):
    for i in range(30):
        for k in range(40):
            if(grid[i][k] in tileDict.keys()):

#Item classes
class Item():
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

class Consumables(Item):
    def __init__(self, name, effect):
        Item.__init__(self, name, effect)

class SpeedPotion(Consumables):
    def __init__(self, name, effect):
        Consumables.__init__(self, name, effect)

class HealthPotion(Consumables):
    def __init__(self, name, effect):
        Consumables.__init__(self, name, effect)

class AttackPotion(Consumables):
    def __init__(self, name, effect):
        Consumables.__init__(self, name, effect)

class Weapons(Item):
    def __init__(self, name, effect, sprite):
        Item.__init__(self, name, effect)
        self.sprite = sprite

class Shield(Weapons):
    def __init__(self, name, effect, sprite):
        Weapons.__init__(self, name, effect, sprite)
    
class Sword(Weapons):
    def __init__(self, name, effect, sprite):
        Weapons.__init__(self, name, effect, sprite)


#Obstacle classes
class Obstacle():
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Character(Obstacle):
    def __init__(self, x, y, name, health, speed, attack, direction):
        Obstacle.__init__(self, x, y)
        self.name = name
        self.health = health
        self.speed = speed
        self.attack = attack
        self.direction = direction
    
    #Functions to detect obstacle collision
    def getGridPos(self, pointX, pointY, grid):
        gridPosX = (pointX - WIDTH/2 + GRID_WIDTH*SQUARE_SIZE/2)/SQUARE_SIZE
        gridPosY = (pointY - GRID_DIST_TOP)/SQUARE_SIZE
        return (gridPosX, gridPosY)

    def isCollide(self, grid, movedX, movedY):
        cornerLocations = []
        cornerLocations.append(self.getGridPos(movedX, movedY, grid))
        cornerLocations.append(self.getGridPos(movedX + SQUARE_SIZE, movedY + SQUARE_SIZE, grid)) 
        
        for i in range(2): #xPos
            for k in range(2): #yPos
                pointX = cornerLocations[i][0]
                pointY = cornerLocations[k][1]
                if(pointX <= -1 or pointX >= GRID_WIDTH+1 or pointY <= -1 or pointY >= GRID_HEIGHT+1):
                   return True
                elif(grid[floor(pointY)+1][floor(pointX)+1] not in moveableSpaces):
                    return True
        return False


class NPC(Character):
    def __init__(self, x, y, name, health, speed, attack, direction, sprites):
        Character.__init__(self, x, y, name, health, speed, attack, direction)
        self.sprites = sprites
    #Functions to move character around
    def moveRight(self):
        self.x += self.speed
    def moveLeft(self):
        self.x -= self.speed
    def moveUp(self):
        self.y += self.speed
    def moveDown(self):
        self.y += self.speed

class Aggressive(NPC):
    def __init__(self, x, y, name, health, speed, attack, direction, sprites):
        NPC.__init__(self, x, y, name, health, speed, attack, direction, sprites)

class Passive(NPC):
    def __init__(self, x, y, name, health, speed, attack, direction, sprites, say, item):
        NPC.__init__(self, x, y, name, health, speed, attack, direction, sprites)
        self.say = say
        self.item = item

class Player(Character):
    def __init__(self, x, y, name, health, speed, attack, direction, inventory, activeSword, activeShield, activeEffects):
        Character.__init__(self, x, y, name, health, speed, attack, direction)
        self.inventory = inventory
        self.activeSword = activeSword
        self.activeShield = activeShield
        self.activeEffects = activeEffects

class PlayerMap(Player):
    sprites = BLUE
    def __init__(self, x, y, name, health, speed, attack, direction, inventory, activeSword, activeShield, activeEffects):
        Player.__init__(self, x, y, name, health, speed, attack, direction, inventory, activeSword, activeShield, activeEffects)
    def drawCharacter(self):
        pygame.draw.rect(display, self.sprites,(self.x, self.y, 25, 25), 0)
    
    def goNewArea(self, grid): #Returns 0 if player has not left area, otherwise returns the direction they left from (clockwise starting from top)
        cornerLocations = []
        cornerLocations.append(self.getGridPos(self.x, self.y, grid))
        cornerLocations.append(self.getGridPos(self.x + SQUARE_SIZE, self.y + SQUARE_SIZE, grid)) 
        
        for i in range(2): #xPos
            for k in range(2): #yPos
                pointX = cornerLocations[i][0]
                pointY = cornerLocations[k][1]
                if(pointY <= 0):
                   return 1
                elif(pointX >= GRID_WIDTH):
                    return 2
                elif(pointY >= GRID_HEIGHT):
                    return 3
                elif(pointX <= 0):
                    return 4
        return 0

    def getMovement(self, grid):
        newX = self.x
        newY = self.y
        for i in range(2):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT]:
                newX += self.speed/2
            elif keys[pygame.K_LEFT]:
                newX -= self.speed/2
            elif keys[pygame.K_UP]:
                newY -= self.speed/2
            elif keys[pygame.K_DOWN]:
                newY += self.speed/2
            if not self.isCollide(grid, newX, newY):
                self.x = newX
                self.y = newY

class PlayerBattle(Player):
    def __init__(self, x, y, name, health, speed, attack, direction, inventory, activeSword, activeShield, activeEffects, battleSpeed):
        Player.__init__(self, x, y, name, health, speed, attack, direction, inventory, activeSword, activeShield, activeEffects)
        self.battleSpeed = battleSpeed


#Environmental obstacles
class Environmental(Obstacle):
    def __init__(self, x, y, sizeX, sizeY):
        Obstacle.__init__(self, x, y)
        self.sizeX = sizeX
        self.sizeY = sizeY

class Sign(Environmental):
    def __init__(self, x, y, sizeX, sizeY, text):
        Environmental.__init__(self, x, y, sizeX, sizeY)
        
#MAIN CODE

#Map drawing and loading

areas = ["", "mapArea1.txt", "mapArea2.txt", "mapArea3.txt", "mapArea4.txt", "mapArea5.txt", "mapArea6.txt", "mapArea7.txt", "mapArea8.txt", "mapArea9.txt"]
areaMap = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
currentAreaNumber = 7
areaNumberX = 0
areaNumberY = 2


#Initializing player character]
player = PlayerMap(275, 700, "Chad", 100, 2, 10, 2, [], "None", "None", "None")
currMap = getMap(currentAreaNumber, areas)


inPlay = True
while(inPlay):
    display.fill(BLACK)
    currMap = getMap(currentAreaNumber, areas)
    drawMap(currMap)
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False

    player.getMovement(currMap)
    player.drawCharacter()
    
    loadMapVal = player.goNewArea(currMap) 
    if(loadMapVal != 0):
        if(loadMapVal == 1):
            areaNumberY -= 1
            player.y = GRID_DIST_TOP + GRID_HEIGHT * SQUARE_SIZE - SQUARE_SIZE - 10
        elif(loadMapVal == 2):
            areaNumberX += 1
            player.x = WIDTH/2 - GRID_WIDTH*SQUARE_SIZE/2 + 10
        elif(loadMapVal == 3):
            areaNumberY += 1
            player.y = GRID_DIST_TOP + 10
        elif(loadMapVal == 4):
            areaNumberX-=1
            player.x = WIDTH/2 + GRID_WIDTH*SQUARE_SIZE/2 - SQUARE_SIZE - 10 
        
        currentAreaNumber = areaMap[areaNumberY][areaNumberX]
    pygame.display.update()
    pygame.time.wait(1)

pygame.quit()