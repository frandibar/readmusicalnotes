from resources import CONFIG_FILE
import cfg
import language

import os

class SetupOptions:
    NO, YES = range(2)
    OFF, SEC5, SEC10, SEC15, SEC20 = range(5)

    def __init__(self):
        self.load()

    def load(self):        
        if not os.path.exists(CONFIG_FILE):
            self.setDefaults()
            self.save()
            return                                                                                                                                      

        cfg.initialise(None, None, CONFIG_FILE)                                                             
        self.timerIndex      = cfg.get_int("notesquiz/timerIndex")
        self.useTrebleClef   = cfg.get_int("notesquiz/useTrebleClef")
        self.useBassClef     = cfg.get_int("notesquiz/useBassClef")
        self.sounds          = cfg.get_int("general/sounds")
        self.softTransitions = cfg.get_int("general/softTransitions")
        self.language        = cfg.get_int("general/language")
        self.fullscreen      = cfg.get_int("general/fullscreen")
        cfg.sync()

    def setDefaults(self):
        self.timerIndex      = self.SEC5
        self.useTrebleClef   = self.YES
        self.useBassClef     = self.YES
        self.sounds          = self.YES
        self.softTransitions = self.YES
        self.language        = language.ENGLISH
        self.fullscreen      = self.NO
        self.save()                                                                 

    def save(self):
        cfg.initialise(None, None, CONFIG_FILE)                                                             
        cfg.set_int("notesquiz/timerIndex", self.timerIndex)
        cfg.set_int("notesquiz/useTrebleClef", self.useTrebleClef)
        cfg.set_int("notesquiz/useBassClef", self.useBassClef)
        cfg.set_int("general/sounds", self.sounds)
        cfg.set_int("general/softTransitions", self.softTransitions)
        cfg.set_int("general/language", self.language)
        cfg.set_int("general/fullscreen", self.fullscreen)
        cfg.sync()

    def getTimerSec(self):
        return self.timerIndex * 5


# export global variable
setupOptions = SetupOptions()        
