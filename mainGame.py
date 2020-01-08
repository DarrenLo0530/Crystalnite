########################################################################
#File Name: CrystalNite.py
#Description: A cool RPG
#Authors: Darren Lo, Daniel Zhang and Sanjary Rajendran
#Date: Dec 16, 2019
#######################################################################
#pylint: disable = E1101

import pygame
from math import floor, ceil
import os

#Initialization
pygame.init()
WIDTH = 1400
HEIGHT = 900
display = pygame.display.set_mode((WIDTH, HEIGHT))
cwd = os.getcwd()   

#Colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (238, 232, 170)
WATER_BLUE = (0, 0, 130)
EDGE = (255, 255, 0)
BEIGE = (207, 185, 151)

#Fonts
textFont = pygame.font.SysFont("Comic Sans MS", 20)
storeFont = pygame.font.SysFont("Comic Sans MS", 15)

#Grid movement in directions(Clockwise starting from 1 is upwards direction)
movement = [[], [0, -1], [1, 0], [0, 1], [-1, 0]]

#Map Information
GRID_DIST_TOP = 25
GRID_WIDTH = 40
GRID_HEIGHT = 30
SQUARE_SIZE = 25
moveableSpaces = ["/", ".", ","]
areaMap = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

#Folder and file information
groundAreas = ["", "mapAreaGround1.txt", "mapAreaGround2.txt", "mapAreaGround3.txt", "mapAreaGround4.txt", "mapAreaGround5.txt", "mapAreaGround6.txt", "mapAreaGround7.txt", "mapAreaGround8.txt", "mapAreaGround9.txt"]
obstacleAreas = ["", "mapArea1.txt", "mapArea2.txt", "mapArea3.txt", "mapArea4.txt", "mapArea5.txt", "mapArea6.txt", "mapArea7.txt", "mapArea8.txt", "mapArea9.txt"]
weaponFiles = ["swordTypes.txt", "shieldTypes.txt"]
weaponArt = ["swordArt", "shieldArt"]

#Tile images
groundDict = {
    "." : pygame.transform.scale(pygame.image.load(os.path.join(cwd, "art", "grassArt.png")), (25, 25)), 
    "," : pygame.transform.scale(pygame.image.load(os.path.join(cwd, "art", "snowArt.png")), (25, 25))
}

obstacleDict = {
    "#" : pygame.transform.scale(pygame.image.load(os.path.join(cwd, "art", "treeArt.png")), (50, 50)),
    "/" : pygame.transform.scale(pygame.image.load(os.path.join(cwd, "art", "pathArt.png")), (25, 25)), 
    "%" : pygame.transform.scale(pygame.image.load(os.path.join(cwd, "art", "waterArt.png")), (25, 25)),
    "^" : pygame.transform.scale(pygame.image.load(os.path.join(cwd, "art", "everGreenTreeArt.png")), (50, 50)),
    "S" : pygame.transform.scale(pygame.image.load(os.path.join(cwd, "art", "signArt.png")), (25, 25)),
    "C" : pygame.transform.scale(pygame.image.load(os.path.join(cwd, "art", "chestArt.png")), (25, 25)),
    "T" : pygame.transform.scale(pygame.image.load(os.path.join(cwd, "art", "smallTreeArt.png")), (25, 25)),
    "O" : pygame.transform.scale(pygame.image.load(os.path.join(cwd, "art", "moveableRock.png")), (25, 25)),
}

def isInConstraint(x, y, xConstraint, yConstraint):
    if x >= 0 and x <= xConstraint and y >= 0 and y <= yConstraint:
        return True
    else:
        return False

def drawTextBoxes(text, delay, backgroundColour):
    for i in range(0, len(text), 2):
        pygame.draw.rect(display, backgroundColour, (150, 770, 1100, 100), 0)
        for k in range(2):
            displayText = textFont.render(text[i+k].strip(), 1, BLACK)
            display.blit(displayText, (175, 790 + k*30))
        
        pygame.display.update()
        pygame.time.wait(delay)

class StoreItem():
    def __init__(self, item, stock, cost):
        self.item = item
        self.stock = stock
        self.cost = cost

#Item classes
class Item():
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect

class Consumables(Item):
    def __init__(self, name, effect):
        Item.__init__(self, name, effect)


class AttackPotion(Consumables):
    def __init__(self, name, effect, time):
        Consumables.__init__(self, name, effect)
        
class SpeedPotion(Consumables):
    def __init__(self, name, effect, time):
        Consumables.__init__(self, name, effect)

class maxHealthPotion(Consumables):
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

