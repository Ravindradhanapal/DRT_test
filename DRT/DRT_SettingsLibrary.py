'''
DRT
Settings Library

Developed by Steven Caro and Gian Favero
4/25/2021
'''

import pygame, math
from DRT_Constants import *

class Buttons(pygame.sprite.Sprite):
    def __init__(self, buttonColour, w_h, text, font, textNotSelectedColour, textSelectedColour):
        # Call the parent class (Sprite) constructor  
        super().__init__()
        self.image = pygame.Surface(w_h)

        # Get colour constants
        self.colour = Colours()

        # Get width and height
        self.w_h = w_h

        # Get font
        self.font = font

        # Get text
        self.text = text

        # Is mouse hovering over button
        self.mouseIsOver = False

        # Was button selected
        self.selected = False

        # Keep track of what category the button is a part of
        self.categoryID = 0
        
        pygame.draw.rect(self.image, buttonColour, [0, 0, w_h[0], w_h[1]])
        self.rect = self.image.get_rect()

        # Create fonts for if button is pressed / not pressed
        self.renderedTextNotSelected = font.render(text, 1, textNotSelectedColour)
        self.renderedTextSelected = font.render(text, 1, textSelectedColour)

        # Set default colour for the text and button
        self.textColour = self.renderedTextNotSelected
        self.buttonColour = buttonColour
        
        self.W = self.renderedTextSelected.get_width()
        self.H = self.renderedTextSelected.get_height()
        self.image.blit(self.textColour, [w_h[0]/2 - self.W/2, w_h[1]/2 - self.H/2])

    def changeButtonColour(self):
        self.mouseIsOver = True
        
        pygame.draw.rect(self.image, self.buttonColour, [0, 0, self.w_h[0], self.w_h[1]])

        self.image.blit(self.textColour, [self.w_h[0]/2 - self.W/2, self.w_h[1]/2 - self.H/2])

    def mouseNotOver(self):
        self.mouseIsOver = False
        
        pygame.draw.rect(self.image, self.colour.BLACK, [0, 0, self.w_h[0], self.w_h[1]])

        self.image.blit(self.textColour, [self.w_h[0]/2 - self.W/2, self.w_h[1]/2 - self.H/2])
        

        
class TextBoxes(pygame.sprite.Sprite):
    def __init__(self, w_h, align, text, font, textColour):
        # Call the parent class (Sprite) constructor  
        super().__init__()
        
        self.image = pygame.Surface(w_h, pygame.SRCALPHA, 32)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()

        self.text = font.render(text, 1, textColour)
        W = self.text.get_width()
        H = self.text.get_height()

        # Align with the left side of box or center of box
        if align == 'l':
            self.image.blit(self.text, [0, w_h[1]/2 - H/2])
        elif align == 'c':
            self.image.blit(self.text, [w_h[0]/2 - W/2, w_h[1]/2 - H/2])


