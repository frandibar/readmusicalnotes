from data import *
from setupoptions import SetupOptions

import os
import pygame
import random

DEBUG = False

class Sounds:
    AMBIENT_VOLUME = 0.5
    TICTAC_VOLUME  = 0.3

    def init(self):
        self.mute = SetupOptions().sounds == SetupOptions().NO
        NCHANNELS = 2
        pygame.mixer.init()
        pygame.mixer.set_reserved(NCHANNELS)
        pygame.mixer.pre_init(44100, -16, False)

        self._channels = {}
        self._channels["ambient"] = pygame.mixer.Channel(1)
        self._channels["tictac"]  = pygame.mixer.Channel(2)
        self._channels["ambient"].set_volume(self.AMBIENT_VOLUME)
        self._channels["tictac"].set_volume(self.TICTAC_VOLUME)

        for s in [INTRO_SND]:
            self._channelSounds(s, self._channels["ambient"], -1)  # -1 to loop forever

        for s in [TICTAC_SND]:
            self._channelSounds(s, self._channels["tictac"], -1)

        for s in [ENTER_SND, MENU_SND, TIMEISUP_SND]:
            self._looseSounds(s)

        for s in noteSounds.values():
            self._looseSounds(s)


    def play(self, sound):
        if self.mute: return
        getattr(self, sound)()

    def fadeOut(self):
        if self.mute: return
        pygame.mixer.fadeout(250)

    def turnOn(self):
        self.init()

    def muteSound(self):
        #pygame.mixer.quit()
        pygame.mixer.stop()

    def muteChannel(self, channel):
        self._channels[channel].stop()

    def _channelSounds(self, s, channel, loops = 0):
        sound = pygame.mixer.Sound(s)
        def play():
            if self.mute: return
            channel.play(sound, loops)

        setattr(self, s, play)
            
    def _looseSounds(self, s):
        sound = pygame.mixer.Sound(s)
        setattr(self, s, sound.play)


sounds = Sounds()

