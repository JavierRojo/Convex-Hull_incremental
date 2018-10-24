from math import sqrt, acos
from random import random

# Document that has most of the functions related with different classes:

# Function that generates a list full of random numbers in
# the range from 0 to factor
def randList(n,factor):
    L=list()
    for i in range(n):
        L.append(random()*factor)
    return L


# Function that calculates the distance between 2 given points
def distance(a, b):
    return sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

# Function that calculates the dotproduct between 2 given vectors
def dotprod(v1, v2):
    v1t = v1.center()
    v2t = v2.center()
    return (v1t.pf.x * v2t.pf.x + v1t.pf.y * v2t.pf.y)

# Funciton that calculates the angle between 2 vectors given the dot product
def angleVecs(v1, v2):
    cosalpha = dotprod(v1,v2) / (v1.module() * v2.module())
    return (acos(cosalpha))


def getxy(points):
    lx=list()
    ly=list()
    for p in points:
        lx.append(p.x)
        ly.append(p.y)
    return([lx,ly])

# Function that returns the double of the area (with sign) between three points
def Area2(pa, pb, pc):
    return (
    ((pb.x-pa.x)*(pc.y-pa.y))-((pc.x-pa.x)*(pb.y-pa.y))
    )

# Function that returns True if the third point is strictly at the 'Left' of the
# vector defined by the two first ones
def Left(pa, pb, pc):
    return Area2(pa,pb,pc)>0

# Function that returns True when the third point in in the same straight lines
# as the two first ones
def collinear(pa, pb, pc):
    return Area2(pa, pb, pc)==0

# Function that returns True when the third point is at the 'Left' of the
# vector defined by the two firsts or if it is collinear.
def Lefton(pa, pb, pc):
    return Area2(pa,pb,pc)>=0


# Function that returns True if the third point is right between the other two
# When being at the critical point of pa=pc or pb=pc then it returns False
def between(pa,pb,pc):
    # If they are not collinear it will never be posible
    if not collinear( pa, pb, pc ):
      return  False

    # If they are not vertical, then we focus on the x coordinate
    if pa.x !=pb.x:
      return ((pa.x < pc.x) and (pc.x < pb.x)) or ((pa.x > pc.x) and (pc.x > pb.x))

    # Else (vertical) we focus on the y coordinate
    else:
      return ((pa.y < pc.y) and (pc.y < pb.y)) or ((pa.y > pc.y) and (pc.y > pb.y))


# Function that checks if, from a given point p, there are any point in the list
# called tgpoints that is collinear to another. In this case, the closest point
# to p will be deleted. Although not opitmized, the normal tgpoints size is 2,
# and the maximum that it will usually receive is a tgpoints list of 4 elements
def checkcolls(tgpoints,p):
    # The most common case of use is a list with just two points that are not
    # collinear. This if-else statement can save a lot of computational cost
    if len(tgpoints)==2:
        return tgpoints
    else:
        ended=False
        while not ended:
            # First we assume that there will be no collinear points
            ended=True

            # For each point of the list, we compare it with the other tgpoints
            # that have not been compared yet.
            for i in range(len(tgpoints)):
                for j in range(i+1, len(tgpoints)):
                    # if collinearity is found, then the closest of the two
                    # points to p must be deleted. Also, the flag is risen
                    if collinear(p,tgpoints[i],tgpoints[j]):
                        ended=False
                        if distance(p,tgpoints[i])<distance(p,tgpoints[j]):
                            tgpoints.remove(tgpoints[i])
                        else:
                            tgpoints.remove(tgpoints[j])
                        break # breaks j loop
                if not ended:
                    break # breaks i loop and restarts the while loop
            else:
                # if there i loop finished without a break, no collinear points
                # were found and so it is time to return the list
                return tgpoints
    return tgpoints


# Function that checks if a point is inside a polygon/hull described by a list
# of points.
def checkinside(Hull,p):
    # Checks wether if p is part of an edge.
    for i in range(0,len(Hull)):
        if between(Hull[i-1],Hull[i],p):
            return True

    # In any other case, more common, then we set a sign based on the vector
    # that closes the polygonal loop
    referencesign = Lefton(p,Hull[-1],Hull[0])

    # Checks that for all other segments the sign is the same
    for i in range(len(Hull)-1):
        # If the sign is not the same for any of them, then the point is outside
        if Lefton(p,Hull[i],Hull[i+1]) != referencesign:
            return False

    # If the code gets to this point, it means all of them had the same sign
    return True


# Function that adds a new point to a convex hull, deleting the points of the
# old hull that end up inside the new one.
def addPoint2Hull(Hull,candidate):
    # If the point introduced was inside the Hull then it is returned
    if checkinside(Hull,candidate):
        return (Hull)
    # tgpoints are the anchors to which the new point will be connected. this
    # means the tangent points.
    tgpoints=list()

    #insiders will store the points of the old hull that get inside the new one
    insiders=list()

    # The tangent points of a convex polygon will meet the condition that
    # the adjacent points will be left at the same side of the vector
    # candidate->tgpoint
    for p in range(len(Hull)):
        # For the special case of the last point of the list, it must be
        # compared with the first one
        if p ==len(Hull)-1:
            samedir = Lefton(candidate,Hull[p],Hull[p-1]) == Lefton(candidate,Hull[p],Hull[0])

        # In any other case it is just compared with the next one
        else:
            samedir = Lefton(candidate,Hull[p],Hull[p-1]) == Lefton(candidate,Hull[p],Hull[p+1])

        if samedir:
            tgpoints.append(Hull[p])


    # Once we have the tangenpoints, we delete those that are collinear, as in
    # some cases more than 2 tangents may be detected
    tgpoints=checkcolls(tgpoints,candidate)

    # The new section of the polygon is defined
    newtriangle = [candidate,tgpoints[0],tgpoints[1]]

    # Old points inside this new section must be deleted in order to keep the
    # polygon coherent
    for p in Hull:
        if checkinside(newtriangle,p) and p not in newtriangle:
            insiders.append(p)

    # If there are any insiders, the new point will take their place
    # pos will store the position where the new point will be inserted
    if len(insiders)>0:
        pos = Hull.index(insiders[0])
    else:
        # If no insiders were found, then if the new point ends up between
        # the first (index 0) and the last (index m) points of the list
        # then it will be placed at the beginning
        if abs(Hull.index(tgpoints[0])-Hull.index(tgpoints[1]))>1:
            pos = 0

        # When it is between two sucesive points,
        # then it will go just between them
        else:
            pos=max(Hull.index(tgpoints[0]),Hull.index(tgpoints[1]))

    # The new point is inserted in the hull
    Hull.insert(pos,candidate)

    # Insiders are removed from the hull
    for p in insiders:
        Hull.remove(p)

    return(Hull)
