
#################################
#   Christopher Perry           #
#   4/13/16                     #
#                               #
#   Functions for drawing       #
#   characters because          #
#   look at how long these are  #
#################################

import math
import string
import random
from time import process_time
from tkinter import *
from pointCalculations import *

def drawBrb(canvas,player):
    (x,y) = player.position
    y += 5 
    yb = y + 1.5*math.cos((process_time()+(x/100)%10)*4)
    color = player.color
    canvas.create_oval((x-10,y-5),(x+10,y-15), 
        fill = color, outline = color)
    canvas.create_oval((x-8,yb-40),(x+8,yb-56), 
        fill = color, outline = color)
    canvas.create_polygon((x-10,y-10),(x+10,y-10),(x,y-35), 
        fill = color, outline = color)

    (x1,y1,x2,y2) = (x,y-48,x-25,y-48)
    r = getDist(x1,y1,x2,y2)
    angle = math.radians(player.drawTheta) + getAngle(x1,y1,x2,y2)
    (pointx,pointy) = getPoint(x1,y1,0,r,angle,2)

    turning = (pointx,pointy)
    canvas.create_polygon(turning,(x,yb-40),(x,yb-56), 
        fill = color, outline = color)
    canvas.create_polygon(turning,(x-8,y-48),(x+8,y-48), 
        fill = color, outline = color)

def drawCat(canvas,player):
    (x,y) = player.position
    y += 5 
    yb = y + 1.5*math.cos((process_time()+(x/100)%10)*4)
    color = player.color
    canvas.create_oval((x-10,y-5),(x+10,y-15), 
        fill = color, outline = color)
    canvas.create_oval((x-8,yb-40),(x+8,yb-56), 
        fill = color, outline = color)
    canvas.create_polygon((x-10,y-10),(x+10,y-10),(x+3,y-33),(x-3,y-33), 
        fill = color, outline = color)
    
    (x3,y3,x4,y4) = (x,y-65,x-10,y-65)
    r2 = getDist(x3,y3,x4,y4)
    angle2 = math.radians(player.drawTheta)+getAngle(x3,y3,x4,y4)+math.pi/2
    earRight = getPoint(x3,y3,-3,r2,angle2,2)
    angle3 = math.radians(player.drawTheta)+getAngle(x3,y3,x4,y4)-math.pi/2
    earLeft = getPoint(x3,y3,-3,r2,angle3,2)

    canvas.create_polygon(earRight,(x,yb-40),(x,yb-53), 
        fill = color, outline = color)
    canvas.create_polygon(earRight,(x-8,y-48),(x+8,y-48), 
        fill = color, outline = color)
    canvas.create_polygon(earLeft,(x,yb-40),(x,yb-53), 
        fill = color, outline = color)
    canvas.create_polygon(earLeft,(x-8,y-48),(x+8,y-48), 
        fill = color, outline = color)

def drawBun(canvas,player):
    (x,y) = player.position
    y += 5 
    yb = y + 1.5*math.cos((process_time()+(x/100)%10)*4)
    color = player.color
    canvas.create_oval((x-10,y-5),(x+10,y-15), 
        fill = color, outline = color)
    canvas.create_oval((x-8,yb-40),(x+8,yb-56), 
        fill = color, outline = color)
    canvas.create_polygon((x-10,y-10),(x+10,y-10),(x,y-33), 
        fill = color, outline = color)

    (x1,y1,x2,y2) = (x,y-48,x-12,y-48)
    r = getDist(x1,y1,x2,y2)
   
    angle = math.radians(player.drawTheta) + getAngle(x1,y1,x2,y2)
    turning = getPoint(x1,y1,0,r,angle,2)
    
    tailAngle = math.radians(player.drawTheta) + getAngle(x,y,x+5,y)
    (tx,ty) = getPoint(x1,y1,30,r,tailAngle,2)

    canvas.create_oval((tx+5,ty+5),(tx-5,ty-5),
    fill = color, outline = color)

    (x3,y3,x4,y4) = (x,y-60,x-7,y-60)
    r2 = getDist(x3,y3,x4,y4)
    
    angle2 = math.radians(player.drawTheta) + getAngle(x3,y3,x4,y4) + math.pi / 2
    (erx,ery) = getPoint(x3,y3,0,r2,angle2,2)

    angle3 = math.radians(player.drawTheta) + getAngle(x3,y3,x4,y4) - math.pi / 2
    (elx,ely) = getPoint(x3,y3,0,r2,angle3,2)


    canvas.create_polygon((turning[0],turning[1]-3),turning,(x,yb-40),(x,yb-52), 
        fill = color, outline = color)
    canvas.create_polygon(turning,(x-8,y-48),(x+8,y-48), 
        fill = color, outline = color)

    canvas.create_oval((erx+2,ery+12),(erx-2,ery-12),
        fill = color, outline = color)
    # canvas.create_polygon(earRight,(x-5,y-48),(x+5,y-48), 
    #     fill = color, outline = color)
    canvas.create_oval((elx+2,ely+12),(elx-2,ely-12),
        fill = color, outline = color)
    # canvas.create_polygon(earLeft,(x-5,y-48),(x+5,y-48), 
    #     fill = color, outline = color)

def drawFox(canvas,player):
    (x,y) = player.position
    y += 5 
    yb = y + 1.5*math.cos((process_time()+(x/100)%10)*4)
    color = player.color
    canvas.create_oval((x-10,y-5),(x+10,y-15), 
        fill = color, outline = color)
    canvas.create_oval((x-8,yb-40),(x+8,yb-56), 
        fill = color, outline = color)
    canvas.create_polygon((x-10,y-10),(x+10,y-10),(x+3,y-33),(x-3,y-33), 
        fill = color, outline = color)

    (x1,y1,x2,y2) = (x,y-48,x-20,y-48)
    r = getDist(x1,y1,x2,y2)
    angle = math.radians(player.drawTheta) + getAngle(x1,y1,x2,y2)
    turning = getPoint(x1,y1,0,r,angle,2)
    
    (x3,y3,x4,y4) = (x,y-65,x-10,y-65)
    r2 = getDist(x3,y3,x4,y4)
    angle2 = math.radians(player.drawTheta) + getAngle(x3,y3,x4,y4) + math.pi / 2
    earRight = getPoint(x3,y3,-5,r2,angle2,2)
    angle3 = math.radians(player.drawTheta) + getAngle(x3,y3,x4,y4) - math.pi / 2
    earLeft = getPoint(x3,y3,-5,r2,angle3,2)

    canvas.create_polygon((turning[0],turning[1]-3),turning,(x,yb-40),(x,yb-52), 
        fill = color, outline = color)
    canvas.create_polygon(turning,(x-8,y-48),(x+8,y-48), 
        fill = color, outline = color)

    canvas.create_polygon(earRight,(x,yb-40),(x,yb-53), 
        fill = color, outline = color)
    canvas.create_polygon(earRight,(x-5,y-48),(x+5,y-48), 
        fill = color, outline = color)
    canvas.create_polygon(earLeft,(x,yb-40),(x,yb-53), 
        fill = color, outline = color)
    canvas.create_polygon(earLeft,(x-5,y-48),(x+5,y-48), 
        fill = color, outline = color)
