
#################################
#   Christopher Perry           #
#   4/21/16                     #
#                               #
#   wisObjectClasses            #
#   Just the object classes     #
#   for Walking in Circles      #
#################################

import math
import random
from characterModels import *
from pointCalculations import *
from threeDeeTrees import *


class Board(object):
    def __init__(self, colors, size):
        self.color = colors
        self.rows = size
        self.cols = size
        self.tile = 100
        self.theta = 0
        self.heights = make2dList(self.rows+1, self.cols+1)
        self.objects = populateBoard(self.rows,self.cols,None,20)

class Forest(Board):
    def __init__(self, colors, treeFeq = 20, size = 6, 
                    path = True, npc = None, objects = None,
                    portal = True, sapling = False):
        super().__init__(colors, size)
        for x in range(len(self.heights)):
            for y in range(len(self.heights[x])):
                self.heights[x][y] =  (math.sin(x)*math.cos(y/3)
                                    *random.randrange(20,40)-20+
                                    random.randrange(-30,0))
        
        if objects == None:
            self.objects = generateForest(populateBoard(
                        self.rows,self.cols,Tree(),treeFeq),npc,portal,sapling)
        else:
            self.objects = objects

class Tree(object):
    def __init__(self, flavor = None, spire = 0):

        self.type = flavor
        if self.type == None:
            tree = random.randrange(4)
            self.type = ["Birtch","Birtch","Maple","Oak"][tree]
        
        if self.type == "Sapling":
            self.tree = generateSapling()
        elif self.type == "Birtch":
            self.tree = generateBirtch()             
        elif self.type == "Maple":
            self.tree = generateMaple()
        elif self.type == "Oak":
            self.tree = generateOak()

        self.spire = spire
        self.theta = random.random() * math.pi * 2
        self.growth = 1000 #Depth = growth / 100, percent = growth%100
        self.grow = 0
        self.growTime = 0

    def get(self):
        return self.tree

    def startGrow(self):
        self.grow = 1
        self.growth = 0


class Player(object):
    def __init__(self, row = 0, col = 0,theta = 90):
        self.row = row
        self.col = col
        self.lastRow = row
        self.lastCol = col
        self.theta = theta
        self.drawTheta = 0
        self.moving = False
        self.color = "silver"
        self.position = (0,0)

class Line(object):
    def __init__(self, speaker, line):
        self.speaker = speaker
        self.line = line

class Npc(Player):
    def __init__(self,row,col,theta,animal,color,script = [None]):
        super().__init__(row,col,theta)
        self.animal = animal
        self.baseColor = color
        self.color = color
        self.script = script
        if theta == 0:
            self.playerPosition = (row,col+1)

    def type(self):
        return self.animal

    def draw(self,canvas):
        if self.animal == "fox":
            drawFox(canvas,self)
        elif self.animal == "brb":
            drawBrb(canvas,self)
        elif self.animal == "cat":
            drawCat(canvas,self)
        elif self.animal == "bun":
            drawBun(canvas,self)

def generateForest(objects,npc,portal,sapling):
    size = len(objects)
    for x in range(size):
        objects[x][2] = None

    objects[0][0] = Tree()
    # objects[3][3] = Tree()
    
    if portal:
        (portalx,portaly) = (random.randrange(size),
            random.randrange(size))
        while portaly == 2 or (portalx,portaly) == (0,0):
            portaly = random.randrange(size)
        objects[portalx][portaly] = "Portal"

    if npc != None:
        objects[npc.row][npc.col] = npc

    if sapling:        
        (sapx,sapy) = (random.randrange(size),random.randrange(size))
        while objects[sapx][sapy] == None:
            sapy = random.randrange(size)
        objects[sapx][sapy] = Tree("Sapling")

    return objects

def populateBoard(rows,cols,thing,feq = 50):
    objects = make2dList(rows,cols,None)
    if type(thing) == Tree:
        for row in range(rows):
            for col in range(cols):
                if random.randrange(0,100) < feq:
                    objects[row][col] = Tree()
                else:
                    objects[row][col] = None
    else:
        for row in range(rows):
            for col in range(cols):
                if random.randrange(0,100) < feq:
                    objects[row][col] = thing
                else:
                    objects[row][col] = None
    return objects