class GameObject():
    def __init__(self, areaNumber):
        self.areaNumber = areaNumber

class FreeMovingObstacle(GameObject):
    def __init__(self, areaNumber, x, y):
        GameObject.__init__(self, areaNumber)
        self.x = x
        self.y = y

class Character(FreeMovingObstacle):
    def __init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction):
        FreeMovingObstacle.__init__(self, areaNumber, x, y)
        self.name = name
        self.remainingHealth = remainingHealth
        self.maxHealth = maxHealth
        self.speed = speed
        self.attack = attack
        self.direction = direction

    #Functions to detect obstacle collision
    def getGridPos(self, pointX, pointY): #Does not account for buffer area around grid
        gridPosX = (pointX - WIDTH/2 + GRID_WIDTH*SQUARE_SIZE/2)/SQUARE_SIZE
        gridPosY = (pointY - GRID_DIST_TOP)/SQUARE_SIZE
        return (gridPosX + 1, gridPosY + 1)

    def isCollide(self, obstacleMap, movedX, movedY):
        cornerLocations = []
        cornerLocations.append(self.getGridPos(movedX, movedY)) #Top left
        cornerLocations.append(self.getGridPos(movedX + SQUARE_SIZE - 1, movedY)) #Top Right
        cornerLocations.append(self.getGridPos(movedX, movedY + SQUARE_SIZE - 1)) #Bottom Left
        cornerLocations.append(self.getGridPos(movedX + SQUARE_SIZE - 1, movedY + SQUARE_SIZE - 1)) #Bottom Right

        for corner in cornerLocations:
            if not isInConstraint(corner[0], corner[1], GRID_WIDTH + 2, GRID_HEIGHT + 2):
                return True
            elif obstacleMap[floor(corner[1])][floor(corner[0])] not in moveableSpaces:
                return True
        return False

class NPC(Character):
    def __init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, sprites):
        Character.__init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction)
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
    def __init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, sprites):
        NPC.__init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, sprites)

class Passive(NPC):
    def __init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, sprites, dialogue):
        NPC.__init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, sprites)
        self.dialogue = dialogue
    def speak(self):
        drawTextBoxes(self.dialogue, 1000, BEIGE)

class SellingVillager(Passive):
    def __init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, sprites, dialogue, store):
        Passive.__init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, sprites, dialogue)
        self.store = store
    
    def sell(self, player):
        selling = True
        while(selling):
            pygame.draw.rect(display, BLACK, (30, 30, 500, 500), 0)
            for storeItem in self.store:
                itemName = storeFont(storeItem.item.name, 1, BLACK)
                itemStock = storeFont(storeItem.stock, 1, BLACK)
                itemCost = storeFont(storeItem.cost, 1, BLACK)
            

class GivingVillager(Passive):
    def __init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, sprites, dialogue, items):
        Passive.__init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, sprites, dialogue)
        self.items = items
    
    def giveItem(self, player):
        if len(self.items) == 0:
            drawTextBoxes("I have no more items to give you!", 1000, BEIGE)

        else:
            for i in self.items:
                player.inventory.append(i)
                drawTextBoxes("YOU GOT " + i.name + "!", 100, BEIGE)           

class Player(Character):
    def __init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, goldAmount, inventory, activeSword, activeShield, activeEffects):
        Character.__init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction)
        self.goldAmount = goldAmount
        self.inventory = inventory
        self.activeSword = activeSword
        self.activeShield = activeShield
        self.activeEffects = activeEffects

