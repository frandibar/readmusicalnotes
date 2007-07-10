#!/usr/bin/python

import data
from engine import Game
from mainmenu import MainMenu


def main():
    xSize = 800
    ySize = 525   
    g = Game((xSize, ySize), framerate = 20, title = "read Music!", icon = data.ICON_IMG)
    g.run(MainMenu(g))

    
if __name__ == "__main__":
    main()
