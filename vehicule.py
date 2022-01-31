from vector import Vector
from constants import *

# Handles Vehicules
class Vehicule:
    _coords = (0,0)   # vector
    _speed = (2,4)    # vector
    _maxspeed = 20 
    _force = (0,0)  # accelerating force
    _maxforce = 10
    _seeInFuture = 3

    def __init__(self, coords=(0,0), speed=(1,1), force =(1,1)):
        self.setRandomColor()
        self._colorfg = tuple([int(c / 2) for c in self._color])
        self._radius = rd.randint(6, 30)
        self._coords = coords
        self._speed = speed
        self._force = force
        t = Thread(target=self.threadRandomColor)
        t.run()

    def setRandomColor(self):
        r = rd.randint(0, 255)
        g = rd.randint(0, 255)
        b = rd.randint(0, 255)
        self._color = (r, g, b)

    def threadRandomColor(self):
        while True:
            self.setRandomColor()
            time.sleep(500)

    def position(self): return self._pos

    def steerUpdate(self, track, vehicules):
        self._force = (0,0)
        self._force = Vector.add(self._force, self.steerPathFollow(track))
        #steerSeparation(self, vehicules)

    def steerPathFollow(self, track):
        (s,p,l) = track._closestSegmentPointToPoint(self._coords)
        # TODO: We should first add a force if l is too large (too far from the middle of the track) 
        # This is the future position
        (sf, futurePosition) = track._segmentPointAddLength(s, p, max(10,approximateLength(self._speed)) * self._seeInFuture) 
        # We just have to register a force to get to futurePosition !
        force = Vector.diff(futurePosition, self._coords)
        force = Vector.scalarMult(force,self._maxforce/approximateLength(force))
        return force

    def steerSeparation(self, vehicules):
        forceAccu = (0,0) # starts with a fresh force
        # for v in vehicules:
        #     if v is not self:


    def drawMe(self, screen):
        pygame.draw.circle(screen,self._color,   self._coords,self._radius,0)
        pygame.draw.circle(screen,self._colorfg, self._coords,self._radius,1)
