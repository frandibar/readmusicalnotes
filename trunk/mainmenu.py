from resources import *
from engine import Game, Scene
from menu import Menu
from options import Setup
from notesquiz import NotesQuiz
from rythmquiz import RythmQuiz
from sounds import sounds

from pygame.color import Color
import pygame


class MainMenu(Scene):
#NOTES_QUIZ, RYTHM_QUIZ, SETUP, QUIT = range(4)
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
                 pygame.font.Font(MAIN_MENU_FONT, 50),
                 pygame.font.Font(MAIN_MENU_FONT, 50),
                 pygame.font.Font(MAIN_MENU_FONT, 70),
#["Notes Quiz", "Rythm Quiz", "Options", "Quit"],
                 ["Notes Quiz", "Options", "Quit"],
                 margin = -40,
                 normalColor    = Color('black'),
                 selectedColor  = Color('dark red'),
                 alternateColor = Color('black'),
                 centered = True
                 )

        x = self.game.screen.get_width() / 2
        y = (self.game.screen.get_height() - self._menu.get_height()) / 2
        self._menuCoords = (x, y)

        self.showAnimation()
        sounds.play(INTRO_SND)
        
    def showAnimation(self):
        self.game.screen.blit(self.background, (0,0))
        pygame.display.flip()
        y1 = 20
        y2 = 500               
        self.game.screen.blit(self._decorationImg1, (10, y1))
        self.game.screen.blit(self._decorationImg2, (10, y2))
        for x in range(0, self._decorationImg1.get_width(), 1):
            pygame.display.update((self.game.screen.get_width() - x, y2),(self.game.screen.get_width() - x, y2 + self._decorationImg2.get_height()))
            pygame.display.update((x, y1),(x, self._decorationImg1.get_height() + y1))

        self.fadeMenu()


    def fadeMenu(self, fadeIn = True):                                                                                     
        if fadeIn:
            s = self.game.screen.copy()
            self._menu.blit(s, self._menuCoords)
        else:
            # fade to black
            s = pygame.Surface((self.game.screen.get_width(), self.game.screen.get_height())).convert()
            s.fill(Color('black'))
        for i in range(0, 50, 1):
            s.set_alpha(i)
            self.game.screen.blit(s, (0,0))
            pygame.display.flip()


    def paint(self):
        y1 = 20
        y2 = 500               
        self.game.screen.blit(self.background, (0,0))
        self.game.screen.blit(self._decorationImg1, (10, y1))
        self.game.screen.blit(self._decorationImg2, (10, y2))
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
        self.fadeMenu(False)
        if sel == self.NOTES_QUIZ:
            self.game.level = 0                                                                                                   
            self.game.score = 0                                                                                                   
            while True:
                if self.runScene(NotesQuiz(self.game)) not in [NotesQuiz.CORRECT, NotesQuiz.WRONG, NotesQuiz.TIMEISUP]:
                    break                                                                          
                self.game.level += 1                                                                                                   
        #elif sel == self.RYTHM_QUIZ:
            #self.game.level = 0                                                                                                   
            #while True:
                #if self.runScene(RythmQuiz(self.game)) not in [RythmQuiz.CORRECT, RythmQuiz.WRONG, RythmQuiz.TIMEISUP]:
                    #break                                                                          
                #self.game.level += 1                                                                                                   
        elif sel == self.SETUP:
            self.runScene(Setup(self.game, 0))
        elif sel == self.QUIT:
            self.end()
                        
