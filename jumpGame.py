from tkinter import *
import random
import time

root = Tk()

canvas = Canvas(root, width = root.winfo_screenwidth(),height = root.winfo_screenheight(),background = "blue")
canvas.pack()

class Enviroment:
    def setup(self):
        self.x = 10
        self.y = 10
        self.windowHeight = root.winfo_screenheight()
        self.windowWidth = root.winfo_screenwidth()

        self.grounds = []

        i = 0
        while i < self.y:
            k = 0
            x = []
            while k < self.x:
                x.append([0,1])
                k += 1
            self.grounds.append(x)
            i += 1

        i = 0
        while i < 10:
            self.grounds[9][i] = [1,1]
            i += 1

        i = 0
        lastBlock = 9
        twoLastBlock = 9
        threeLastBlock = 9
        while i < 9:
            if i == 0:
                block = random.randint(0,8)
                while block == 4:
                    random.randint(0,8)
            else:
                block = lastBlock + random.randint(-2,2)
                while block == lastBlock or block == twoLastBlock or block > 8 or block < 0 or block == threeLastBlock:
                    block = lastBlock + random.randint(-2,2)
            self.grounds[i][block][0] = 1
            threeLastBlock = twoLastBlock
            twoLastBlock = lastBlock
            lastBlock = block
            i += 1
    def render(self):
        canvas.delete(ALL)
        i = 0
        while i < len(self.grounds):
            k = 0
            while k < len(self.grounds[i]):
                if self.grounds[i][k][0] == 1:
                    if self.grounds[i][k][1] == 1:
                        canvas.create_rectangle(self.windowWidth/10 * k + self.windowWidth/20 + self.windowWidth/20,self.windowHeight/10 * i + self.windowHeight/20 + self.windowHeight/20,self.windowWidth/10 * k + self.windowWidth/20 - self.windowWidth/20,self.windowHeight/10 * i + self.windowHeight/20 - self.windowHeight/20,fill = "red")
                    else:
                        canvas.create_rectangle(self.windowWidth/10 * k + self.windowWidth/20 + self.windowWidth/20,self.windowHeight/10 * i + self.windowHeight/20 + self.windowHeight/20,self.windowWidth/10 * k + self.windowWidth/20 - self.windowWidth/20,self.windowHeight/10 * i + self.windowHeight/20 - self.windowHeight/20,fill = "green")
                k += 1
            i += 1

class Player:
    def setup(self):
        self.x = 4
        self.y = 8

    def left(event,self):
        self.x -= 1
        print(self.x)
        print(self.y)
    def right(event,self):
        self.x += 1
        print(self.x)

    def render(self):
        enviroment.grounds[self.y][self.x] = [1,0]

enviroment = Enviroment()
enviroment.setup()

player = Player()
player.setup()

root.bind("a",player.left)
root.bind("d",player.right)
while True:
    player.render()
    enviroment.render()

    root.update()
