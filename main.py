from math import sqrt,degrees
from Point import Point
from Vector import Vector
from Cloud import Cloud
from Funcs import *
import matplotlib.pyplot as plt


# defining X and Y coordinates of the points
xlist = randList(100,100)
ylist = randList(100,100)

# Merging the coordinates in order to add them in just one
# function to the cloud of points
xylist = [xlist, ylist]
mycloud = Cloud([])
mycloud.addFromList(xlist,ylist)


# Calculate the convex hull of the cloud of points using the incremental method
convhull = mycloud.IncrConvexHull()


# --PLOTTING THE RESULTS--

# Transforms the list of points into a list of two
# lists of coordinates (X and Y)
xyhull = getxy(convhull)

# Adding again the first point to make the loop
xyhull[0].append(xyhull[0][0])
xyhull[1].append(xyhull[1][0])

# Storing the plot of:
# all points, the convex hull points and the line joining them, respectively
plt.plot(xylist[0],xylist[1],'ro')
plt.plot(xyhull[0],xyhull[1],'b-.')
plt.plot(xyhull[0],xyhull[1],'gs')
plt.show()
