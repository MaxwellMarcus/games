try:
    from tkinter import *
except:
    from Tkinter import *

root = Tk()
canvas = Canvas(root,width=root.winfo_screenwidth(),height=root.winfo_screenheight())
canvas.pack()

class Game:
    def __init__(self):
        self.game = True
        self.bg = canvas.create_rectangle(0,0,0,0)
        self.players = []
        self.keys = []
        root.bind('<KeyPress>',self.keyPress)
        root.bind('<KeyRelease>',self.keyRelease)
    def newPlayer(self,x,y,color):
        self.players.append(Player(x,y,color))
    def keyPress(self,event):
        self.keys.append(event.keysym)
    def keyRelease(self,event):
        for event.keysym in self.keys:
            self.keys.remove(event.keysym)
    def update(self):
        self.render()
        for i in self.players:
            i.update()
    def render(self):
        canvas.delete(self.bg)
        self.bg = canvas.create_rectangle(0,0,root.winfo_screenwidth(),root.winfo_screenheight(),fill='Black')
        for i in self.players:
            i.render()
class Player:
    def __init__(self,x,y,color):
        self.x = x
        self.y = y
        self.velX = 0
        self.velY = 0
        self.color = color
        self.skin = canvas.create_rectangle(0,0,0,0)
    def update(self):
        self.input()
        self.x += self.velX
        self.y += self.velY
    def input(self):
        if 'w' in game.keys:
            if self.velY < 6:
                self.velY += .2
        if 's' in game.keys:
            if self.velY > -6:
                self.velY -= .2
        self.velY -= self.velY/25
        if 'w' in game.keys:
            if self.velYX > -6:
                self.velX -= .2
        if 's' in game.keys:
            if self.velX < 6:
                self.velX += .2
        self.velX -= self.velX/25
    def render(self):
        canvas.delete(self.skin)
        self.skin = canvas.create_rectangle(self.x+10,self.y+10,self.x-10,self.y-10,fill=self.color)

game = Game()
game.newPlayer(root.winfo_screenwidth()/2,root.winfo_screenheight()/4,'green')
while game.game:
    game.update()
    root.update()
