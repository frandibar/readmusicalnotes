from resources import *
from setupoptions import setupOptions, SetupOptions

import os
import pygame
import random

DEBUG = False

class Sounds:

    def init(self):
        self._mute = setupOptions.sounds == SetupOptions.NO
        self._looseSounds = {}
        self._channelSounds = {}

        pygame.mixer.pre_init(44100, -16, False)
        pygame.mixer.init()
        #pygame.mixer.set_num_channels(1)

        for s in [ENTER_SND, MENU_SND, TICTAC_SND, TIMEISUP_SND, OPTION_SND]:
            self._looseSounds[s] = pygame.mixer.Sound(s)

        for s in noteSounds.values():
            self._looseSounds[s] = pygame.mixer.Sound(s)

        self._channels = [pygame.mixer.Channel(0)]

        for s in [INTRO_SND]:
            self._channelSounds[s] = pygame.mixer.Sound(s)

    def play(self, sound, loops = 0):
        """'sound' is a path to the sound file"""
        if not self._mute and sound in self._looseSounds:
            self._looseSounds[sound].play(loops)
        elif sound in self._channelSounds:
            #for i in self._channels.get_keys():                                          
            self._channels[0].play(self._channelSounds[sound], loops)                                          
            if loops == FOREVER and self._mute:
                self._channels[0].pause()

    def pauseChannel(self, channel = 0):
        if self._mute: return
        self._channels[channel].pause()

    def unpauseChannel(self, channel = 0):
        if self._mute: return
        self._channels[channel].unpause()

    def stop(self, sound):
        if sound in self._looseSounds:
            self._looseSounds[sound].stop()

    def fadeOut(self):
        if self._mute: return
        pygame.mixer.fadeout(250)

    def turnOn(self):
        try:
            self._mute = False
            pygame.mixer.unpause()
        except:
            pass            

    def turnOff(self):
        try:
            self._mute = True
            pygame.mixer.pause()
        except:
            pass            


if not pygame.mixer: print "Warning, sound disabled."
# export global variable
sounds = Sounds()

