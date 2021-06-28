'''
DRT
Main Program

Developed by Steven Caro and Gian Favero
4/25/2021
'''

#SSH remote repostitory added s
import random, pygame, csv, datetime
from DRT_SettingsLibrary import *
from DRT_Constants import *
from DRT_BoxLibrary import *

def main():
    """ Main function for the game. """
    pygame.init()
 
    # Set the width and height of the screen [width,height]
    screenSizeSmall = [300,200]
    screenSizeMedium = [600,400]
    screenSizeLarge = [900, 600]
    size = screenSizeLarge
    screen = pygame.display.set_mode(size)
    
    pygame.display.set_caption("DRT")
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # Get constants
    colour = Colours()

    # Declare box variations
    boxVariables = [["Window Size", ["Small", "Medium", "Large"]],
                    ["Object Size", ["Small", "Medium", "Large"]],
                    ["Object Colour", ["Red", "Black", "Blue"]],
                    ["Object Shape", ["Square", "Circle"]],
                    ["Sound", ["Off", "On"]]]

    # Get configuration from settings menu
    # If None, it means that user is still on the settings menu
    configuration = None

    # Initialize Settings Menu
    settings = Settings(screen, size[0], size[1], boxVariables)

    # Initialize beep sound
    beep = pygame.mixer.Sound('DRT_Beep.wav')

    # Set min and max time for random interval of object appearance
    timeIntv = [5,10] # eg. [5,10] --> object appears randomly between 5 and 10 secondss

    # create variable to store current date and time for csv file
    now = time.strftime("%a, %d %b %Y %H_%M_%S") #for filename
    nowString = time.strftime("%m/%d/%y %H:%M:%S") #for file cell

    # Create .csv file
    with open(f'{now} - DRT_Statistics.csv', mode='w', newline="") as outfile:
        outfile_write = csv.writer(outfile, delimiter=',', quotechar='"')

        while not done:
            # --- Main event loop

            # --- Event processing goes below
            mousePos = pygame.mouse.get_pos()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if configuration == None:
                    if event.type == pygame.MOUSEBUTTONUP:
                        settings.click = True
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        box.button.Press = True

            # --- Event processing goes above

            # --- Game logic goes below

            # Update settings screen if "Start" button has not been pressed yet
            if configuration == None:
                configuration = settings.update(mousePos[0], mousePos[1])
                if configuration != None:
                    # Initialize main program
                    # Set screen size
                    if configuration[0] == "Small":
                        size = screenSizeSmall
                    elif configuration[0] == "Medium":
                        size = screenSizeMedium
                    else:
                        size = screenSizeLarge
                    screen = pygame.display.set_mode(size)
                    box = Create(screen, configuration[3], configuration[2], configuration[1], random.randint(timeIntv[0], timeIntv[1]))
                    # If sound setting is enabled, play the sound
                    if configuration[4] == "On":
                        beep.play()

                    # Add date and time to the data exported to the csv
                    configuration_export = []
                    configuration_export.extend(configuration)
                    configuration_export.insert(0, nowString)

                    # Write the column titles and configuration info to the csv
                    outfile_write.writerows([['Date: ', 'Window Size: ', 'Object Size: ', 'Colour: ', 'Shape: ', 'Sound: '], configuration_export, "", ['Delay Time', 'Object Appears: ', 'Object Clicked: ', 'Latency: ']])

            # Else update main screen
            else:
                TimerCheck = box.update() #check to see if sleep time has passed and to draw next object

                if TimerCheck:
                    box = Create(screen, configuration[3], configuration[2], configuration[1], random.randint(timeIntv[0], timeIntv[1])) # create next object in random place accoring to settings chosen
                    box.button.creationTime = time.time()
                    box.button.formattedCTime = time.strftime("%H:%M:%S")
                    
                    # If sound setting is enabled, play the sound
                    if configuration[4] == "On":
                        beep.play()

                # update CSV file with the data from each round of objects appearing
                if box.button.goodToWrite:
                    outfile_write.writerow([box.sleepTime, box.button.formattedCTime, box.button.formattedETime, box.button.delta])
                    box.button.goodToWrite = False

            # --- Game logic goes above


            # --- Screen-clearing code goes below
            screen.fill(colour.WHITE)
            # --- Screen-clearing code goes above
            
            # --- Drawing code goes below
            
            if configuration == None:
                settings.draw()
            else:
                box.draw()

            # --- Drawing code goes above

            # --- Updates screen with drawing
            pygame.display.flip()

            # --- 60 fps MAX
            clock.tick(60)

        # Quits program and closes window
        pygame.quit()


if __name__ == "__main__":
    main()