class PlayerMap(Player):
    sprites = BLUE
    def __init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, goldAmount, inventory, activeSword, activeShield, activeEffects):
        Player.__init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, goldAmount, inventory, activeSword, activeShield, activeEffects)
    def drawCharacter(self):
        pygame.draw.rect(display, self.sprites,(self.x, self.y, 25, 25), 0)
    
    def goNewArea(self): #Returns 0 if player has not left area, otherwise returns the direction they left from (clockwise starting from top)
        cornerLocations = []
        cornerLocations.append(self.getGridPos(self.x, self.y))
        cornerLocations.append(self.getGridPos(self.x + SQUARE_SIZE, self.y + SQUARE_SIZE)) 
        
        for i in range(2): #xPos
            for k in range(2): #yPos
                pointX = cornerLocations[i][0]
                pointY = cornerLocations[k][1]
                if(pointY <= 1):
                   return 1
                elif(pointX >= GRID_WIDTH+1):
                    return 2
                elif(pointY >= GRID_HEIGHT+1):
                    return 3
                elif(pointX <= 1):
                    return 4
        return 0

    def getMovement(self, grid):
        newX = self.x
        newY = self.y
        for i in range(self.speed):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_RIGHT] or keys[pygame.K_LEFT] or keys[pygame.K_UP] or keys[pygame.K_DOWN]:
                if keys[pygame.K_RIGHT]:
                    self.direction = 2
                elif keys[pygame.K_LEFT]:
                    self.direction = 4
                elif keys[pygame.K_UP]:
                    self.direction = 1
                elif keys[pygame.K_DOWN]:
                    self.direction = 3
                newX += movement[self.direction][0]
                newY += movement[self.direction][1]

            if not self.isCollide(grid, newX, newY):
                self.x = newX
                self.y = newY
    
    def getSpaceInfront(self): #Extra +- 1 removes issue of player being exactly right next to the sign due to nature of coordinate system
        if self.direction == 1:
            playerCoord = self.getGridPos(self.x + SQUARE_SIZE/2, self.y)
            return (floor(playerCoord[0]), floor(playerCoord[1]) - 1)
        elif self.direction == 2:
            playerCoord = self.getGridPos(self.x + SQUARE_SIZE - 1, self.y + SQUARE_SIZE/2)
            return (floor(playerCoord[0]) + 1, floor(playerCoord[1]))
        elif self.direction == 3:
            playerCoord = self.getGridPos(self.x + SQUARE_SIZE/2, self.y + SQUARE_SIZE - 1)
            return (floor(playerCoord[0]), floor(playerCoord[1]) + 1)
        elif self.direction == 4:
            playerCoord = self.getGridPos(self.x, self.y + SQUARE_SIZE/2)
            return (floor(playerCoord[0]) - 1, floor(playerCoord[1]))

    def interactAndUpdate(self, currentAreaNumber, currObstacleMap, signs, chests): #Used to interact with environment
        spaceInfront = self.getSpaceInfront()
        if isInConstraint(spaceInfront[0], spaceInfront[1], GRID_WIDTH + 2, GRID_HEIGHT + 2):
            if currObstacleMap[spaceInfront[1]][spaceInfront[0]] == "S":
                for s in signs:
                    if s.areaNumber == currentAreaNumber and s.gridX == spaceInfront[0] and s.gridY == spaceInfront[1]:
                        s.read()
                return False
            elif currObstacleMap[spaceInfront[1]][spaceInfront[0]] == "C":
                for c in chests:
                    if c.areaNumber == currentAreaNumber and c.gridX == spaceInfront[0] and c.gridY == spaceInfront[1]:
                        c.giveItem(self.inventory)
                return False
            elif currObstacleMap[spaceInfront[1]][spaceInfront[0]] == "T":
                currObstacleMap[spaceInfront[1]][spaceInfront[0]] = "."
                return True
            elif currObstacleMap[spaceInfront[1]][spaceInfront[0]] == "O":
                movedX = spaceInfront[0] + movement[self.direction][0]
                movedY = spaceInfront[1] + movement[self.direction][1]
                if isInConstraint(movedX, movedY, GRID_WIDTH, GRID_HEIGHT):
                    if currObstacleMap[movedY][movedX] == ".":
                        currObstacleMap[movedY][movedX] = "O"
                        currObstacleMap[spaceInfront[1]][spaceInfront[0]] = "."
                return True

#Environmental obstacles
class GridRestrictedObstacle(GameObject):
    def __init__(self, areaNumber, gridX, gridY):
        GameObject.__init__(self, areaNumber)
        self.gridX = gridX
        self.gridY = gridY

class Environmental(GridRestrictedObstacle):
    def __init__(self, areaNumber, gridX, gridY):
        GridRestrictedObstacle.__init__(self, areaNumber, gridX, gridY)

class Sign(Environmental):
    def __init__(self, areaNumber, gridX, gridY, text):
        Environmental.__init__(self, areaNumber, gridX, gridY)
        self.text = text
    def read(self):
        drawTextBoxes(self.text, 1000, WHITE)

class Chest(Environmental):
    def __init__(self, areaNumber, gridX, gridY, items):
        Environmental.__init__(self, areaNumber, gridX, gridY)
        self.items = items
    def giveItem(self, inventory):
        for i in self.items:
            inventory.append(i)
        self.items.clear()

#Functions that load different parts of the game
def getMap(areaNumber, areas, folder):
    mapGrid = []
    with open(os.path.join(cwd, folder, areas[areaNumber]), "r") as mapFile:
        for line in mapFile:
            mapGrid.append(list(line.strip("\n")))
    return mapGrid

