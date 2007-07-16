from data import *
import colors

import pygame

class Silence:
    def blit(self, surface, (x,y)):
        surface.blit(self._img, (x, y))

    def getDuration(self):
        return self._duration


class FullSilence(Silence):
    def __init__(self):
        self._img = pygame.image.load(FULL_SILENCE_IMG).convert_alpha()    
        self._duration = 1

class HalfSilence(Silence):
    def __init__(self):
        self._img = pygame.image.load(HALF_SILENCE_IMG).convert_alpha()    
        self._duration = 0.5

class QuarterSilence(Silence):
    def __init__(self):
        self._img = pygame.image.load(QUARTER_SILENCE_IMG).convert_alpha()    
        self._duration = 0.25

class EightSilence(Silence):
    def __init__(self):
        self._img = pygame.image.load(EIGHT_SILENCE_IMG).convert_alpha()    
        self._duration = 0.125

class SixteenthSilence(Silence):
    def __init__(self):
        self._img = pygame.image.load(SIXTEENTH_SILENCE_IMG).convert_alpha()    
        self._duration = 0.0625


class Note:
    validNotes = [ 'C', 'D', 'E', 'F', 'G', 'A', 'B' ]
    validOctaves = range(1,6)  # 1 to 5
    validAccidents = [ 'b', 'n', '#' ]                                       
    def __init__(self, note, octave, staff = None):
        self._note = note[0]
        if len(note) == 2:
            self._accident = note[-1]                         
        else:
            self._accident = 'n'             
        self._octave = octave                         
        self._staff = staff                                                      
        self.useHiStem = False                                                                                 

    def getNote(self):
        return self._note + self._accident

    def getAccident(self):
        return self._accident

    def getOctave(self):
        return self._octave

    def getDuration(self):
        return self._duration

    def isValid(self):
        return self._note in validNotes \
               and self._octave in validOctaves \
               and self._accident in validAccidents                                                 

    def blit(self, surface, (x,y)):
        if self.useHiStem:
            surface.blit(self._hiStemImg, (x, y))
        else:                                                 
            surface.blit(self._loStemImg, (x, y))

    def isHigherThan(self, note):
        if self._octave != note.getOctave():
            return self._octave > note.getOctave()
        i = 0
        note2 = note.getNote()[0]
        for n in self.validNotes:
            if self._note == n: ind1 = i
            if note2 == n: ind2 = i
            i += 1                                              
        if ind1 > ind2:
            return True
        elif ind1 < ind2:
            return False
        else:
            i = 0
            acc = note.getAccident()
            for a in self.validAccidents:
                if self._accident == a: ind1 = i
                if acc == a: ind2 = i
                i += 1                                              
            return ind1 > ind2

                                                                
class FullNote(Note):
    def __init__(self, note, octave, staff):
        base.__init__(self, note, octave, staff)
        self._hiStemImg = pygame.image.load(FULL_IMG).convert_alpha()
        self._loStemImg = self._hiStemImg
        self._duration = 1                                                               
        self.useHiStem = True                                                                                         

class HalfNote(Note):
    def __init__(self, note, octave, staff):
        base.__init__(self, note, octave, staff)
        self._hiStemImg = pygame.image.load(HALF_HI_STEM_IMG).convert_alpha()
        self._loStemImg = pygame.image.load(HALF_LO_STEM_IMG).convert_alpha()
        self._duration = 0.5                                                               

class QuarterNote(Note):
    def __init__(self, note, octave, staff):
        base.__init__(self, note, octave, staff)
        self._hiStemImg = pygame.image.load(QUARTER_HI_STEM_IMG).convert_alpha()
        self._loStemImg = pygame.image.load(QUARTER_LO_STEM_IMG).convert_alpha()
        self._duration = 0.25                                                               

class EightNote(Note):
    def __init__(self, note, octave, staff):
        base.__init__(self, note, octave, staff)
        self._hiStemImg = pygame.image.load(EIGHT_HI_STEM_IMG).convert_alpha()
        self._loStemImg = pygame.image.load(EIGHT_LO_STEM_IMG).convert_alpha()
        self._duration = 0.125                                                               

