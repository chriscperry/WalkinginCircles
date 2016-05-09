##################################
##      Walking in Circles      ##
##     by Christopher Perry     ##
##################################


import math
import string
import random
import copy
from time import process_time, sleep
from tkinter import *
from characterModels import *
from pointCalculations import *
from simpleAudio import *
from threeDeeTrees import *
from wisObjectClasses import *
from levels import *

def init(data):
    stopSound()
    data.player = Player(0,2)
    npcs = npcDictionary()
    data.levels =  [
                    None,
                    Forest("Sunset", 22, npc = npcs["cat1"], portal = False),
                    Forest("Morning",22),
                    Forest("Midday", 24, npc = npcs["fox1"]),
                    Forest("Sunset", 26, npc = npcs["fox2"]),
                    Forest("Morning",32, npc = npcs["bun1"]),
                    Forest("Midday",34),
                    Forest("Sunset",36, npc = npcs["cat2"]),
                    #Forest("Twilight",38),
                    None
                    ]
    # for x in range(len(data.levels)):
    #     print(data.levels[x].objects)
    data.level = 0
    data.objects = data.levels[1].objects
    data.theta = 0
    data.tilt = 2
    data.pause = False
    data.time = 0
    data.moveTime = 0
    data.textTime = 0
    data.stepTime = .5
    data.showTitle = False
    data.npcColor = "#000000"
    data.cx = data.width /2
    data.cy = data.height/1.5
    #data.npc = [Player(5,2,270)]
    data.driftIn = True
    data.driftTime = process_time()
    data.driftRate = 3
    data.rotate = False
    data.click = (0,0)
    data.titles = ["","\tWalking in\n\tCircles",
                    "\tChapter One",
                    "\tChapter Two",
                    "\tChapter Three",
                    "\tChapter Four",""]
    data.bgColor1 = (24,22,32)
    data.bgColor2 = (50,40,40)
    data.rain = 0
    data.canChange = False

    data.lineIndex = 0
    data.nextLine = False

    data.magicTree = (3,3)
    # data.timeSinceTeleport = process_time()

    # startSound("07 The Last Iron Horse.m4a", async=True, loop=True)

def getMapPoints(data):
    board = data.levels[data.level]
    (cx, cy) = (board.rows*board.tile / 2 + 1, board.rows*board.tile / 2  + 1)
    allpoints = make2dList(len(board.heights),len(board.heights[0]),None)
    for row in range(len(board.heights)):
        for col in range(len(board.heights[row])):
            (x,y) = (col * board.tile, row * board.tile)
            z = (board.heights[row][col] + 
                (math.sin(process_time()*2+(row-col+1))) + driftIn(data))
            r = getDist(cx,cy,x,y)
            angle = math.radians(data.theta) + getAngle(x,y,cx,cy)
            (pointx,pointy) = getPoint(data.cx,data.cy,z,r,angle,data.tilt)
            allpoints[row][col] = (int(pointx),int(pointy))
    return allpoints

def driftIn(data):
    time = (process_time() - data.driftTime)*data.driftRate
    if data.driftIn == True and time <= math.pi:
        data.tilt = math.pi / time * 3 - 1
        data.rotate = False
        data.theta = 180/time - 360
        height = -(math.cos(time)+1)*350
        if height > -350:
            data.showTitle = True
        else:
            data.showTitle = False
        return height
    elif data.driftIn == True:
        data.tilt = 2
        data.driftIn = False
    return 0

def drawMap(canvas, data):
    maxcolor = 255
    board = data.levels[data.level]
    player = data.player
    allpoints = getMapPoints(data)
    objects = data.objects

# Draw Background, Title, and Shadow
    if data.showTitle: 
        drawTitle(canvas,data,allpoints,min(3,board.rows-1),min(3,board.cols-1))
        if  data.theta % 360 > 300: data.showTitle = False
    drawShadow(canvas,data,allpoints,board.heights)

