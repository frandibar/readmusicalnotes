from data import *
from engine import Game, Scene
from menu import Menu
from pygame.locals import *
from sounds import sounds
import colors
import hollow
import os
import pygame
import random
import string
import time

DEBUG = False

bassClefImages = [
    "fa1.png", "fa2.png", "fb1.png", "fb2.png", "fc1.png", "fc2.png", "fc3.png",
    "fd1.png", "fd2.png", "fe1.png", "fe2.png", "ff1.png", "ff2.png", "fg1.png",
    "fg2.png"
]

trebleClefImages = [
    "ga3.png", "ga4.png", "gb3.png", "gb4.png", "gc4.png", "gc5.png", "gd3.png", 
    "gd4.png", "ge3.png", "ge4.png", "gf3.png", "gf4.png", "gg3.png", "gg4.png"
]

# these are the notes corresponding to the bassClefImages
bassNotes = [
    'A', 'A', 'B', 'B', 'C', 'C', 'C',
    'D', 'D', 'E', 'E', 'F', 'F', 'G', 'G'
]

# these are the notes corresponding to the trebleClefImages
trebleNotes = [
    'A', 'A', 'B', 'B', 'C', 'C', 'D',
    'D', 'E', 'E', 'F', 'F', 'G', 'G'
]

notesIndexMenu = { 'B': 0, 
                   'A': 1, 
                   'G': 2, 
                   'F': 3, 
                   'E': 4, 
                   'D': 5, 
                   'C': 6 
} 

# these are the sounds to play when an item from the menu is selected
menuSounds = ['b3', 'a3', 'g3', 'f3', 'e3', 'd3', 'c3', 'pasa'] 


class BlinkingText:
    '''displays a blinking text message'''
    def __init__(self, text = "", (xpos, ypos) = (0,0), soundToPlay = None, centered = True, fontColor = colors.RED, fontBorderColor = colors.BLACK, delay = 0, blinkTime = 0.5, soundTime = 3):
        font = pygame.font.Font(MAIN_MENU_FONT, 50)
        self._text = hollow.textOutline(font, text, fontColor, fontBorderColor)
        self._delay = delay
        self._blinkTime = blinkTime
        self._soundTime = soundTime
    
        self._isOn = False
        self._start = None
        self._blinkOn = False
        self._lastBlinkTime = None
        self._lastSoundTime = None
        self._xpos = xpos
        self._ypos = ypos
        self._centered = centered
        self._played = False
        self._soundToPlay = soundToPlay

    def turnOn(self):
        self._start = time.time()
        self._isOn = True

    def turnOff(self):
        self._isOn = False
        
    def blit(self, screen):
        if self._isOn:
            now = time.time()
            if now - self._start > self._delay:
                self.play()
                if self._lastBlinkTime is None:
                    self._lastBlinkTime = time.time()
                    
                if now - self._lastBlinkTime > self._blinkTime:
                    self._blinkOn = not self._blinkOn
                    self._lastBlinkTime = time.time()
                    
                if self._blinkOn:
                    if self._centered:
                        screen.blit(self._text, (self._xpos - self._text.get_width()/2, self._ypos))
                    else:
                        screen.blit(self._text, (self._xpos, self._ypos))

                if self._lastSoundTime is None:
                    self._lastSoundTime = time.time()
                    
                if now - self._lastSoundTime > self._soundTime:
                    self._lastSoundTime = now

    def play(self):                    
        if self._played == False:
            sounds.play(self._soundToPlay)
            self._played = True


class Timer:
    def __init__(self, totalTime, enabled = True):
        self.alarm = BlinkingText("Time is up!", (400, 100), "timeisup")                                                                                      

        self._totalTime = totalTime
        self._enabled = enabled
        self._isRunning = False
        self._timeLeft  = totalTime
        self._tic = True                                                                                                                               
        
    @property
    def enabled(self):
        return self._enabled

    def disable(self):
        self._enabled = false

    def getTotalTime(self):
        if not self._enabled: return
        return self._totalTime

    def timeIsUp(self):
        if not self._enabled: return
        if self._timeLeft <= 0:
            self.stop(True)
            return True                       
        return False

    def start(self):
        if not self._enabled: return
        self._isRunning = True        
        self._timeLeft = self._totalTime

    def isRunning(self):
        return self._isRunning

    def stop(self, playAlarm = False):
        if not self._enabled: return
        self._isRunning = False        
        if playAlarm:
            self.alarm.turnOn()
        sounds.muteChannel("tictac")

    def tick(self):                                    
        if not self._enabled: return
        self._timeLeft -= 1
        if self._tic:
            sounds.play("tic")
        else:
            sounds.play("tac")
        self._tic = not self._tic

    def blit(self, surface, (x, y)):
        '''draw the timer as a vertical column decrementing in height'''
        if not self._enabled: return
        fullHeight = 300
        width = 20
        height = max(self._timeLeft * fullHeight / self.getTotalTime(), 0)
        pygame.draw.rect(surface, colors.BLACK, Rect(x-1, y-1, width+3, fullHeight+2))
        pygame.draw.rect(surface, colors.YELLOW, Rect(x, y + fullHeight - height, width, height))
        

