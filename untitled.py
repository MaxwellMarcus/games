try:
    from tkinter import *
except:
    from Tkinter import *
from time import *
root = Tk()
canvas = Canvas(root,width=root.winfo_screenwidth(),height=root.winfo_screenheight())
canvas.pack()

class Game:
    def __init__(self):
        self.game = True
        self.bg = canvas.create_rectangle(0,0,0,0)
        self.platform = canvas.create_rectangle(0,0,0,0)
        self.players = []
        self.ais = []
        self.keys = []
        self.button = False
        self.dead = False
        self.startScreen = True
        self.startText = canvas.create_text(0,0)
        root.bind('<KeyPress>',self.keyPress)
        root.bind('<KeyRelease>',self.keyRelease)
        root.bind('<Button-1>',self.buttonPress)
        root.bind('<ButtonRelease->',self.buttonRelease)
    def newPlayer(self,x,y,color,pulseColor,inputs):
        self.players.append(Player(x,y,color,pulseColor,inputs))
    def newAI(self,x,y,color,pulseColor):
        self.ais.append(AI(x,y,color,pulseColor))
    def keyPress(self,event):
        self.keys.append(event.keysym)
    def keyRelease(self,event):
        l=[]
        for i in self.keys:
            if i != event.keysym:
                l.append(i)
        self.keys = l
    def buttonPress(self,event):
        self.button = True
    def buttonRelease(self,event):
        self.button = False
    def respawnPlayers(self):
        self.dead = False
        for i in self.players:
            i.respawn()
        for i in self.ais:
            i.respawn()
    def moveAIs(self):
        for i in self.ais:
            closest = None
            for l in self.players:
                if not closest:
                    closest = l
                else:
                    lDistX = abs(i.x-l.x)
                    lDistY = abs(i.y-l.y)
                    closestDistX = abs(i.x-closest.x)
                    closestDistY = abs(i.y-closest.y)
                    if lDistX+lDistY < closestDistX+closestDistY:
                        closest = l
            if not self.dead:
                distX = abs(closest.x-i.x)
                if distX == 0:
                    distX = 1
                distY = abs(closest.y-i.y)
                if distY == 0:
                    distY = 1
                if distX+distY<abs(i.x-root.winfo_screenwidth()/10) and distX+distY<abs(i.x-(root.winfo_screenwidth()-root.winfo_screenwidth()/10)):
                    if i.velX < 6:
                        i.velX += (closest.x-i.x)/distX*.2
                else:
                    closestWallX = -.1
                    if abs(i.x-root.winfo_screenwidth()/10) < abs(i.x-(root.winfo_screenwidth()-root.winfo_screenwidth()/2)):
                        closestWallX = .1
                    if i.velX < 6:
                        i.velX += closestWallX
                if distX+distY<abs(i.y-root.winfo_screenwidth()/10) and distX+distY<abs(i.y-(root.winfo_screenheight()-root.winfo_screenwidth()/10)):
                    if i.velY < 6:
                        i.velY += (closest.y-i.y)/distY*.2
                else:
                    closestWallY = -.1
                    if abs(i.y-root.winfo_screenwidth()/10) < abs(i.y-(root.winfo_screenheight()-root.winfo_screenwidth()/2)):
                        closestWallY = .1
                    if i.velY < 6:
                        i.velY += closestWallY
                if abs(closest.x-i.x) < 50 and abs(closest.y-i.y) < 50 and i.pulseAvailible:
                    i.pulseHitTime = time()
                    i.pulse = True
                    i.pulseAvailible = False

    def drawStartScreen(self):
        canvas.delete(self.startText)
        self.startText = canvas.create_text(root.winfo_screenwidth()/2,root.winfo_screenheight()/2,text='untitled',font=('TkTextFont',100),fill='blue')
    def update(self):
        if not self.startScreen:
            self.render()
            for i in self.players:
                i.update()
                if i.pulse:
                    for l in self.players:
                        if l != i:
                            if l.x-25<i.x+25 and l.x+25>i.x-25 and l.y-25<i.y+25 and l.y+25>i.y-25:
                                xDist = abs(l.x-i.x)
                                if xDist == 0:
                                    xDist = 1
                                yDist = abs(l.x-i.x)
                                if yDist == 0:
                                    yDist = 1
                                xrat = xDist/yDist
                                yrat = yDist/xDist
                                l.velX = 6 * (l.x-i.x)/xDist*xrat
                                l.velY = 6 * (l.y-i.y)/yDist*yrat
                    for l in self.ais:
                        if l.x-25<i.x+25 and l.x+25>i.x-25 and l.y-25<i.y+25 and l.y+25>i.y-25:
                            xDist = abs(l.x-i.x)
                            if xDist == 0:
                                xDist = 1
                            yDist = abs(l.x-i.x)
                            if yDist == 0:
                                yDist = 1
                            xrat = xDist/yDist
                            yrat = yDist/xDist
                            l.velX = 6 * (l.x-i.x)/xDist*xrat
                            l.velY = 6 * (l.y-i.y)/yDist*yrat
            self.moveAIs()
            for i in self.ais:
                i.update()
                if i.pulse:
                    for l in self.players:
                        if l.x-25<i.x+25 and l.x+25>i.x-25 and l.y-25<i.y+25 and l.y+25>i.y-25:
                            xDist = abs(l.x-i.x)
                            if xDist == 0:
                                xDist = 1
                            yDist = abs(l.x-i.x)
                            if yDist == 0:
                                yDist = 1
                            xrat = xDist/yDist
                            yrat = yDist/xDist
                            l.velX = -6 * (l.x-i.x)/xDist*xrat
                            l.velY = -6 * (l.y-i.y)/yDist*yrat
                    for l in self.ais:
                        if l != i:
                            if l.x-25<i.x+25 and l.x+25>i.x-25 and l.y-25<i.y+25 and l.y+25>i.y-25:
                                xDist = abs(l.x-i.x)
                                if xDist == 0:
                                    xDist = 1
                                yDist = abs(l.x-i.x)
                                if yDist == 0:
                                    yDist = 1
                                xrat = xDist/yDist
                                yrat = yDist/xDist
                                l.velX = -6 * (l.x-i.x)/xDist*xrat
                                l.velY = -6 * (l.y-i.y)/yDist*yrat
        else:
            self.render()
            self.drawStartScreen()
            if not len(self.keys)==0 or self.button:
                self.startScreen = False
        if 'Escape' in self.keys:
            self.game = False
        elif 'r' in self.keys and self.dead:
            self.respawnPlayers()

    def render(self):
        canvas.delete(self.bg)
        canvas.delete(self.platform)
        self.bg = canvas.create_rectangle(0,0,root.winfo_screenwidth(),root.winfo_screenheight(),fill='blue')
        self.platform = canvas.create_rectangle(root.winfo_screenwidth()/10,root.winfo_screenwidth()/10,root.winfo_screenwidth()-root.winfo_screenwidth()/10,root.winfo_screenheight()-root.winfo_screenwidth()/10,fill='Black')
        for i in self.players:
            i.render()
        for i in self.ais:
            i.render()
