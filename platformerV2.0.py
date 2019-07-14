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
        self.game_start = time.time()
        self.last_update = time.time()

        self.screen_width = root.winfo_screenwidth()
        self.screen_height = root.winfo_screenheight()
        self.screen_diff_x = self.screen_width/1040
        self.screen_diff_y = self.screen_height/900

        self.start_screen = True
        self.pause_screen = False
        self.level_complete_screen = False
        self.you_died_screen = False

        self.coin_img = PhotoImage(file='IMG_1073.gif')
        scale = int(1032/50)
        self.coin_img = self.coin_img.subsample(scale,scale)
        self.platform_img = PhotoImage(file='IMG_1079.gif')
        scale_x = int(1000/100)
        scale_y = int(400/25)
        self.platform_img = self.platform_img.subsample(scale_x,scale_y)
        self.bg = PhotoImage(file='bg.gif')
        scale_x = int(self.screen_width/40)
        scale_y = int(self.screen_height/25)
        self.bg = self.bg.zoom(scale_x,scale_y)
        self.bg_x = 0
        self.bg_2 = PhotoImage(file='bg_2.gif')
        scale_x = int(self.screen_width/40)
        scale_y = int(self.screen_height/25)
        self.bg_2 = self.bg_2.zoom(scale_x,scale_y)
        self.bg_2_x = self.screen_width

        self.loop = True

        self.level = 2

        self.keys = []

        self.timer = time.time()

        self.mirrored = []

        self.colliders = [Collider(0,0,self.screen_width,50),Collider(0,0,50,self.screen_height),Collider(0,self.screen_height-50,self.screen_width,self.screen_height),Collider(self.screen_width-50,self.screen_height,self.screen_width,0)]
        self.blocks = []

        self.coins = []
        self.geysers = []
        self.time = None
        self.started = False
        self.done_starting = False

        self.geyser_levels = 6
        self.mirror_levels = 10
        self.mirror_geyser_levels = 14

        self.extra = canvas.create_rectangle(0,0,0,0)

    def set_coins(self):
        self.coins = []
        self.blocks = []
        if self.level == 1:
            for i in range(4):
                x = i*300
                self.coins.append(Collider(x+50,100,x+100,150,image=self.coin_img))
            for i in range(4):
                x = i*300+1250
                y = i*100+200
                self.coins.append(Collider(x,y,x+50,y+50,image=self.coin_img))
            for i in range(4):
                x = i*300+2450
                y = 400 - i*100
                self.coins.append(Collider(x,y,x+50,y+50,image=self.coin_img))
            for i in range(8):
                x = i*300+3650
                y = i*100+200
                self.coins.append(Collider(x,y,x+50,y+50,image=self.coin_img))
            for i in range(2):
                x = i*300+6050
                y = 900 - i*800
                self.coins.append(Collider(x,y,x+50,y+50,image=self.coin_img))
        elif self.level == 2:
            self.coins.append(Collider(50,100,100,150,image=self.coin_img))
            self.coins.append(Collider(400,100,450,150,image=self.coin_img,moving_x=300,starting_pos_x=0))
            self.coins.append(Collider(1000,100,1050,150,image=self.coin_img,moving_x=300,starting_pos_x=300))
            self.coins.append(Collider(1600,100,1650,150,image=self.coin_img,moving_y=300,starting_pos_y=0))
            self.coins.append(Collider(2000,400,2050,450,image=self.coin_img,moving_y=300,starting_pos_y=300))
            self.coins.append(Collider(2300,700,2350,750,image=self.coin_img,moving_y=300,starting_pos_y=0,moving_x=300,starting_pos_x=0))
            self.coins.append(Collider(2700,1000,2750,1050,image=self.coin_img,moving_x=400,starting_pos_x=0))
            self.coins.append(Collider(2700,100,2750,150,image=self.coin_img,moving_x=400,starting_pos_x=400))
            for i in range(5):
                x = i*300+3400
                y = i*100+200
                self.coins.append(Collider(x,y,x+50,y+50,image=self.coin_img))
            self.coins.append(Collider(3400,100,34 50,150,image=self.coin_img,moving_y=700,starting_pos_y=0,moving_x=700,starting_pos_x=0))
    def set_platforms(self):
        self.colliders = [Collider(0,0,50000,15),Collider(0,0,15,self.screen_height),Collider(0,self.screen_height-15,self.screen_width,self.screen_height)]
        for i in self.coins:
            x1 = i.starting_x - 50
            x2 = i.starting_x + 50
            y1 = i.starting_y - 60
            y2 = i.starting_y - 35
            self.colliders.append(Collider(x1,y1,x2,y2,image=self.platform_img,mirror=i.mirror,moving_x=i.moving_x,starting_pos_x=i.starting_pos_x,moving_y=i.moving_y,starting_pos_y=i.starting_pos_y))
        for i in self.blocks:
            self.colliders.append(i)


    def set_geysers(self):
        self.geysers = []

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
        if not self.start_screen and not self.pause_screen and not self.level_complete_screen and not self.you_died_screen:
            if self.delta_time > 0:
                canvas.delete(ALL)
                if player.x > self.bg_x + self.screen_width*1.5:
                    self.bg_x += self.screen_width*2
                if player.x > self.bg_2_x + self.screen_width*1.5:
                    self.bg_2_x += self.screen_width*2
                while player.x < self.bg_x - self.screen_width*.5:
                    self.bg_x -= self.screen_width*2
                if player.x < self.bg_2_x - self.screen_width*.5:
                    self.bg_2_x -= self.screen_width*2
                canvas.create_image(game.screen_width/2-player.x+self.bg_x,player.y-game.screen_height/7, anchor=NW, image=self.bg)
                canvas.create_image(game.screen_width/2-player.x+self.bg_2_x,player.y-game.screen_height/7, anchor=NW, image=self.bg_2)
                if self.started:
                    if not self.time == None:
                        timer = int(self.time-self.timer)
                        size = 100
                        x = self.screen_width/2
                        y = self.screen_height/2
                        word = 'Time: '
                    else:
                        timer = int(time.time()-self.timer)
                        size = 25
                        x = self.screen_width-100
                        y = 100
                        word = 'Timer: '
                    canvas.create_text(x,y,text=word+str(timer),font=('TkTextFont',size))
                if len(self.coins) == 0:
                    self.set_coins()
                    self.set_platforms()
                    self.set_geysers()
                player.render()
                forwards = False
                backwards = False
                player_speed = (self.delta_time)*75#100 p/s: dt/s*100
                if 'd' in self.keys:
                    forwards = True
                    player.accelerate(2,0)
                    self.started = True
                if 'a' in self.keys:
                    backwards = True
                    player.accelerate(-2,0)
                    self.started = True
                if 'r' in self.keys:
                    player.x = 51
                    player.y = 400
                if 'Escape' in self.keys:
                    self.pause_screen = True
                    self.keys = []
                if player.walks == 2:
                    player.walks = 0
                if forwards == True:
                    player.walks += 1
                    player.direction = 'forward'
                elif backwards == True:
                    player.walks += 1
                    player.direction = 'backward'
                self.last_update = time.time()
                if self.started and not self.done_starting:
                    self.done_starting = True
                    self.timer = time.time()
                #Gravty
                player.accelerate(0,-1)
                for i in self.colliders:
                    i.render()
                    l = i.has_collided(player.collider)#player.collider.has_collided(i)
                #    print(len(self.colliders))
                #    print(i)
                #    print('')
                #    for q in self.colliders:
                #        print(q)
                #    print(self.colliders.index(i))
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
                                    player.accelerate(0,40)
                                    self.key_release(None,'w')
                                if i.moving_x > 0 and i.direction_x == 'up':
                                    player.x += 2
                                elif i.moving_x > 0 and i.direction_x == 'down':
                                    player.x -= 2
                                if i.moving_y > 0 and i.direction_y == 'up':
                                    player.y += 2
                                elif i.moving_y > 0 and i.direction_y == 'down':
                                    player.y -= 2
                            else:
                                player.y = i.start_y
                                player.vel_y -= abs(player.vel_y)
                        try:
                            if self.colliders.index(i) == 0:
                                self.set_coins()
                                self.set_platforms()
                                self.keys = []
                                self.you_died_screen = True
                                player.x = 51
                                player.y = 400
                                player.vel_y = -15
                        except:
                            pass

                for i in self.coins:
                    i.render()
                    platform = self.colliders[self.coins.index(i)+3]
                    x1 = i.start_x - 25
                    x2 = i.start_x + 75
                    y1 = i.end_y - 85
                    y2 = i.end_y - 60
                    #platform.start_x = x1
                    #platform.end_x = x2
                    #platform.start_y = y1
                    #platform.end_y = y2
                    if i.has_collided(player.collider):
                        self.coins.remove(i)
                        canvas.delete(i.skin)
                        if len(self.coins) == 0:
                            self.level += 1
                            self.level_complete_screen = True
                            self.keys = []
                            player.x = 51
                            player.y = 400
                            player.vel_y = -15
                            self.set_coins()
                            self.set_geysers()
                            self.set_platforms()
                for i in self.geysers:
                    i.render()
                    i.update()
                    if i.collider.has_collided(player.collider):
                        self.set_coins()
                        self.set_platforms()
                        self.keys = []
                        self.you_died_screen = True
                        player.x = 51
                        player.y = 400
                        player.vel_y = -15
                player.move(player_speed)
                root.update()
        else:
            if self.start_screen:
                canvas.delete(ALL)
                canvas.create_image(0,0, anchor=NW, image=self.bg)
                canvas.create_text(self.screen_width/2,self.screen_height/2-self.screen_height/10,text='game',font=('TkTextFont',100),anchor=CENTER,fill='gray60')
                canvas.create_text(self.screen_width/2,self.screen_height/2+self.screen_height/7,text='press any key to start',font=('TkTextFont',50),anchor=CENTER,fill='gray25')
                if len(self.keys) > 0:
                    self.start_screen = False
                    self.keys = []
            elif self.pause_screen:
                canvas.delete(ALL)
                canvas.create_image(0,0, anchor=NW, image=self.bg)
                canvas.create_text(self.screen_width/2,self.screen_height/2-self.screen_height/10,text='paused',font=('TkTextFont',100),anchor=CENTER,fill='gray60')
                canvas.create_text(self.screen_width/2,self.screen_height/2+self.screen_height/7,text='press any key to continue',font=('TkTextFont',50),anchor=CENTER,fill='gray25')
                player.render()
                for i in self.colliders:
                    i.render()
                for i in self.coins:
                    i.render()
                for i in self.geysers:
                    i.render()
                if len(self.keys) > 0:
                    self.pause_screen = False
                    self.keys = []
            elif self.level_complete_screen:
                canvas.delete(ALL)
                canvas.create_image(0,0, anchor=NW, image=self.bg)
                canvas.create_text(self.screen_width/2,self.screen_height/2-self.screen_height/10,text='Level Complete!',font=('TkTextFont',100),anchor=CENTER,fill='gray60')
                canvas.create_text(self.screen_width/2,self.screen_height/2+self.screen_height/7,text='press any key to continue',font=('TkTextFont',50),anchor=CENTER,fill='gray25')
                if len(self.keys) > 0:
                    self.level_complete_screen = False
                    self.keys = []
            elif self.you_died_screen:
                canvas.delete(ALL)
                canvas.create_image(0,0, anchor=NW, image=self.bg)
                canvas.create_text(self.screen_width/2,self.screen_height/2-self.screen_height/10,text='You Died',font=('TkTextFont',100),anchor=CENTER,fill='gray60')
                canvas.create_text(self.screen_width/2,self.screen_height/2+self.screen_height/7,text='press any key to restart',font=('TkTextFont',50),anchor=CENTER,fill='gray25')
                if len(self.keys) > 0:
                    self.you_died_screen = False
                    self.keys = []




            root.update()

