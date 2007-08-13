from resources import *
from engine import Game, Scene
from language import *
from menu import Menu
from options import Setup
from notesquiz import NotesQuiz
from setupoptions import SetupOptions
from sounds import sounds

from pygame.color import Color
import pygame

class MainMenu(Scene):
    NOTES_QUIZ, SETUP, QUIT = range(3)
    def init(self):
        cur = pygame.cursors.compile(CURSOR_DATA)
        cursorSize = (len(CURSOR_DATA), len(CURSOR_DATA[0]))
        hotspot = (0, len(CURSOR_DATA)-1)            
        pygame.mouse.set_cursor(cursorSize, hotspot, *cur)
        self._decorationImg1 = pygame.image.load(DECORATION1_IMG).convert_alpha()
        self._decorationImg2 = pygame.image.load(DECORATION2_IMG).convert_alpha()
        self._background = pygame.image.load(BACKGROUND_IMG).convert()
        self._menu = Menu(
                 [dict[T_NOTES_QUIZ], dict[T_OPTIONS], dict[T_QUIT]],
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
        sounds.play(INTRO_SND, FOREVER)

        if SetupOptions().softTransitions == SetupOptions.YES:
            self.showAnimation()
        else:
            self.paint()
        
    def showAnimation(self):
        if SetupOptions().softTransitions == SetupOptions.NO: return
        self.fadeIn()
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
            self._clock.tick(ANIMATION_FR)                                                                                      

        self.fadeInMenu()

    def fadeInMenu(self):                                                                                     
        if SetupOptions().softTransitions == SetupOptions.NO: return
        s = self.game.screen.copy()
        self._menu.blit(s, self._menuCoords)
        for i in range(0, 50, 1):
            s.set_alpha(i)
            self.game.screen.blit(s, (0,0))
            pygame.display.flip()
            self._clock.tick(ANIMATION_FR)                                                                                  

    def paint(self):
        self.game.screen.blit(self.background, (0,0))
        self.game.screen.blit(self._decorationImg1, self._decoImg1Coords)
        self.game.screen.blit(self._decorationImg2, self._decoImg2Coords)
        self._menu.blit(self.game.screen, self._menuCoords)
        
    def event(self, evt):
        if evt.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]:
            x, y = pygame.mouse.get_pos()
            x -= self._menuCoords[0]                                         
            y -= self._menuCoords[1]                                         
            if evt.type == pygame.MOUSEMOTION:
                if self._menu.setItem((x,y)):
                    sounds.play(MENU_SND)
                    self.paint()
            else:
                # MOUSEBUTTONUP, user clicked on menu
                sel = self._menu.selectItem((x,y))
                if sel is not None:
                    self.doAction(sel)
        elif evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_ESCAPE:
                self.fadeOut()
                self.end()
            elif evt.key == pygame.K_DOWN:
                self._menu.next()
                sounds.play(MENU_SND)
                self.paint()  # TODO: refresh only menu part of screen
            elif evt.key == pygame.K_UP:
                self._menu.prev()
                sounds.play(MENU_SND)
                self.paint()
            elif evt.key in [pygame.K_RETURN, pygame.K_SPACE, pygame.K_LEFT, pygame.K_RIGHT]:
                sel = self._menu.selected
                self.doAction(sel)
                
    def doAction(self, sel):
        sounds.play(ENTER_SND)
        self.fadeOut()
        if sel == self.NOTES_QUIZ:
            self.game.level = 1                                                                                                   
            self.game.score = 0                                                                                                   
            sounds.pauseChannel()                       
            while True:
                if self.runScene(NotesQuiz(self.game)) not in [NotesQuiz.CORRECT, NotesQuiz.WRONG, NotesQuiz.TIMEISUP]:
                    break                                                                          
                self.game.level += 1                                                                                                   
            sounds.unpauseChannel()
            sounds.play(INTRO_SND, FOREVER) # TODO: previous line not working, start again
        elif sel == self.SETUP:
            self.runScene(Setup(self.game, 0))
        elif sel == self.QUIT:
            self.end()
        self.showAnimation()                                                                                                                                       
