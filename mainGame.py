########################################################################
#File Name: CrystalNite.py
#Description: A cool RPG
#Authors: Darren Lo, Daniel Zhang and Sanjary Rajendran
#Date: Dec 16, 2019
#######################################################################

import pygame
import os

#Initialization
pygame.init()
WIDTH = 1400
HEIGHT = 900
display = pygame.display.set_mode((WIDTH, HEIGHT))

#Colours
BLACK = (255, 255, 255)

def loadMap(playerX, playerY):
    #Loads 35 from left, right, top, and bottom resulting in a 71x71 grid
    mapGrid = [["" for i in range(71)] for k in range(71)]
    with open("mapArea1.txt", "r") as mapFile:
        for line in mapFile:
            mapGrid.append(line.split())
    return mapGrid

def drawMap(grid):

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

class Character():
    
    def __init__(self, x, y, sprites, name, health, speed, attack, direction):
        def __

while(True):
    currDisplay = loadMap(0, 0)