class Player:
    def __init__(self):
        self.x = 51
        self.y = 400

        self.walks = 0

        self.collider = Collider(self.x,self.y,self.x+24,self.y-24)

        self.vel_x = 0
        self.vel_y = 0

        self.skin_1 = PhotoImage(file='IMG_1070.gif')
        self.skin_1 = self.skin_1.subsample(int(43),int(43))
        self.skin_2 = PhotoImage(file='IMG_1072.gif')
        self.skin_2 = self.skin_2.subsample(43,43)
        self.skin_1_backwards = PhotoImage(file='IMG_1075.gif')
        self.skin_1_backwards = self.skin_1_backwards.subsample(43,43)
        self.skin_2_backwards = PhotoImage(file='IMG_1076.gif')
        self.skin_2_backwards = self.skin_2_backwards.subsample(43,43)

        self.direction = 'forward'

        self.gravity = True
    def accelerate(self,x,y):
        self.vel_x += x
        self.vel_y += y
    def set_vel(self,x,y):
        self.vel_x = x
        self.vel_y = y
    def move(self,speed):
        self.x += self.vel_x*speed
        self.y += self.vel_y
        self.collider.start_x = self.x
        self.collider.start_y = self.y-24
        self.collider.end_x = self.x+24
        self.collider.end_y = self.y
        self.vel_x -= self.vel_x/5.0
        self.vel_y -= self.vel_y/5.0
        if abs(self.vel_x) < 0.1:
            self.vel_x = 0
        if abs(self.vel_y) < 0.1:
            self.vel_y = 0
    def render(self):
        x = game.screen_width/2-12#self.x
        y = game.screen_height - game.screen_height/3#game.screen_height - self.y
        #pos = game.fit_to_screen(self.x,self.y)
        #x = pos[0]
        #y = pos[1]
        if self.walks == 1:
            if self.direction == 'forward':
                self.label = canvas.create_image(x,y, anchor=NW, image=self.skin_1)
            else:
                self.label = canvas.create_image(x,y, anchor=NW, image=self.skin_1_backwards)
        else:
            if self.direction == 'forward':
                self.label = canvas.create_image(x,y, anchor=NW, image=self.skin_2)
            else:
                self.label = canvas.create_image(x,y, anchor=NW, image=self.skin_2_backwards)