class SixteenthNote(Note):
    def __init__(self, note, octave, staff):
        base.__init__(self, note, octave, staff)
        self._hiStemImg = pygame.image.load(SIXTEENTH_HI_STEM_IMG).convert_alpha()
        self._loStemImg = pygame.image.load(SIXTEENTH_LO_STEM_IMG).convert_alpha()
        self._duration = 0.0625                                                               


class Staff:
    GUIDE_LENGTH = 35
    def __init__(self, length, width = 3, color = colors.BLACK):
        self._length = length
        self._width = width
        self._color = color
        self._ycoords = []   # stores each lines y coord (from bottom to top)
                                                                                                    
    def blit(self, surface, (x,y)):
        self._calculateYCoords(y)                                                  
        for i in range(5):
            pygame.draw.rect(surface, self._color, pygame.locals.Rect(x, self._ycoords[i], self._length, self._width))

    def _calculateYCoords(self, y):                                                  
        self._ycoords = [y]
        for i in range(5):
            y -= 19
            self._ycoords.append(y)

class TimeSignature:
    def __init__(self, beats = 4, noteValue = 4, color = colors.BLACK):    
        self._beats = beats
        self._noteValue = noteValue
        self._color = color                                   

    def blit(self, surface, (x,y)):
        font = pygame.font.Font(MAIN_MENU_FONT, 40)
        beats = font.render(str(self._beats), True, self._color)
        value = font.render(str(self._noteValue), True, self._color)
        surface.blit(beats, (x, y))
        surface.blit(value, (x, y + beats.get_height() - 20))


class Clef:                                                                                                    
    def __init__(self):
        self._image = None

    def blit(self, surface, (x,y)):
        surface.blit(self._image, (x,y))

class TrebleClef(Clef):
    def __init__(self):
        self._image = pygame.image.load(TREBLE_CLEF_IMG).convert_alpha()

class BassClef(Clef):
    def __init__(self):
        self._image = pygame.image.load(BASS_CLEF_IMG).convert_alpha()



class BarLine:
    def __init__(self, height, width = 3, color = colors.BLACK):
        self._height = height
        self._width = width
        self._color = color

    def blit(self, surface, (x,y)):
        pass

class OrdinaryBarline(BarLine):
    def blit(self, surface, (x,y)):
        pygame.draw.rect(surface, self._color, pygame.locals.Rect(x, y, self._width, self._height))

class DoubleBarLine(BarLine):
    def blit(self, surface, (x,y)):
        pygame.draw.rect(surface, self._color, pygame.locals.Rect(x, y, self._width, self._height))
        pygame.draw.rect(surface, self._color, pygame.locals.Rect(x + 2*self._width, y, self._width, self._height))

class EndBarLine(BarLine):
    def blit(self, surface, (x,y)):
        pass

class OpenRepeatBarLine(BarLine):
    def blit(self, surface, (x,y)):
        pass

class CloseRepeatBarLine(BarLine):
    def blit(self, surface, (x,y)):
        pass

class OpenCloseRepeatBarLine(BarLine):
    def blit(self, surface, (x,y)):
        pass

class KeySignature:
    def __init__(self, key = 'C'):
        self._key = key    
        self._setImage()                          

    def getKey(self):
        return self._key

    def setKey(self, key):
        self._key = key        

    def blit(self, surface, (x,y)):
        if self._key != 'C':
            surface.blit(self._image, (x, y))

    def _setImage(self):
        if self._key == 'D':
            self._image = pygame.image.load(D_KEY_IMG).convert_alpha()
        elif self._key == 'E':                                                                
            self._image = pygame.image.load(E_KEY_IMG).convert_alpha()
        # TODO: add more valid keys                                                                

class ScoreBuilder:
    def __init__(self, clef, staffLength, keySignature, beats = 4, noteValue = 4, notesList = [], color = colors.BLACK):
        self.notes = notesList
        self.clef = clef
        self.color = color                                                                                            
        self.timeSignature = TimeSignature(beats, noteValue, color)                               
        self._staff = Staff(staffLength)                                                                                                   

    def blit(self, surface, (x,y)):
        self.clef.blit(surface, (x,y))
        self.timeSignature.blit(surface, (x + 100, y + 40))
        self._staff.blit(surface, (x,y + 113))
        XOFFSET = 20
        # TODO: add barlines, count durations                    
        for i in self.notes:
            i.blit(surface, (x,y))
            x += XOFFSET


