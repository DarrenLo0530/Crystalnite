########################################################################
#File Name: CrystalNite.py
#Description: A cool RPG
#Authors: Darren Lo, Daniel Zhang and Sanjary Rajendran
#Date: Dec 16, 2019
#######################################################################
#pylint: disable = E1101

import pygame
from math import floor, ceil
from random import randint
import os
import time

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
titleFont = pygame.font.SysFont("Comic Sans MS", 40)

#Grid movement in directions(Clockwise starting from 1 is upwards direction)
movement = [[], [0, -1], [1, 0], [0, 1], [-1, 0]]

#Map Information
GRID_DIST_TOP = 25
GRID_WIDTH = 40
GRID_HEIGHT = 30
SQUARE_SIZE = 25
moveableSpaces = ["/", ".", ",", "-", "I"]
areaMap = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
spawnChances = [
    [],
    [20, 30, 50],
    [50, 50, 0],
    [10, 10, 80],
    [50, 40, 10],
    [30, 30, 40],
    [40, 50, 10],
    [100, 0, 0],
    [60, 30, 10],
    [40, 40, 20]
]

spawnRates = [0, 3, 3, 3, 3, 3, 3, 1, 3, 3]

#Folder and file information
groundAreas = ["", "mapAreaGround1.txt", "mapAreaGround2.txt", "mapAreaGround3.txt", "mapAreaGround4.txt", "mapAreaGround5.txt", "mapAreaGround6.txt", "mapAreaGround7.txt", "mapAreaGround8.txt", "mapAreaGround9.txt"]
obstacleAreas = ["", "mapArea1.txt", "mapArea2.txt", "mapArea3.txt", "mapArea4.txt", "mapArea5.txt", "mapArea6.txt", "mapArea7.txt", "mapArea8.txt", "mapArea9.txt"]
weaponFiles = ["weaponTypes.txt", "shieldTypes.txt"]

def loadTile(fileName, size):
    pygame.transform.scale(pygame.image.load(os.path.join(cwd, "art", "tileArt", fileName)), (size, size))

#Tile images
groundDict = {
    "." : loadTile("grassArt.png", 25),
    "," : loadTile("snowArt.png", 25),
    "/" : loadTile("pathArt.png", 25),
    "!" : loadTile("charredGroundArt.png", 25)
}

obstacleDict = {
    "#" : loadTile("treeArt.png", 50),
    "%" : loadTile("waterArt.png", 25),
    "^" : loadTile("everGreenTreeArt.png", 50),
    "S" : loadTile("signArt.png", 25),
    "C" : loadTile("chestArt.png", 25),
    "T" : loadTile("smallTreeArt.png", 25),
    "O" : loadTile("moveableRockArt.png", 25),
    "I" : loadTile("iceArt.png", 25),
    "L" : loadTile("staticRockArt.png", 50),
    "B" : loadTile("bushArt.png", 25)
}

#Game information
bossDefeated = False
def loadDirectionalSprites(folder, fileName): #Image rotation results in loss of quality
    sprites = [""]
    for i in range(1, 5):
        sprites.append(pygame.transform.scale(pygame.image.load(os.path.join(cwd, "art", folder, fileName + str(i) + ".png")), (25, 25)))
    return sprites

def isInConstraint(x, lower, upper):
    if x >= lower and x <= upper:
        return True
    else:
        return False

def drawTextBoxes(text, delay, backgroundColour):
    for i in range(0, len(text), 2):
        pygame.draw.rect(display, backgroundColour, (150, 770, 1100, 100), 0)
        for k in range(2):
            if i+k <= len(text) - 1:
                displayText = textFont.render(text[i+k].strip(), 1, BLACK)
                display.blit(displayText, (175, 790 + k*30))
        pygame.display.update()
        pygame.time.wait(delay)

def getScreenPos(gridX, gridY):
    screenX = gridX * SQUARE_SIZE - GRID_WIDTH*SQUARE_SIZE/2 + WIDTH/2 - SQUARE_SIZE
    screenY = gridY * SQUARE_SIZE + GRID_DIST_TOP - SQUARE_SIZE
    return (screenX, screenY)

