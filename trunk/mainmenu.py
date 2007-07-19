from data import *
from engine import Game, Scene
from menu import Menu
from config import Setup
from notesquiz import NotesQuiz
from rythmquiz import RythmQuiz
from sounds import sounds
import colors

import pygame


class MainMenu(Scene):
    NOTES_QUIZ, RYTHM_QUIZ, SETUP, QUIT = range(4)
    def init(self):
        self._background = pygame.image.load(MAIN_MENU_IMG).convert()
        self._font = pygame.font.Font(MAIN_MENU_FONT, 90)
        self._menu = Menu(
                 pygame.font.Font(MAIN_MENU_FONT, 50),
                 pygame.font.Font(MAIN_MENU_FONT, 50),
                 pygame.font.Font(MAIN_MENU_FONT, 70),
                 ["Notes Quiz", "Rythm Quiz", "Setup", "Quit"],
                 margin = -40,
                 normalColor    = colors.GRAY,
                 selectedColor  = colors.RED,
                 alternateColor = colors.GRAY,
                 centered = True
                 )
        sounds.play('bach_846_prelude1')
        self._overlay = pygame.image.load(MAIN_OVERLAY_IMG).convert_alpha()
        
    def paint(self):
        self.game.screen.blit(self.background, (0,0))
        self.game.screen.blit(self._overlay, (0,0))
        self._menu.blit(self.game.screen, (400,180))
        
    def event(self, evt):
        if evt.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]:
            x, y = pygame.mouse.get_pos()
            x -= 400
            y -= 180
            if evt.type == pygame.MOUSEMOTION:
                if self._menu.setItem((x,y)):
                    sounds.play('pasa')
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
                sounds.play('pasa')
                self.paint()
            elif evt.key == pygame.K_UP:
                self._menu.prev()
                sounds.play('pasa')
                self.paint()
            elif evt.key in [pygame.K_RETURN, pygame.K_SPACE]:
                sel = self._menu.selected
                sounds.play('enter')
                self.do_action(sel)
                sounds.play('bach_846_prelude1')
                
    def do_action(self, sel):
        if sel == self.NOTES_QUIZ:
            self.game.level = 0                                                                                                   
            while True:
                if self.runScene(NotesQuiz(self.game)) not in [NotesQuiz.CORRECT, NotesQuiz.WRONG, NotesQuiz.TIMEISUP]:
                    break                                                                          
                self.game.level += 1                                                                                                   
        elif sel == self.RYTHM_QUIZ:
            self.game.level = 0                                                                                                   
            while True:
                if self.runScene(RythmQuiz(self.game)) not in [RythmQuiz.CORRECT, RythmQuiz.WRONG, RythmQuiz.TIMEISUP]:
                    break                                                                          
                self.game.level += 1                                                                                                   
        elif sel == self.SETUP:
            self.runScene(Setup(self.game, 0))
        elif sel == self.QUIT:
            self.end()
                        
