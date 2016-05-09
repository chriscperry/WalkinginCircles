
#################################
#   Christopher Perry           #
#   4/13/16                     #
#                               #
#   Here be trees!              #
#   And all tree related        #
#   shenanigans and such        #
#################################

import math
import random
from time import process_time
from tkinter import *
from pointCalculations import *


def generateBirtch():
    r = random.random()
    return generateTree(2.8,15 + r * 3,math.pi,math.pi,r * 20 + 180,(.2,.35,2))

def generateMaple():
    size = 400
    while size > 300:# or size[0] + size [1] < 250:
        maple = generateTree(3,20,math.pi,math.pi,200,(.1,.8,.8))
        point = getTreeSize(maple)
        size = getDist(0,0,point[0],point[1])
    return maple

def generateSapling():
    r = random.random()
    return generateTree(3.2,2 + r * 3,math.pi,math.pi,r * 5 + 30 ,(.2,.5,5))

def generateOak():
    r = random.random()
    size = 400
    while size > 300:# or size[0] + size [1] < 250:
        oak = generateTree(2.5,18+r*3,math.pi,math.pi,r * 20 + 120,(.2,.6,5))
        point = getTreeSize(oak)
        size = getDist(0,0,point[0],point[1])
    return oak

def getTreeSize(tree,size = (0,0)):
    if type(tree) == tuple or type(tree[1]) == tuple or type(tree[2]) == tuple:
        return size#(tree[0],tree[1])
    return max(getTreeSize(tree[1],(size[0]+abs(tree[0][0]),
        size[1]+abs(tree[0][1]))),getTreeSize(tree[2],
        (size[0]+abs(tree[0][0]),size[1]+abs(tree[0][1]))))


def generateTree(depth, width, thetax, thetay, length, factor):
    # Factor: (width decrease, angle increase, length decrease)
    x = int(math.sin(thetax) * length) 
    y = int(math.sin(thetay) * length) 
    z = int(math.cos((thetay+thetax)/2) * length)
    branch = (x,y,z,int(width))
    (s1,s2) = (1,1)
    if random.randrange(30//(width+1)) == 0 and length > 10: s1 = 0
    if random.randrange(30//(width+1)) == 0 and length > 10: s2 = 0
    widthFactor = width / (1.5 + random.random())

    d = 1
    if depth % 2 == 0: d = -1

    if depth > 0:
        return [branch,
        generateTree(depth-s1, width - widthFactor + width*factor[0],
        thetay+random.random()*factor[1]*d, thetax+random.random()*factor[1],
        length*(factor[2]+random.random())/(factor[2]+1),factor),
        generateTree(depth-s2, widthFactor + width*factor[0],
        thetay-random.random()*factor[1]*d, thetax-random.random()*factor[1],
        length*(factor[2]+random.random())/(factor[2]+1),factor)]
    else:
        return branch
    # Tree organization: [(branch),[following branches],[]]
    # Branch: (x,y,z)

def getTreePoints(branch,data,board,base,treeTheta):
    (cx,cy,cz) = (1,1,1)
    (x,y,z,width) = branch
    r = getDist(cx,cy,x,y)
    # Angle is more complecated here because more realistic 3D
    angle = math.radians(data.theta) + (getAngle(x,y,cx,cy) + 
        getAngle(x,z,cx,cz) + getAngle(y,z,cy,cz)) / 3 + treeTheta
    # Duplicated from getMapPoints
    (pointx,pointy) = getPoint(base[0],base[1],z,r,angle,data.tilt)
    return (pointx,pointy,width)

def drawTree(canvas,data,board,tree,base,treeTheta,colorValue,growth):
    if type(tree[0]) == tuple:
        colorValue = fadeColor(colorValue,(0,0,0),98)
        color = "#%02x%02x%02x" % colorValue
        (x,y,width) = getTreePoints(tree[0],data,board,base,treeTheta)
        # Details: (Wind and overlap)
        x += (math.sin(process_time()*2+(x-y)/200)*2)#*(data.theta+100)/150)
        (x1,y1) =  (weightAvg(x,base[0],min(growth,110)),
                    weightAvg(y,base[1],min(growth,110)))
        # Draw lines
        try:
            canvas.create_line(base,(x1,y1),width = width,fill = color)
        # Draw the next branches
            if growth > 100:
                for n in range(len(tree)-1):
                    drawTree(canvas,data,board,tree[n+1],
                        (x,y),treeTheta,colorValue,growth-100)
        except:
            return None

def growTree(tree):
    if tree.grow == 1:
        tree.growth += 20
    if not 0 < tree.growth < 1000:
        tree.grow = 0

def expand(tree, factor = 1):
    if type(tree) != list:
        return None
    tree[0] = (tree[0][0]*(1+.005*factor),tree[0][1]*(1+.005*factor),
        tree[0][2]-1,tree[0][3]*(1+.01*factor))
    return [tree[0],expand(tree[1],factor),expand(tree[2],factor)]


