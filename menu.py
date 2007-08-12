# -*- coding: latin-1 -*-
from pygame.color import Color
from setupoptions import setupOptions
import language
import pygame

class Menu:
    """Implements a menu with highlighting options"""
    def __init__(self, options, normalFont, selectedFont, margin = 0, normalColor = Color("white"), selectedColor = Color("white"), centered = True):
        self.selected = 0
        self.alternate = -1                         

        self._options = options
        self._centered = centered   # are items centered?

        self._selectedImages  = []
        self._normalImages    = []
        self._alternateImages = []
        
        self._margin = margin
        self._lineStep = 0      # stores the height of an item
        self._width = 0
        # generate images of text items and fill _selectedImages, _normalImages and _alternateImages lists
        for opt in self._options:
            selectedImages = []
            normalImages = []
            for i in range(len(language.languages)):
                sel = selectedFont.render(opt[i], True, selectedColor)
                normal = normalFont.render(opt[i], True, normalColor)
                selectedImages.append(sel)
                normalImages.append(normal)
                self._lineStep = max(max(sel.get_height(), normal.get_height()) + margin, self._lineStep)
                self._width = max(max(sel.get_width(), normal.get_width()), self._width)
            self._selectedImages.append(selectedImages)
            self._normalImages.append(normalImages)

        self.useMarker = False     # the marker is an image in front of the selected option
        self._markerImg = None

    def getOption(self, i):
        return self._options[i][setupOptions.language]

    def setMarker(self, img):
        self.useMarker = True
        self._markerImg = pygame.image.load(img).convert_alpha()

    def setAlternateFont(self, font, color):
        self._alternateImages = []
        for opt in self._options:
            alternateImages = []                                 
            for i in range(len(language.languages)):
                img = font.render(opt[i], True, color)
                alternateImages.append(img)
                self._lineStep = max(img.get_height() + self._margin, self._lineStep)
                self._width = max(img.get_width(), self._width)
            self._alternateImages.append(alternateImages)

    def get_height(self):
      return self._lineStep * len(self._options)

    def get_width(self):
      return self._width

    def blit(self, surface, (center_x, start_y)):
        """prints to screen"""
        for i in range(len(self._options)):
            if i == self.selected:
                img = self._selectedImages[i][setupOptions.language]
            elif i == self.alternate and len(self._alternateImages) > i:
                img = self._alternateImages[i][setupOptions.language]                                    
            else:                                     
                img = self._normalImages[i][setupOptions.language] 

            x = center_x
            if self._centered:                
                x -= img.get_width()/2

            y = start_y + self._lineStep * i - img.get_height()/2
            surface.blit(img, (x,y))
            # blit marker ?
            if i == self.selected and self.useMarker and self._markerImg is not None:
                y = start_y + self._lineStep * i - self._markerImg.get_height()/2
                surface.blit(self._markerImg, (x - self._markerImg.get_width() - 10, y))
            
    def next(self):
        """selects next item"""
        self.selected = (self.selected + 1) % len(self._options)
        
    def prev(self):
        """selects previous item"""
        self.selected = (self.selected - 1) % len(self._options)     
        
    def setItem(self, coords):
        """returns True if coords (x,y) corresponds to an item different from the currently selected one"""
        i = self._getItem(coords)
        if i is not None and  i != self.selected:
            self.selected = i
            return True        
        return False                                    
    
    def selectItem(self, coords):
        """returns index of menu corresponding to coords (x,y), or None"""
        i = self._getItem(coords)
        if i is not None:
            self.alternate = i
        return i      
            
    def _getItem(self, (x, y)):
        """returns index corresponding to coords (x,y), or None"""
        for i in range(len(self._options)):
            img = self._selectedImages[i][setupOptions.language]
                
            dx = -img.get_width()/2
            dy = self._lineStep * i - img.get_height()/2
            
            if dx <= x <= dx + img.get_width():
                if dy + 10 <= y <= dy + img.get_height() - 10:
                    return i
        return None
        