class Player:
    def __init__(self,x,y,color,pulseColor,inputSet):
        self.x = x
        self.y = y
        self.originalX = x
        self.originalY = y
        self.velX = 0
        self.velY = 0
        self.deaths = 0
        self.color = color
        self.skin = canvas.create_rectangle(0,0,0,0)
        self.pulse = None
        self.pulseSkin = canvas.create_rectangle(0,0,0,0)
        self.pulseColor = pulseColor
        self.pulseAvailible = True
        self.pulseHitTime = time()*100
        self.scoreText = canvas.create_text(0,0)
        self.scoreWords = canvas.create_text(0,0)
        self.inputs = inputSet
    def respawn(self):
        self.x = self.originalX
        self.y = self.originalY
        self.velX = 0
        self.velY = 0
    def update(self):
        self.input()
        if self.x>root.winfo_screenwidth()/10 and self.x<root.winfo_screenwidth()-root.winfo_screenwidth()/10 and self.y>root.winfo_screenwidth()/10 and self.y<root.winfo_screenheight()-root.winfo_screenwidth()/10:
            self.x += self.velX
            self.y += self.velY
        else:
            if not game.dead:
                self.deaths += 1
            game.dead = True

        if time()-self.pulseHitTime >= .1 and self.pulse:
            self.pulse = False
        elif time()-self.pulseHitTime >= .5:
            self.pulseAvailible = True
    def input(self):
        if self.inputs == 'wasd':
            if 'w' in game.keys:
                if self.velY < 6:
                    self.velY += .2
            if 's' in game.keys:
                if self.velY > -6:
                    self.velY -= .2
            if 'd' in game.keys:
                if self.velX > -6:
                    self.velX -= .2
            if 'a' in game.keys:
                if self.velX < 6:
                    self.velX += .2
            if 'space' in game.keys and self.pulseAvailible:
                self.pulseAvailible = False
                self.pulse = True
                self.pulseHitTime = time()
        if self.inputs == 'arrows':
            if 'Up' in game.keys:
                if self.velY < 6:
                    self.velY += .2
            if 'Down' in game.keys:
                if self.velY > -6:
                    self.velY -= .2
            if 'Right' in game.keys:
                if self.velX > -6:
                    self.velX -= .2
            if 'Left' in game.keys:
                if self.velX < 6:
                    self.velX += .2
            if game.button and self.pulseAvailible:
                self.pulseAvailible = False
                self.pulse = True
                self.pulseHitTime = time()
    def render(self):
        if self.pulse:
            canvas.delete(self.pulseSkin)
            self.pulseSkin = canvas.create_rectangle(self.x+50,self.y+50,self.x-50,self.y-50,fill=self.pulseColor)

        canvas.delete(self.skin)
        self.skin = canvas.create_rectangle(self.x+10,self.y+10,self.x-10,self.y-10,fill=self.color)

        canvas.delete(self.scoreWords)
        canvas.delete(self.scoreText)
        self.scoreText = canvas.create_text(self.originalX, root.winfo_screenheight()-root.winfo_screenheight()/10,text=self.deaths,font=('TkTextFont',50))
        self.scoreWords = canvas.create_text(self.originalX, root.winfo_screenheight()-root.winfo_screenheight()/10-50,text='Deaths',font=('TkTextFont',50))
