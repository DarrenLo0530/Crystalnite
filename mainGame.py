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

class Obstacle():
    
    def __init__(x, y, sprites):
        this.x = x
        this.y = y
        this.sprites = sprites
    def isCollision(grid):
        for(int i = 0)        
