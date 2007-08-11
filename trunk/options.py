from engine import Scene
from menu import OptionsMenu
from resources import *
from setupoptions import setupOptions, SetupOptions
from sounds import sounds
from language import *

import colors
from pygame.color import Color
import pygame

class Setup(Scene):
    TREBLE_CLEF, BASS_CLEF, TIMER, SOUNDS, SOFT_TRANSITIONS, LANGUAGE, BACK = range(7)
    def init(self, game):
        self._background    = pygame.image.load(BACKGROUND_IMG).convert()
        self._decorationImg = pygame.image.load(DECORATION3_IMG).convert_alpha()

        yesNoOpts = [dict[T_NO], dict[T_YES]]
        timeOpts = [dict[T_OFF], dict[T_5SEC], dict[T_10SEC], dict[T_15SEC], dict[T_20SEC]]
        self._options = [dict[T_TREBLE_CLEF], dict[T_BASS_CLEF], dict[T_TIMER], dict[T_SOUNDS], dict[T_SOFT_TRANSITIONS], dict[T_LANGUAGE], dict[T_BACK]]
        languages = [dict[T_ENGLISH], dict[T_SPANISH]]
        self._values = [yesNoOpts, yesNoOpts, timeOpts, yesNoOpts, yesNoOpts, languages, None]
        self._menu = OptionsMenu(
                 self._options,
                 self._values,
                 pygame.font.Font(OPTIONS_FONT, 30),
                 pygame.font.Font(OPTIONS_FONT, 30),
                 margin = 0,
                 normalColor   = colors.OCRE,
                 selectedColor = Color("dark red")
                 )

        iconsOn  = [TREBLE_CLEF_SEL_IMG, BASS_CLEF_SEL_IMG, TIMER_SEL_IMG, SOUND_SEL_IMG, None, None, None]
        iconsOff = [TREBLE_CLEF_UNSEL_IMG, BASS_CLEF_UNSEL_IMG, TIMER_UNSEL_IMG, SOUND_UNSEL_IMG, None, None, None]
        self._menu.addIcons(iconsOn, iconsOff)
        self._menu.setMarker(MENU_MARKER_IMG)

        font = pygame.font.Font(OPTIONS_FONT, 50)
        self._title = font.render(dict[T_OPTIONS][setupOptions.language], True, pygame.color.Color("black"))

        self._titleCoords      = (40, 53)
        self._menuCoords       = (350, 200)
        self._decorationCoords = (10, 100)

        self._clock = pygame.time.Clock()
        self.loadOptionValues()
        if setupOptions.softTransitions == SetupOptions.YES:
            self.showAnimation()
        else:
            self.paint()

    def paint(self):
        self.game.screen.blit(self.background, (0,0))
        self.game.screen.blit(self._decorationImg, self._decorationCoords)
        self.game.screen.blit(self._title, self._titleCoords)
        self._menu.blit(self.game.screen, self._menuCoords)

    def showAnimation(self):
        if setupOptions.softTransitions == SetupOptions.NO: return
        self.game.screen.blit(self.background, (0,0))
        self.fadeIn()
        self.game.screen.blit(self._decorationImg, self._decorationCoords)
        for x in range(self._decorationCoords[0], self._decorationCoords[0] + self._decorationImg.get_width(), 5):
            pygame.display.update((x, self._decorationCoords[1]),(x, self._decorationCoords[1] + self._decorationImg.get_height()))
            self._clock.tick(ANIMATION_FR)

        self.fadeInMenu()

    def fadeInMenu(self):                                                                                     
        if setupOptions.softTransitions == SetupOptions.NO: return
        s = self.game.screen.copy()
        s.blit(self._title, self._titleCoords)
        self._menu.blit(s, self._menuCoords)
        for i in range(0, 50, 1):
            s.set_alpha(i)
            self.game.screen.blit(s, (0,0))
            pygame.display.flip()
            self._clock.tick(ANIMATION_FR)

    def event(self, evt):
        if evt.type in [pygame.MOUSEMOTION, pygame.MOUSEBUTTONUP]:
            x, y = pygame.mouse.get_pos()
            x -= self._menuCoords[0]                                                  
            y -= self._menuCoords[1]
            if evt.type == pygame.MOUSEMOTION:
                if self._menu.setItem((x,y)):
                    sounds.play(MENU_SND)
                    self.paint()
            else:
                # MOUSEBUTTONUP, user clicked on menu
                sel = self._menu.selectItem((x,y))
                if sel is not None:
                    sounds.play(OPTION_SND)
                    self.doAction(sel)
        elif evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_ESCAPE:
                self.exit()
            elif evt.key == pygame.K_DOWN:
                self._menu.next()
                sounds.play(MENU_SND)
                self.paint()
            elif evt.key == pygame.K_UP:
                self._menu.prev()
                sounds.play(MENU_SND)
                self.paint()
            elif evt.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                sounds.play(OPTION_SND)
                self.doAction(self._menu.selected, evt.key)
            elif evt.key in [pygame.K_RETURN, pygame.K_SPACE]:
                sounds.play(OPTION_SND)
                self.doAction(self._menu.selected)
                
    def exit(self):
        setupOptions.save()                                                
        self.fadeOut()
        self.end()

    def doAction(self, sel, dir = pygame.K_RIGHT):
        if self._menu.getOption(sel) == self._options[self.BACK]:
            self.exit()                                                                                    
        else:                          
            self._menu.changeOption(sel, dir)
            option = self._menu.getOption(sel)                                             
            i = self._menu.getValueIndex(sel)
            if option == self._options[self.TREBLE_CLEF]:
                setupOptions.useTrebleClef = i
            elif option == self._options[self.BASS_CLEF]:
                setupOptions.useBassClef = i
            elif option == self._options[self.TIMER]:
                setupOptions.timerIndex = i
            elif option == self._options[self.SOUNDS]:
                setupOptions.sounds = i
                if i == SetupOptions.NO:
                    sounds.turnOff()                                        
                else:
                    sounds.turnOn()                    
            elif option == self._options[self.SOFT_TRANSITIONS]:
                setupOptions.softTransitions = i
            elif option == self._options[self.LANGUAGE]:
                setupOptions.language = i
            self.paint()
                        

    def loadOptionValues(self):
        self._menu.setValueIndex(self.TREBLE_CLEF, setupOptions.useTrebleClef)
        self._menu.setValueIndex(self.BASS_CLEF, setupOptions.useBassClef)
        self._menu.setValueIndex(self.TIMER, setupOptions.timerIndex)
        self._menu.setValueIndex(self.SOUNDS, setupOptions.sounds)
        self._menu.setValueIndex(self.SOFT_TRANSITIONS, setupOptions.softTransitions)
        self._menu.setValueIndex(self.LANGUAGE, setupOptions.language)