class AI:
    def __init__(self,x,y,color,pulseColor):
        self.x = x
        self.y = y
        self.originalX = x
        self.originalY = y
        self.velX = 0
        self.velY = 0
        self.deaths = 0
        self.color = color
        self.skin = canvas.create_rectangle(0,0,0,0)
        self.pulse = None
        self.pulseSkin = canvas.create_rectangle(0,0,0,0)
        self.pulseColor = pulseColor
        self.pulseAvailible = True
        self.pulseHitTime = time()*100
        self.scoreText = canvas.create_text(0,0)
        self.scoreWords = canvas.create_text(0,0)
    def respawn(self):
        self.x = self.originalX
        self.y = self.originalY
        self.velX = 0
        self.velY = 0
    def update(self):
        if self.x>root.winfo_screenwidth()/10 and self.x<root.winfo_screenwidth()-root.winfo_screenwidth()/10 and self.y>root.winfo_screenwidth()/10 and self.y<root.winfo_screenheight()-root.winfo_screenwidth()/10:
            self.x += self.velX
            self.y += self.velY
        else:
            if not game.dead:
                self.deaths += 1
            game.dead = True

        if time()-self.pulseHitTime >= .1 and self.pulse:
            self.pulse = False
        elif time()-self.pulseHitTime >= .5:
            self.pulseAvailible = True
    def render(self):
        if self.pulse:
            canvas.delete(self.pulseSkin)
            self.pulseSkin = canvas.create_rectangle(self.x+50,self.y+50,self.x-50,self.y-50,fill=self.pulseColor)

        canvas.delete(self.skin)
        self.skin = canvas.create_rectangle(self.x+10,self.y+10,self.x-10,self.y-10,fill=self.color)

        canvas.delete(self.scoreWords)
        canvas.delete(self.scoreText)
        self.scoreText = canvas.create_text(self.originalX, root.winfo_screenheight()-root.winfo_screenheight()/10,text=self.deaths,font=('TkTextFont',50))
        self.scoreWords = canvas.create_text(self.originalX, root.winfo_screenheight()-root.winfo_screenheight()/10-50,text='Deaths',font=('TkTextFont',50))

game = Game()
game.newAI(root.winfo_screenwidth()-root.winfo_screenwidth()/4,root.winfo_screenheight()/2,'green','red')
game.newPlayer(root.winfo_screenwidth()/4,root.winfo_screenheight()/2,'orange','purple','wasd')

while game.game:
    game.update()
    root.update()