# Figure out where to start drawing from back to front
    theta = (math.radians(data.theta)+(math.pi/2)) % (2 * math.pi)
    (stepThroughRows,stepThroughCols) = getStepThrough(board.rows,board.cols,theta)

# Draw the board (future, make triangles objects?)
    for row in stepThroughRows:
        for col in stepThroughCols:
            (a,b,c,d) = (allpoints[row][col],allpoints[row+1][col],
                         allpoints[row][col+1],allpoints[row+1][col+1])
            
            colorValue = getColor(row,col,board.color,
                            min(max(data.theta,0),360))
            if (row,col) == (0,0): 
                data.bgColor1 = fadeColor(colorValue, data.bgColor1, 3)
            elif (row,col) == (board.rows-1,board.cols-1):
                data.bgColor2 = fadeColor(colorValue, data.bgColor2, 3)

            color = "#%02x%02x%02x" % colorValue

            # if objects[row][col] == "path":
            if col == 2 and data.level < 6:
                f = 5
                pathColor = "#%02x%02x%02x" % fadeColor(colorValue, (112,73,54), 50)
                (a2,b2,c2,d2) = (shiftP(a,f),shiftP(b,f),shiftP(c,f),shiftP(d,f))
                canvas.create_polygon(a2,b2,c2, fill = pathColor,outline = pathColor)
                canvas.create_polygon(b2,c2,d2, fill = pathColor,outline = pathColor)
            else:
                canvas.create_polygon(a,b,c, fill = color,outline = color)
                canvas.create_polygon(b,c,d, fill = color,outline = color)

            if ((row,col) == (player.row,player.col) or 
                (row,col) == (player.lastRow,player.lastCol)):
                drawMovingPlayer(colorValue,allpoints,player,data,canvas)

            elif isinstance(objects[row][col],Tree):
                treeColorValue = fadeColor(colorValue,(0,0,0),97)
                base = getCorners(allpoints,row,col,0,0,0,0)[0]
                tree = objects[row][col]
                treeTheta = objects[row][col].theta
                growTree(tree)
                drawTree(canvas,data,board,tree.get(),
                    base,treeTheta,treeColorValue,tree.growth)
                data.magicTree =(row,col)

            elif isinstance(objects[row][col],Npc):
                npc = objects[row][col]
                npc.color = "#%02x%02x%02x" % fadeColor(colorValue,npc.baseColor,40)
                npcPosition = getCorners(allpoints,row,col,0,0,0,0)[0]     
                npc.position = npcPosition
                npc.drawTheta = npc.theta + data.theta
                npc.draw(canvas)
                
            if objects[row][col] == "Portal":
                drawPortal(canvas,allpoints,row,col,colorValue)
                if (row,col) == (player.row,player.col):
                    for level in range(data.level-1,data.level+1):
                        if (level < len(data.levels) and
                            isinstance(data.levels[level],Board) and
                            data.levels[level].objects[row][col] == "Portal"):
                            data.level = level
                            break
                    data.theta = data.theta % 360 - 360
                    objects[row][col] = None
                    data.showTitle = True
                #drawPlayer(canvas,p,data.theta-90,color)

            # if (row,col) == (3,3):
            #     drawBlock(row,col,allpoints,canvas,board.heights,data.theta)

    treeSwapAlpha(data,allpoints,objects)
# Swap the trees
    return allpoints

def forcePortal(data):
    canPortal = (data.level+1 < len(data.levels) and 
                isinstance(data.levels[data.level],Forest)
                and data.levels[data.level] != None)
    objects = data.levels[data.level+1].objects
    if (data.theta > 360 and 
        "Portal" in objects and canPortal):
        print("focing portal")
        for row in range(len(objects)):
            for col in range(len(objects)):
                if objects[row][col] == "Portal":
                    data.objects[row][col] = "Portal"


