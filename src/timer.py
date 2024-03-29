from resources import *
from sounds import sounds
import colors

from pygame.color import Color
import pygame
import time

class BlinkingText:
    """displays a blinking text message"""
    def __init__(self, text, font, (x,y) = (0,0), centered = True, fontColor = Color("dark red"), delayBetweenBlinks = 0, blinkDuration = 0.5):
        self._font = font
        self._fontColor = fontColor
        self._text = text
        self._img = font.render(text, True, fontColor)                                                       
    
        self._isOn = False
        self._start = None
        self._blinkOn = False
        self._lastBlinkTime = None
        self._lastSoundTime = None

        self.coords = (x,y)
        self.centered = centered

        self.delayBetweenBlinks = delayBetweenBlinks
        self.blinkDuration = blinkDuration

        self.soundToPlay = None
        self.soundDuration = 3

    def setFont(self, font):
        self._img = font.render(self._text, True, self._color)

    def setFontColor(self, color):
        self._img = self._font.render(self._text, True, color)

    def setText(self, text):
        self._img = self._font.render(text, True, self._color)

    def turnOn(self):
        if self._isOn:
            return

        self._start = time.time()
        self._isOn = True
        if self.soundToPlay is not None:
            sounds.play(self.soundToPlay)

    def turnOff(self):
        self._isOn = False
        
    def blit(self, screen):
        if not self._isOn:
            return

        now = time.time()
        if now - self._start > self.delayBetweenBlinks:
            if self._lastBlinkTime is None:
                self._lastBlinkTime = time.time()
                
            if now - self._lastBlinkTime > self.blinkDuration:
                self._blinkOn = not self._blinkOn
                self._lastBlinkTime = time.time()
                
            if self._blinkOn:
                if self.centered:
                    x,y = self.coords
                    screen.blit(self._img, (x - self._img.get_width() / 2, y))
                else:
                    screen.blit(self._img, self.coords)

            if self._lastSoundTime is None:
                self._lastSoundTime = time.time()
                
            if now - self._lastSoundTime > self.soundDuration:
                self._lastSoundTime = now


class Timer:
    def __init__(self, totalTime, alarm = None):
        # totalTime is in seconds
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
        sounds.play(TICTAC_SND, FOREVER)

    def isRunning(self):
        return self._isRunning

    def stop(self, playAlarm = False):
        self._isRunning = False        
        sounds.stop(TICTAC_SND)
        if playAlarm:
            self.alarm.turnOn()


class FlareTimer(pygame.sprite.Sprite, Timer):
    def __init__(self, totalTime, alarm, (x,y), length):
        # call base class constructors
        Timer.__init__(self, totalTime, alarm)
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(FLARE_IMG)
        self.rect = self.image.get_rect()                                                 
        self._length = length - (length % totalTime)

        self._startCoords = (x,y)
        self.setPos((x,y))
        self._render = pygame.sprite.RenderClear(self)
        self._speed = (self._length / float(totalTime), 0)
        
    def setPos(self, (x,y)):
        self.rect.left = x
        self.rect.top = y

    def update(self, ms):
        elapsed = ms / 1000.0        # elapsed time in seconds
        self._timeLeft -= elapsed
        xdist = ((self._totalTime - self._timeLeft) * self._length) / self._totalTime
        xdist += self._startCoords[0]
        ydist = self._startCoords[1]
        self.setPos((xdist, ydist))

    def blit(self, surface, background):
        self._render.clear(surface, background)
        x0, y0 = self._startCoords
        x0 += self.image.get_width() / 2
        y0 += self.image.get_height() / 2
        x1 = self.rect.center[0]
        xf = x0 + self._length
        pygame.draw.line(surface, Color("gray30"), (x0, y0), (xf, y0), 3)
        pygame.draw.line(surface, colors.OCRE, (x0, y0), (x1, y0), 3)
        self._render.draw(surface)
        self.alarm.blit(surface)

