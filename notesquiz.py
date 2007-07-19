from config import setupOptions
from data import *
from engine import Game, Scene
from menu import Menu
from sounds import sounds
from timer import Timer, BlinkingText
import colors
import hollow
import score

import os
import pygame
import random
import string
import time

DEBUG = False


class NotesQuiz(Scene):
    notesIndexMenu = ['B', 'A', 'G', 'F', 'E', 'D', 'C'] 
    # these are the sounds to play when an item from the menu is selected
    menuSounds = ['b3', 'a3', 'g3', 'f3', 'e3', 'd3', 'c3', 'pasa'] 
        
    WAITING, WRONG, CORRECT, FINISH, TIMEISUP = range(5)   # status values
    CLOCK_TICK = pygame.USEREVENT

    def init(self):
        # select a random note
        # start choosing a clef
        clefs = []
        if setupOptions.useTrebleClef == setupOptions.YES: clefs.append(score.TrebleClef())
        if setupOptions.useBassClef == setupOptions.YES: clefs.append(score.BassClef())
        clef = random.choice(clefs)
        # select the octaves according to the clef
        if clef.__class__ == score.TrebleClef:
            octave = random.choice(range(3,5))
        else:
            octave = random.choice(range(1,3))
        # this stores the letter the user must input
        self._answer = random.choice(score.Note.validNotes)
        note = score.QuarterNote(self._answer, octave)
        self._quiz = score.ScoreBuilder(clef, 200, showTimeSignature = False, notesList = [note])

        # load images
        self._images = {}
        self._images["correct"] = pygame.image.load(CORRECT_IMG).convert()
        self._images["wrong"]   = pygame.image.load(WRONG_IMG).convert()
        font = pygame.font.Font(NOTES_FONT, 15)
        self._images["instructions"] = font.render("Use keys up, down, C, D, E, F, G, A, B and Enter", True, colors.BLACK)
        font = pygame.font.Font(MAIN_MENU_FONT, 30)
        self._images["pressKey"] = font.render("Press any key to continue", True, colors.RED)
        self._images["overlay"] = pygame.image.load(QUIZ_OVERLAY_IMG).convert_alpha()

        self._showInstructions = True
        self._showPressKeyMsg  = False

        # menu
        self._menu = Menu(
                 pygame.font.Font(NOTES_FONT, 50),
                 pygame.font.Font(NOTES_FONT, 50),
                 pygame.font.Font(NOTES_FONT, 70),
                 ["B si", "A la", "G sol", "F fa", "E mi", "D re", "C do", "back"],
                 margin = -40,
                 normalColor    = colors.GRAY,
                 selectedColor  = colors.RED,
                 alternateColor = colors.YELLOW,
                 centered = False
                 )

        pygame.time.set_timer(self.CLOCK_TICK, 1000)        
        useTimer = setupOptions.timerIndex != setupOptions.OFF
        self._timer = Timer(setupOptions.getTimerSec(), useTimer)
        if useTimer:
            self._timer.start()

        # set coordinates
        self._menuCoords = (50, 100)
        self._imgCoords = (300, 200)

        self._status = self.WAITING

        sounds.muteSound()
        self.start()

    def paint(self):
        self.game.screen.blit(self.background, (0,0))
        self.game.screen.blit(self._images["overlay"], (0,0))
        self._quiz.blit(self.game.screen, self._imgCoords)
        # show score
        font = pygame.font.Font(MAIN_MENU_FONT, 40)
        score = font.render("Score:   " + str(self.game.score) + " / " + str(self.game.level), True, colors.BLACK)
        self.game.screen.blit(score, (self.game.screen.get_width() - score.get_width() - 20, 10))

        self._menu.blit(self.game.screen, self._menuCoords)
        if self._timer.timeIsUp():
            self._showPressKeyMsg = True
            self._status = self.TIMEISUP
        if self._showPressKeyMsg:
            self.game.screen.blit(self._images["pressKey"], ((self.game.screen.get_width() - self._images["pressKey"].get_width())/2, 400))
        if self._showInstructions:                    
            self.game.screen.blit(self._images["instructions"], ((self.game.screen.get_width() - self._images["instructions"].get_width())/2, 480))                                 

        
    def event(self, evt):                
        if self._status in [self.CORRECT, self.WRONG, self.TIMEISUP]:
            if (evt.type == pygame.KEYDOWN and evt.key != pygame.K_ESCAPE) or evt.type == pygame.MOUSEBUTTONUP:
                self.end(self._status)
                return                                    

        if evt.type == pygame.QUIT: 
            sys.exit()
        elif evt.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]:
            x, y = pygame.mouse.get_pos()
            x -= self._menuCoords[0]
            y -= self._menuCoords[1]
            if evt.type == pygame.MOUSEMOTION:
                if self._menu.setItem((x,y)):
                    self._menu.setItem((x,y))
                    sounds.play(self.menuSounds[self._menu.selected])
                    self.paint()
            else:                                
                # MOUSEBUTTONUP, user clicked on menu
                sel = self._menu.selectItem((x,y))
                if sel is not None:
                    self.do_action(sel)
        elif evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_ESCAPE:
                self.end(self.FINISH)
            elif evt.key == pygame.K_DOWN:
                self._menu.next()
                sounds.play(self.menuSounds[self._menu.selected])
                self.paint()
            elif evt.key == pygame.K_UP:
                self._menu.prev()
                sounds.play(self.menuSounds[self._menu.selected])
                self.paint()
            elif evt.key in [pygame.K_RETURN, pygame.K_SPACE]:
                sel = self._menu.selected
                sounds.play(self.menuSounds[sel])
                self.do_action(sel)
            else:                                   
                #try:
                    keypressed = string.upper(chr(evt.key))
                    if keypressed not in score.Note.validNotes:
                        print "Invalid key!", chr(evt.key)
                        return
                    else:
                        self.evaluate(keypressed)                    
                #except:
                    #pass   # ignore keys such as ALT, CTRL, SHIFT, etc

        elif evt.type == self.CLOCK_TICK:
            if self._timer.isRunning():
                self._timer.tick()
                pygame.time.set_timer(self.CLOCK_TICK, 1000)
                

    def evaluate(self, guess):
        sounds.play(self.menuSounds[self._menu.selected])
        # select option from menu
        self._menu.selected  = self.notesIndexMenu.index(guess)
        self._menu.alternate = self.notesIndexMenu.index(guess)

        if guess == self._answer:
            self.game.score += 1
            self._status = self.CORRECT
        else:
            self._status = self.WRONG

        self._showPressKeyMsg = True
        self._timer.stop()
        self.paint()


    def do_action(self, sel):
        if sel == 7:   # quit            
            self.end(self.FINISH)
            return

        self._menu.alternate = sel
        self.evaluate(self._menu.options[sel][0])


    def loop(self):
        x, y = self._imgCoords                        
        x += 250
        y -= 50
        self.paint()
        if self._status == self.WRONG:
            self.game.screen.blit(self._images["wrong"], (x, y))
        elif self._status == self.CORRECT:
            self.game.screen.blit(self._images["correct"], (x, y))

    def update(self):
        self._timer.blit(self.game.screen, (770, 100))
        self._timer.alarm.blit(self.game.screen)
        pass

    def start(self):
        self._lastUpdate = self._startTime = time.time()



