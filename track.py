from constants import *
from vector import Vector

class Track:
    _circuit = None
    _cback = (0,0,0)
    _cfore = (10,10,10)
    _width = 50
    _screen = None
    _cachedLength = []
    _cachedNormals = []

    def __init__(self, screen, circuit=CIRCUIT):
        self._circuit = circuit
        self._screen = screen
        for i in range(0,len(self._circuit)):
            v1 = Vector(self._circuit[i])
            v2 = Vector(self._circuit[len(self._circuit)-1 if i-1 < 0 else i-1])
            #
            self._cachedNormals.append(Vector.diff(v1, v2))
            #
            self._cachedLength.append(self._cachedNormals[i].approximateLength())
            #
            self._cachedNormals[i] = (self._cachedNormals[i][0]/self._cachedLength[i], 
                                      self._cachedNormals[i][1]/self._cachedLength[i] )


    def _segmentPointAddLength(self, segment, point, length):
        ''' get the segment and point (on it) after adding length to the segment and point (on it), by following the
        path'''
        nextStep = approximateDistance(point, self._circuit[segment])
        if nextStep > length: # We stay on the same segment
            nextPoint = vecAdd(point, vecScalarMult(self._cachedNormals[segment], length))
            return (segment, (int(nextPoint[0]), int(nextPoint[1])))
        length -= nextStep
        segment = segment+1 if segment+1<len(self._circuit) else 0
        while length > self._cachedLength[segment]:
            length -= self._cachedLength[segment]
            segment = segment+1 if segment+1<len(self._circuit) else 0
        nextPoint = vecAdd(self._circuit[segment-1 if segment > 0 else len(self._circuit)-1],
                vecScalarMult(self._cachedNormals[segment], length))
        return (segment, (int(nextPoint[0]), int(nextPoint[1])))

    def _closestSegmentPointToPoint(self,point):
        bestLength = None
        bestPoint = None
        bestSegment = None
        for i in range(0, len(self._circuit)):
            p = self._closestPointToSegment(i,point)
            l = approximateDistance(p,point)
            if bestLength is None or l < bestLength:
                bestLength = l
                bestPoint = p
                bestSegment = i
        return (bestSegment, bestPoint, bestLength)

    def _closestPointToSegment(self, numSegment, point):
        ''' Returns the closest point on the circuit segment from point'''
        p0 = self._circuit[len(self._circuit)-1 if numSegment-1 < 0 else numSegment-1]
        p1 = self._circuit[numSegment]
        local = vecDiff(point, p0)
        projection = vecDot(local, self._cachedNormals[numSegment])
        if projection < 0:
            return p0
        if projection > self._cachedLength[numSegment]:
            return p1
        return vecAdd(p0,vecScalarMult(self._cachedNormals[numSegment], projection))

    def drawMe(self, scene = None):

        for p in self._circuit: # Draw simple inner joins
            pygame.draw.circle(self._screen,self._cback,p,int(self._width/2),0)

        pygame.draw.lines(self._screen, self._cback, True, self._circuit, self._width)
        #
        pygame.draw.lines(self._screen, (255, 255, 255), True, self._circuit, 1)

        if True:
            for i,p in enumerate(self._circuit):
                pygame.draw.line(self._screen, (0,0,250), p, vecAdd(p,vecScalarMult(self._cachedNormals[i], 50)))

        # if scene is not None:
        #     for i,p in enumerate(self._circuit):
        #         scene.drawText(str(int(self._cachedLength[i])), p)
