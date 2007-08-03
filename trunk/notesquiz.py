from resources import *
from engine import Game, Scene
from menu import Menu
from sounds import sounds
import timer
import colors
import options
import score

import os
import pygame
import random
import string
import time

from pygame.color import Color

DEBUG = False


class NotesQuiz(Scene):
    notesIndexMenu = ['B', 'A', 'G', 'F', 'E', 'D', 'C'] 
    # these are the sounds to play when an item from the menu is selected
    menuSounds = ["b3", "a3", "g3", "f3", "e3", "d3", "c3"] 
        
    WAITING, WRONG, CORRECT, FINISH, TIMEISUP = range(5)   # status values
    CLOCK_TICK = pygame.USEREVENT

    def init(self):
        # select a random note
        # start choosing a clef
        clefs = []
        self._setupOptions = options.SetupOptions()
        if self._setupOptions.useTrebleClef == self._setupOptions.YES: clefs.append(score.TrebleClef())
        if self._setupOptions.useBassClef == self._setupOptions.YES: clefs.append(score.BassClef())
        clef = random.choice(clefs)
        # select the octaves according to the clef
        if clef.__class__ == score.TrebleClef:
            octave = random.choice(range(3,5))
        else:
            octave = random.choice(range(1,3))
        # this stores the letter the user must input
        self._answer = random.choice(score.Note.validNotes)
        note = score.QuarterNote(self._answer, octave)
        #quiz = score.ScoreBuilder(clef, 300, showTimeSignature = False, notesList = [note]).getImage(self.game.screen.get_size())
        quiz = score.ScoreBuilder(clef, 580, showTimeSignature = False, notesList = [note]).getImage(self.game.screen.get_size())
        #self._quizImg = pygame.transform.scale2x(quiz)
        self._quizImg = quiz

        # load images
        self._images = {}
        self._images["correct"] = pygame.image.load(CORRECT_IMG).convert_alpha()
        self._images["wrong1"]  = pygame.image.load(WRONG1_IMG).convert_alpha()
        self._images["wrong2"]  = pygame.image.load(WRONG2_IMG).convert_alpha()
        font = pygame.font.Font(NOTES_FONT, 15)
        self._images["instructions"] = font.render("Use keys up, down, C, D, E, F, G, A, B and Enter", True, Color('black'))
        font = pygame.font.Font(LEGEND_FONT, 30)
        self._images["pressKey"] = font.render("Press any key to continue", True, Color('black'))
        OVERLAY_HEIGHT = 70
        self._images["overlay"] = pygame.Surface((self.game.screen.get_width(), OVERLAY_HEIGHT)).convert()
        self._images["overlay"].fill(Color('dark red'))
        self._images["overlay"].set_alpha(85)
        img = pygame.image.load(SOUND_ON_IMG).convert_alpha()
        self._images["soundOn"]  = pygame.transform.scale(img, (img.get_width()/2 , img.get_height()/2))
        self._images["soundOff"]  = pygame.image.load(SOUND_OFF_IMG).convert_alpha()

        self._showInstructions = False
        self._showPressKeyMsg  = False

        self.background = pygame.image.load(BACKGROUND_IMG).convert()

        # menu
        self._menu = Menu(
                 pygame.font.Font(NOTES_FONT, 30),
                 pygame.font.Font(NOTES_FONT, 30),
                 pygame.font.Font(NOTES_FONT, 50),
                 ["B si", "A la", "G sol", "F fa", "E mi", "D re", "C do"],
                 margin = -20,
                 normalColor    = Color('black'),
                 selectedColor  = Color('dark red'),
                 alternateColor = colors.BROWN,
                 centered = False
                 )

        # set coordinates
        self._menuCoords   = (670, 100)
        self._imgCoords    = (50, 50)
        self._answerCoords = (500, 50)

        sounds.fadeOut()

        self._useTimer = self._setupOptions.timerIndex != self._setupOptions.OFF
        if self._useTimer:
            self._timerCoords = (50, 400)
            pygame.time.set_timer(self.CLOCK_TICK, 100)        
            font = pygame.font.Font(LEGEND_FONT, 50) 
            alarm = timer.BlinkingText("Time is up!", font, (400, 400), TIMEISUP_SND)                                                                                      
            self._timer = timer.FlareTimer(self._setupOptions.getTimerSec(), alarm, self._timerCoords, 600)
            self._timer.start()

        self._status = self.WAITING
        self._soundOn = self._setupOptions.sounds == self._setupOptions.YES

        self.start()

    def paint(self):
        self.game.screen.blit(self.background, (0,0))
        self.game.screen.blit(self._quizImg, self._imgCoords)
        # show score
        font = pygame.font.Font(SCORE_FONT, 40)
        ok = font.render(str(self.game.score), True, colors.OLIVE_GREEN)
        total = font.render(" - " + str(self.game.level), True, Color('black'))
        self.game.screen.blit(ok, (self.game.screen.get_width() - ok.get_width() - total.get_width() - 50, self.game.screen.get_height() - ok.get_height()*0.8))
        self.game.screen.blit(total, (self.game.screen.get_width() - total.get_width() - 50, self.game.screen.get_height() - total.get_height()*0.8))

        self._menu.blit(self.game.screen, self._menuCoords)
        # show messages
        if self._useTimer and self._timer.timeIsUp():
                self._showPressKeyMsg = True
                self._status = self.TIMEISUP
        if self._showPressKeyMsg:
            self.game.screen.blit(self._images["pressKey"], ((self.game.screen.get_width() - self._images["pressKey"].get_width())/2, self.game.screen.get_height() - self._images["pressKey"].get_height()))
        if self._showInstructions:                    
            self.game.screen.blit(self._images["instructions"], ((self.game.screen.get_width() - self._images["instructions"].get_width())/2, self.game.screen.get_height() - self._images["pressKey"].get_height() - 10))                                 

        # show statusbar                                                                                                                                                                                                                                                           
        self.game.screen.blit(self._images["overlay"], (0, self.game.screen.get_height() - self._images["overlay"].get_height()))                                 
        #if not self._soundOn:
            #self.game.screen.blit(self._images["soundOn"], (40, self.game.screen.get_height() - self._images["soundOn"].get_height() - 15))
            #self.game.screen.blit(self._images["soundOff"], (25, self.game.screen.get_height() - self._images["soundOff"].get_height() - 5))
        if self._useTimer: 
            self._timer.blit(self.game.screen, self.background, self._timerCoords)

        
    def event(self, evt):                
        if self._status in [self.CORRECT, self.WRONG, self.TIMEISUP]:
            if (evt.type == pygame.KEYDOWN and evt.key != pygame.K_ESCAPE) or evt.type == pygame.MOUSEBUTTONUP:
                sounds.fadeOut()                                                                                                               
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
                    if self._soundOn:
                        print noteSounds[self.menuSounds[self._menu.selected]]                                     
                        sounds.play(noteSounds[self.menuSounds[self._menu.selected]])
                    self.paint()
            else:                                
                # MOUSEBUTTONUP, user clicked on menu
                sel = self._menu.selectItem((x,y))
                if sel is not None:
                    self.do_action(sel)
                #else:
                    ## check if sound icon was clicked
                    #x, y = pygame.mouse.get_pos()
                    #if 25 <= x <= 75 and 570 <= y <= 615:
                        #self._soundOn = not self._soundOn
                        #if not self._soundOn: sounds.muteSound()
                        #else: sounds.turnOn()
                        #self.paint()
                        
        elif evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_ESCAPE:
                sounds.muteSound()                                                                                                               
                self.end(self.FINISH)
            elif evt.key == pygame.K_DOWN:
                self._menu.next()
                sounds.play(noteSounds[self.menuSounds[self._menu.selected]])
                self.paint()
            elif evt.key == pygame.K_UP:
                self._menu.prev()
                sounds.play(noteSounds[self.menuSounds[self._menu.selected]])
                self.paint()
            elif evt.key in [pygame.K_RETURN, pygame.K_SPACE]:
                sel = self._menu.selected
                sounds.play(noteSounds[self.menuSounds[sel]])
                self.do_action(sel)
            else:                                   
                try:
                    keypressed = string.upper(chr(evt.key))
                    if keypressed not in score.Note.validNotes:
                        #print "Invalid key!", chr(evt.key)
                        return
                    else:
                        self.evaluate(keypressed)                    
                except:
                    pass   # ignore keys such as ALT, CTRL, SHIFT, etc

        elif evt.type == self.CLOCK_TICK:
            if self._timer.isRunning():
                self._timer.update(100)
                pygame.time.set_timer(self.CLOCK_TICK, 100)
                

    def evaluate(self, guess):
        sounds.play(noteSounds[self.menuSounds[self._menu.selected]])
        # select option from menu
        self._menu.selected  = self.notesIndexMenu.index(guess)
        self._menu.alternate = self.notesIndexMenu.index(guess)

        if guess == self._answer:
            self.game.score += 1
            self._status = self.CORRECT
        else:
            self._status = self.WRONG

        self._showPressKeyMsg = True
        if self._useTimer:
            self._timer.stop()

        self.paint()
        self.animateEvaluation()

    def animateEvaluation(self):
        if self._status == self.CORRECT:
            self.game.screen.blit(self._images["correct"], self._answerCoords)
            for x in range(0, 900):
                pygame.display.update((x, 0),(x, 700))
                # TODO: update only image part
            #for x in range(self._answerCoords[0], self._answerCoords[0] + self._images["correct"].get_width()):
                #pygame.display.update((x, self._answerCoords[1]),(x, self._images["correct"].get_height() + self._answerCoords[1]))
                #print x, self._answerCoords[1],x, self._images["correct"].get_height() + self._answerCoords[1]
        elif self._status == self.WRONG:
            self.game.screen.blit(self._images["wrong1"], self._answerCoords)
            for x in range(0, 900):
                pygame.display.update((x, 0),(x, 700))
            self.game.screen.blit(self._images["wrong2"], (self._answerCoords[0] + 80, self._answerCoords[1]))
            for y in range(0, 600):
                pygame.display.update((0, y),(800, y))


    def do_action(self, sel):
        self._menu.alternate = sel
        self.evaluate(self._menu.options[sel][0])


    def loop(self):
        self.paint()
        if self._status == self.WRONG:
            self.game.screen.blit(self._images["wrong1"], self._answerCoords)
            self.game.screen.blit(self._images["wrong2"], (self._answerCoords[0] + 80, self._answerCoords[1]))
        elif self._status == self.CORRECT:
            self.game.screen.blit(self._images["correct"], self._answerCoords)

    def start(self):
        self._lastUpdate = self._startTime = time.time()

