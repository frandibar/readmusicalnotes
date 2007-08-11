#!/usr/bin/python

import resources
import engine
from mainmenu import MainMenu

import os

def main():
    # this is used so that when run from start bar, or desktop it works. 
    if os.path.dirname(__file__):
        os.chdir(os.path.dirname(__file__))

    g = engine.Game(framerate = 100, title = "read Music!", icon = resources.ICON_IMG)
    g.run(MainMenu(g))
    

if __name__ == "__main__":
    main()
