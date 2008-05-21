#!/usr/bin/python
# -*- coding: latin-1 -*-

import colors
from resources import *
from score import *

import pygame
import pygame.locals



def blit(surface, (x,y)):

    notes = [
             QuarterNote('F',2), 
             QuarterNote('G',2), 
             QuarterNote('A',2), 
             QuarterNote('B',2), 
             QuarterNote('C',3), 
             QuarterNote('D',3), 
             QuarterNote('E',3), 
             QuarterNote('F',3), 
             QuarterNote('G',3), 
             QuarterNote('A',3), 
             QuarterNote('B',3), 
             QuarterNote('C',4),
             QuarterNote('D',4),
             QuarterNote('E',4),
             QuarterNote('F',4),
             QuarterNote('G',4),
             QuarterNote('A',4),
             QuarterNote('B',4),
             QuarterNote('C',5),
             QuarterNote('D',5)
                               ]

    notes = [
             WholeNote('C',3),
             WholeNote('D',3),
             WholeNote('E',3),
             WholeNote('F',3),
             WholeRest(),
             HalfRest(),
             QuarterRest(),
             QuarterRest(),
             #HalfNote('G',4),
             HalfNote('A',4),
             HalfNote('B',4),
             HalfNote('C',5),
             #HalfNote('F',2), 
             #HalfNote('G',2), 
             #HalfNote('A',2), 
             #HalfNote('B',2), 
             HalfNote('C',3), 
             QuarterNote('D',3), 
             QuarterNote('E',3), 
             QuarterNote('F',3), 
             HalfNote('G',3), 
             QuarterNote('A',3), 
             HalfNote('B',3), 
             HalfNote('C',4),
             HalfNote('D',4),
             HalfNote('E',4),
             HalfNote('F',4),
             HalfNote('G',4),
             HalfNote('A',4),
             HalfNote('B',4),
             HalfNote('C',5),
             HalfNote('D',5)
                               ]

    #notes = [
             #EighthNote('F',2), 
             #EighthRest(),
             #EighthNote('A',2), 
             #EighthNote('B',2), 
             #EighthNote('C',3), 
             #EighthNote('D',3), 
             #EighthNote('E',3), 
             #EighthNote('F',3), 
             #EighthNote('G',3), 
             #EighthNote('A',3), 
             #EighthNote('B',3), 
             #EighthNote('C',4),
             #EighthNote('D',4),
             #EighthNote('E',4),
             #EighthNote('F',4),
             #EighthNote('G',4),
             #EighthNote('A',4),
             #EighthNote('B',4),
             #EighthNote('C',5),
             #EighthNote('D',5)
                               #]
    #notes = [Chord([QuarterNote('C',3), QuarterNote('E',3), QuarterNote('G',3)])]
    #notes = [Chord([EighthNote('C',3), EighthNote('E',3), EighthNote('G',3)])]

    #score = ScoreBuilder(TrebleClef(), 800, KeySignature('C#M'), 1, 4, notes)
    score = ScoreBuilder(BassClef(), 800, KeySignature('CbM'), False, 1, 4, notes)
    #score = ScoreBuilder(BassClef(), 800, KeySignature('CM'), 1, 4, notes)
    score.blit(surface, (x,y))
    return                              

def main():
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('score builder test')

    # Fill background
    background = pygame.image.load(BACKGROUND_IMG).convert()

    # Display some text
    font = pygame.font.Font(None, 36)
    text = font.render("àñáEscala", 1, (10, 10, 10))
    textpos = text.get_rect()
    textpos.centerx = background.get_rect().centerx
    background.blit(text, textpos)

    #notes = [Chord([EighthNote('C',3), EighthNote('E',3), EighthNote('G',3)])]
    notes = [QuarterNote('C',3), QuarterNote('D',3), QuarterNote('E',3), QuarterNote('F',3), QuarterNote('G',3), QuarterNote('A',3), QuarterNote('B',3), QuarterNote('C',4), QuarterNote('D',4)]
    notes = [QuarterNote('C',4), QuarterNote('D',4), QuarterNote('E',4), QuarterNote('F',4), QuarterNote('G',4), QuarterNote('A',4), QuarterNote('B',4), QuarterNote('C',5), QuarterNote('D',5)]
    score = ScoreBuilder(TrebleClef(), 800, KeySignature('CM'), False, 1, 4, notes)
    #score = ScoreBuilder(BassClef(), 800, KeySignature('CM'), False, 1, 4, notes)
    img = score.getImage(screen.get_size())
    #img = pygame.transform.scale2x(img)

    # Blit everything to the screen
    screen.blit(background, (0,0))
    screen.blit(img, (0,0))
    pygame.display.flip()

    # Event loop
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        screen.blit(background, (0,0))
        screen.blit(img, (100,0))

        overlay = pygame.Surface((400, 100)).convert()                                                                                                                                                                                    
        overlay.fill(colors.DARK_RED)
        overlay.set_alpha(85)
        screen.blit(overlay, (0,400))
        pygame.display.flip()




if __name__ == '__main__': main()
