
# A very simple class that stores an X and an Y values
class Point:
    # Constructor
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init

    # Changes the position by the given X and Y coordinates
    def shift(self, x, y):
        self.x += x
        self.y += y

    # Representation of the Point class
    def __repr__(self):
        return "".join(["Point(", "{0:.2f}".format(self.x), ",", "{0:.2f}".format(self.y), ")"])
