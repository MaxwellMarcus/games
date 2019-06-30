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

        self.level = 1

        self.keys = []

        self.colliders = [Collider(0,0,self.screen_width,50),Collider(0,0,50,self.screen_height),Collider(0,self.screen_height-50,self.screen_width,self.screen_height),Collider(self.screen_width-50,self.screen_height,self.screen_width,0)]
    #    self.colliders.append(Collider(0,75,100,100))
    #    self.colliders.append(Collider(300,175,400,200))
    #    self.colliders.append(Collider(600,275,700,300))
    #    self.colliders.append(Collider(0,475,100,500))
    #    self.colliders.append(Collider(300,375,400,400))
    #    self.colliders.append(Collider(300,575,400,600))
    #    self.colliders.append(Collider(600,675,700,700))
    #    self.colliders.append(Collider(900,575,1000,600))
    #    self.colliders.append(Collider(1200,475,1300,500))
    #    self.colliders.append(Collider(900,375,1000,400))
    #    self.colliders.append(Collider(900,175,1000,200))
    #    self.colliders.append(Collider(1200,75,1300,100))
    #    self.colliders.append(Collider(0,275,100,300))
    #    self.colliders.append(Collider(1200,275,1300,300))
    #    self.colliders.append(Collider(600,475,700,500))

        self.coins = []
    #    self.coins.append(Collider(25,110,75,160))
    #    self.coins.append(Collider(325,210,375,260))
    #    self.coins.append(Collider(625,310,675,360))
    #    self.coins.append(Collider(925,410,975,460))
    #    self.coins.append(Collider(1225,510,1275,560))
    #    self.coins.append(Collider(25,310,75,360))
    #    self.coins.append(Collider(325,410,375,460))
    #    self.coins.append(Collider(625,510,675,560))
    #    self.coins.append(Collider(925,610,975,660))
    #    self.coins.append(Collider(25,510,75,560))
    #    self.coins.append(Collider(325,610,375,660))
    #    self.coins.append(Collider(625,710,675,760))
    #    self.coins.append(Collider(1225,110,1275,160))
    #    self.coins.append(Collider(1225,310,1275,360))
    #    self.coins.append(Collider(925,210,975,260))

        self.extra = canvas.create_rectangle(0,0,0,0)

    def set_coins(self):
        self.coins = []
        if self.level == 2:
            self.coins.append(Collider(25,110,75,160))
            self.coins.append(Collider(325,210,375,260))
            self.coins.append(Collider(625,310,675,360))
            self.coins.append(Collider(925,410,975,460))
            self.coins.append(Collider(1225,510,1275,560))
            self.coins.append(Collider(25,310,75,360))
            self.coins.append(Collider(325,410,375,460))
            self.coins.append(Collider(625,510,675,560))
            self.coins.append(Collider(925,610,975,660))
            self.coins.append(Collider(25,510,75,560))
            self.coins.append(Collider(325,610,375,660))
            self.coins.append(Collider(625,710,675,760))
            self.coins.append(Collider(1225,110,1275,160))
            self.coins.append(Collider(1225,310,1275,360))
            self.coins.append(Collider(925,210,975,260))
        elif self.level == 1:
            self.coins.append(Collider(25,110,75,160))
            self.coins.append(Collider(325,210,375,260))
            self.coins.append(Collider(625,310,675,360))
            self.coins.append(Collider(925,410,975,460))
            self.coins.append(Collider(1225,510,1275,560))
        elif self.level == 3:
            self.coins.append(Collider(25,110,75,160))
            self.coins.append(Collider(400,210,450,260))
            self.coins.append(Collider(775,310,825,360))
            self.coins.append(Collider(1125,410,1175,460))
        elif self.level == 4:
            self.coins.append(Collider(25,110,75,160))
            self.coins.append(Collider(310,255,360,305))
            self.coins.append(Collider(585,400,635,450))
            self.coins.append(Collider(870,545,920,590))
    def set_platforms(self):
        self.colliders = [Collider(0,0,self.screen_width,50),Collider(0,0,50,self.screen_height),Collider(0,self.screen_height-50,self.screen_width,self.screen_height),Collider(self.screen_width-50,self.screen_height,self.screen_width,0)]
        for i in self.coins:
            x1 = i.start_x - 25
            x2 = i.start_x + 75
            y1 = i.end_y - 85
            y2 = i.end_y - 60
            self.colliders.append(Collider(x1,y1,x2,y2))
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
            canvas.delete(ALL)
            if len(self.colliders) <= 4:
                self.set_platforms()
            if len(self.coins) == 0:
                self.set_coins()
            player.render()
        #    player_speed = (self.delta_time)*500#100 p/s: dt/s*100
            if 'd' in self.keys:
                player.accelerate(1,0)
            if 'a' in self.keys:
                player.accelerate(-1,0)
            if 'r' in self.keys:
                player.x = 51
                player.y = 400
            self.last_update = time.time()
            #Gravty
            player.accelerate(0,-.5)
            for i in self.colliders:
                i.render()
                l = i.has_collided(player.collider)#player.collider.has_collided(i)
                if l:
                    collided = True
                    x = player.x+24
                    y = player.y-24
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
                    x_num = player.vel_x
                    y_num = player.vel_y
                    if x_num == 0 and y_num == 0:
                        x_num = 1
                        y_num = 1
                    done = False
                    while not done:
                        if _y < i.start_y or _y > i.end_y:
                            done = True
                            y_direction = True
                        elif _x < i.start_x or _x > i.end_x:
                            done = True
                            y_direction = False
                        _y -= y_num
                        _x -= x_num
                    if not y_direction:
                        if x > half_x:
                            player.vel_x += abs(player.vel_x*2)
                        else:
                            player.vel_x -= abs(player.vel_x*2)
                    else:
                        if y > half_y:
                            player.y = i.end_y+24
                            player.vel_y += abs(player.vel_y)
                            if 'w' in self.keys:
                                player.accelerate(0,20)
                                self.key_release(None,'w')
                        else:
                            player.y = i.start_y
                            player.vel_y -= abs(player.vel_y)
                    try:
                        if self.colliders.index(i) == 0:
                            self.set_coins()
                            self.set_platforms()
                            player.x = 51
                            player.y = 400
                            player.vel_y = -15
                    except:
                        pass

            for i in self.coins:
                i.render(color='yellow')
                if i.has_collided(player.collider):
                    self.coins.remove(i)
                    canvas.delete(i.skin)
                    if len(self.coins) == 0:
                        self.level += 1
                        self.set_coins()
                        self.set_platforms()
            player.move()
            root.update()
