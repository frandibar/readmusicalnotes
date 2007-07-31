from data import *

import os
import pygame
import random

DEBUG = False

class Sounds:
    AMBIENT_VOLUME = 0.5
    TICTAC_VOLUME  = 0.6

    def __init__(self, mute):
        self.mute = mute

    def init(self):
        NCHANNELS = 2
        pygame.mixer.set_reserved(NCHANNELS)
        pygame.mixer.pre_init(44100, -16, False)
        pygame.mixer.init()

        self._channels = {}
        self._channels["ambient"] = pygame.mixer.Channel(1)
        self._channels["tictac"]  = pygame.mixer.Channel(2)
        self._channels["ambient"].set_volume(self.AMBIENT_VOLUME)
        self._channels["tictac"].set_volume(self.TICTAC_VOLUME)

        for s in ["bach_846_prelude1"]:
            self._channelSounds(s, self._channels["ambient"], -1)

        for s in ["ticking.wav"]:
            self._channelSounds(s, self._channels["tictac"], -1)

        for s in ["enter.wav", "menu.wav", "timeisup.wav", "b3.ogg", "a3.ogg", "g3.ogg", "f3.ogg", "e3.ogg", "d3.ogg", "c3.ogg"]:
            self._looseSounds(s)

    def play(self, sound):
        if self.mute: return
        getattr(self, sound)()

    def muteSound(self):
        if self.mute: return
        pygame.mixer.fadeout(250)

    def muteChannel(self, channel):
        self._channels[channel].stop()

    def _buildSound(self, s):
        if self.mute: return
        if "." not in s:
            s += ".ogg"
        if DEBUG: print "Loading sound:", s
        return pygame.mixer.Sound(os.path.join(SOUNDS_PATH, s))

    def _channelSounds(self, s, channel, loops = 0):
        if self.mute: return
        sound = self._buildSound(s)
        def play():
            channel.play(sound, loops)

        if s.endswith(".wav"):
            s = s[:-4]
        setattr(self, s, play)
            
    def _looseSounds(self, s):
        if self.mute: return
        sound = self._buildSound(s)
        if s.endswith(".wav") or s.endswith(".ogg"):
            s = s[:-4]
        setattr(self, s, sound.play)

sounds = Sounds(mute = False)