#Information container classes  
class Node():
    def __init__(self, f, g, h, parent, position):
        self.f = f
        self.g = g
        self.h = h
        self.parent = parent
        self.position = position

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

class Equipable(Item):
    def __init__(self, name, effect, sprite):
        Item.__init__(self, name, effect)
        self.sprite = sprite

class Shield(Equipable):
    def __init__(self, name, effect, sprite):
        Equipable.__init__(self, name, effect, sprite)
    
class Weapon(Equipable):
    def __init__(self, name, effect, sprite):
        Equipable.__init__(self, name, effect, sprite)

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
    def getGridPos(self, pointX, pointY, floored): 
        gridPosX = (pointX - WIDTH/2 + GRID_WIDTH*SQUARE_SIZE/2)/SQUARE_SIZE
        gridPosY = (pointY - GRID_DIST_TOP)/SQUARE_SIZE
        if(floored):
            return (floor(gridPosX + 1), floor(gridPosY + 1))
        else:
            return (gridPosX + 1, gridPosY + 1)

    def slide(self, obstacleMap, mobs):
        middle = self.getGridPos(self.x + SQUARE_SIZE/2, self.y + SQUARE_SIZE/2, True)
        for i in range(3):
            if obstacleMap[middle[1]][middle[0]] == "I":
                newX = self.x + movement[self.direction][0]
                newY = self.y + movement[self.direction][1]

                for mob in mobs:
                    if mob != self:
                        if self.isContactEntity(mob, newX, newY):
                            return False
                if self.isCollide(obstacleMap, newX, newY):
                    return False
                else:
                    self.x = newX
                    self.y = newY 
            else:
                return False
        return True

    def isCollide(self, obstacleMap, movedX, movedY):
        cornerLocations = []
        cornerLocations.append(self.getGridPos(movedX, movedY, False)) #Top left
        cornerLocations.append(self.getGridPos(movedX + SQUARE_SIZE - 1, movedY, False)) #Top Right
        cornerLocations.append(self.getGridPos(movedX, movedY + SQUARE_SIZE - 1, False)) #Bottom Left
        cornerLocations.append(self.getGridPos(movedX + SQUARE_SIZE - 1, movedY + SQUARE_SIZE - 1, False)) #Bottom Right

        for corner in cornerLocations:
            if not isInConstraint(corner[0], 0, GRID_WIDTH + 2) or not isInConstraint(corner[1], 0, GRID_HEIGHT + 2):
                return True
            elif obstacleMap[floor(corner[1])][floor(corner[0])] not in moveableSpaces:
                return True
        return False

    def isContactEntity(self, entity, movedX, movedY):
        newPos = self.getGridPos(movedX + SQUARE_SIZE/2, movedY + SQUARE_SIZE/2, False)
        entityLocation = self.getGridPos(entity.x + SQUARE_SIZE/2, entity.y + SQUARE_SIZE/2, False)

        if isInConstraint(newPos[0], entityLocation[0] - 1, entityLocation[0] + 1) and isInConstraint(newPos[1], entityLocation[1] - 1, entityLocation[1] + 1):
            return True
        else:
            return False

class NPC(Character):
    def __init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction):
        Character.__init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction)
    
