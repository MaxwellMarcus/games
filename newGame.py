try:
    from tkinter import *
except ImportError:
    from Tkinter import *
from time import *
root = Tk()
canvas = Canvas(root,width=root.winfo_screenwidth(),height=root.winfo_screenheight())
canvas.pack()

class Game:
    def __init__(self):
        self.game = True
        self.lastUpdate = time()

        self.keys = []
        self.player = Player()
        root.bind('<KeyPress>',self.keyPressed)
        root.bind('<KeyRelease>',self.keyReleased)
    def update(self):
        timePassed = time()-self.lastUpdate
        self.player.update(timePassed)
        if 'Escape' in self.keys:
            self.game = False
    def keyPressed(self,event):
        self.keys.append(event.keysym)
    def keyReleased(self,event):
        new = []
        for i in self.keys:
            if not i == event.keysym:
                new.append(i)
        self.keys = new
class Player:
    def __init__(self):
        self.x = root.winfo_screenwidth()/2
        self.y = root.winfo_screenheight()/2
        self.velX = 0
        self.velY = 0
        self.skin = canvas.create_oval(0,0,0,0)
    def update(self,time):
        self.velY += 9.8*time
        if self.y+5 >= root.winfo_screenheight():
            self.velY *= -.5
            self.y += self.velY
        else:
            self.y += self.velY
        self.x += self.velX
        if 'a' in game.keys:
            self.velX -= .1
        if 'd' in game.keys:
            self.velX += .1
        self.render()
    def render(self):
        canvas.delete(self.skin)
        self.skin = canvas.create_oval(self.x-5,self.y-5,self.x+5,self.y+5,fill='black')
game = Game()
while game.game:
    game.update()
    root.update()
