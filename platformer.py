try:
    from tkinter import *
except:
    from Tkinter import *
import time
import math
root = Tk()
canvas = Canvas(root,width=root.winfo_screenwidth(),height=root.winfo_screenheight())
canvas.pack()

bg = PhotoImage(file='bg.gif')
canvas.create_image(0,0,anchor=NW,image=bg)
while True:
    root.update()
