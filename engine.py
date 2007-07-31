from sounds import sounds

import pygame
import sys

DEBUG = False

class Game:
    def __init__(self, framerate = 30, title = None, icon = None):
        pygame.init()
        try:
            sounds.init()
        except Exception, e:
            print str(e)
            print "Could not initialize sounds: running with no sound."

        self.framerate = framerate   
        if title:
            pygame.display.set_caption(title) 

        if icon:
            icon = pygame.image.load(icon)
            pygame.display.set_icon(icon) 

        #self._xySize = pygame.display.list_modes()[1]
        xySize = pygame.display.list_modes()[1]
        #self.screen = pygame.display.set_mode(self._xySize)
        self.screen = pygame.display.set_mode(xySize, pygame.FULLSCREEN)
        #self.fullscreen = False
        self.clock = pygame.time.Clock()

        self.score = 0
        self.level = 0
        
    #def toggle_fullscreen(self):
        #if self.fullscreen:
            #self.screen = pygame.display.set_mode(self._xySize)
        #else:                                                                                  
            #self.screen = pygame.display.set_mode(self._xySize, pygame.FULLSCREEN)
        #self.fullscreen = not self.fullscreen                                                                                  

    def run(self, scene):
        scene.run()
        if DEBUG: print "FPS:", self.clock.get_fps()
        
    def tick(self):
        self.clock.tick(self.framerate)

   
        
class SceneExit(Exception):
    pass
    
class Scene:
    BG_COLOR = pygame.color.Color('white')
    
    @property 
    def background(self):
        if self._background is None:
            self._background = pygame.Surface(self.game.screen.get_size()).convert()
            self._background.fill(self.BG_COLOR)
        return self._background
        
    def __init__(self, game, *args, **kwargs):
        self.game = game
        self._background = None
        self.subscenes = []
        self.init(*args, **kwargs)
        
    def init(self): 
        pass
        
    def end(self, value = None):
        self.return_value = value
        raise SceneExit()
        
    def runScene(self, scene):
        ret = scene.run()
        if DEBUG: print "Left Scene", str(scene), "with", ret
        self.paint()
        return ret
        
    def run(self):
        if DEBUG: print "Entering Scene:", str(self)
        self.game.screen.blit(self.background, (0,0))
        for s in self.subscenes: 
            s.paint()
        self.paint()
        pygame.display.flip()
        while True:
            self.game.tick()
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                else:
                    try:
                        self.event(event)
                    except SceneExit:
                        return self.return_value
                    
            try:
                self.loop()
                for s in self.subscenes: 
                    s.loop()
            except SceneExit:
                return self.return_value

            for s in self.subscenes: 
                s.update()
            self.update()
            pygame.display.flip()
        
    def event(self, evt):
        pass
        
    def loop(self):
        pass
        
    def update(self):
        pass
        
    def paint(self):
        self.update()
     
