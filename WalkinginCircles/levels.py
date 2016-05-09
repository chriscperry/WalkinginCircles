
#################################
#   Christopher Perry           #
#   4/21/16                     #
#                               #
#   Here are the levels!        #
#   scripts kept here 'cause    #
#   they're too gosh darn big   #
#################################

from wisObjectClasses import *

def npcDictionary():
    return {
            "cat1" : Npc(random.randrange(5)+1,2,
            random.randrange(4)*90,"cat",(230,80,10),catScript1()),
            "fox1" : Npc(random.randrange(6),2,
            random.randrange(4)*90,"fox",(200,50,20),foxScript1()),
            "fox2" : Npc(random.randrange(6),2,
            random.randrange(4)*90,"fox",(245,165,50),foxScript2()),
            "bun1" : Npc(random.randrange(6),2,
            random.randrange(4)*90,"bun",(150,150,150),bunScript1()),
            "cat2" : Npc(random.randrange(5)+1,2,
            random.randrange(4)*90,"cat",(55,50,48),catScript2()),
            "bun2" : Npc(random.randrange(6),random.randrange(6),
            random.randrange(4)*90,"bun",(150,150,150),bunScript2()),
            "fox3" : Npc(random.randrange(6),random.randrange(6),
            random.randrange(4)*90,"fox",(245,165,50),foxScript3()),
            "cat3" : Npc(4,4,
            random.randrange(4)*90,"cat",(55,50,48),catScript3()),
            }

def level0():

    npc = Npc(random.randrange(6),2,random.randrange(4)*90,"cat",(200,50,20))

    objects=[[Tree(), None,   None,   None,   None,   Tree()],
             [None,   Tree(), None,   None,   None,   None],
             [None,   None,   None,   None,   Tree(), None],
             [None,   None,   npc,    None,   None,   None],
             [None,   None,   None,   Tree(), None,   None],
             [Tree(), None,   None,   None,   None,   None]]
    return objects

def catScript1():
    return[None,
Line("player",  "Cat! Do you live\naround here?"),
Line("npc",     "Near enough to know\nthat you do not"),
Line("player",  "Okay..."),
Line("player",  "Can you show me the\nway to the Ivory Tower?"),
Line("npc",     "No, but I will watch\nyou get hopelessly lost."),                
Line("npc",     "And besides, it's\nmore fun to have\na look around."),
Line("player",  "What"),
Line("npc",   "Click and drag\nclockwise for a\nchange in perspective"),
None
        ]

def foxScript1():
    return[None,
Line("npc",     "There are strange\nshimmers in these woods"),
Line("npc",     "I had a friend who\nwent in one once"),
Line("player",  "..."),
Line("npc",     "Haven't seen\nhim in weeks")
        ]

def foxScript2():
    return[None,
Line("npc",     "See those sparkles?"),
Line("npc",     "It's the mark of\nfairies that will\nsteal you away"),
Line("player",  "..."),
Line("npc",     "Have you seen my\nfriend? Reddish\nfox, my height?")
        ]

def bunScript1():
    return[None,
Line("player",  "Excuse me,"),
Line("npc",     "Oh!"),
Line("npc",     "Hello,"),
Line("npc",     "Can I help you?"),
Line("player",  "Yes, I'm looking\nfor the Ivory Tower"),
Line("npc",     "Hmm"),
Line("npc",     "The Ivory Tower\nyou say?"),
Line("player",  "Yes!"),
Line("player",  "Do you know where it is?"),
Line("npc",     "They say that\nit is just beyond\nthe Great Tree"),
Line("player",  "How do I get there?"),
Line("npc",     "..."),
Line("npc",     "I don't know"),
        ]

def catScript2():
    return [None,
Line("player",  "I'm looking for\nthe Great Tree"),
Line("player",  "So that I can find\nthe Ivory Tower"),
Line("npc",     "Hmph."),
Line("npc",     "The Great Tree is\nnot simply found."),
Line("player",  ":/"),
Line("npc",     "Bring me four saplings,"),
Line("npc",     "and I will help you\nfind what you are\nlooking for."),
Line("player",  "Sweet"),
        ]

