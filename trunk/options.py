import cfg
from engine import Scene
from data import *
from sounds import sounds

import pygame

DEBUG = False

class Setup(Scene):
    COL1 = 200                  
    COL2 = 350                  
    COL3 = 500                  
    def init(self, game):
        self.setupOptions = SetupOptions()
        self._background = pygame.image.load(BACKGROUND_IMG).convert()
        self._fontTitle = pygame.font.Font(MAIN_MENU_FONT, 70)
        self._fontText = pygame.font.Font(MAIN_MENU_FONT, 50)

        # render text options                                                                                            
        color = pygame.color.Color('dark red')
        yes = self._fontText.render("yes", True, color)
        no  = self._fontText.render("no", True, color)
        off = self._fontText.render("off", True, color)
        time5  = self._fontText.render("5 sec", True, color)
        time10 = self._fontText.render("10 sec", True, color)
        time15 = self._fontText.render("15 sec", True, color)
        time20 = self._fontText.render("20 sec", True, color)

        self._yesnoImg = [no, yes]                                                       
        self._timesImg = [off, time5, time10, time15, time20]                                                                                      

    def paint(self):
        self.game.screen.blit(self.background, (0,0))
        color = pygame.color.Color('dark red')
        setup  = self._fontTitle.render("Options", True, color)
        clefs  = self._fontText.render("Clefs", True, color)
        treble = self._fontText.render("treble:", True, color)
        bass   = self._fontText.render("bass:", True, color)
        timer  = self._fontText.render("Timer:", True, color)
        back   = self._fontText.render("back", True, color)
        self.game.screen.blit(setup, (self.game.screen.get_width()/2 - setup.get_width()/2, 70))
        ypos = 150
        rowheight = 50                  
        self.game.screen.blit(clefs, (self.COL1, ypos))
        ypos += rowheight                                               
        self.game.screen.blit(treble, (self.COL2, ypos))
        self.game.screen.blit(self._yesnoImg[self.setupOptions.useTrebleClef], (self.COL3, ypos))
        ypos += rowheight                                               
        self.game.screen.blit(bass, (self.COL2, ypos))
        self.game.screen.blit(self._yesnoImg[self.setupOptions.useBassClef], (self.COL3, ypos))
        ypos += rowheight                                               
        self.game.screen.blit(timer, (self.COL1, ypos))
        self.game.screen.blit(self._timesImg[self.setupOptions.timerIndex], (self.COL3, ypos))
        self.game.screen.blit(back, (self.COL3, ypos + 100))

    def event(self, evt):
        if evt.type == pygame.KEYDOWN:
            self.setupOptions.save()
            self.end()
        elif evt.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            if DEBUG: print x, y                                         
            if self.COL3 <= x <= self.COL3 + 100:
                sounds.play("menu")                                       
                if 200 <= y <= 250:
                    # disallow treble and bass both set to no                                                                                                                                                
                    if not (self.setupOptions.useTrebleClef == self.setupOptions.YES and self.setupOptions.useBassClef == self.setupOptions.NO):
                        self.setupOptions.useTrebleClef = (self.setupOptions.useTrebleClef + 1) % len(self._yesnoImg)
                elif 250 < y <= 300:
                    if not (self.setupOptions.useTrebleClef == self.setupOptions.NO and self.setupOptions.useBassClef == self.setupOptions.YES):
                        self.setupOptions.useBassClef = (self.setupOptions.useBassClef + 1) % len(self._yesnoImg)
                elif 300 < y <= 350:
                    self.setupOptions.timerIndex = (self.setupOptions.timerIndex + 1) % len(self._timesImg)
                elif 400 < y <= 450:
                    self.setupOptions.save()
                    self.end()                                    
                self.paint()                                                                          



class SetupOptions:
    BASS, TREBLE, TIMER, TIME = range(4)
    NO, YES = range(2)
    OFF, SEC5, SEC10, SEC15, SEC20 = range(5)
    def __init__(self):
        self.load()

    def load(self):        
        cfg.initialise(None, None, CONFIG_FILE)                                                             
        self.timerIndex    = cfg.get_int("notesquiz/timerIndex")
        self.useTrebleClef = cfg.get_int("notesquiz/useTrebleClef")
        self.useBassClef   = cfg.get_int("notesquiz/useBassClef")
        self.mute          = cfg.get_int("notesquiz/mute")
        cfg.sync()

    def setDefaults(self):
        self.timerIndex    = self.SEC5
        self.useTrebleClef = self.YES
        self.useBassClef   = self.YES
        self.mute          = self.NO
        self.save()                                                                 

    def save(self):
        cfg.initialise(None, None, CONFIG_FILE)                                                             
        cfg.set_int("notesquiz/timerIndex", self.timerIndex)
        cfg.set_int("notesquiz/useTrebleClef", self.useTrebleClef)
        cfg.set_int("notesquiz/useBassClef", self.useBassClef)
        cfg.set_int("notesquiz/mute", self.mute)
        cfg.sync()

    def getTimerSec(self):
        return self.timerIndex * 5