def drawPortal(canvas,allpoints,row,col,colorValue):
    portalSize = 20
    for seed in range(-portalSize,portalSize,portalSize//5):
       drawSparkle(canvas,allpoints,row,col,colorValue,seed) 

def drawSparkle(canvas,allpoints,row,col,colorValue,seed):
    base = (int((math.sin(process_time()/4+seed)+1)*50+100),
        int((math.sin(process_time()/4+2*math.pi/3+seed)+1)*50+100),
        int((math.sin(process_time()/4+4*math.pi/3+seed)+1)*50+100))
    timeFactor = int((math.sin(process_time()*10+seed)+1) * 20 + 10)
    color = "#%02x%02x%02x" % fadeColor(colorValue,base,timeFactor)
    (p1,p2) = getCorners(allpoints,row,col,
                seed,math.sin(process_time()*2+seed)*30-60,
                seed,math.cos(process_time()*1.5+seed)*30-30)
    canvas.create_line(p1,p2,width = .25, fill = color)

def drawBlock(row,col,allpoints,canvas,heights,theta):
    blockHeight = 100
    h = [heights[row][col],heights[row+1][col],heights[row+1][col+1],heights[row][col+1]]
    p = [allpoints[row][col],allpoints[row+1][col],allpoints[row+1][col+1],allpoints[row][col+1]]
    top = []
    quadrant = int((theta % 360 + 90) // 90)
    for side in range(quadrant,quadrant+len(p)):
        x = side % len(p)
        p1 = (p[x][0],p[x][1]-h[x]-blockHeight)
        p2 = (p[(x+1)%len(p)][0],p[(x+1)%len(p)][1]-h[(x+1)%len(h)]-blockHeight)
        slope = getAngle(p1[0],p1[1],p2[0],p2[1])+4
        color = "#%02x%02x%02x" % (0,0,int(slope*20))
        canvas.create_polygon(p1,p2,p[(x+1)%len(p)],p[x],fill = color)
        top.append(p1)
    canvas.create_polygon(top,fill = "white")

def treeSwap(data,allpoints,objects):
    for row in range(len(objects)):
        for col in range(len(objects[row])):
            (magicRow,magicCol) = data.magicTree 
            (x1, y1) = allpoints[ row][col]
            (x2, y2) = allpoints[magicRow][magicCol]
            angle = math.atan2(y1-y2,x1-x2)
            if (data.canChange and -math.pi/2 < angle < math.pi/2 and
                isinstance(data.levels[(data.level+1)%len(data.levels)],Board)):
                data.objects[row][col] = data.levels[(data.level+1)%len(data.
                levels)].objects[row][col]
            elif (data.canChange and
                isinstance(data.levels[(data.level)%len(data.levels)],Board)):
                data.objects[row][col] = data.levels[(data.level)%len(data.
                levels)].objects[row][col]

def treeSwapAlpha(data,allpoints,objects):
    for row in range(len(objects)):
        for col in range(len(objects[row])):
            (x1, y1) = allpoints[row][col]
            (magicRow,magicCol) = data.magicTree
            (x2, y2) = allpoints[magicRow][magicCol]
            angle = getAngle(x1,y1,x2,y2)
            if (data.canChange) and 0 < data.theta < 180:
                if angle > math.pi / 2 and isinstance(data.levels[(data.level+1)
                    %len(data.levels)],Board):
                    newBoardObject = data.levels[(data.level+1)%len(data.
                        levels)].objects[row][col]
                elif isinstance(data.levels[(data.level)%len(data.levels)],Board):
                    newBoardObject = data.levels[(data.level)%len(data.
                        levels)].objects[row][col]
                if type(objects[row][col]) != type(newBoardObject):
                    if type(newBoardObject) == Tree:
                        newBoardObject.startGrow()
                    data.objects[row][col] = newBoardObject

def conversation(allpoints,canvas,data):
    p = data.player
    theta = p.theta % 360
    row = 0
    col = 0
    if theta == 0: col = 1
    elif theta == 90: row = 1
    elif theta == 180: col = -1
    elif theta == 270: row = -1
    if ((0 <= p.row + row < len(data.objects)) and 
        (0 <= p.col + col < len(data.objects)) and 
        isinstance(data.objects[p.row+row][p.col+col],Npc)):
        data.objects[p.row+row][p.col+col].theta = p.theta + 180
        data.nextLine = True
        converse(canvas,data,allpoints,p,data.objects[p.row+row][p.col+col]) 
    else:
        data.lineIndex = 0
        data.textTime = process_time()*50

def converse(canvas,data,allpoints,player,npc):
    if data.lineIndex < len(npc.script):
        line = npc.script[data.lineIndex]
        if line != None:
            if line.speaker == "player":
                (row,col) = (player.row,player.col)
            else:
                (row,col) = (npc.row,npc.col)
            drawTextBox(canvas,data,allpoints,row,col,line.line)
    verbalQueue(data)

def verbalQueue(data):
    if data.level > 1 or data.lineIndex == 3:
        data.canChange = True

def getStepThrough(rows,cols,theta):
    if theta > math.pi:
        r = range(rows)
    else:
       r = range(rows-1,-1,-1)
    if math.pi * 1.5 > theta > math.pi * .5:
        c = range(cols-1,-1,-1)
    else:
        c = range(cols)
    return (r,c)

def drawTextBox(canvas,data,allpoints,row,col,text = ""):
    text = text[:int((process_time()*50)-data.textTime)]
    (width,height) = getLongestLineAndRows(text)
    (x,y) = (width * 5 + 30, 130)
    (y1,y2) = (y + height * 10 + 10, y - height * 10 - 10)
    (p1,p2) = getCorners(allpoints,row,col,-x,-y1,x,-y2)
    (cx,cy) = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    canvas.create_polygon(cx+10,cy,cx-10,cy,cx,cy+60,
        fill = "#240106",outline = "#240106")
    canvas.create_rectangle(p1,p2,
        fill = "#240106",outline = "#240106")
    canvas.create_text(cx,cy,
        text = text[:int((process_time()*50)-data.textTime)],
        fill =  "silver", font = ("Courier", "18", "normal")) 

def getLongestLineAndRows(s):
    # Returns the longest line and the number of rows in a block of text
    currentLenght = 0
    longest = 0
    for c in range(len(s)):
        currentLenght += 1
        if s[c] == "\n":
            currentLenght = 0
        elif currentLenght >= longest:
            longest = currentLenght
    return (longest,s.count("\n")+1)

def drawShadow(canvas,data,allpoints,heights,color = "#240106"):
    ((s1a,s1b),(s2a,s2b),(s3a,s3b),(s4a,s4b)) = (allpoints[0][0],
    allpoints[0][-1],allpoints[-1][-1],allpoints[-1][0])
    s = 20
    h = heights
    drift = driftIn(data)*1.5
    s1 = (s1a, s1b+s-h[0][0]-drift)
    s2 = (s2a, s2b+s-h[0][-1]-drift)
    s3 = (s3a, s3b+s-h[-1][-1]-drift)
    s4 = (s4a, s4b+s-h[-1][0]-drift)
    canvas.create_polygon(s1,s2,s3,s4, fill = color)

def drawMovingPlayer(colorValue,allpoints,player,data,canvas):
    player.color = "#%02x%02x%02x" % fadeColor(colorValue,(255,255,255),50)
    p1 = getCorners(allpoints,player.row,player.col,0,0,0,0)[0]
    p2 = None
    if player.moving:
        f = process_time() * 10 - data.moveTime
        if f > data.stepTime: 
            player.moving = False
            (player.lastRow,player.lastCol) = (player.row,player.col)
        p2 = getCorners(allpoints,player.lastRow,
                        player.lastCol,0,0,0,0)[0]
        p1 = (weightAvg(p1[0],p2[0],f,data.stepTime),
              weightAvg(p1[1],p2[1],f,data.stepTime))
        startSound("walkingThroughGrass.wav", async=True, loop=False)
    player.position = p1
    player.drawTheta = player.theta + data.theta
    drawBrb(canvas,player)
    # drawPlayer(canvas,player)

def drawRain(canvas, data):
    if (data.level < len(data.levels) 
        and isinstance(data.levels[data.level],Board) 
        and data.levels[data.level].color == "Midday"):
        if random.random() < data.rain/800:
            startSound("medium_rainstorm-Mike_Koenig-1134528361.wav", 
                async=True, loop=False)
        data.rain = min(data.theta // 10,50)

    else:
        data.rain = 0
    for x in range(int(data.rain * (math.sin(process_time()*3)/2+2))):
         drawRaindrop(canvas,data)

def drawRaindrop(canvas, data):
    x1 = random.random() * data.width
    y1 = random.random() * data.height
    l = random.random() * 100
    x2 = l * math.sin(2.7+data.theta/10000) + x1
    y2 = l * math.cos(2.7+data.theta/10000) + y1
    bright = random.randrange(50)
    color = "#%02x%02x%02x" % (100+bright,100+bright,int(100+bright*1.5))
    canvas.create_line(x1,y1,x2,y2, width = .25, fill = color)

def shiftP(p,f):
    (x,y) = p
    return (x,y+f)

def isNear(x1,x2):
    return abs(x1-x2) < .01

def getCorners(allpoints,row,col,x3,y3,x4,y4):
    (x1,y1) = allpoints[row+1][col]
    (x2,y2) = allpoints[row][col+1]
    p1 = ((x1+x2)/2+x3,(y1+y2)/2+y3)
    p2 = ((x1+x2)/2+x4,(y1+y2)/2+y4)
    return (p1,p2)

def drawTitle(canvas, data, allpoints, row, col, color = "silver"):
    (x,y) = allpoints[row+1][col]
    (x1,y1) = allpoints[0][1]
    (x2,y2) = allpoints[1][0]
    (width,height) = (int((x1+x2)/2),int((y1+y2)/2))
    if data.level < len(data.titles):
        text = data.titles[data.level]
    else:
        text = ""
    canvas.create_text(x,110,text = text,
        fill = color, font = ("Helvetica", 56, "bold"))
    drawBG(canvas,data,height,width)

def nextLevel(data):
    data.level = (data.level+1) % len(data.levels)
    data.driftIn = True
    data.driftTime = process_time()
    #stopSound()

def movePlayer(data,move):
    p = data.player
    #b = data.levels[data.level]
    theta = p.theta%360
    row = 0
    col = 0
    if theta == 0: col = move
    elif theta == 90: row = move
    elif theta == 180: col = -move
    elif theta == 270: row = -move
    if ((0 <= p.row + row < len(data.objects)) and 
        (0 <= p.col + col < len(data.objects)) and 
        type(data.objects[p.row+row][p.col+col]) != Tree and
        type(data.objects[p.row+row][p.col+col]) != Npc):

        p.lastCol = p.col
        p.lastRow = p.row
        p.row += row
        p.col += col
        p.moving = True
        data.moveTime = process_time() * 10

def drawBG(canvas,data,height,width):
    data.bgColor1 = (data.bgColor2[0]//2,max(data.bgColor2[1],data.bgColor2[2]),
                    max(data.bgColor2[1],data.bgColor2[2]))
    data.bgColor2 = (max(data.bgColor2[0],data.bgColor2[1]),
                    data.bgColor2[1],data.bgColor2[2])
    for y in range(0,height,20):
        value = fadeColor(data.bgColor2,data.bgColor1,y,data.height)
        color = "#%02x%02x%02x" % fadeColor((40,40,40),value,y//10+10)
        canvas.create_line(0,y,width,y,fill = color,width = 20)

def drawTitle1(canvas,data):
    canvas.create_text(data.width/2,data.height/2-100,
        text = "Walking in Circles",
        fill = "silver", font = ("Helvetica", 78, "bold"))
    canvas.create_text(data.width/2,data.height/2,
        text = "Press space to interact,\narrow keys or wasd to move",
        fill = "silver", font = ("Helvetica", 30, "bold"), justify = CENTER)

def drawTitle2(canvas,data):
    canvas.create_text(data.width/2,data.height/2-100,
        text = "Congrats!",
        fill = "silver", font = ("Helvetica", 78, "bold"))
    canvas.create_text(data.width/2,data.height/2,
        text = "You've made it out of the woods",
        fill = "silver", font = ("Helvetica", 30, "bold"))

def checkMapSpin(data):
    if data.theta > 720:
        data.theta = data.theta % 360 + 360
    elif data.theta < -360:
        data.theta = data.theta % 360 - 360


def mousePressed(event, data):
    if data.canChange:
        data.rotate = True
        data.click = (event.x,event.y)
    forcePortal(data)

def mouseRelease(event, data):
    data.rotate = False
    checkMapSpin(data)


def keyPressed(event, data):
    if (event.keysym == "q"):
        init(data)
    if (event.keysym == "p"):
        data.pause = not data.pause
    if not data.player.moving and not data.pause:
        if (event.keysym == "a" or event.keysym == "Left"): 
            data.player.theta -= 90
        elif (event.keysym == "d" or event.keysym == "Right"): 
            data.player.theta += 90
        elif (event.keysym == "s" or event.keysym == "Down"): 
            movePlayer(data,-1)
        elif (event.keysym == "w" or event.keysym == "Up"): 
            movePlayer(data,1)
    if(event.keysym == "n"):
        nextLevel(data)
    if(event.keysym == "m"):
        data.level = (data.level+1) % len(data.levels)
        data.theta = data.theta % 360 - 360
    if (event.keysym == "space" and data.nextLine):
        data.lineIndex += 1 
        data.textTime = process_time()*50
    if(event.keysym == "space" and data.level == 0):
        nextLevel(data)
    if event.keysym == "r":
        print (data.level, data.theta)
        print(data.levels[data.level].objects, "\n")
        print(data.levels[data.level+1].objects, "\n")
        print(data.objects, "\n")

    # if (event.keysym == "z"):
    #     data.levels[data.level].objects[3][3].theta += .1
 
def timerFired(data):
    pass

def onMouseMoved(data, event):
    if not data.pause and data.rotate:
        (lastX,lastY) = data.click
        theta1 = math.degrees(math.atan2(
            lastY-data.cy,lastX-data.cx))
        if theta1 < 0: theta1 += 360
        theta2 = math.degrees(math.atan2(
            event.y-data.cx,event.x-data.cy))
        if theta2 < 0: theta2 += 360
        if -180 < theta2 - theta1 < 180:
            data.theta += theta2 - theta1
        data.click = (event.x,event.y)

def redrawAll(canvas, data):
    drawBG(canvas,data,data.height,data.width)   
    data.level = data.level % len(data.levels)
    if isinstance(data.levels[data.level],Board):
        allpoints = drawMap(canvas,data)
        drawRain(canvas,data)
        conversation(allpoints,canvas,data)
    elif data.level == 0:
        drawTitle1(canvas,data)
    elif data.level == len(data.levels) - 1:
        drawTitle2(canvas,data)


####################################
# use the run function
####################################

def run(width=1024, height=768):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data, root):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)
        # root.focus_set() # <-- move focus to this widget
        # root.focus()

    def mouseReleaseWrapper(event, canvas, data):
        mouseRelease(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def motionWrapper(event, canvas, data):
        onMouseMoved(data, event)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 15 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    root.title("Walking in Circles")

    # make it cover the entire screen
    # data.width, data.height = root.winfo_screenwidth(), root.winfo_screenheight()
    # root.overrideredirect(1)
    # root.geometry("%dx%d+0+0" % (data.width, data.height))

    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data, root))
    root.bind("<ButtonRelease-1>", lambda event:
                            mouseReleaseWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    root.bind("<Motion>", lambda event: motionWrapper(event, canvas, data))
    root.bind("<Escape>", lambda event: e.widget.quit())
    timerFiredWrapper(canvas, data)

    # and launch the app
    root.mainloop()  # blocks until window is closed

    stopSound()
    print("bye!"),

run()
stopSound()
