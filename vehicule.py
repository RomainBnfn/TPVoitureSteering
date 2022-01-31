from vector import Vector
from constants import *
from threading import Thread, current_thread
#import time
import pygame
from math import cos, atan, sin

# Handles Vehicules
class Vehicule:
    _coords = (0,0)   # vector
    _speed = (2,4)    # vector
    _maxspeed = 20 
    _force = (0,0)  # accelerating force
    _maxforce = 10
    _color = (200,100,100)
    _colorfg = tuple([int(c/2) for c in _color])
    _seeInFuture = 3

    def __init__(self, coords=(0,0), speed=(1,1), force =(1,1), color=(200,100,100)):
        self.setRandomColor()
        self._colorfg = tuple([int(c / 2) for c in self._color])
        self._radius = rd.randint(MIN_VEHICULE_SIZE, MAX_VEHICULE_SIZE)
        self._coords = coords
        self._speed = speed
        self._force = force

    def setRandomColor(self):
        r = rd.randint(0, 255)
        g = rd.randint(0, 255)
        b = rd.randint(0, 255)
        self._color = (r, g, b)


    def position(self): return self._pos

    def steerUpdate(self, track, vehicules):
        self._force = (0,0)
        self._force = Vector.add(self._force, self.steerPathFollow(track))
        self.steerSeparation(vehicules)

    def steerPathFollow(self, track):
        (s,p,l) = track._closestSegmentPointToPoint(self._coords)
        init_force = (0, 0)
        if l > ROAD_SIZE/2 :
            # Too far from the middle of the track
            init_force = Vector.diff(p, self._coords)
            # Out of the road --> Addapt the road
            track.out_position(self._coords)
        (sf, futurePosition) = track._segmentPointAddLength(s, p, max(10, Vector.approximateLength(self._speed)) * self._seeInFuture) 
        # We just have to register a force to get to futurePosition !
        force = Vector.diff(futurePosition, self._coords)
        #force = Vector.add(force, init_force)
        force = Vector.scalarMult( force, 
                                self._maxforce / Vector.approximateLength(force) if Vector.approximateLength(force) > 0.5 else self._maxforce )
        return force

    def steerSeparation(self, vehicules):
        forceAccu = (0,0) # starts with a fresh force
        for i, v in enumerate(vehicules._vehicules):
            if v is not self:
                pass


    def drawMe(self, screen):
        pygame.draw.circle(screen,self._color,   self._coords,self._radius,0)
        pygame.draw.circle(screen,self._colorfg, self._coords,self._radius,1)


class SetOfVehicules:
    _vehicules = []

    def get_new_coord(self, v1, v2, correctDist, realDist):
        # We could have took in consideration the weigth of each vehicule (throug radius)
        (x1, y1) = v1
        (x2, y2) = v2
        if realDist >= correctDist:
            return x1, y1, x2, y2
        #Thales theorem 
        x, y = abs(x1-x2), abs(y1-y2)
        if x == 0:
            dX = 0
            dY = (correctDist - y)/2
        else:
            angle = atan(y/x)
            dX = (cos(angle) * correctDist - x)/2
            dY = (sin(angle) * correctDist - y)/2
        # Correct sign
        s = -1
        if(x1<x2):
            s = 1
        x1 -= dX * s
        x2 += dX * s
        s = -1
        if(y1<y2):
            s = 1
        y1 -= dY * s
        y2 += dY * s
        return x1, y1, x2, y2
            
    def handleCollisions(self):
        for i,v1 in enumerate(self._vehicules):
            for v2 in self._vehicules[i+1:]:
                diff = Vector.diff(v2._coords, v1._coords)
                dist = Vector.approximateLength(diff)
                if dist < v1._radius + v2._radius:
                    # Collision
                    x1, y1, x2, y2 = self.get_new_coord(v1._coords, v2._coords, v1._radius + v2._radius, dist) 
                    v1._coords=(x1, y1)
                    v2._coords=(x2, y2)

    def updatePositions(self):
        for v in self._vehicules:
            v._speed = Vector.add(v._speed, v._force)
            l = Vector.approximateLength(v._speed)
            if l > v._maxspeed:
                v._speed = Vector.scalarMult(v._speed, v._maxspeed / l)
            v._coords= (v._coords[0]+int(v._speed[0]), v._coords[1]+int(v._speed[1]))

    def append(self,item):
        self._vehicules.append(item)

    def drawMe(self, screen, scene = None):
        for v in self._vehicules: v.drawMe(screen)
