import colors
from engine import Scene
from data import *
from sounds import sounds
import hollow

import pygame

DEBUG = False

class Setup(Scene):
    COL1 = 200                  
    COL2 = 350                  
    COL3 = 500                  
    def init(self, game):
        self._background = pygame.image.load(MAIN_MENU_IMG).convert()
        self._overlay = pygame.image.load(SETUP_OVERLAY_IMG).convert_alpha()
        self._fontTitle = pygame.font.Font(MAIN_MENU_FONT, 70)
        self._fontText = pygame.font.Font(MAIN_MENU_FONT, 50)

        # render text options                                                                                            
        yes = hollow.textOutline(self._fontText, "yes", colors.RED, colors.BLACK)
        no  = hollow.textOutline(self._fontText, "no", colors.RED, colors.BLACK)
        off = hollow.textOutline(self._fontText, "off", colors.RED, colors.BLACK)
        time5  = hollow.textOutline(self._fontText, "5 sec", colors.RED, colors.BLACK)
        time10 = hollow.textOutline(self._fontText, "10 sec", colors.RED, colors.BLACK)
        time15 = hollow.textOutline(self._fontText, "15 sec", colors.RED, colors.BLACK)
        time20 = hollow.textOutline(self._fontText, "20 sec", colors.RED, colors.BLACK)

        self._yesnoImg = [yes, no]                                                       
        self._timesImg = [off, time5, time10, time15, time20]                                                                                      

    def paint(self):
        self.game.screen.blit(self.background, (0,0))
        self.game.screen.blit(self._overlay, (50,0))
        setup = hollow.textOutline(self._fontTitle, "Setup", colors.RED, colors.BLACK)
        clefs = hollow.textOutline(self._fontText, "Clefs", colors.RED, colors.BLACK)
        treble = hollow.textOutline(self._fontText, "treble:", colors.RED, colors.BLACK)
        bass = hollow.textOutline(self._fontText, "bass:", colors.RED, colors.BLACK)
        timer = hollow.textOutline(self._fontText, "Timer:", colors.RED, colors.BLACK)
        back = hollow.textOutline(self._fontText, "back", colors.RED, colors.BLACK)
        self.game.screen.blit(setup, (self.game.screen.get_width()/2 - setup.get_width()/2, 70))
        ypos = 150
        rowheight = 50                  
        self.game.screen.blit(clefs, (self.COL1, ypos))
        ypos += rowheight                                               
        self.game.screen.blit(treble, (self.COL2, ypos))
        self.game.screen.blit(self._yesnoImg[setupOptions.useTrebleClef], (self.COL3, ypos))
        ypos += rowheight                                               
        self.game.screen.blit(bass, (self.COL2, ypos))
        self.game.screen.blit(self._yesnoImg[setupOptions.useBassClef], (self.COL3, ypos))
        ypos += rowheight                                               
        self.game.screen.blit(timer, (self.COL1, ypos))
        self.game.screen.blit(self._timesImg[setupOptions.getTimerIndex()], (self.COL3, ypos))
        self.game.screen.blit(back, (self.COL3, ypos + 100))

    def event(self, evt):
        if evt.type == pygame.KEYDOWN:
            self.end()
        elif evt.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            if DEBUG: print x, y                                         
            if self.COL3 <= x <= self.COL3 + 100:
                sounds.play("pasa")                                       
                if 200 <= y <= 250:
                    if DEBUG: print 'changing treble', (setupOptions.useTrebleClef + 1) % len(self._yesnoImg)                                   
                    # disallow treble and bass both set to no                                                                                                                                                
                    if not (setupOptions.useTrebleClef == setupOptions.YES and setupOptions.useBassClef == setupOptions.NO):
                        setupOptions.setUseTrebleClef((setupOptions.useTrebleClef + 1) % len(self._yesnoImg))
                elif 250 < y <= 300:
                    if DEBUG: print 'changing bass', (setupOptions.useBassClef + 1) % len(self._yesnoImg)                                   
                    if not (setupOptions.useTrebleClef == setupOptions.NO and setupOptions.useBassClef == setupOptions.YES):
                        setupOptions.setUseBassClef((setupOptions.useBassClef + 1) % len(self._yesnoImg))
                elif 300 < y <= 350:
                    if DEBUG: print 'changing timer', (setupOptions.getTimerIndex() + 1) % len(self._timesImg)                                   
                    setupOptions.setTimer((setupOptions.getTimerIndex() + 1) % len(self._timesImg))
                elif 400 < y <= 450:
                    self.end()                                    
                self.paint()                                                                          



class SetupOptions:
    BASS, TREBLE, TIMER, TIME = range(4)
    YES, NO = range(2)
    OFF, SEC5, SEC10, SEC15, SEC20 = range(5)
    def __init__(self, timerIndex, useTrebleClef, useBassClef):
        self._timerIndex = timerIndex
        self._useTrebleClef = useTrebleClef
        self._useBassClef = useBassClef
        self._update()                                       

    def setUseTrebleClef(self, yesno):
        '''possible values: YES, NO'''
        self._useTrebleClef = yesno
        self._update()

    @property
    def useTrebleClef(self):
        return self._useTrebleClef

    @property
    def useBassClef(self):
        return self._useBassClef

    def setUseBassClef(self, yesno):
        '''possible values: YES, NO'''
        self._useBassClef = yesno
        self._update()

    def setTimer(self, timeIndex):
        '''possible values: OFF, SEC5, ...SEC20'''
        self._timerIndex = timeIndex

    def getTimerIndex(self):
        return self._timerIndex

    def getTimerSec(self):
        return self._timerIndex * 5

    @property        
    def images(self):
        return self._images

    @property        
    def notes(self):
        return self._notes

    def _update(self):        
        self._images = []
        self._notes  = []

        if self._useTrebleClef == self.YES: 
            self._images += trebleClefImages
            self._notes  += trebleNotes
        if self._useBassClef == self.YES:
            self._images += bassClefImages
            self._notes  += bassNotes

setupOptions = SetupOptions(SetupOptions.SEC5, SetupOptions.YES, SetupOptions.YES)