class Aggressive(NPC):
    path = []
    sprites = []
    index = 1
    pathAvailable = True
    timeSinceLastSearch = 1

    def __init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, level):
        NPC.__init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction)
        self.level = level
    
    def draw(self):
        display.blit(self.sprites[self.direction], (self.x, self.y))

    def getPlayerPath(self, player, obstacleMap, mobs): #aStar algorithm
        if(self.pathAvailable or self.timeSinceLastSearch % 50 == 0):
            self.timeSinceLastSearch = 1
            self.index = 1
            end = player.getGridPos(player.x, player.y, True)
            start = player.getGridPos(self.x, self.y, True)

            openSet = set()
            openList = []
            closedSet = set()

            openList.append(Node(0, 0, 0, None, start))
            openSet.add(start)

            minf = 100000
            toCheckIndex = 0

            while len(openSet) > 0:
                #Finds node with smallest f value
                for i, node in enumerate(openList):
                    if node.f < minf:
                        minf = node.f
                        toCheckIndex = i
                
                #Gets the current node
                currentNode = openList.pop(toCheckIndex)
                openSet.remove(currentNode.position)
                closedSet.add(currentNode.position)

                #Check if the node is the end
                if currentNode.position == end:
                    currentCheckNode = currentNode
                    path = []
                    while(currentCheckNode.parent != None):
                        path.insert(0, currentCheckNode.position)
                        currentCheckNode = currentCheckNode.parent
                    path.insert(0, start)
                    self.pathAvailable = True
                    self.path = path
                    return

                for i in movement[1:]:
                    newPos = (currentNode.position[0] + i[0], currentNode.position[1] + i[1])
                    #Makes sure it is in the map
                    if isInConstraint(newPos[0], 1, GRID_WIDTH) and isInConstraint(newPos[1], 1, GRID_HEIGHT):
                        if obstacleMap[newPos[1]][newPos[0]] in moveableSpaces:
                            if newPos in closedSet or newPos in openSet:
                                continue
                            else:
                                g = currentNode.g + 1
                                h = (currentNode.position[0] - newPos[0]) ** 2 + (currentNode.position[1] - newPos[1]) **2
                                f = g+h
                                openSet.add(newPos)
                                openList.append(Node(f, g, h, currentNode, newPos))
            self.path = []
            self.pathAvailable = False
        else:
            self.timeSinceLastSearch += 1

    def moveToGridCoord(self, obstacleMap, gridX, gridY, mobs):
        screenPos = getScreenPos(gridX, gridY)  
        for i in range(self.speed):
            if self.y < screenPos[1] and not self.isCollide(obstacleMap, self.x, self.y + 1):
                self.direction = 3
            elif self.x > screenPos[0] and not self.isCollide(obstacleMap, self.x - 1, self.y):
                self.direction = 4
            elif self.y > screenPos[1] and not self.isCollide(obstacleMap, self.x, self.y - 1):
                self.direction = 1
            elif self.x < screenPos[0] and not self.isCollide(obstacleMap, self.x + 1, self.y):
                self.direction = 2
            else:
                return True

            newX = self.x + movement[self.direction][0]
            newY = self.y + movement[self.direction][1]

            if not self.isCollide(obstacleMap, newX, newY):
                noEntityBlock = True
                for mob in mobs:
                    if mob != self:
                        if self.isContactEntity(mob, newX, newY):
                            noEntityBlock = False
                if noEntityBlock:
                    self.x = newX
                    self.y = newY
        return False

    def moveToPlayer(self, player, obstacleMap, mobs):
        playerPos = self.getGridPos(self.x, self.y, True)
        if not self.slide(obstacleMap, mobs) and self.index < len(self.path):
            if playerPos not in self.path:
                return
            if self.moveToGridCoord(obstacleMap, self.path[self.index][0], self.path[self.index][1], mobs):
                if self.index < len(self.path) - 1:
                    self.index += 1
        else:
            self.getPlayerPath(player, obstacleMap, mobs)
 
    
class Zombie(Aggressive):
    sprites = loadDirectionalSprites("zombie", "Zombie")
    def __init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, level):
        Aggressive.__init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, level)

class Book(Aggressive):
    sprites = loadDirectionalSprites("Book", "Book")
    def __init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, level):
        Aggressive.__init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, level)

class Slime(Aggressive):
    sprites = loadDirectionalSprites("slime", "Slime")
    def __init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, level):
        Aggressive.__init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, level)

class Necromancer(Aggressive):
    sprites = loadDirectionalSprites("necromancer", "Necromancer")
    def __init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, level):
        Aggressive.__init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, level)

class Passive(NPC):
    def __init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, sprites, dialogue):
        NPC.__init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction)
        self.sprites = sprites
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
    def speak(self):
        drawTextBoxes(self.dialogue, 1000, BEIGE)
    
    def giveItem(self, player):
        if(len(player.inventory) == player.maxInventorySize):
            drawTextBoxes(["Throw out some items please"], 1000, BEIGE)
        else:
            if len(self.items) == 0:
                drawTextBoxes(["I have no more items to give you!"], 1000, BEIGE)
            else:
                for i in self.items:
                    player.inventory.append(i)
                    drawTextBoxes(["YOU GOT A " + i.name + "!"], 1000, BEIGE)           

