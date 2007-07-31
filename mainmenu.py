from data import *
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
        self._decorationImg = pygame.image.load(DECORATION_IMG).convert_alpha()
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
        sounds.play('bach_846_prelude1')
        

    def paint(self):
        self.game.screen.blit(self.background, (0,0))
        self.game.screen.blit(self._decorationImg, (10,20))
        x = self.game.screen.get_width() / 2
        y = (self.game.screen.get_height() - self._menu.get_height()) / 2
        self._menu.blit(self.game.screen, (x,y))
        
    def event(self, evt):
        if evt.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]:
            x, y = pygame.mouse.get_pos()
            x -= self.game.screen.get_width() / 2
            y -= (self.game.screen.get_height() - self._menu.get_height()) / 2
            if evt.type == pygame.MOUSEMOTION:
                if self._menu.setItem((x,y)):
                    sounds.play('menu')
                    self.paint()
            else:
                # MOUSEBUTTONUP, user clicked on menu
                sel = self._menu.selectItem((x,y))
                if sel is not None:
                    sounds.play('enter')
                    self.do_action(sel)
        elif evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_ESCAPE:
                self.end()
            elif evt.key == pygame.K_DOWN:
                self._menu.next()
                sounds.play('menu')
                self.paint()
            elif evt.key == pygame.K_UP:
                self._menu.prev()
                sounds.play('menu')
                self.paint()
            elif evt.key in [pygame.K_RETURN, pygame.K_SPACE]:
                sel = self._menu.selected
                sounds.play('enter')
                self.do_action(sel)
                sounds.play('bach_846_prelude1')
                
    def do_action(self, sel):
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
                        
