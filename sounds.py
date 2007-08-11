from resources import *
from setupoptions import setupOptions, SetupOptions

import os
import pygame
import random

DEBUG = False

class Sounds:

    def init(self):
        pygame.mixer.pre_init(44100, -16, False)
        pygame.mixer.init()

        self._mute = setupOptions.sounds == SetupOptions.NO
        self._looseSounds = {}
        for s in [ENTER_SND, MENU_SND, TICTAC_SND, TIMEISUP_SND, OPTION_SND]:
            self._looseSounds[s] = pygame.mixer.Sound(s)

        for s in noteSounds.values():
            self._looseSounds[s] = pygame.mixer.Sound(s)

        self._channels = {}
        self._channels[1] = pygame.mixer.Channel(1)

        self._channelSounds = {}
        for s in [INTRO_SND]:
            self._channelSounds[s] = pygame.mixer.Sound(s)

    def play(self, sound, loops = 0):
        """'sound' is a path to the sound file"""
        if self._mute: return
        if sound in self._looseSounds:
            self._looseSounds[sound].play(loops)
        elif sound in self._channelSounds:
            #for i in self._channels.get_keys():                                          
            self._channels[1].play(self._channelSounds[sound], loops)                                          

    def pauseChannel(self, channel = 1):
        self._channels[channel].pause()

    def unpauseChannel(self, channel = 1):
        self._channels[channel].unpause()

    def stop(self, sound):
        if sound in self._looseSounds:
            self._looseSounds[sound].stop()

    def fadeOut(self):
        if self._mute: return
        pygame.mixer.fadeout(250)

    def turnOn(self):
        self._mute = False

    def turnOff(self):
        self._mute = True
        pygame.mixer.stop()


if not pygame.mixer: print "Warning, sound disabled."
# export global variable
sounds = Sounds()

