########################################################################
#File Name: CrystalNite.py
#Description: A cool RPG
#Authors: Darren Lo, Daniel Zhang and Sanjay Rajendran
#Date: Dec 16, 2019
#######################################################################

import pygame
import os

#Initialization
pygame.init()
WIDTH = 1400
HEIGHT = 900
display = pygame.display.set_mode((WIDTH, HEIGHT))

x = os.getcwd()
print(x)
print("HI")

#Colours
BLACK = (255, 255, 255)

grid = [["." for i in range(10)] for i in range(10)]

def loadMap(x,y):
    mapGrid = []
    with open("mapArea1.txt", "r") as mapFile:
        for line in mapFile:
            mapGrid.append(line.split())
        


class Obstacle():
    
    def __init__(this, x, y, sprites):
        this.x = x
        this.y = y
        this.sprites = sprites

loadMap(0,0)         
