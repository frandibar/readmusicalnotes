from data import *
from engine import Game, Scene
from menu import Menu
from sounds import sounds
from timer import Timer, BlinkingText
import colors
import options
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
        quiz = score.ScoreBuilder(clef, 300, showTimeSignature = False, notesList = [note]).getImage(self.game.screen.get_size())
        self._quizImg = pygame.transform.scale2x(quiz)

        # load images
        self._images = {}
        self._images["correct"] = pygame.image.load(CORRECT_IMG).convert_alpha()
        self._images["wrong"]   = pygame.image.load(WRONG_IMG).convert_alpha()
        font = pygame.font.Font(NOTES_FONT, 15)
        self._images["instructions"] = font.render("Use keys up, down, C, D, E, F, G, A, B and Enter", True, colors.BLACK)
        font = pygame.font.Font(LEGEND_FONT, 30)
        self._images["pressKey"] = font.render("Press any key to continue", True, colors.BLACK)
        OVERLAY_HEIGHT = 60
        self._images["overlay"] = pygame.Surface((self.game.screen.get_width(), OVERLAY_HEIGHT)).convert()
        self._images["overlay"].fill(colors.DARK_RED)
        self._images["overlay"].set_alpha(85)
        self._images["soundOn"]  = pygame.image.load(SOUND_ON_IMG).convert_alpha()
        self._images["soundOff"] = pygame.image.load(SOUND_OFF_IMG).convert_alpha()

        self._showInstructions = False
        self._showPressKeyMsg  = False

        self.background = pygame.image.load(BACKGROUND_IMG).convert()

        # menu
        self._menu = Menu(
                 pygame.font.Font(NOTES_FONT, 30),
                 pygame.font.Font(NOTES_FONT, 30),
                 pygame.font.Font(NOTES_FONT, 30),
                 ["B si", "A la", "G sol", "F fa", "E mi", "D re", "C do"],
                 margin = 0,
                 normalColor    = colors.BLACK,
                 selectedColor  = colors.DARK_RED,
                 alternateColor = colors.BROWN,
                 centered = False
                 )

        pygame.time.set_timer(self.CLOCK_TICK, 1000)        
        useTimer = self._setupOptions.timerIndex != self._setupOptions.OFF
        self._timer = Timer(self._setupOptions.getTimerSec(), useTimer)
        self._ticks = 0
        notetimer = NoteTimer()
        notetimer.setYpos(400)
        self._timerSprite = pygame.sprite.RenderClear(notetimer)
        if useTimer:
            self._timer.start()

        # set coordinates
        self._menuCoords = (700, 100)
        self._imgCoords = (50, 50)

        self._status = self.WAITING

        sounds.muteSound()
        self.start()

    def paint(self):
        self.game.screen.blit(self.background, (0,0))

        # show timer
        self._timerSprite.clear(self.game.screen, self.background)
        self._timerSprite.draw(self.game.screen)
        
        self.game.screen.blit(self._quizImg, self._imgCoords)
        # show score
        font = pygame.font.Font(SCORE_FONT, 30)
        ok = font.render(str(self.game.score), True, colors.OLIVE_GREEN)
        total = font.render(" - " + str(self.game.level), True, colors.BLACK)
        self.game.screen.blit(ok, (self.game.screen.get_width() - ok.get_width() - total.get_width() - 50, self.game.screen.get_height() - ok.get_height()))
        self.game.screen.blit(total, (self.game.screen.get_width() - total.get_width() - 50, self.game.screen.get_height() - total.get_height()))

        self._menu.blit(self.game.screen, self._menuCoords)
        # show messages
        if self._timer.timeIsUp():
            self._showPressKeyMsg = True
            self._status = self.TIMEISUP
        if self._showPressKeyMsg:
            self.game.screen.blit(self._images["pressKey"], ((self.game.screen.get_width() - self._images["pressKey"].get_width())/2, self.game.screen.get_height() - self._images["pressKey"].get_height() - 10))
        if self._showInstructions:                    
            self.game.screen.blit(self._images["instructions"], ((self.game.screen.get_width() - self._images["instructions"].get_width())/2, self.game.screen.get_height() - self._images["pressKey"].get_height() - 10))                                 

        # show statusbar                                                                                                                                                                                                                                                           
        self.game.screen.blit(self._images["overlay"], (0, self.game.screen.get_height() - self._images["overlay"].get_height()))                                 
        self.game.screen.blit(self._images["soundOn"], (50, self.game.screen.get_height() - self._images["soundOn"].get_height()))                                 
        
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
                if self._ticks % 10 == 0:
                    self._timer.tick()
                self._ticks += 1                                      
                pygame.time.set_timer(self.CLOCK_TICK, 100)
                self._timerSprite.update()
                

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
        x += 450
        y -= 0
        self.paint()
        if self._status == self.WRONG:
            self.game.screen.blit(self._images["wrong"], (x, y))
        elif self._status == self.CORRECT:
            self.game.screen.blit(self._images["correct"], (x, y))

    def update(self):
        #self._timer.blit(self.game.screen, (770, 100))
        self._timer.alarm.blit(self.game.screen)
        pass

    def start(self):
        self._lastUpdate = self._startTime = time.time()


class NoteTimer(pygame.sprite.Sprite):
    DISTANCE = 400
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #call Sprite initalizer
        self.image = pygame.image.load(TIMER_IMG)
        self.rect = self.image.get_rect()                                                 
        self.rect.center = (self.image.get_width() / 2, self.image.get_height() / 2)
        self.xSpeed = self.DISTANCE / (options.SetupOptions().getTimerSec() * 10)
        self.ySpeed = 1

    def setYpos(self, ypos):
        self.rect.top = ypos

    def update(self):
        self.rect.move_ip((self.xSpeed, self.ySpeed))
        if self.rect.top % 10 == 0:
            self.ySpeed = -1 * self.ySpeed                                  

