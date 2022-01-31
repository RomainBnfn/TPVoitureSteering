import imp
from constants import *
import pygame
import pygame.draw
from track import Track
from vehicule import Vehicule, SetOfVehicules

class Scene:
    _track= None
    _vehicules = None
    _screen = None
    _font = None

    _mouseCoords = (0,0)

    def __init__(self, screenSize = SCREEN_SIZE):
        pygame.init()
        self._screen = pygame.display.set_mode(screenSize)
        self._track = Track(self._screen)
        self._vehicules = SetOfVehicules()
        #self._font = pygame.font.SysFont('Arial', 25)

    def drawMe(self):
        self._screen.fill((0,0,0))
        self._track.drawMe(scene = self)
        self._vehicules.drawMe(self._screen, scene = self)

        # Illustrate the closestSegmentPointToPoint function
        (s,p,l) = self._track._closestSegmentPointToPoint(self._mouseCoords)
        pygame.draw.line(self._screen, (128,255,128),p, self._mouseCoords)
        #print(self._track._segmentPointAddLength(s,p,150))
        pygame.draw.circle(self._screen, (128,255,128),self._track._segmentPointAddLength(s,p,150)[1],20,1)

        pygame.display.flip()

    def drawText(self, text, position, color = (255,128,128)):
        self._screen.blit(self._font.render(text,1,color),position)

    def update(self):
        for v in self._vehicules._vehicules:
            v.steerUpdate(self._track, self._vehicules)
        self._vehicules.updatePositions()
        self._vehicules.handleCollisions()
        self.drawMe()

    def eventClic(self,coord,b):
        print("Adding Vehicule at ",coord[0],",",coord[1])
        self._vehicules.append(Vehicule((coord[0],coord[1])))
        
    def recordMouseMove(self, coord):
        self._mouseCoords = coord