class Collider:
    def __init__(self,start_x,start_y,end_x,end_y,image=None,mirror=False,starting_pos_x=0,starting_pos_y=0,moving_x=0,moving_y=0):
        self.start_x = min([start_x,end_x])
        self.start_y = min([start_y,end_y])
        self.end_x = max([start_x,end_x])
        self.end_y = max([start_y,end_y])
        self.mid_x = (self.end_x-self.start_x)/2+self.start_x
        self.mid_y = (self.end_y-self.start_y)/2+self.start_y

        self.starting_pos_x = starting_pos_x
        self.starting_pos_y = starting_pos_y
        self.moving_x = moving_x
        self.moving_y = moving_y
        self.direction_x = 'up'
        self.direction_y = 'up'
        self.starting_x = self.mid_x
        self.starting_y = self.mid_y
        if not self.moving_x == 0:
            self.start_x += self.starting_pos_x
            self.end_x += self.starting_pos_x
            self.mid_x += self.starting_pos_x
        if not self.moving_y == 0:
            self.start_y += self.starting_pos_y
            self.end_y += self.starting_pos_y
            self.mid_y += self.starting_pos_y

        self.mirror = mirror

        self.image = image

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
        if self.moving_x:
            if self.mid_x < self.starting_x+self.moving_x and self.direction_x == 'up':
                self.start_x += 2
                self.end_x += 2
                self.mid_x += 2
            elif self.direction_x == 'up':
                self.direction_x = 'down'
            if self.mid_x > self.starting_x and self.direction_x == 'down':
                if not self.moving_x < 0:
                    self.start_x -= 2
                    self.end_x -= 2
                    self.mid_x -= 2
            elif self.direction_x == 'down':
                self.direction_x = 'up'

        if self.moving_y:
            if self.mid_y < self.starting_y+self.moving_y and self.direction_y == 'up':
                if not self.moving_y < 0:
                    self.start_y += 2
                    self.end_y += 2
                    self.mid_y += 2
            elif self.direction_y == 'up':
                self.direction_y = 'down'
            if self.mid_y > self.starting_y and self.direction_y == 'down':
                if not self.moving_y < 0:
                    self.start_y -= 2
                    self.end_y -= 2
                    self.mid_y -= 2
            elif self.direction_y == 'down':
                self.direction_y = 'up'

        if self.start_x < player.x + game.screen_width/2 and self.end_x > player.x - game.screen_width/2:
            canvas.delete(self.skin)
            if not self.mirror:
                y = game.screen_height-(game.screen_height/3 + (self.start_y-player.y))
                x = game.screen_width/2 + (self.start_x-player.x)

                #pos = game.fit_to_screen(self.start_x,self.start_y)
                #x1 = pos[0]
                #y1 = pos[1]
                if self.image and not self.image == 'color':
                    canvas.create_image(x,y, anchor=SW, image=self.image)
                elif self.image == 'color':
                    canvas.create_rectangle(x1,y1,x2,y2,fill = 'gray',outline='gray')
            else:
                y1 = game.screen_height/2 - self.start_y
                y2 = game.screen_height/2 - self.end_y
                x1 = self.start_x
                x2 = self.end_y
                if self.image and not self.image == 'color':
                    canvas.create_image(x1,y1, anchor=SW, image=self.image)
                elif self.image == 'color':
                    canvas.create_rectangle(x1,y1,x2,y2,fill = 'gray',outline='gray')
