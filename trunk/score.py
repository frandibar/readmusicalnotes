from data import *
import colors

import pygame

class Rest:
    def blit(self, surface, (x,y)):
        surface.blit(self._image, (x, y))

    def blit(self, surface, x, staff, clef):
        '''blits note to staff on surface'''
        # clef parameter is not needed, added so call for note.blit has same signature           
        ypos = self._calculateYCoord(staff.getCoords())
        surface.blit(self._image, (x, ypos))

    def getDuration(self):
        return self._duration

    def _calculateYCoord(self, staffCoords):
        return staffCoords[4]

class WholeRest(Rest):
    def __init__(self):
        self._image = pygame.image.load(WHOLE_REST_IMG).convert_alpha()    
        self._duration = 1

    def _calculateYCoord(self, staffCoords):
        return staffCoords[3]

class HalfRest(Rest):
    def __init__(self):
        self._image = pygame.image.load(HALF_REST_IMG).convert_alpha()    
        self._duration = 0.5

    def _calculateYCoord(self, staffCoords):
        return staffCoords[3] + (staffCoords[0] - staffCoords[1]) / 2

class QuarterRest(Rest):
    def __init__(self):
        self._image = pygame.image.load(QUARTER_REST_IMG).convert_alpha()    
        self._duration = 0.25

class EighthRest(Rest):
    def __init__(self):
        self._image = pygame.image.load(EIGHTH_REST_IMG).convert_alpha()    
        self._duration = 0.125

    def _calculateYCoord(self, staffCoords):
        return staffCoords[3]

class SixteenthRest(Rest):
    def __init__(self):
        self._image = pygame.image.load(SIXTEENTH_REST_IMG).convert_alpha()    
        self._duration = 0.0625


class Note:
    validNotes = [ 'C', 'D', 'E', 'F', 'G', 'A', 'B' ]
    validOctaves = range(1,6)  # 1 to 5
    validAccidents = [ 'b', 'n', '#' ]                                       
    def __init__(self, note, octave):
        self._note = note[0]
        if len(note) == 2:
            self._accident = note[-1]                         
        else:
            self._accident = 'n'             
        self._octave = octave                         
        self.useStemUp = False                                                                                 

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

    def next(self):
        if self._note == 'B': 
            self._octave += 1                
        self._note = self.validNotes[(self.validNotes.index(self._note) + 1) % len(self.validNotes)]
        return self

    def previous(self):
        if self._note == 'C': 
            self._octave -= 1                
        self._note = self.validNotes[(self.validNotes.index(self._note) - 1) % len(self.validNotes)]
        return self

    def blit(self, surface, (x,y)):
        '''blits note to surface on (x,y)'''
        if self.useStemUp:
            surface.blit(self._stemUpImg, (x, y))
        else:                                                 
            surface.blit(self._stemDownImg, (x, y))

    def blit(self, surface, x, staff, clef):
        '''blits note to staff on surface'''
        ypos = self._calculateYCoord(staff.getCoords(), clef)

        self.useStemUp = ypos > staff.getCoords()[3]         

        if self.useStemUp:
            surface.blit(self._stemUpImg, (x, ypos - 63))
        else:                                                 
            surface.blit(self._stemDownImg, (x, ypos - 9))

        self._blitGuides(surface, x, ypos, staff)                                                        

    def equals(self, note):
        return self.getNote() == note.getNote() and self._octave == note.getOctave()

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

    def _calculateYCoord(self, staffYCoords, clef):                                                  

        if clef.__class__ == TrebleClef:
            dist = self._calculateNotesBetween(Note('E', 3))
        elif clef.__class__ == BassClef:
            dist = self._calculateNotesBetween(Note('G', 1))
        
        y = staffYCoords[0]            
        if dist != 0:
            if dist % 2 == 0:
                y -= dist * (staffYCoords[0] - staffYCoords[1]) / 2
            else:                
                y -= (dist - 1) * (staffYCoords[0] - staffYCoords[1]) / 2
                y -= (staffYCoords[0] - staffYCoords[1]) / 2
        return y                
                                                                

    def _calculateNotesBetween(self, note):
        '''returns the number of notes between self and note'''
        ret = 0   
        aux = note                                       
        if self.isHigherThan(note):           
            while not self.equals(aux):
                ret += 1
                aux = aux.next()
        else:
            while not self.equals(aux):
                ret -= 1
                aux = aux.previous()
        return ret                            

    def _blitGuides(self, surface, x, y, staff):
        coords = staff.getCoords()
        step = coords[0] - coords[1]
        if y > coords[0]:
            if (y - coords[0]) % step != 0:
                y -= step / 2 + 1
            while y > coords[0]:                                                                  
                pygame.draw.rect(surface, staff.color, pygame.locals.Rect(x, y, staff.GUIDE_LENGTH, staff.width))
                y -= step

        elif y < coords[4]:
            if (coords[4] - y) % step != 0:
                y += step / 2                                           
            while y < coords[4]:                                                                  
                pygame.draw.rect(surface, staff.color, pygame.locals.Rect(x, y, staff.GUIDE_LENGTH, staff.width))
                y += step


