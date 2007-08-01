from data import *
from sounds import sounds
import colors

from pygame.color import Color
import pygame
import time

class BlinkingText:
    '''displays a blinking text message'''
    def __init__(self, text, font, (xpos, ypos) = (0,0), soundToPlay = None, centered = True, fontColor = Color('dark red'), fontBorderColor = Color('black'), delay = 0, blinkTime = 0.5, soundTime = 3):
        self._text = font.render(text, True, fontColor)
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
        self._soundToPlay = soundToPlay

    def turnOn(self):
        sounds.play(self._soundToPlay)
        self._start = time.time()
        self._isOn = True

    def turnOff(self):
        self._isOn = False
        
    def blit(self, screen):
        if not self._isOn:
            return

        now = time.time()
        if now - self._start > self._delay:
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


class Timer:
    def __init__(self, totalTime, alarm = None):
        self.alarm = alarm

        self._totalTime = totalTime
        self._isRunning = False
        self._timeLeft  = totalTime
        self._tic = True                                                                                                                               

    def getTotalTime(self):
        return self._totalTime

    def timeIsUp(self):
        if self._timeLeft <= 0:
            self.stop(True)
            return True                       
        return False

    def start(self):
        self._isRunning = True        
        self._timeLeft = self._totalTime
        sounds.play(TICTAC_SND)

    def isRunning(self):
        return self._isRunning

    def stop(self, playAlarm = False):
        self._isRunning = False        
        if playAlarm:
            self.alarm.turnOn()
        sounds.muteChannel("tictac")


class FlareTimer(pygame.sprite.Sprite, Timer):
    def __init__(self, totalTime, alarm, (x,y), length):
        # call base class constructors
        Timer.__init__(self, totalTime, alarm)
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(FLARE_IMG)
        self.rect = self.image.get_rect()                                                 
        #self.rect.center = (self.image.get_width() / 2, self.image.get_height() / 2)
        self.length = length - (length % totalTime)

        self.setPos((x,y))
        self._render = pygame.sprite.RenderClear(self)
        
    def setPos(self, (x,y)):
        self.rect.left = x
        self.rect.top = y

    def update(self, ms):
        if not self.timeIsUp():
            step = ms / 1000.0
            inc = self.length / self._totalTime * step
            self._timeLeft -= step
            self.rect.move_ip((inc, 0))
        elif self.alarm is not None:
            self.alarm.turnOn()                                        


    def blit(self, surface, background, (x, y)):
        self._render.clear(surface, background)
        x0 = x + self.image.get_width() / 2
        y0 = y + self.image.get_height() / 2
        x1 = self.rect.center[0]
        xf = x + self.length
        pygame.draw.line(surface, Color('gray55'), (x0, y0), (xf, y0), 3)
        pygame.draw.line(surface, colors.BROWN, (x0, y0), (x1, y0), 3)
        self._render.draw(surface)
        self.alarm.blit(surface)
        #print x0, x1, xf                                  