def bunScript2():
    return [None,
Line("player",  "Oh, Hello again"),
Line("npc",     "Hey! Any luck\non the tree?"),
Line("player",  "I met a black cat\nwho said she would\nhelp me"),
Line("npc",     "Oh. Oh dear."),
Line("player",  "?"),
Line("npc",     "She's a witch, you know?"),
Line("npc",     "I don't trust her,\nbut I hope she can\nhelp you..."),
Line("player",  "Well, thanks"),
Line("npc",     "No prob, Bob")
        ]

def foxScript3():
    return [None,
Line("npc",     "Oh! It's you again!"),
Line("npc",     "How did you get back here?"),
Line("player",  "...Through the\nforest sparkles..."),
Line("npc",     "O_o"),
        ]

def catScript3():
    return [None,
Line("player",  "I have your saplings!"),
Line("npc",     "Yes, yes. These\nshould do nicely."),
Line("player",  "What should I\ndo with them?"),
Line("npc",     "Just stay there."),
Line("npc",     "..."),
Line("npc",     "*deep breath*\n Are you ready?"),
Line("player",  "I- I'm not sure?"),
Line("npc",     "Here we go!"),
Line("player",  "Whoa!"),
Line("player",  "What's happening?"),
Line("npc",     "Haven't you seen how\nthis forest shifts?"),
Line("npc",     "The Great Trees\ncontrol this forest"),
Line("npc",     "Which makes them\ndifficult to find,\nbut easy to grow"),
Line("npc",     "It is a payment for\npassage. I hope you\nfind what you seek"),
Line("player",  "That's...\npretty cool?"),
Line("npc",     "Oh, Hell yeah."),
Line("npc",     "O Great forest\nspirits! We have for\nyou a new vessel!"),
Line("npc",     "In return please\nshow us the way to\nyour Ivory Tower!"),
            ]

def getColor(row,col, color = "Midday",theta = 0):
    if color == "Test":
        return (int(math.sin(row/5)*80+theta/3), # Test
        int(math.cos(math.radians(theta))*20+50),
        int(math.cos(col/6)*50+100-theta/5))
    if color == "Fall":
        return (int(abs(math.cos(row/8)*50+110-theta/10)), # Fall
        int(abs(math.cos((col-row)/8)*40+40+theta/10)),
        int(abs(math.cos(col/4)*50+20)))
    if color == "Winter":
        return (int(abs(math.cos((col-row)/4)*20+180)), # Winter
        int(abs(math.cos((col-row)/4)*20+200)),
        int(abs(math.cos((col-row)/4)*50+200)))
    if color == "Midday":
        return (int(abs(math.cos(row/4)*40+40)), # Midday
        int(abs(math.cos((col+row)/10)*60+70-theta/10)),
        int(abs(math.cos(col/4)*40+30)))
    if color == "Twilight":
        return (int(abs(math.cos(row/4)*40+50)), # Twilight
        int(abs(math.cos((col+row)/10)*60+40)),
        int(abs(math.cos(col/4)*40+40)))
    elif color == "Dusk2":
        return (int(abs(math.cos(row/4)*50)), # Dusk2
        int(abs(math.cos((col+row)/10)*40)),
        int(abs(math.cos(col/5)*40)))
    elif color == "Dusk":
        return (int(abs(math.cos(row/4)*30+50)), # Dusk
        int(abs(math.cos((col+row)/10)*30+20)),
        int(abs(math.cos(col/5)*70+20)))
    elif color == "Morning":
        return (int(abs(math.cos(row/4)*70+50)), # Morning
        int(abs(math.cos((col+row)/10)*120+theta/10)),
        int(abs(math.cos(col/5)*70+20)))
    elif color == "Sunset":
        theta = 360 - theta
        return (int(abs(math.cos(row/4)*180-theta/6+20)), # Sunset
        int(abs(math.cos((col+row)/10)*80+20+theta/10)),
        int(abs(math.cos(col/5)*70+20)))