#            print('')


class Player:
    def __init__(self):
        self.x = 51
        self.y = 400

        self.walks = 0

        self.collider = Collider(self.x,self.y,self.x+24,self.y-24)

        self.vel_x = 0
        self.vel_y = 0

        self.skin_1 = PhotoImage(file='IMG_1070.gif')
        self.skin_1 = self.skin_1.subsample(43,43)
        self.skin_2 = PhotoImage(file='IMG_1072.gif')
        self.skin_2 = self.skin_2.subsample(43,43)

        self.gravity = True
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
        self.collider.start_y = self.y-24
        self.collider.end_x = self.x+24
        self.collider.end_y = self.y
        self.vel_x -= self.vel_x/10.0
        self.vel_y -= self.vel_y/10.0
        if abs(self.vel_x) < 0.1:
            self.vel_x = 0
        if abs(self.vel_y) < 0.1:
            self.vel_y = 0
    def render(self):
        x = self.x
        x2 = self.x + 24
        y = game.screen_height - self.y
        y2 = game.screen_height- (self.y-24)
        if self.walks < 6:
            self.label = canvas.create_image(x,y, anchor=NW, image=self.skin_1)
        else:
            self.label = canvas.create_image(x,y, anchor=NW, image=self.skin_2)
        if self.walks == 10:
            self.walks = 0
        else:
            self.walks += 1

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
    def render(self,color=None):
        canvas.delete(self.skin)
        y1 = game.screen_height - self.start_y
        y2 = game.screen_height - self.end_y
        x1 = self.start_x
        x2 = self.end_x
        if color:
            self.skin = canvas.create_rectangle(x1,y1,x2,y2,fill = color,outline=color)
        else:
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