class Player(Character):
    maxInventorySize = 8
    def __init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, goldAmount, inventory, activeWeapon, activeShield, activeEffects):
        Character.__init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction)
        self.goldAmount = goldAmount
        self.inventory = inventory
        self.activeWeapon = activeWeapon
        self.activeShield = activeShield
        self.activeEffects = activeEffects

class PlayerMap(Player):
    sprites = loadDirectionalSprites("player", "Player")
    def __init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, goldAmount, inventory, activeWeapon, activeShield, activeEffects):
        Player.__init__(self, areaNumber, x, y, name, remainingHealth, maxHealth, speed, attack, direction, goldAmount, inventory, activeWeapon, activeShield, activeEffects)
    def draw(self):
         display.blit(self.sprites[self.direction], (self.x, self.y))
    def goNewArea(self): #Returns 0 if player has not left area, otherwise returns the direction they left from (clockwise starting from top)
        cornerLocations = []
        cornerLocations.append(self.getGridPos(self.x, self.y, False))
        cornerLocations.append(self.getGridPos(self.x + SQUARE_SIZE, self.y + SQUARE_SIZE, False)) 
        
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

    def getMovement(self, grid, mobs):
        if not player.slide(currObstacleMap, mobs): 
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
        
    def getSpaceInfront(self): #Extra +- 1 removes issue of player being exactly right next to object due to nature of coordinate system
        if self.direction == 1:
            playerCoord = self.getGridPos(self.x + SQUARE_SIZE/2, self.y, True)
            return (playerCoord[0], playerCoord[1] - 1)
        elif self.direction == 2:
            playerCoord = self.getGridPos(self.x + SQUARE_SIZE - 1, self.y + SQUARE_SIZE/2, True)
            return (playerCoord[0] + 1, playerCoord[1])
        elif self.direction == 3:
            playerCoord = self.getGridPos(self.x + SQUARE_SIZE/2, self.y + SQUARE_SIZE - 1, True)
            return (playerCoord[0], playerCoord[1] + 1)
        elif self.direction == 4:
            playerCoord = self.getGridPos(self.x, self.y + SQUARE_SIZE/2, True)
            return (playerCoord[0] - 1, playerCoord[1])

    def interactAndUpdate(self, currentAreaNumber, currObstacleMap, signs, chests, givingVillagers): #Used to interact with environment
        spaceInfront = self.getSpaceInfront()
        if isInConstraint(spaceInfront[0], 0, GRID_WIDTH + 2) and isInConstraint(spaceInfront[1], 0, GRID_HEIGHT + 2):
            if currObstacleMap[spaceInfront[1]][spaceInfront[0]] == "S":
                for s in signs:
                    if s.areaNumber == currentAreaNumber and s.gridX == spaceInfront[0] and s.gridY == spaceInfront[1]:
                        s.read()
                    return False
            elif currObstacleMap[spaceInfront[1]][spaceInfront[0]] == "C":
                for c in chests:
                    if c.areaNumber == currentAreaNumber and c.gridX == spaceInfront[0] and c.gridY == spaceInfront[1]:
                        c.giveItem(self)
                        return False
            elif currObstacleMap[spaceInfront[1]][spaceInfront[0]] == "T":
                currObstacleMap[spaceInfront[1]][spaceInfront[0]] = "."
                return True
            elif currObstacleMap[spaceInfront[1]][spaceInfront[0]] == "O":
                movedX = spaceInfront[0] + movement[self.direction][0]
                movedY = spaceInfront[1] + movement[self.direction][1]
                if currObstacleMap[movedY][movedX] == ".":
                    currObstacleMap[movedY][movedX] = "O"
                    currObstacleMap[spaceInfront[1]][spaceInfront[0]] = "."
                    return True
            elif currObstacleMap[spaceInfront[1]][spaceInfront[0]] == "G":
                for v in givingVillagers:
                    if v.areaNumber == currentAreaNumber and v.gridX == spaceInfront[0] and v.gridY == spaceInfront[1]:
                        v.speak()
                        v.giveItem(self)
                        return False
                
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
    def __init__(self, areaNumber, gridX, gridY, items, gold):
        Environmental.__init__(self, areaNumber, gridX, gridY)
        self.items = items
        self.gold = gold
    def giveItem(self, player):
        if(len(player.inventory) == player.maxInventorySize):
            drawTextBoxes(["Your bag is too heavy to take another item"], 1000, BEIGE)
        else:
            for i in self.items:
                player.inventory.append(i)
                drawTextBoxes(["YOU GOT " + i.name + "!"], 1000, BEIGE)  

        if self.gold != 0:
            player.goldAmount += self.gold
            drawTextBoxes(["The chest had " + str(self.gold) + " gold!"], 1000, BEIGE)           
            self.gold = 0
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
            signInfo = line.split(";")
            signs.append(Sign(int(signInfo[0]), int(signInfo[1]), int(signInfo[2]), signInfo[3].split("/")))
    return signs

