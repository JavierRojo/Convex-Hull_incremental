from Funcs import *
from Point import Point

# A very simple class that stores two points:
# the origin and the end of the vector
# This way the direction and the sense are stored
# Although not used in the final script, it may be helpful
class Vector:
    # Constructor of the class
    def __init__(self,p1,p2):
        self.pi=p1
        self.pf=p2

    # Returns the module of the vector
    def module(self):
        return distance(self.pf,self.pi)

    # In order to make some calculations easier, the vector return the value of
    # the end point when the origin is set to the (0,0)
    def center(self):
        return Vector(Point(0,0), Point(self.pf.x-self.pi.x, self.pf.y-self.pi.y))

    # Representation of the Vector class
    def __repr__(self):
        return "".join(["Vector[", str(self.pi), ",", str(self.pf), "]"])
