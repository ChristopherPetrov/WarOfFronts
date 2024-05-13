import pygame as pg
import os

pg.init()

# Creates and sets the display to 1600x900 with diplay.set_mode
WIN_HEIGHT, WIN_WIDTH = 1600, 900
pg.display.set_mode((WIN_HEIGHT, WIN_WIDTH))

# A function to quickly get a file:
def getFile(fileName):
    return pg.image.load(fileName)

#Image variables:
BACKGROUND = getFile("BG-1600.png")


def Main():
    run = True
    while run:
        for event in pg.event.get():
            if event == pg.QUIT:
                run = False

if __name__ == "__main__":
    Main()

# Atribute Image by <a href="https://www.freepik.com/free-photo/vintage-rusty-scratched-wall_10746799.htm#query=rust%20overlay&position=0&from_view=keyword&track=ais_user&uuid=01c0e15f-befa-45c9-bc30-1485cd5ec620">Freepik</a>