class OptionsMenu(Menu):
    """Implements a menu with highlighting options and with another column that holds different values"""
    COL_OFFSET = 50
    def __init__(self, options, values, normalFont, selectedFont, margin = 0, normalColor = Color("white"), selectedColor = Color("white")):
        Menu.__init__(self, options, normalFont, selectedFont, margin, normalColor, selectedColor, False)

        assert(len(options) == len(values))
        self._selectedValuesImages = []
        self._normalValuesImages   = []
        
        self._currentValues = len(options) * [0]
        self._values = values
        self._col1width = self._width
        # generate images of text items and fill _selectedImages and _normalImages lists
        width = 0
        for v in values:
            if v is not None:
                selectedValuesImages = []
                normalValuesImages = []
                for text in v:
                    selOpts = []
                    normalOpts = []
                    for i in range(len(language.languages)):
                        selOpts.append(selectedFont.render(text[i], True, selectedColor))
                        normalOpts.append(normalFont.render(text[i], True, normalColor))
                        width = max(max(selOpts[-1].get_width(), normalOpts[-1].get_width()), width)
                    selectedValuesImages.append(selOpts)
                    normalValuesImages.append(normalOpts)
                self._selectedValuesImages.append(selectedValuesImages)
                self._normalValuesImages.append(normalValuesImages)
            else:
                self._selectedValuesImages.append(None)
                self._normalValuesImages.append(None)
        self._col2width = width
        self._width = self._col1width + self.COL_OFFSET + self._col2width
        self._useIcons = False

    def addIcons(self, selectedIconsList, unselectedIconsList):
        """adds an icon for each option. 'iconsList' is a list of paths to each image"""        
        assert(len(self._options) == len(selectedIconsList) == len(unselectedIconsList))
        self._useIcons = True
        self._selectedIcons = []                             
        self._unselectedIcons = []                             
        width = 0                                                     
        for i in selectedIconsList:                             
            if i is not None:                                                                
                img = pygame.image.load(i).convert_alpha()
                width = max(width, img.get_width())
            else:
                img = None                
            self._selectedIcons.append(img)
        for i in unselectedIconsList:                             
            if i is not None:                                                                
                img = pygame.image.load(i).convert_alpha()
                width = max(width, img.get_width())
            else:
                img = None                
            self._unselectedIcons.append(img)
        self._col3width = width                                   
        self.width = self._col1width + self.COL_OFFSET + self._col2width + self.COL_OFFSET + self._col3width

    def blit(self, surface, (x,y)):
        """prints to screen"""
        Menu.blit(self, surface, (x,y))
        # blit columns                                       
        x += self._col1width + self.COL_OFFSET
        for i in range(len(self._options)):
            try:
                if i == self.selected:
                    img = self._selectedValuesImages[i][self._currentValues[i]][setupOptions.language]
                else:
                    img = self._normalValuesImages[i][self._currentValues[i]][setupOptions.language]
                yf = y + self._lineStep * i - img.get_height()/2
                surface.blit(img, (x, yf))
            except Exception, e:
                # ignore when img is None                                
                pass                                
            try:                
                # blit icons                                         
                if self._useIcons:                                         
                    if i == self.selected:
                        img = self._selectedIcons[i]
                    else:
                        img = self._unselectedIcons[i]
                    surface.blit(img, (x + self._col2width + self.COL_OFFSET, yf))
            except Exception, e:
                # ignore when img is None                                
                pass                                
            
    def changeOption(self, i, dir = pygame.K_RIGHT):
        """changes the second column"""
        try:           
            if dir == pygame.K_RIGHT:
                self._currentValues[i] = (self._currentValues[i] + 1) % len(self._values[i])
            elif dir == pygame.K_LEFT:
                self._currentValues[i] = (self._currentValues[i] - 1) % len(self._values[i])
        except Exception, e:
            # ignore None values                            
            pass                            
                                                                                      
    def getValueIndex(self, option):
        """returns the index corresponding to the value for option"""
        return self._currentValues[option]        

    def setValueIndex(self, option, index):
        """sets the index corresponding to the value for option"""
        self._currentValues[option] = index        

    def selectItem(self, coords):
        """returns index of menu corresponding to coords (x,y), or None"""
        i = self._getItem(coords)
        if i is not None:
            self.alternate = i
        return i      
            
    def _getItem(self, (x, y)):
        """returns index corresponding to coords (x,y), or None"""
        item = Menu._getItem(self, (x,y))
        if item is not None:
            return item

        for i in range(len(self._options)):
            try:
                img = self._normalValuesImages[i][self._currentValues[i]]
                    
                dy = self._lineStep * i - img.get_height()/2
                if 0 <= x <= self._width:
                    if dy + 10 <= y <= dy + img.get_height() - 10:
                        return i
            except Exception:
                # ignore if no values for option                             
                pass                             
        return None

