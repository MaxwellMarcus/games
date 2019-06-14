try:
    from tkinter import *
except:
    from Tkinter import *
import time
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

        self.colliders = [Collider(100,99,200,110)]

    def key_press(self,event):
        self.keys.append(event.keysym)
    def key_release(self,event):
        while self.keys.count(event.keysym) > 0:
            self.keys.remove(event.keysym)
    def update(self):
        self.delta_time = time.time()-self.last_update
        if self.delta_time > 0:
            player.render()
            player_speed = (self.delta_time)*500#100 p/s: dt/s*100
            if 'd' in self.keys:
                player.set_vel(player_speed,0)
            if 'a' in self.keys:
                player.set_vel(-player_speed,0)
            player.move()
            self.last_update = time.time()

            for i in self.colliders:
                i.render()
                print(i.has_collided(player.x,player.y))
            root.update()


class Player:
    def __init__(self):
        self.x = 10
        self.y = 100

        self.vel_x = 0
        self.vel_y = 0

        self.skin = canvas.create_rectangle(0,0,0,0)
    def set_vel(self,x,y):
        self.vel_x = x
        self.vel_y = y
    def move(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_x -= self.vel_x/10
        self.vel_y -= self.vel_y/10
        if abs(self.vel_x) < 0.1:
            self.vel_x = 0
        if abs(self.vel_y) < 0.1:
            self.vel_y = 0
    def render(self):
        canvas.delete(self.skin)
        x = self.x
        y = game.screen_height - self.y
        self.skin = canvas.create_rectangle(x,y,x+50,y-100,fill='black')

class Collider:
    def __init__(self,start_x,start_y,end_x,end_y):
        self.start_x = min([start_x,end_x])
        self.start_y = min([start_y,end_y])
        self.end_x = max([start_x,end_x])
        self.end_y = max([start_y,end_y])

        self.skin = canvas.create_rectangle(0,0,0,0)
    def has_collided(self,object):
        has_collided = False
        if object.start_x > self.start_x:
            if object.start_x < self.end_x:
                if object.start_y > self.start_y:
                    if object.start_y < self.end_y:
                        has_collided = True
        if object.end_x > self.start_x:
            if object.end_x < self.end_x:
                if object.start_y > self.start_y:
                    if object.start_y < self.end_y:
                        has_collided = True
        if object.end_x > self.start_x:
            if object.end_x < self.end_x:
                if object.end_y > self.start_y:
                    if object.start_y < self.end_y:
                        has_collided = True
        return False
    def render(self):
        canvas.delete(self.skin)
        y1 = game.screen_height - self.start_y
        y2 = game.screen_height - self.end_y
        x1 = self.start_x
        x2 = self.end_x

        self.skin = canvas.create_rectangle(x1,y1,x2,y2,fill='green',outline='red')

game = Game()
player = Player()

root.bind('<KeyPress>',game.key_press)
root.bind('<KeyRelease>',game.key_release)

while game.loop:
    game.update()