def loadChests():
    chests = []
    with open(os.path.join(cwd, "objectFiles", "chests.txt"), "r") as chestFile:
        for line in chestFile:
            chestInfo = line.split(";")
            chestItems = []
            
            chestItemNames = chestInfo[3].split("/")
            for i in chestItemNames:
                chestItems.append(createWeapon(i))

            chests.append(Chest(int(chestInfo[0]), int(chestInfo[1]), int(chestInfo[2]), chestItems, int(chestInfo[4])))
    return chests

def loadSellingVillagers():
    sellingVillagers = []
    with open(os.path.join(cwd, "objectFiles", "sellingVillagers.txt")) as sellingVillagerFile:
        for line in sellingVillagerFile:
            listOfStoreItems = []
            vInfo = line.split(";")
            dialogue = vInfo[6].split("/")
            allStoreItems = vInfo[7].split("/")
            for storeItem in allStoreItems:
                storeItemInfo = storeItem.split(":")
                listOfStoreItems.append(StoreItem(createWeapon(storeItemInfo[0]), storeItemInfo[1], storeItemInfo[2]))
            sellingVillagers.append(SellingVillager(vInfo[0], vInfo[1], vInfo[2], vInfo[3], 0, 0, 0, 0, vInfo[4], vInfo[5], dialogue, listOfStoreItems))
    return sellingVillagers

def loadGivingVillagers():
    givingVillagers = []
    with open(os.path.join(cwd, "objectFiles", "givingVillagers.txt")) as givingVillagerFile:
        for line in givingVillagerFile:
            #Gets villager's dialogue
            vInfo = line.split(";")
            dialogue = vInfo[6].split("/")
            #Gets villager's items
            items = []
            for i in vInfo[7].split("/"):
                items.append(createWeapon(i))
            givingVillagers.append(GivingVillager(vInfo[0], vInfo[1], vInfo[2], vInfo[3], 0, 0, 0, 0, vInfo[4], vInfo[5], dialogue, items))

def createWeapon(weaponName):
    with open(os.path.join(cwd, "objectFiles", "weaponTypes.txt")) as weaponFile:
        for line in weaponFile:
            weaponInfo = line.split(";")
            if weaponInfo[0] == weaponName:
                return Weapon(weaponInfo[0], weaponInfo[1], pygame.image.load(os.path.join(cwd, "art", "weaponArt", weaponInfo[2].strip())))
    
    with open(os.path.join(cwd, "objectFiles", "shieldTypes.txt")) as shieldFile:
        for line in shieldFile:
            weaponInfo = line.split(";")
            if weaponInfo[0] == weaponName:
                return Shield(weaponInfo[0], weaponInfo[1], pygame.image.load(os.path.join(cwd, "art", "shieldArt", weaponInfo[2].strip())))

