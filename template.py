try:
    from tkinter import *
except:
    from Tkinter import *
import time
import math
import random
root = Tk()
canvas = Canvas(root,width=root.winfo_screenwidth(),height=root.winfo_screenheight())
canvas.pack()

class Game:
    def __init__(self):
        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        self.running = True

        self.keys = []

        self.colliders = []

    def key_press(self,event):
        if not event.keysym in self.keys:
            self.keys.append(event.keysym)

    def key_release(self,event):
        self.keys.remove(event.keysym)

    def update(self):
        #clearing the canvas
        canvas.delete(ALL)

        #upddating the players position and rendering it on the screen
        if 'd' in self.keys:
            player.accel_x = 1

        elif 'a' in self.keys:
            player.accel_x = -1

        else:
            player.accel_x = 0

        if 'w' in self.keys:
            player.accel_y = 1

        elif 's' in self.keys:
            player.accel_y = -1

        else:
            player.accel_y = 0

        player.update()
        player.render()

        #updating the canvas
        root.update()


class Player:
    def __init__(self):
        self.x = 0
        self.y = 100

        self.width = game.screen_width/50
        self.height = game.screen_height/30

        self.vel_x = 0
        self.vel_y = 0

        self.accel_x = 0
        self.accel_y = 0

        self.collider = Collider(0,100,self.width,100+self.height)

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y

        self.vel_x += self.accel_x
        self.vel_y += self.accel_y

        self.vel_x -= self.vel_x/10.0
        self.vel_y -= self.vel_y/10.0

        self.collider.start_x = self.x
        self.collider.end_x = self.x + self.width
        self.collider.start_y = self.y
        self.collider.end_y = self.y + self.height

    def bounce(self,c):
        if self.x+(self.width/2) < c.start_x+(abs(c.start_x-c.end_x)/2):
            x = (self.x+self.width) - self.vel_x
        else:
            x = self.x - self.vel_x
        if self.y+(self.height/2) < c.start_y+(abs(c.start_y-c.end_y)/2):
            y = (self.y+self.height) - self.vel_y
        else:
            y = self.y - self.vel_y

        if x < c.start_x:
            self.x = c.start_x-(self.width)
            self.vel_x = 0

        elif x > c.end_x:
            self.x = c.end_x
            self.vel_x = 0

        if y < c.start_y:
            self.y = c.start_y-(self.height)
            self.vel_y = 0

        elif y > c.end_y:
            self.y = c.end_y
            self.vel_y = 0


    def render(self):
        canvas.create_rectangle(self.x,game.screen_height-self.y,self.x + self.width,game.screen_height-(self.y+self.height),fill='purple',outline='purple')

class Collider:
    def __init__(self,start_x,start_y,end_x,end_y):
        self.start_x = min(start_x,end_x)
        self.end_x = max(start_x,end_x)
        self.start_y = min(start_y,end_y)
        self.end_y = max(start_x,end_y)

    def has_collided(self,other):
        collided = False
        x_in = False
        y_in = False
        if self.start_x >= other.start_x and self.start_x <= other.end_x:
            x_in = True
        elif self.end_x >= other.start_x and self.end_x <= other.end_x:
            x_in = True

        if self.start_y >= other.start_y and self.start_y <= other.end_y:
            y_in = True
        elif self.end_y >= other.start_y and self.end_y <= other.end_y:
            y_in = True

        if y_in and x_in:
            collided = True

        return collided

game = Game()
player = Player()

root.bind('<KeyPress>',game.key_press)
root.bind('<KeyRelease>',game.key_release)

while game.running:
    game.update()