class WholeNote(Note):
    def __init__(self, note, octave):
        Note.__init__(self, note, octave)
        self._stemUpImg = pygame.image.load(WHOLE_IMG).convert_alpha()
        self._stemDownImg = self._stemUpImg
        self._duration = 1                                                               
        self.useStemUp = True                                                                                         

class HalfNote(Note):
    def __init__(self, note, octave):
        Note.__init__(self, note, octave)
        self._stemUpImg = pygame.image.load(HALF_STEM_UP_IMG).convert_alpha()
        self._stemDownImg = pygame.image.load(HALF_STEM_DOWN_IMG).convert_alpha()
        self._duration = 0.5                                                               

class QuarterNote(Note):
    def __init__(self, note, octave):
        Note.__init__(self, note, octave)
        self._stemUpImg = pygame.image.load(QUARTER_STEM_UP_IMG).convert_alpha()
        self._stemDownImg = pygame.image.load(QUARTER_STEM_DOWN_IMG).convert_alpha()
        self._duration = 0.25                                                               

class EighthNote(Note):
    def __init__(self, note, octave):
        Note.__init__(self, note, octave)
        self._stemUpImg = pygame.image.load(EIGHTH_STEM_UP_IMG).convert_alpha()
        self._stemDownImg = pygame.image.load(EIGHTH_STEM_DOWN_IMG).convert_alpha()
        self._duration = 0.125                                                               

class SixteenthNote(Note):
    def __init__(self, note, octave):
        Note.__init__(self, note, octave)
        self._stemUpImg = pygame.image.load(SIXTEENTH_STEM_UP_IMG).convert_alpha()
        self._stemDownImg = pygame.image.load(SIXTEENTH_STEM_DOWN_IMG).convert_alpha()
        self._duration = 0.0625                                                               


class Chord:
    def __init__(self, notes = []):
        self.notes = notes

    def blit(self, surface, x, staff, clef):
        for i in self.notes:
            i.blit(surface, x, staff, clef)

    def getDuration(self):
        return self.notes[0].getDuration()

    #def blit(self, surface, (x,y)):
        #for i in self.notes:
            #i.blit(surface, (x,y))



class Staff:
    GUIDE_LENGTH = 35
    def __init__(self, length, width = 3, color = colors.BLACK):
        self.length = length
        self.width = width
        self.color = color
        self._ycoords = []   # stores each lines y coord (from bottom to top)
        self._calculateYCoords(0)
                                                                                                    
    def blit(self, surface, (x,y)):
        self._calculateYCoords(y)                                                  
        for i in range(5):
            pygame.draw.rect(surface, self.color, pygame.locals.Rect(x, self._ycoords[i], self.length, self.width))

    def getCoords(self):
        return self._ycoords

    def getHeight(self):
        return self._ycoords[0] - self._ycoords[4]

    def _calculateYCoords(self, y):                                                  
        self._ycoords = [y]
        for i in range(4):
            y -= 19
            self._ycoords.append(y)


class TimeSignature:
    def __init__(self, beats = 4, noteValue = 4, color = colors.BLACK):    
        self.beats = beats
        self.noteValue = noteValue
        self.color = color                                   

    def blit(self, surface, (x,y)):
        font = pygame.font.Font(MAIN_MENU_FONT, 40)
        beats = font.render(str(self.beats), True, self.color)
        value = font.render(str(self.noteValue), True, self.color)
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
        self.height = height
        self.width = width
        self.color = color

    def blit(self, surface, (x,y)):
        pass

class OrdinaryBarline(BarLine):
    def blit(self, surface, (x,y)):
        pygame.draw.rect(surface, self.color, pygame.locals.Rect(x, y, self.width, self.height))

class DoubleBarLine(BarLine):
    def blit(self, surface, (x,y)):
        pygame.draw.rect(surface, self.color, pygame.locals.Rect(x, y, self.width, self.height))
        pygame.draw.rect(surface, self.color, pygame.locals.Rect(x + 2*self.width, y, self.width, self.height))

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
    STAFF_Y_OFFSET = 113                                                           
    def __init__(self, clef, staffLength, keySignature, beats = 4, noteValue = 4, notesList = [], color = colors.BLACK):
        self.notes = notesList
        self.clef = clef
        self.color = color                                                                                            
        self.timeSignature = TimeSignature(beats, noteValue, color)                               
        self._staff = Staff(staffLength)                                                                                                   

    def blit(self, surface, (x,y)):
        barline = OrdinaryBarline(self._staff.getHeight())
        self._staff.blit(surface, (x + 10, y + self.STAFF_Y_OFFSET))
        barline.blit(surface, (x + 10, y + self.STAFF_Y_OFFSET - self._staff.getHeight()))
        self.clef.blit(surface, (x + 20, y))
        self.timeSignature.blit(surface, (x + 80, y + 40))
        XOFFSET = 35
        x += 110                    
        time = 0                                    
        for i in self.notes:
            i.blit(surface, x, self._staff, self.clef)
            x += XOFFSET
            time += i.getDuration()
            if time == self.timeSignature.beats:
                time = 0
                x += XOFFSET / 2
                barline.blit(surface, (x, y + self.STAFF_Y_OFFSET - self._staff.getHeight()))
                x += XOFFSET / 2



