from engine import Scene
from resources import *
from setupoptions import SetupOptions
from sounds import sounds

import pygame

DEBUG = True

class Setup(Scene):
    COL1 = 200                  
    COL2 = 350                  
    COL3 = 500                  
    def init(self, game):
        self.setupOptions = SetupOptions()
        self._background = pygame.image.load(BACKGROUND_IMG).convert()
        self._borderImg  = pygame.image.load(BORDER_IMG).convert_alpha()
        self._fontTitle = pygame.font.Font(OPTIONS_FONT, 50)
        self._fontText  = pygame.font.Font(OPTIONS_FONT, 30)

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
        #self.game.screen.blit(self._borderImg, (0,0))
        color = pygame.color.Color('dark red')
        setup  = self._fontTitle.render("Options", True, color)
        clefs  = self._fontText.render("Clefs", True, color)
        treble = self._fontText.render("treble:", True, color)
        bass   = self._fontText.render("bass:", True, color)
        timer  = self._fontText.render("Timer:", True, color)
        sound  = self._fontText.render("Sounds:", True, color)
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
        ypos += rowheight                                               
        self.game.screen.blit(sound, (self.COL1, ypos))
        self.game.screen.blit(self._yesnoImg[self.setupOptions.sounds], (self.COL3, ypos))
        self.game.screen.blit(back, (self.COL3, ypos + 100))

    def event(self, evt):
        if evt.type == pygame.KEYDOWN:
            self.setupOptions.save()
            self.end()
        elif evt.type == pygame.MOUSEBUTTONUP:
            x, y = pygame.mouse.get_pos()
            if DEBUG: print x, y                                         
            if self.COL3 <= x <= self.COL3 + 100:
                sounds.play(MENU_SND)                                       
                if 200 <= y <= 250:
                    # disallow treble and bass both set to no                                                                                                                                                
                    if not (self.setupOptions.useTrebleClef == self.setupOptions.YES and self.setupOptions.useBassClef == self.setupOptions.NO):
                        self.setupOptions.useTrebleClef = (self.setupOptions.useTrebleClef + 1) % len(self._yesnoImg)
                elif 250 < y <= 300:
                    if not (self.setupOptions.useTrebleClef == self.setupOptions.NO and self.setupOptions.useBassClef == self.setupOptions.YES):
                        self.setupOptions.useBassClef = (self.setupOptions.useBassClef + 1) % len(self._yesnoImg)
                elif 300 < y <= 350:
                    self.setupOptions.timerIndex = (self.setupOptions.timerIndex + 1) % len(self._timesImg)
                elif 350 < y <= 400:
                    self.setupOptions.sounds = (self.setupOptions.sounds + 1) % len(self._yesnoImg)
                    sounds.mute = self.setupOptions.sounds == self.setupOptions.NO
                elif 450 < y <= 500:
                    self.setupOptions.save()
                    self.end()                                    
                self.paint()                                                                          