def spawnMobs(player, obstacleMap): 
    mobs = []
    excludeX = []
    excludeY = []
    mobChances = spawnChances[player.areaNumber]

    if player.areaNumber == 3 and not bossDefeated:
        mobs.append(Necromancer(3, 700, 300, "Overlord", 500, 500, 20, 10, 3, 5))
    if spawnRates[player.areaNumber] == 0:
        return mobs

    playerLocation = player.getGridPos(player.x, player.y, True)

    for i in range(spawnRates[player.areaNumber]):
        correctSpawn = False
        while(not correctSpawn):
            x = randint(3, GRID_WIDTH - 1)
            y = randint(3, GRID_HEIGHT - 1)
            #Checks if location is an obstacle or the player
            if (obstacleMap[y][x] in moveableSpaces) and playerLocation != (x, y):
                #Checks if location is another mob already
                if not x in excludeX and not y in excludeY:
                    correctSpawn = True
                    excludeX.append(x)
                    excludeY.append(y)
                    mobNumber = randint(1, 100)
                    mobLevel = randint(1, 3)
                    screenPos = getScreenPos(x, y)
                    
                    if mobNumber <= mobChances[0]:
                        mobs.append(Zombie(player.areaNumber, screenPos[0], screenPos[1], "Zombie", 40 + mobLevel*3, 40 + mobLevel*3, 1+mobLevel, 5+mobLevel*2, 3, mobLevel))
                    elif mobNumber > mobChances[1] + mobChances[0] and mobNumber <= mobChances[2] + mobChances[1] + mobChances[0]:
                        mobs.append(Slime(player.areaNumber, screenPos[0], screenPos[1], "Slime", 40 + mobLevel*3, 40 + mobLevel*3, 1+mobLevel, 5+mobLevel*2, 3, mobLevel))
                    else:
                        mobs.append(Book(player.areaNumber, screenPos[0], screenPos[1], "Book", 40 + mobLevel*3, 40 + mobLevel*3, 1+mobLevel, 5+mobLevel*2, 3, mobLevel))
    return mobs


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
givingVillagers = loadGivingVillagers
enemies = []
rocks = []
cuttableTrees = []
chests = loadChests()
signs = loadSigns()
mobs = spawnMobs(player, currObstacleMap)
mobPathCounter = 0

inPlay = True
clock = pygame.time.Clock()

startScreen = True
mapScreen = False
battle = False

while(inPlay):
    eventQueue = pygame.event.get()
    for event in eventQueue:
            if event.type == pygame.QUIT:
                inPlay = False
                

    if startScreen:
        display.fill(BLACK)
        title = titleFont.render("CRYSTALNITE", 1, WHITE)
        titleRect = title.get_rect(center = (WIDTH/2, 400))
        start = textFont.render("Press space to start...", 1, WHITE)
        startRect = start.get_rect(center = (WIDTH/2, 500))
        display.blit(title, titleRect)
        display.blit(start, startRect)
        pygame.display.update()
        for event in eventQueue:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    startScreen = False
                    mapScreen = True

    #Death message
    elif player.remainingHealth == 0:
            display.fill(BLACK)
            pygame.display.update()
            pygame.time.wait(1000)
            battle = False
            mapScreen = True
            player.x = 275
            player.y = 700
            player.areaNumber = areaMap[areaNumberY][areaNumberX]
            currGroundMap = getMap(player.areaNumber, groundAreas, "mapAreaGround")
            currObstacleMap = getMap(player.areaNumber, obstacleAreas, "mapAreaObstacles")
            background = getMapSurface(currGroundMap, currObstacleMap)
            mobs = spawnMobs(player, currObstacleMap)

    #If player is moving around the map
    elif mapScreen:
        mobPathCounter += 1
        #If player is dead
        display.fill(BLACK)
        display.blit(background, (0, 0))

        #Character movement
        player.getMovement(currObstacleMap, mobs)
        player.draw()

        for i, mob in enumerate(mobs):
            mob.draw()
            if mobPathCounter % 30 == 0:
                mob.getPlayerPath(player, currObstacleMap, mobs)
            mob.moveToPlayer(player, currObstacleMap, mobs)
            if mob.isContactEntity(player, mob.x, mob.y):
                if mob.name == "Overlord":
                    bossDefeated = True
                mobs.pop(i)

        for event in eventQueue:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    isUpdate = player.interactAndUpdate(player.areaNumber, currObstacleMap, signs, chests, givingVillagers)
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
            mobs = spawnMobs(player, currObstacleMap)

        if mobPathCounter == 1000:
                mobPathCounter = 0
        pygame.display.update()
    
    clock.tick(70)
pygame.quit()