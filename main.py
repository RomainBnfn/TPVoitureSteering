import sys, math
import time
from threading import Thread, current_thread

from scene import Scene
from track import Track
from vehicule import Vehicule
from vector import Vector
from constants import *

class SetOfVehicules:
    _vehicules = []

    def handleCollisions(self):
        " Simple collision checking. Not a very good one, but may do the job for simple simulations"
        for i,v1 in enumerate(self._vehicules):
            for v2 in self._vehicules[i+1:]:
                offset = Vector.diff(v2._coords, v1._coords)
                al = approximateLength(offset)
                if al != 0 and al < v1._radius + v2._radius - 1: # collision
                        v1._coords=(int(v1._coords[0]+offset[0]/al*(v1._radius+v2._radius)),
                                    int(v1._coords[1]+offset[1]/al*(v1._radius+v2._radius)))

                        v2._coords = (int(v2._coords[0] - offset[0] / al * (v2._radius + v1._radius)),
                              int(v2._coords[1] - offset[1] / al * (v2._radius + v2._radius)))

    def updatePositions(self):
        for v in self._vehicules:
            v._speed = Vector.add(v._speed, v._force)
            l = approximateLength(v._speed)
            if l > v._maxspeed:
                v._speed = Vector.scalarMult(v._speed, v._maxspeed / l)
            v._coords= (v._coords[0]+int(v._speed[0]), v._coords[1]+int(v._speed[1]))

    def append(self,item):
        self._vehicules.append(item)

    def drawMe(self, screen, scene = None):
        for v in self._vehicules: v.drawMe(screen)

def main():
    scene = Scene()
    done = False
    clock = pygame.time.Clock()
    while done == False:
        clock.tick(20)
        scene.update()
        scene.drawMe()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: done=True
            if event.type == pygame.KEYDOWN: done=True
            if event.type == pygame.MOUSEBUTTONDOWN:
                scene.eventClic(event.dict['pos'],event.dict['button'])
            elif event.type == pygame.MOUSEMOTION:
                scene.recordMouseMove(event.dict['pos'])

    pygame.quit()

if not sys.flags.interactive: main()

