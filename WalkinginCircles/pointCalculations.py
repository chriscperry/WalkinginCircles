
#################################
#   Christopher Perry           #
#   4/13/16                     #
#                               #
#   Here are some useful        #
#   functions for confuzling    #
#   points in 3D!               #
#################################

import math

def getPoint(x,y,z,r,theta,tilt):
    pointx = (x + r  * math.cos(theta))
    pointy = (y + r  * math.sin(theta)/tilt + z)
    return (pointx,pointy)

def getDist(x1,y1,x2,y2):
    return ((x1-x2)**2+(y1-y2)**2)**.5

def getAngle(x1,y1,x2,y2):
    a = 0
    if (x1-x2) == 0:
        a = 0.0001
    slope = (y1-y2)/(x1-x2+a)
    if x2 < x1:
        return math.pi+(math.atan(slope))
    else:
        return (math.atan(slope))

def weightAvg(x,y,factor = 50,slices = 100):
    return (x * factor + y * (slices - factor)) // slices

def fadeColor(color1, color2, factor, slices = 100):
    #factor = factor % slices
    (r1,g1,b1) = color1
    (r2,g2,b2) = color2
    r = weightAvg(r1,r2,factor,slices) % 255
    g = weightAvg(g1,g2,factor,slices) % 255
    b = weightAvg(b1,b2,factor,slices) % 255
    return (r,g,b)

def make2dList(rows, cols, fill=0):
    a=[]
    for row in range(rows): a += [[fill]*cols]
    return a