class Settings():
    def __init__(self, screen, screenWidth, screenHeight, boxVars):
        # Get constants
        self.colour = Colours()

        # Get main screen width and height
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight

        # Set box variation options
        self.boxVars = boxVars
        
        # Set screen from main
        self.screen = screen

        # Relative object sizes based on screen size
        buttonSize = [screenWidth / 14, screenHeight / 16]
        textBoxSize = [screenWidth / 9, screenHeight / 12]
        textSize = round(math.sqrt(buttonSize[0]**2 + buttonSize[1]**2)/5)

        # Create font for text
        self.font_small = pygame.font.SysFont('Arial', textSize)
        self.font_large = pygame.font.SysFont('Arial', textSize*2)

        # Create list of sprites for textboxes and buttons
        self.textBoxList = pygame.sprite.Group()
        self.buttonList = pygame.sprite.Group()
        self.startList = pygame.sprite.Group()

        # Record mouse clicks
        self.click = False

        # Record the selections user makes (creates an array with size = number of categories
        self.selection = []
        for i in range(len(self.boxVars)):
            self.selection.append(None)

        # Create pop-up window
        self.canvas = pygame.Surface((screenWidth * 3/4, screenHeight * 3/4))
        self.canvas.fill(self.colour.BLUE)

        # Create title text
        titleText = TextBoxes([textBoxSize[0]*2.5, textBoxSize[1]*1.5], 'c', "Study Configuration", self.font_large, self.colour.RED)
        titleText.rect.centerx = self.canvas.get_rect().centerx
        titleText.rect.y = screenHeight/2000
        self.textBoxList.add(titleText)

        # Create Start Button
        startButton = Buttons(self.colour.GREY, [buttonSize[0]*3, buttonSize[1]*3], "Start", self.font_large, self.colour.RED, self.colour.RED)
        startButton.rect.right = self.canvas.get_rect().right - self.canvas.get_rect().size[0]/10
        startButton.rect.centery = self.canvas.get_rect().centery
        self.startList.add(startButton)
        
        for i in range(len(self.boxVars)):
            # Create text boxes
            textBoxPos = [(buttonSize[0]/2), (2.5*buttonSize[1] + i*2*buttonSize[1]) - 0.75*textBoxSize[1]]
            tempText = TextBoxes(textBoxSize, 'l', self.boxVars[i][0], self.font_small, self.colour.RED)

            # Set x and y of the textbox
            tempText.rect.x = textBoxPos[0]
            tempText.rect.y = textBoxPos[1]

            # Add to sprite list
            self.textBoxList.add(tempText)

            # Create buttons
            j = 0
            for buttonText in self.boxVars[i][1]:
                # Create a temporary button
                buttonPos = [buttonSize[0]/2 + j*1.5*buttonSize[0], 2.5*buttonSize[1] + i*2*buttonSize[1]]
                tempButton = Buttons(self.colour.BLACK, buttonSize, buttonText, self.font_small, self.colour.YELLOW, self.colour.RED)

                # Set x and y of the button
                tempButton.rect.x = buttonPos[0]
                tempButton.rect.y = buttonPos[1]

                # Set category id of button
                tempButton.categoryID = i

                # Add to sprite list
                self.buttonList.add(tempButton)

                j+=1


    def update(self, mPosX, mPosY):
        # Adjust mouse position since coords here are relative to the smaller window, not the full window
        mPosX = mPosX - self.screenWidth*1/8
        mPosY = mPosY - self.screenHeight*1/8

        done = False


        # Check every button if mouse is touching it
        for button in self.buttonList:

            # If button was previously selected, but a different button in the same row is currently selected, revert colour
            if button.textColour == button.renderedTextSelected and self.selection[button.categoryID] != button.text:
                button.buttonColour = self.colour.BLACK
                button.changeButtonColour()
                button.textColour = button.renderedTextNotSelected
                button.image.blit(button.textColour, [button.w_h[0]/2 - button.W/2, button.w_h[1]/2 - button.H/2])

            # Check if mouse is colliding with button
            if button.rect.collidepoint(mPosX, mPosY):
                button.mouseIsOver = True
                
                if not button.selected:
                    button.buttonColour = self.colour.GREY
                    button.changeButtonColour()

                # Check if mouse is clicked
                if self.click:
                    
                    # Reset all buttons to "Not Selected" colour
                    button.selected = False

                    button.buttonColour = self.colour.BLACK
                    button.changeButtonColour()
                    
                    button.textColour = button.renderedTextNotSelected
                    button.image.blit(button.textColour, [button.w_h[0]/2 - button.W/2, button.w_h[1]/2 - button.H/2])
                    

                    if self.selection[button.categoryID] != button.text: # If this option is not selected, select it
                        button.selected = True
                        
                        # Change button colour to "Selected"
                        button.buttonColour = self.colour.GREEN
                        button.changeButtonColour()

                        button.textColour = button.renderedTextSelected
                        button.image.blit(button.textColour, [button.w_h[0]/2 - button.W/2, button.w_h[1]/2 - button.H/2])
                        
                        # Set selection to the button
                        self.selection[button.categoryID] = button.text
    
                    else:                                       # If this option was already selected, unselect it
                        button.selected = False
                        self.selection[button.categoryID] = None
                        
            # Check if mouse is not colliding with button, but was in the previous frame
            elif button.mouseIsOver:
                button.mouseIsOver = False
                
                if not button.selected:
                    button.buttonColour = self.colour.BLACK
                    button.changeButtonColour()

        # Check if all options have been selected (if i == number of selections, all options have been selected)
        i = 0
        for option in self.selection:
            if option == None:
                break
            i += 1

        for startButton in self.startList:
            if i == len(self.selection):
                # If all options have been selected, enable the start button
                startButton.buttonColour = self.colour.GREEN
                startButton.changeButtonColour()
                if startButton.rect.collidepoint(mPosX, mPosY) and self.click:
                    done = True

            else:
                startButton.buttonColour = self.colour.GREY
                startButton.changeButtonColour()
                    
        self.click = False
        self.textBoxList.update()
        self.buttonList.update()
        self.startList.update()

        if done:
            return self.selection
        else:
            return None

                

    def draw(self):
        # Draw settings menu to the screen
        self.screen.blit(self.canvas, self.canvas.get_rect(center = (self.screen.get_rect().center))) # second input makes center of popup same as center of screen

        # Add all the text boxes and buttons
        self.textBoxList.draw(self.canvas)
        self.buttonList.draw(self.canvas)
        self.startList.draw(self.canvas)

        
        