def getMapSurface(groundGrid, obstacleGrid):
    background = pygame.Surface((WIDTH, HEIGHT))
    for i in range(30):
        for k in range(40):
            if groundGrid[i+1][k+1] in groundDict.keys():
                background.blit(groundDict[groundGrid[i+1][k+1]], (WIDTH/2 - GRID_WIDTH * SQUARE_SIZE/2 + k*SQUARE_SIZE, GRID_DIST_TOP + i*SQUARE_SIZE))
    for i in range(30):
        for k in range(40):  
            if obstacleGrid[i+1][k+1] in obstacleDict.keys():
                background.blit(obstacleDict[obstacleGrid[i+1][k+1]], (WIDTH/2 - GRID_WIDTH * SQUARE_SIZE/2 + k*SQUARE_SIZE, GRID_DIST_TOP + i*SQUARE_SIZE))
    return background

#Code to load in objects from the files
def loadSigns():
    signs = []
    with open(os.path.join(cwd, "objectFiles", "signs.txt"), "r") as signFile:
        for line in signFile:
            signInfo = line.split(" ")
            signs.append(Sign(int(signInfo[0]), int(signInfo[1]), int(signInfo[2]), signInfo[3].split("/")))
    return signs

def loadChests():
    chests = []
    with open(os.path.join(cwd, "objectFiles", "chests.txt", "r")) as chestFile:
        for line in chestFile:
            chestInfo = line.split(" ")
            chestItems = []
            
            chestItemNames = chestInfo[3].split("/")
            for i in chestItemNames:
                chestItems.append(createWeapon(i))

            chests.append(Chest(chestInfo[0], chestInfo[1], chestInfo[2], chestItems))
    return chests

def loadSellingVillagers():
    sellingVillagers = []
    with open(os.path.join(cwd, "objectFiles", "sellingVillagers.txt")) as sellingVillagerFile:
        for line in sellingVillagerFile:
            store = []
            storeItem = StoreItem()

def createWeapon(weaponName):
    for i in range(2):
        with open(os.path.join(cwd, "objectFiles", weaponFiles[i])) as weaponFile:
            for line in weaponFile:
                weaponInfo = line.split(" ")
                if weaponInfo[0] == weaponName:
                    return Sword(weaponInfo[0], weaponInfo[1], pygame.image.load(os.path.join(cwd, weaponArt[i], weaponInfo[2])))
        

########################################################################################################################################

#Initializing player character
player = PlayerMap(7, 275, 700, "Chad", 100, 100, 4, 10, 1, 0, [], "None", "None", [])

#Initializing map information
areaNumberX = 0
areaNumberY = 2
currGroundMap = getMap(player.areaNumber, groundAreas, "mapAreaGround")
currObstacleMap = getMap(player.areaNumber, obstacleAreas, "mapAreaObstacles")

background = getMapSurface(currGroundMap, currObstacleMap)

#Lists that store enemy positions
enemies = []
rocks = []
cuttableTrees = []
chests = []
signs = loadSigns()

inPlay = True
while(inPlay):
    display.fill(BLACK)
    display.blit(background, (0, 0))
    eventQueue = pygame.event.get()

    for event in eventQueue:
        if event.type == pygame.QUIT:
            inPlay = False
    #Character movement
    player.getMovement(currObstacleMap)
    player.drawCharacter()

    for event in eventQueue:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                isUpdate = player.interactAndUpdate(player.areaNumber, currObstacleMap, signs, chests)
                if isUpdate:
                    background = getMapSurface(currGroundMap, currObstacleMap)
            break

    #Loads in new map area or stays in current one
    loadMapVal = player.goNewArea() 
    if loadMapVal != 0:
        if loadMapVal == 1:
            areaNumberY -= 1
            player.y = GRID_DIST_TOP + GRID_HEIGHT * SQUARE_SIZE - SQUARE_SIZE - 10
        elif loadMapVal == 2:
            areaNumberX += 1
            player.x = WIDTH/2 - GRID_WIDTH*SQUARE_SIZE/2 + 10
        elif loadMapVal == 3:
            areaNumberY += 1
            player.y = GRID_DIST_TOP + 10
        elif loadMapVal == 4 :
            areaNumberX-=1
            player.x = WIDTH/2 + GRID_WIDTH*SQUARE_SIZE/2 - SQUARE_SIZE - 10 
        
        player.areaNumber = areaMap[areaNumberY][areaNumberX]
        currGroundMap = getMap(player.areaNumber, groundAreas, "mapAreaGround")
        currObstacleMap = getMap(player.areaNumber, obstacleAreas, "mapAreaObstacles")
        background = getMapSurface(currGroundMap, currObstacleMap)

    pygame.display.update()
    pygame.time.wait(5)

pygame.quit()