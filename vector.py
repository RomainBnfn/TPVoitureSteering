import math
ROOT2 = math.sqrt(2)

class Vector:

    def __init__(self, x, y=None):
        if type(x) == float:
            assert type(y) == float
            self.coord = (x , y)
        elif type(x) == tuple:
            self.coord = (x[0], x[1])
          
    def __getitem__(self, index: int):
        return self.coord[index]
    
    def _copy(self):
        return Vector(self[0], self[1])
    
    def _add(self, v2):
        self.coord = (self[0]+v2[0], self[1]+v2[1])
        return self
    
    def _diff(self, v2):
        self.coord = (self[0]-v2[0], self[1]-v2[1])
        return self
    
    def _scalarMult(self, s: float):
        self.coord = (self[0] * s, self[1] * s)
        return self
    
    def _approximateLength(self):
        _max = max(self[0], self[1])
        _min = min(self[0], self[1])
        if _max == 0:
            return 0
        ratio = _min/_max
        # Without pow or sqrt
        return _max * (1 + ratio * (ROOT2 - 1) )
    
    ## Static
            
    @staticmethod
    def diff(v1, v2):
        v1 = v1._copy()
        return v1._diff(v2)

    @staticmethod
    def add(v1, v2):
        v1 = v1._copy()
        return v1._add(v2)
    
    @staticmethod
    def scalarMult(v, s : float):
        v = v._copy()
        return v._scalarMult(s)
    
    @staticmethod
    def dot(v1, v2):
        return v1[0]*v2[0]+v1[1]*v2[1]
    
    @staticmethod
    def inter(scalar: float, v1, v2):
        v2 = v2._copy()
        v2._diff(v1)
        v2._scalarMult(scalar)
        return v2._add(v1)
    
    @staticmethod
    def approximateLength(v1):
        return v1._approximateLength()
    
    @staticmethod
    def approximateDistance(v1, v2):
        v1 = v1._copy()
        v1._diff(v2)
        return v1._approximateLength()