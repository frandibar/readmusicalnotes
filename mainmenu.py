from resources import *
from engine import Game, Scene
#from help import Help
from menu import Menu
from options import Setup
from notesquiz import NotesQuiz
from sounds import sounds

from pygame.color import Color
import pygame


class MainMenu(Scene):
    #NOTES_QUIZ, SETUP, HELP, QUIT = range(4)
    NOTES_QUIZ, SETUP, QUIT = range(3)
    FRAMERATE = 100
    def init(self):
        cur = pygame.cursors.compile(CURSOR_DATA)
        cursorSize = (len(CURSOR_DATA), len(CURSOR_DATA[0]))
        hotspot = (0, len(CURSOR_DATA)-1)            
        pygame.mouse.set_cursor(cursorSize, hotspot, *cur)
        self._decorationImg1 = pygame.image.load(DECORATION1_IMG).convert_alpha()
        self._decorationImg2 = pygame.image.load(DECORATION2_IMG).convert_alpha()
        self._background = pygame.image.load(BACKGROUND_IMG).convert()
        self._menu = Menu(
                 #["Notes Quiz", "Options", "Help", "Quit"],
                 ["Notes Quiz", "Options", "Quit"],
                 pygame.font.Font(MAIN_MENU_FONT, 50),
                 pygame.font.Font(MAIN_MENU_FONT, 70),
                 margin = -40,
                 normalColor    = Color("black"),
                 selectedColor  = Color("dark red"),
                 centered = True
                 )

        x = self.game.screen.get_width() / 2
        y = (self.game.screen.get_height() - self._menu.get_height()) / 2
        self._menuCoords = (x, y)

        self._decoImg1Coords = (10, 20)
        self._decoImg2Coords = (10, 500)

        self._clock = pygame.time.Clock()
        self.showAnimation()
        sounds.play(INTRO_SND)
        
    def showAnimation(self):
        self.game.screen.blit(self.background, (0,0))
        pygame.display.flip()
        self.game.screen.blit(self._decorationImg1, self._decoImg1Coords)
        self.game.screen.blit(self._decorationImg2, self._decoImg2Coords)
        y1o = self._decoImg1Coords[1]
        y2o = self._decoImg2Coords[1]
        for x in range(0, self.game.screen.get_width(), 5):
            y1f = y1o + self._decorationImg1.get_height()
            pygame.display.update((x, y1o), (x, y1f))
            x2 = self.game.screen.get_width() - x
            y2f = y2o + self._decorationImg2.get_height()
            pygame.display.update((x2, y2o),(x2, y2f))
            self._clock.tick(self.FRAMERATE)                                                                                      

        self.fadeInMenu()


    def fadeInMenu(self):                                                                                     
        s = self.game.screen.copy()
        self._menu.blit(s, self._menuCoords)
        for i in range(0, 50, 1):
            s.set_alpha(i)
            self.game.screen.blit(s, (0,0))
            pygame.display.flip()
            self._clock.tick(self.FRAMERATE)                                                                                      


    def paint(self):
        self.game.screen.blit(self.background, (0,0))
        self.game.screen.blit(self._decorationImg1, self._decoImg1Coords)
        self.game.screen.blit(self._decorationImg2, self._decoImg2Coords)
        self._menu.blit(self.game.screen, self._menuCoords)
        
    def event(self, evt):
        if evt.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]:
            x, y = pygame.mouse.get_pos()
            x -= self.game.screen.get_width() / 2
            y -= (self.game.screen.get_height() - self._menu.get_height()) / 2
            if evt.type == pygame.MOUSEMOTION:
                if self._menu.setItem((x,y)):
                    sounds.play(MENU_SND)
                    self.paint()
            else:
                # MOUSEBUTTONUP, user clicked on menu
                sel = self._menu.selectItem((x,y))
                if sel is not None:
                    sounds.play(ENTER_SND)
                    self.doAction(sel)
        elif evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_ESCAPE:
                self.end()
            elif evt.key == pygame.K_DOWN:
                self._menu.next()
                sounds.play(MENU_SND)
                self.paint()
            elif evt.key == pygame.K_UP:
                self._menu.prev()
                sounds.play(MENU_SND)
                self.paint()
            elif evt.key in [pygame.K_RETURN, pygame.K_SPACE]:
                sel = self._menu.selected
                sounds.play(ENTER_SND)
                self.doAction(sel)
                sounds.play(INTRO_SND)
                
    def doAction(self, sel):
        self.fadeOut()
        if sel == self.NOTES_QUIZ:
            self.game.level = 1                                                                                                   
            self.game.score = 0                                                                                                   
            while True:
                if self.runScene(NotesQuiz(self.game)) not in [NotesQuiz.CORRECT, NotesQuiz.WRONG, NotesQuiz.TIMEISUP]:
                    break                                                                          
                self.game.level += 1                                                                                                   
        elif sel == self.SETUP:
            self.runScene(Setup(self.game, 0))
        #elif sel == self.HELP:
            #self.runScene(Help(self.game))
        elif sel == self.QUIT:
            self.end()
                        
