from pygame.color import Color
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
        for text in self._options:
            sel = selectedFont.render(text, True, selectedColor)
            normal = normalFont.render(text, True, normalColor)
            self._selectedImages.append(sel)
            self._normalImages.append(normal)
            self._lineStep = max(max(sel.get_height(), normal.get_height()) + margin, self._lineStep)
            self._width = max(max(sel.get_width(), normal.get_width()), self._width)

        self.useMarker = False     # the marker is an image in front of the selected option
        self._markerImg = None

    def getOption(self, i):
        return self._options[i]

    def setMarker(self, img):
        self.useMarker = True
        self._markerImg = pygame.image.load(img).convert_alpha()

    def setAlternateFont(self, font, color):
        self._alternateImages = []
        for text in self._options:
            img = font.render(text, True, color)
            self._alternateImages.append(img)
            self._lineStep = max(img.get_height() + self._margin, self._lineStep)
            self._width = max(img.get_width(), self._width)

    def get_height(self):
      return self._lineStep * len(self._options)

    def get_width(self):
      return self._width

    def blit(self, surface, (center_x, start_y)):
        """prints to screen"""
        for i in range(len(self._options)):
            if i == self.selected:
                img = self._selectedImages[i]
            elif i == self.alternate and len(self._alternateImages) > i:
                img = self._alternateImages[i]                                     
            else:                                     
                img = self._normalImages[i]

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
            img = self._selectedImages[i]
                
            dx = -img.get_width()/2
            dy = self._lineStep * i - img.get_height()/2
            
            if dx <= x <= dx + img.get_width():
                if dy + 10 <= y <= dy + img.get_height() - 10:
                    return i
        return None
        

class OptionsMenu(Menu):
    """Implements a menu with highlighting options and with another column that holds different values"""
    COL2_OFFSET = 50
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
        for opts in values:
            if opts is not None:
                selOpts = []
                normalOpts = []
                for text in opts:
                    selOpts.append(selectedFont.render(text, True, selectedColor))
                    normalOpts.append(normalFont.render(text, True, normalColor))
                    width = max(max(selOpts[-1].get_width(), normalOpts[-1].get_width()), width)
                self._selectedValuesImages.append(selOpts)
                self._normalValuesImages.append(normalOpts)
            else:
                self._selectedValuesImages.append(None)
                self._normalValuesImages.append(None)
        self._width += width + self.COL2_OFFSET

    def blit(self, surface, (x,y)):
        """prints to screen"""
        Menu.blit(self, surface, (x,y))
        # blit second column                                       
        x += self._col1width + self.COL2_OFFSET
        for i in range(len(self._options)):
            try:
                if i == self.selected:
                    img = self._selectedValuesImages[i][self._currentValues[i]]
                else:
                    img = self._normalValuesImages[i][self._currentValues[i]]
                yf = y + self._lineStep * i - img.get_height()/2
                surface.blit(img, (x,yf))
            except Exception, e:
                # ignore when img is None                                
                pass                                
            
    def changeOption(self, i, dir = pygame.K_RIGHT):
        """changes the second column"""
        if dir == pygame.K_RIGHT:
            self._currentValues[i] = (self._currentValues[i] + 1) % len(self._values[i])
        elif dir == pygame.K_LEFT:
            self._currentValues[i] = (self._currentValues[i] - 1) % len(self._values[i])
                                                                                      
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
                #if 0 <= x <= self._selectedImages[i].get_width() + self.COL2_OFFSET + img.get_width():
                print self._width
                if 0 <= x <= self._width:
                    if dy + 10 <= y <= dy + img.get_height() - 10:
                        return i
            except Exception:
                # ignore if no values for option                             
                pass                             
        return None

