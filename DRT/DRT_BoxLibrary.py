'''
DRT
Box Library

Developed by Steven Caro and Gian Favero
4/25/2021
'''

import pygame, math
import random
import time
from DRT_Constants import *

# class for the objects that appear in the game
class Button(pygame.sprite.Sprite):
    def __init__(self, shape, colour, size):
        super().__init__()

        w, h = pygame.display.get_surface().get_size()

        # dynamic sizing of the appearing objects based on the configuration setting
        if (w < h):
            if (size == "Small"):
                length = w/15
            elif (size == "Medium"):
                length = w/10
            elif (size == "Large"):
                length = w/5
        if (h < w):
            if (size == "Small"):
                length = w/15
            elif (size == "Medium"):
                length = w/10
            elif (size == "Large"):
                length = w/5

        length = round(length)

        self.image = pygame.Surface([length, length], pygame.SRCALPHA, 32) # create the surface to draw the object on
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        if (shape == "Square"):
            button = pygame.draw.rect(self.image, colour, [0, 0, length, length])

        elif (shape == "Circle"):
            button = pygame.draw.circle(self.image, colour, [length/2, length/2], length/2)

        # setting some object variables to be used in the main code and in the csv file
        self.creationTime = time.time()
        self.formattedCTime = time.strftime("%H:%M:%S")
        self.exitTime = None
        self.formattedETime = None
        self.Press= False
        self.delta = 0
        self.goodToWrite = False

# class to create and update the appearing objects
class Create:
    def __init__(self, screen, shape, colour, size, sleepTime):

        self.screen = screen
        self.buttonList = pygame.sprite.Group()
        self.sleepTime = sleepTime

        # Create button to be pressed
        self.button = Button(shape, colour, size)

        # Width and Height of screen
        w, h = screen.get_size()

        # Width and height of button
        bw, bh = self.button.rect.size
        
        self.button.rect.centerx = random.randint(bw / 2, w - bw / 2)
        self.button.rect.centery = random.randint(bh / 2, h - bh / 2)
        #print(self.button.rect.centerx, self.button.rect.centery)

        self.buttonList.add(self.button)

    #draws the appearing object
    def draw(self):
        self.buttonList.draw(self.screen)

    # listens for mouse click (object variable becomes true).
    def update(self):
        self.buttonList.update()
        makeNewObject = False

        # if mouse clicks object, find CSV data, remove object from view, start sleep timer, prepare for next round
        if self.button.Press is True:
                x, y = pygame.mouse.get_pos()
                if (self.button.rect.collidepoint(x, y)):
                    self.button.exitTime = time.time()
                    self.button.formattedETime = time.strftime("%H:%M:%S")

                    self.button.delta = self.button.exitTime - self.button.creationTime

                    self.buttonList.empty()

                    self.button.Press = False
                    self.button.goodToWrite = True

                # if mouse does not click the object, continue with current round
                else:
                    self.button.Press = False
                    return False
        #sleep timer
        if (self.button.exitTime is not None) and (time.time() - self.button.exitTime >= self.sleepTime):
            #return True
            makeNewObject = True
        else:
            #return False
            pass

        #return False
        return makeNewObject #the variable used in main to control when the next object is created
