from tkinter import *

root = Tk()

canvas = Canvas(root, width = root.winfo_screenwidth(),height = root.winfo_screenheight())
canvas.pack()

class Enviroment:
    def setup(self):
        self.windowHeight = root.winfo_screenheight()
        self.windowWidth = root.winfo_screenwidth()

        self.grounds = [[0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0],
                        ]
        print(self.grounds)
        self.bg = canvas.create_rectangle(0,0,self.windowWidth,self.windowHeight,fill = "blue")

        self.base = canvas.create_rectangle(0,self.windowHeight,self.windowWidth,self.windowHeight - self.windowHeight/10,fill = "brown")
        self.grounds[9] = [1,1,1,1,1,1,1,1,1,1]
        print(self.grounds)

class Player:
    def setup(self):
        print("Player")

enviroment = Enviroment()
enviroment.setup()

while True:
    root.update()