class Geyser:
    def __init__(self,x,time_between):
        self.x = x
        self.y = 0
        self.time = time_between
        self.start_time = time.time()
        self.speed = random.randint(5,20)
        if random.randint(0,1) == 1:
            self.extending = True
            self.wait = 0
        else:
            self.extending = False
            self.wait = random.randint(1,2)
        self.deextending = False
        self.collider = Collider(self.x-25,0,self.x+25,self.y)

    def update(self):
        if time.time()-self.start_time > self.time and not self.extending and not self.deextending and time.time()-self.start_time > self.wait:
            self.extending = True
            self.wait = True
        if self.extending:
            if not self.y > game.screen_height:
                self.y += self.speed
            else:
                self.extending = False
                self.deextending = True
        elif self.deextending:
            if not self.y == 0:
                self.y -= self.speed
            else:
                self.deextending = False
                self.start_time = time.time()
        self.collider.start_x = self.x-25
        self.collider.end_x = self.x+25
        self.collider.start_y = 0
        self.collider.end_y = self.y
    def render(self):
        y1 = game.screen_height
        y2 = game.screen_height - self.y
        canvas.create_rectangle(self.x-25,y1,self.x+25,y2,fill='blue')



game = Game()
player = Player()

root.bind('<KeyPress>',game.key_press)
root.bind('<KeyRelease>',game.key_release)

while game.loop:
    game.update()
