import sys

from scene import Scene
from constants import *

import pygame

def main():
    scene = Scene()
    done = False
    clock = pygame.time.Clock()
    while done == False:
        clock.tick(20)
        scene.update()
        scene.drawMe()
        for event in pygame.event.get():
            #if event.type == pygame.QUIT: done=True
            #if event.type == pygame.KEYDOWN: done=True
            if event.type == pygame.MOUSEBUTTONDOWN:
                scene.eventClic(event.dict['pos'],event.dict['button'])
            elif event.type == pygame.MOUSEMOTION:
                scene.recordMouseMove(event.dict['pos'])

    pygame.quit()

if not sys.flags.interactive: main()

