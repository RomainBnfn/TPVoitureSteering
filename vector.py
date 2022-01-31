import math
from os import stat
ROOT2 = math.sqrt(2)

class Vector:

    @staticmethod
    def diff(v1, v2):
        return (v1[0]-v2[0], v1[1]-v2[1])

    @staticmethod
    def add(v1, v2):
        return (v1[0]+v2[0], v1[1]+v2[1])
    
    @staticmethod
    def scalarMult(v, s : float):
        return (v[0] * s, v[1] * s)
    
    @staticmethod
    def dot(v1, v2):
        return v1[0]*v2[0]+v1[1]*v2[1]
    
    @staticmethod
    def inter(scalar: float, v1, v2):
        diff = Vector.diff(v2, v1)
        diff = Vector.scalarMult(diff, scalar)
        return Vector.add(diff, v1)
    
    @staticmethod
    def approximateLength(v):
        _max = max( abs(v[0]), abs(v[1]))
        _min = min( abs(v[0]), abs(v[1]))
        if _max == 0:
            return 0
        ratio = _min/_max
        # Without pow or sqrt
        return _max * (1 + ratio * (ROOT2 - 1) )
    
    @staticmethod
    def approximateDistance(v1, v2):
        diff = Vector.diff(v1, v2)
        return Vector.approximateLength(diff)