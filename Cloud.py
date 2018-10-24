from Funcs import checkinside, addPoint2Hull
from Point import Point

# Debug:
# from Funcs import getxy
# import matplotlib.pyplot as plt

# This class represents a cloud of points, represented by a list of points
# although the order in the list has no relevance for the cloud
class Cloud:
    # Constructor
    def __init__(self,plist):
        self.VertexList = plist

    # Represents all the points forming the list
    def __repr__(self):
        descr = "".join(["Cloud of ",str(len(self.VertexList))," points"])
        points = ""
        for pi in self.VertexList:
            points = points + str(pi) + "\n"
        return "---\n" + descr + ":\n" + points + "---"

    # Adds a point to the inner list
    def addPoint2Cloud(self,p):
        self.VertexList.append(p)

    # Adds a series of points given by two lists: one with the X coordinate
    # and another with the Y coordinate
    def addFromList(self,xlist,ylist):
            # First, we check for the length of the lists being the same
            if len(xlist) != len(ylist):
                raise ValueError('xlist and ylist must be same length')
            else:
                points=list()
                # All the elements are added in the form of new points
                for i in range(len(xlist)):
                    self.VertexList.append(Point(xlist[i],ylist[i]))

    # Returns the convex hull calculated with the incremental method
    def IncrConvexHull(self):
        # If the cloud of points is less than four points, it can only be convex
        if len(self.VertexList) <=3:
            Hull = self.VertexList

        else:
            # At the begining, the Hull is empty and the points not evaluated
            # points take the whole list.
            noteval = self.VertexList
            Hull = list()

            # As the points of the cloud are randomly positioned, this indexed
            # selection just works as a random selection
            Hull = self.VertexList[0:3]
            noteval = noteval[3:len(noteval)]

            # All the inner points inside the initial triangle are deleted in
            # order to save computational cost later
            for p in noteval:
                if checkinside(Hull,p):
                    # The point is completely removed, as it could never
                    # bee part of the final convex hull
                    noteval.remove(p)

            # while there are elements in noteval, the first one will be taken
            # as a candidate point in order to extend the convex hull.
            while len(noteval)>0:
                #take the first point of the non evaluated
                candidate = noteval[0]
                noteval.pop(0)

                # Generate new convex hull. If by any chance the candidate is
                # inside the hull then the hull is returned as it is. This can
                # be due to an error when identifying if a point is in or out.
                Hull = addPoint2Hull(Hull,candidate)

                # Checks for the rest of the points in order to remove them in
                # case they end up inside the new convex hull
                for p in noteval:
                    if checkinside(Hull,p):
                        noteval.remove(p)

                # Warning: For some reason, executing the command just once
                # makes python skip some points or misscalculate them.
                #
                # Debug: use these lines to plot the temporary convex hull:
                #
                # xynotev = getxy(noteval)
                # xyhull = getxy(Hull)
                # xylist = getxy(self.VertexList)
                # xyhull[0].append(xyhull[0][0])
                # xyhull[1].append(xyhull[1][0])
                #
                # plt.plot(xylist[0],xylist[1],'ro')
                # plt.plot(xynotev[0],xynotev[1],'go')
                # plt.plot(xyhull[0],xyhull[1],'b-.')
                # plt.plot(xyhull[0],xyhull[1],'bs')
                # plt.show()
                #
        return Hull
