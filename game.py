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
        self.colliders.append(Collider(0,0,100000,self.screen_height/10))

        self.camera_pos_x = 0
        self.camera_pos_y = 0
        self.camera_vel_x = 0
        self.camera_vel_y = 0

        self.level = 1
    def create_level(self):
        self.colliders = []
        if self.level == 1:
            self.colliders.append(Collider(0,0,100000,self.screen_height/10))
            y = self.screen_height/10
            self.colliders.append(Collider(self.screen_width/5,y,self.screen_width/5+self.screen_width/15,y+self.screen_height/10))
            x = self.screen_width/5+self.screen_width/15
            self.colliders.append(Collider(x,y,x+self.screen_width/15,y+self.screen_height/5))
            x = x+self.screen_width/15
            self.colliders.append(Collider(x,y,x+self.screen_width/15,y+self.screen_height/10+self.screen_height/5))
            x = x+self.screen_width/15
            self.colliders.append(Collider(x,y,x+self.screen_width/15,y+self.screen_height/5*2))
            x = x+self.screen_width/15*2
            self.colliders.append(Collider(x,y,x+self.screen_width/15,y+self.screen_height/5*2))
            x = x+self.screen_width/15
            self.colliders.append(Collider(x,y,x+self.screen_width/15,y+self.screen_height/5*2+self.screen_height/10))
    def key_press(self,event):
        if not event.keysym in self.keys:
            self.keys.append(event.keysym)

    def key_release(self,event):
        self.keys.remove(event.keysym)

    def update(self):
        #clearing the canvas
        canvas.delete(ALL)

        self.create_level()

        #checking if they player has collided and rendering the different objects that are part of the game
        for i in self.colliders:
            if player.collider.has_collided(i):
                player.bounce(i)

            pos = self.renderify(i.start_x,i.start_y)
            x1 = pos[0]
            y1 = pos[1]

            pos = self.renderify(i.end_x,i.end_y)
            x2 = pos[0]
            y2 = pos[1]

            canvas.create_rectangle(x1,y1,x2,y2,fill='blue',outline='blue')

        #Using keyboard inputs to move the player
        if 'd' in self.keys:
            player.accel_x = self.screen_width/700

        elif 'a' in self.keys:
            player.accel_x = -self.screen_width/700

        else:
            player.accel_x = 0

        if 'w' in self.keys and player.jumpable:
            player.accel_y = self.screen_height/115

            player.jumpable = False

        #Gravity
        if player.accel_y > -self.screen_height/500:
            player.accel_y -= self.screen_height/500

        #changing camera position based on player
        dist = player.x - self.camera_pos_x
        self.camera_vel_x = dist/5
        self.camera_pos_x += self.camera_vel_x
        dist = (player.y-self.screen_height/2) - self.camera_pos_y
        if abs(dist) > self.screen_height/2-self.screen_height/8:
            self.camera_vel_y = dist/10

        if abs(dist) < self.screen_height/4:
            if abs(self.camera_vel_y) > .1:
                self.camera_vel_y -= self.camera_vel_y/10
            else:
                self.camera_vel_y = 0

        self.camera_pos_y += self.camera_vel_y


        #upddating the players position and rendering it on the screen
        player.update()
        player.render()

        #updating the canvas
        root.update()

    def renderify(self,x,y):
        x -= self.camera_pos_x-self.screen_width/2
        y -= self.camera_pos_y

        y = self.screen_height - y
        return x,y

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

        self.jumpable = True

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

            self.jumpable = True


    def render(self):
        pos = game.renderify(self.x,self.y)
        x = pos[0]
        y = pos[1]
        canvas.create_rectangle(x,y,x+self.width,y-self.height,fill='purple',outline='purple')

class Collider:
    def __init__(self,start_x,start_y,end_x,end_y):
        self.start_x = min(start_x,end_x)
        self.end_x = max(start_x,end_x)
        self.start_y = min(start_y,end_y)
        self.end_y = max(start_y,end_y)

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