class Setup(Scene):
    COL1 = 100                  
    COL2 = 250                  
    COL3 = 400                  
    def init(self, game):
        self._background = pygame.image.load(MAIN_MENU_IMG).convert()
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


class NotesQuiz(Scene):
    WAITING, WRONG, CORRECT, FINISH, TIMEISUP = range(5)   # status values
    CLOCK_TICK = pygame.USEREVENT
    def init(self):
        # select a random image
        random.shuffle(range(len(setupOptions.images)))
        self._answerIndex = random.choice(range(len(setupOptions.images)))
        quiz = os.path.join(IMAGES_PATH, setupOptions.images[self._answerIndex])
        self._images = {}
        self._images["quiz"]    = pygame.image.load(quiz).convert()
        self._images["correct"] = pygame.image.load(CORRECT_IMG).convert()
        self._images["wrong"]   = pygame.image.load(WRONG_IMG).convert()
        font = pygame.font.Font(NOTES_FONT, 20)
        self._images["instructions"] = font.render("Use keys C, D, E, F, G, A and B", True, colors.BLACK)
        font = pygame.font.Font(MAIN_MENU_FONT, 30)
        self._images["pressKey"]     = font.render("Press any key to continue", True, colors.RED)

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
        useTimer = setupOptions.getTimerIndex() != setupOptions.OFF
        self._timer = Timer(setupOptions.getTimerSec(), useTimer)
        if useTimer:
            self._timer.start()

        # image coordinates
        xpos = (self.game.screen.get_size()[0] - self._images["quiz"].get_width()) / 2
        ypos = (self.game.screen.get_size()[1] - self._images["quiz"].get_height()) / 2
        self._imgCoords = (xpos, ypos)

        # menu coordinates
        self._menuCoords = (100, 100)

        self._status = self.WAITING

        sounds.muteSound()
        self.start()

    def paint(self):
        self.game.screen.blit(self.background, (0,0))
        # show score
        font = pygame.font.Font(MAIN_MENU_FONT, 20)
        score = font.render("Score: " + str(self.game.score) + " / " + str(self.game.level), True, colors.BLACK)
        self.game.screen.blit(score, (10,10))

        self.game.screen.blit(self._images["quiz"], self._imgCoords)
        self._menu.blit(self.game.screen, self._menuCoords)
        if self._timer.timeIsUp():
            self._showPressKeyMsg = True
            self._status = self.TIMEISUP
        if self._showPressKeyMsg:
            self.game.screen.blit(self._images["pressKey"], ((self.game.screen.get_width() - self._images["pressKey"].get_width())/2, 400))
        if self._showInstructions:                    
            self.game.screen.blit(self._images["instructions"], ((self.game.screen.get_width() - self._images["instructions"].get_width())/2, 450))                                 

        
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
                    sounds.play(menuSounds[self._menu.selected])
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
                sounds.play(menuSounds[self._menu.selected])
                self.paint()
            elif evt.key == pygame.K_UP:
                self._menu.prev()
                sounds.play(menuSounds[self._menu.selected])
                self.paint()
            elif evt.key in [pygame.K_RETURN, pygame.K_SPACE]:
                sel = self._menu.selected
                sounds.play(menuSounds[sel])
                self.do_action(sel)
            else:                                   
                try:
                    keypressed = string.upper(chr(evt.key))
                    if keypressed not in setupOptions.notes:
                        print "Invalid key!", chr(evt.key)
                        return
                    else:
                        self.evaluate(keypressed)                    
                except:
                    pass   # ignore keys such as ALT, CTRL, SHIFT, etc

        elif evt.type == self.CLOCK_TICK:
            if self._timer.isRunning():
                self._timer.tick()
                pygame.time.set_timer(self.CLOCK_TICK, 1000)
                

    def evaluate(self, guess):
        sounds.play(menuSounds[self._menu.selected])
        # select option from menu
        self._menu.selected  = notesIndexMenu[guess]
        self._menu.alternate = notesIndexMenu[guess]

        answer = setupOptions.notes[self._answerIndex]
        if guess == answer:
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
        xpos = x + 300
        self.paint()
        if self._status == self.WRONG:
            self.game.screen.blit(self._images["wrong"], (xpos, y))
        elif self._status == self.CORRECT:
            self.game.screen.blit(self._images["correct"], (xpos, y))

    def update(self):
        self._timer.blit(self.game.screen, (770, 50))
        self._timer.alarm.blit(self.game.screen)
        pass

    def start(self):
        self._lastUpdate = self._startTime = time.time()



setupOptions = SetupOptions(SetupOptions.SEC5, SetupOptions.YES, SetupOptions.YES)
