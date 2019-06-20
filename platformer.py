try:
    from tkinter import *
except:
    from Tkinter import *
import time
import math
root = Tk()
canvas = Canvas(root,width=root.winfo_screenwidth(),height=root.winfo_screenheight())
canvas.pack()

class Game:
    def __init__(self):
        self.game_start = time.time()
        self.last_update = time.time()

        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()

        self.loop = True

        self.keys = []

        self.colliders = [Collider(100,0,200,500)]

    def key_press(self,event):
        self.keys.append(event.keysym)
    def key_release(self,event,key=None):
        if event:
            while self.keys.count(event.keysym) > 0:
                self.keys.remove(event.keysym)
        if key:
            while self.keys.count(key) > 0:
                self.keys.remove(key)
    def update(self):
        self.delta_time = time.time()-self.last_update
        if self.delta_time > 0:
            player.render()
        #    player_speed = (self.delta_time)*500#100 p/s: dt/s*100
            if 'd' in self.keys:
                player.accelerate(1,0)
            if 'a' in self.keys:
                player.accelerate(-1,0)
            player.move()
            self.last_update = time.time()

            for i in self.colliders:
                i.render()
                l = i.has_collided(player.collider)#player.collider.has_collided(i)
                if l:
                    print('working')
                    if l == 1:
                        print('working * 2')
                        x = player.collider.start_x
                        y = player.collider.start_y
                        if y > i.start_y and y < i.end_x:
                            print('working * 3')
                            player.set_vel(-player.vel_x,player.vel_y)
                        else:
                            print('working*3')
                            player.set_vel(player.vel_x,-player.vel_y)
            root.update()


class Player:
    def __init__(self):
        self.x = 10
        self.y = 400

        self.collider = Collider(self.x,self.y,self.x+50,self.y-100)

        self.vel_x = 0
        self.vel_y = 0

        self.skin = canvas.create_rectangle(0,0,0,0)
    def accelerate(self,x,y):
        self.vel_x += x
        self.vel_y += y
    def set_vel(self,x,y):
        self.vel_x = x
        self.vel_y = y
    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.collider.start_x = self.x
        self.collider.start_y = self.y-100
        self.collider.end_x = self.x+50
        self.collider.end_y = self.y
        self.vel_x -= self.vel_x/30
        self.vel_y -= self.vel_y/30
        if abs(self.vel_x) < 0.1:
            self.vel_x = 0
        if abs(self.vel_y) < 0.1:
            self.vel_y = 0
    def render(self):
        canvas.delete(self.skin)
        x = self.x
        x2 = self.x + 50
        y = game.screen_height - self.y
        y2 = game.screen_height- (self.y-100)
        self.skin = canvas.create_rectangle(x,y2,x2,y,fill='black')

class Collider:
    def __init__(self,start_x,start_y,end_x,end_y):
        self.start_x = min([start_x,end_x])
        self.start_y = min([start_y,end_y])
        self.end_x = max([start_x,end_x])
        self.end_y = max([start_y,end_y])

        self.skin = canvas.create_rectangle(0,0,0,0)
        self.collided = False
    def has_collided(self,object):
        corner = False
        if object.start_x >= self.start_x:
            if object.start_x <= self.end_x:
                if object.start_y >= self.start_y:
                    if object.start_y <= self.end_y:
                        corner = 1
        elif object.end_x >= self.start_x:
            if object.end_x <= self.end_x:
                if object.start_y >= self.start_y:
                    if object.start_y <= self.end_y:
                        corner = 1
        elif object.end_x >= self.start_x:
            if object.end_x <= self.end_x:
                if object.end_y >= self.start_y:
                    if object.end_y <= self.end_y:
                        corner = 1
        elif object.start_x >= self.start_x:
            if object.start_x <= self.end_x:
                if object.end_y >= self.start_y:
                    if object.end_y <= self.end_y:
                        corner = 1
        elif object.has_collided2(self):
            corner = True
        print(corner)
        if not corner == False:
            self.collided = True
        else:
            self.collided = False
        return corner
    def has_collided2(self,object):
        has_collided = False
        if object.start_x >= self.start_x:
            if object.start_x <= self.end_x:
                if object.start_y >= self.start_y:
                    if object.start_y <= self.end_y:
                        has_collided = True
        elif object.end_x >= self.start_x:
            if object.end_x <= self.end_x:
                if object.start_y >= self.start_y:
                    if object.start_y <= self.end_y:
                        has_collided = True
        elif object.end_x >= self.start_x:
            if object.end_x <= self.end_x:
                if object.end_y >= self.start_y:
                    if object.end_y <= self.end_y:
                        has_collided = True
        elif object.start_x >= self.start_x:
            if object.start_x <= self.end_x:
                if object.end_y >= self.start_y:
                    if object.end_y <= self.end_y:
                        has_collided = True
        return has_collided
    def render(self):
        canvas.delete(self.skin)
        y1 = game.screen_height - self.start_y
        y2 = game.screen_height - self.end_y
        x1 = self.start_x
        x2 = self.end_x
        if self.collided == True:
            self.skin = canvas.create_rectangle(x1,y1,x2,y2,fill='green',outline='red')
        else:
            self.skin = canvas.create_rectangle(x1,y1,x2,y2,fill='red',outline='green')

game = Game()
player = Player()

root.bind('<KeyPress>',game.key_press)
root.bind('<KeyRelease>',game.key_release)

while game.loop:
    game.update()
