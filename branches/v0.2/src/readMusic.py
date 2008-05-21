#!/usr/bin/python

#import resources
#import engine
from mainmenu import MainMenu
import pygext.gl.all

import os

def main():
    # this is used so that when run from start bar, or desktop it works. 
    try:
        if os.path.dirname(__file__):
            os.chdir(os.path.dirname(__file__))
    except:
        # probably running from py2exe (__file__ is not set)
        pass        

    pygext.gl.all.screen.init((800,600), title = "read Music!")
    pygext.gl.all.director.run(MainMenu)
    #g = engine.Game(framerate = 100, title = "read Music!", icon = resources.ICON_IMG)
    #g.run(MainMenu(g))
    

if __name__ == "__main__":
    main()
