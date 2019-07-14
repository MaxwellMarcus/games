try:
    from tkinter import *
except:
    from Tkinter import *
import time
import math
root = Tk()
bg = PhotoImage(file='bg_3.gif')
canvas = Canvas(root,width=root.winfo_screenwidth(),height=root.winfo_screenheight(),bg=bg)
canvas.pack(fill=BOTH,expand=YES)

canvas.create_image(0,0,anchor=NW,image=bg)
canvas.addtag_all('all')
canvas.scale('all',0,0,10,10)
while True:
    root.update()
