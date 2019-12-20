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

grid = [["." for i in range(10)] for i in range(10)]

def loadMap(x,y):
    mapGrid = []
    with open("mapArea1.txt", "r") as mapFile:
        for line in mapFile:
            mapGrid.append(line.split())
    return mapGrid

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




#Obstacle classes
class Obstacle():
    
    def __init__(self, x, y, sprites):
        self.x = x
        self.y = y
        self.sprites = sprites

while(True):
    currDisplay = loadMap(0, 0)
    for i in r
