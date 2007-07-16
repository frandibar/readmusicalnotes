from data import *
import colors
import hollow
from sounds import sounds

import pygame
import time

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
        pygame.draw.rect(surface, colors.BLACK, pygame.locals.Rect(x-1, y-1, width+2, fullHeight+2))
        pygame.draw.rect(surface, colors.YELLOW, pygame.locals.Rect(x, y + fullHeight - height, width, height))
        
