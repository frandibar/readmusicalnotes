import colors

class Menu:
    '''Implements a menu with highlighting options'''
    def __init__(self, normalFont, alternateFont, selectedFont, options, margin = 0, normalColor = colors.WHITE, selectedColor = colors.WHITE, alternateColor = colors.YELLOW, centered = True):
        self.selected = 0
        self.alternate = -1                         

        self._options = options
        self._centered = centered   # are items centered?

        self._selectedImages  = []
        self._normalImages    = []
        self._alternateImages = []
        
        self._lineStep = 0      # stores the height of an item
        self._width = 0
        # generate images of text items and fill _selectedImages, _normalImages and _alternateImages lists
        for text in self.options:
            sel = selectedFont.render(text, True, selectedColor)
            normal = normalFont.render(text, True, normalColor)
            altern = alternateFont.render(text, True, alternateColor)
            self._selectedImages.append(sel)
            self._normalImages.append(normal)
            self._alternateImages.append(altern)
            self._lineStep = max(max(max(sel.get_height(), normal.get_height()), altern.get_height()) + margin, self._lineStep)
            self._width = max(max(max(sel.get_width(), normal.get_width()), altern.get_width()), self._width)

    def get_height(self):
      return self._lineStep * len(self._options)

    def get_width(self):
      return self._width

    @property
    def options(self):
        return self._options

    def blit(self, surface, (center_x, start_y)):
        '''prints to screen'''
        for i in range(len(self.options)):
            if i == self.selected:
                img = self._selectedImages[i]
            elif i == self.alternate:
                img = self._alternateImages[i]                                     
            else:                                     
                img = self._normalImages[i]

            x = center_x
            if self._centered:                
                x -= img.get_width()/2

            y = start_y + self._lineStep * i - img.get_height()/2
            surface.blit(img, (x,y))
            
    def next(self):
        '''selects next item'''
        self.selected = (self.selected + 1) % len(self.options)
        
    def prev(self):
        '''selects previous item'''
        self.selected = (self.selected - 1) % len(self.options)     
        
    def setItem(self, coords):
        '''returns True if coords (x,y) corresponds to an item different from the currently selected one'''
        i = self._getItem(coords)
        if i is not None and  i != self.selected:
            self.selected = i
            return True        
        return False                                    
    
    def selectItem(self, coords):
        '''returns index of menu corresponding to coords (x,y), or None'''
        i = self._getItem(coords)
        if i is not None:
            self.alternate = i
        return i      
            
    def _getItem(self, (x, y)):
        '''returns index corresponding to coords (x,y), or None'''
        for i in range(len(self.options)):
            img = self._selectedImages[i]
                
            dx = -img.get_width()/2
            dy = self._lineStep * i - img.get_height()/2
            
            if dx <= x <= dx + img.get_width():
                if dy + 10 <= y <= dy + img.get_height() - 10:
                    return i
        return None
        
