from constants import *
from vector import Vector
import pygame

class Track:
    _circuit = None
    _width = 30
    _screen = None
    _cachedLength = []
    _cachedNormals = []
    _out_points = []

    def __init__(self, screen, circuit = CIRCUIT):
        self._circuit = circuit
        self._screen = screen
        for i in range(0,len(self._circuit)):
            self._cachedNormals.append(Vector.diff(self._circuit[i], self._circuit[len(self._circuit)-1 if i-1 < 0 else i-1]))
            length = Vector.approximateLength(self._cachedNormals[i])
            self._cachedLength.append(length)
            self._cachedNormals[i] = (self._cachedNormals[i][0]/length if length != 0 else 0,
                                      self._cachedNormals[i][1]/length if length != 0 else 0)


    def _segmentPointAddLength(self, segment, point, length):
        ''' get the segment and point (on it) after adding length to the segment and point (on it), by following the
        path'''
        nextStep = Vector.approximateDistance(point, self._circuit[segment])
        if nextStep > length: # We stay on the same segment
            nextPoint = Vector.add(point, Vector.scalarMult(self._cachedNormals[segment], length))
            return (segment, (int(nextPoint[0]), int(nextPoint[1])))
        length -= nextStep
        segment = segment+1 if segment+1<len(self._circuit) else 0
        while length > self._cachedLength[segment]:
            length -= self._cachedLength[segment]
            segment = segment+1 if segment+1<len(self._circuit) else 0
        nextPoint = Vector.add(self._circuit[segment-1 if segment > 0 else len(self._circuit)-1],
                Vector.scalarMult(self._cachedNormals[segment], length))
        return (segment, (int(nextPoint[0]), int(nextPoint[1])))

    def _closestSegmentPointToPoint(self,point):
        bestLength = None
        bestPoint = None
        bestSegment = None
        for i in range(0, len(self._circuit)):
            p = self._closestPointToSegment(i,point)
            l = Vector.approximateDistance(p,point)
            if bestLength is None or l < bestLength:
                bestLength = l
                bestPoint = p
                bestSegment = i
        return (bestSegment, bestPoint, bestLength)

    def _closestPointToSegment(self, numSegment, point):
        ''' Returns the closest point on the circuit segment from point'''
        p0 = self._circuit[len(self._circuit)-1 if numSegment-1 < 0 else numSegment-1]
        p1 = self._circuit[numSegment]
        local = Vector.diff(point, p0)
        projection = Vector.dot(local, self._cachedNormals[numSegment])
        if projection < 0:
            return p0
        if projection > self._cachedLength[numSegment]:
            return p1
        return Vector.add(p0,Vector.scalarMult(self._cachedNormals[numSegment], projection))
    
    def out_position(self, coords):
        # When a vehicules cross the road
        canAdd = True
        for p in self._out_points:
            if Vector.approximateDistance(coords, p) < 8:
                canAdd = False
                break
        if canAdd:
            self._out_points.append(coords)

    def drawMe(self, scene = None):
        for p in self._circuit: # Draw simple inner joins
            pygame.draw.circle(self._screen, ROAD_COLOR ,p,int(self._width/2),0)
        for p in self._out_points:
            pygame.draw.circle(self._screen, ROAD_COLOR ,p,int(self._width/2),0)
        pygame.draw.lines(self._screen, ROAD_COLOR , True, self._circuit, self._width)
        pygame.draw.lines(self._screen, LINE_COLOR , True, self._circuit, 1)

        if True:
            for i,p in enumerate(self._circuit):
                pygame.draw.line(self._screen, (0,0,250), p, Vector.add(p,Vector.scalarMult(self._cachedNormals[i], 50)))