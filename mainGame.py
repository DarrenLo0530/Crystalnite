########################################################################
#File Name: CrystalNite.py
#Description: A cool RPG
#Authors: Darren Lo, Daniel Zhang and Sanjary Rajendran
#Date: Dec 16, 2019
#######################################################################

import pygame


#Initialization
pygame.init()
WIDTH = 1400
HEIGHT = 900
display = pygame.display.set_mode((WIDTH, HEIGHT))

#Colours
BLACK = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

def loadMap(areaNumber, areas):
    mapGrid = []
    with open(areas[areaNumber], "r") as mapFile:
        for line in mapFile:
            mapGrid.append(list(line))
    return mapGrid


def drawMap(grid, tileDict):
    for i in range(30):
        for k in range(40):
            pygame.draw.rect(display, tileDict[grid[i][k]], (k*20, i*20, 20, 20), 0)

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
    def __init__(self, x, y, sprites):
        self.x = x
        self.y = y
        self.sprites = sprites

class Character(Obstacle):
    def __init__(self, x, y, sprites, name, health, speed, attack, direction):
        Obstacle.__init__(self, x, y, sprites)
        self.name = name
        self.health = health
        self.speed = speed
        self.attack = attack
        self.direction = direction

tileDict = {
    "#" : GREEN, 
    "." : RED,
    "+" : GREEN
}
areas = ["", "mapArea1.txt", "mapArea2.txt", "mapArea3.txt", "mapArea4.txt", "mapArea5.txt", "mapArea6.txt", "mapArea7.txt", "mapArea8.txt", "mapArea9.txt"]
mapArea = 7

currArea = loadMap(mapArea, areas)
drawMap(currArea, tileDict)
pygame.display.update()
pygame.time.wait(2000)