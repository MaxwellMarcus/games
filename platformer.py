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

        self.colliders = [Collider(0,0,self.screen_width,50),Collider(0,0,50,self.screen_height),Collider(0,self.screen_height-50,self.screen_width,self.screen_height),Collider(self.screen_width-50,self.screen_height,self.screen_width,0)]
        self.colliders.append(Collider(300,0,500,100))
        self.colliders.append(Collider(500,100,700,200))
        self.colliders.append(Collider(700,200,900,300))
        self.colliders.append(Collider(900,300,1100,400))
        self.colliders.append(Collider(1100,400,1300,500))
        self.extra = canvas.create_rectangle(0,0,0,0)

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
            if 'd' in self.keys and not player.collided_right:
                if abs(player.vel_x) < 10:
                    player.accelerate(1,0)
            if 'a' in self.keys and not player.collided_left:
                if abs(player.vel_x) < 10:
                    player.accelerate(-1,0)
            if 'w' in self.keys and not player.collided_up and player.collided_down:
                player.accelerate(0,15)
                self.key_release(None,'w')
            if 'r' in self.keys:
                player.y += 1
                self.key_release(None,'r')
            player.move()
            self.last_update = time.time()
            player.collided_right = False
            player.collided_left = False
            player.collided_up = False
            player.collided_down = False
            for i in self.colliders:
                i.render()
                l = i.has_collided(player.collider)#player.collider.has_collided(i)
                if l:
                    collided = True
                    x = player.x+25
                    y = player.y-50
                    half_x = (i.end_x-i.start_x)/2 + i.start_x
                    half_y = (i.end_y-i.start_y)/2 + i.start_y
                    if x > half_x:
                        x = player.collider.start_x
                    else:
                        x = player.collider.end_x
                    if y > half_y:
                        y = player.collider.start_y
                    else:
                        y = player.collider.end_y
                    _x = x
                    _y = y
                    x_num = 0
                    y_num = 0
                    while not (_x < i.start_x or _x > i.end_x) and not player.vel_x == 0:
                        _x -= player.vel_x
                        x_num += 1
                    while not (_y < i.start_y or _y > i.end_y) and (not player.vel_y == 0 or not player.gravity):
                        if not player.gravity:
                            _y -= -10
                        else:
                            _y -= player.vel_y
                        y_num += 1
                    if (y_num < x_num or player.vel_x == 0) and (not player.vel_y == 0 or not player.gravity):
                        y_direction = True
                    else:
                        y_direction = False
                    if not y_direction:
                        player.vel_x -= player.vel_x*2
                        if x < half_x:
                            player.collided_right = True
                        else:
                            player.collided_left = True
                    else:
                        player.vel_y -= player.vel_y*2
                        if y < half_y:
                            player.collided_up = True
                        else:
                            player.collided_down = True


            root.update()


class Player:
    def __init__(self):
        self.x = 300
        self.y = 400

        self.collider = Collider(self.x,self.y,self.x+50,self.y-100)

        self.vel_x = 0
        self.vel_y = 0

        self.skin = canvas.create_rectangle(0,0,0,0)

        self.collided_up = False
        self.collided_down = False
        self.collided_left = False
        self.collided_right = False

        self.gravity = True
    def accelerate(self,x,y):
        self.vel_x += x
        self.vel_y += y
    def set_vel(self,x,y):
        self.vel_x = x
        self.vel_y = y
    def move(self):
        if not self.collided_down:
            self.gravity = True
        #    if self.vel_y > -10:
            self.accelerate(0,-.5)
        else:
            self.gravity = False

        print(self.collided_up)
        print(self.collided_down)
        print(self.collided_left)
        print(self.collided_right)
        print('')
        self.x += self.vel_x
        self.y += self.vel_y
        self.collider.start_x = self.x
        self.collider.start_y = self.y-100
        self.collider.end_x = self.x+50
        self.collider.end_y = self.y
        self.vel_x -= self.vel_x/10.0
        self.vel_y -= self.vel_y/10.0
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
        if object.end_x >= self.start_x and corner == False:
            if object.end_x <= self.end_x:
                if object.start_y >= self.start_y:
                    if object.start_y <= self.end_y:
                        corner = 1
        if object.end_x >= self.start_x and corner == False:
            if object.end_x <= self.end_x:
                if object.end_y >= self.start_y:
                    if object.end_y <= self.end_y:
                        corner = 1
        if object.start_x >= self.start_x and corner == False:
            if object.start_x <= self.end_x:
                if object.end_y >= self.start_y:
                    if object.end_y <= self.end_y:
                        corner = 1
        elif object.has_collided2(self):
            corner = True
        self.collided = corner
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
        if not self.collided == False:
            self.skin = canvas.create_rectangle(x1,y1,x2,y2,fill='green',outline='red')
        else:
            self.skin = canvas.create_rectangle(x1,y1,x2,y2,fill='red',outline='green')

game = Game()
player = Player()

root.bind('<KeyPress>',game.key_press)
root.bind('<KeyRelease>',game.key_release)

while game.loop:
    game.update()
