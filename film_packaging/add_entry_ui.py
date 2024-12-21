from db_parse import *
from tkinter import *

MAIN_WINDOW_WIDTH = 600
MAIN_WINDOW_HEIGHT = 600
PADDING = 10
LF_WIDTH = 100
LF_HEIGHT = 50

root = Tk()

root.title("film")
root.geometry(str(MAIN_WINDOW_WIDTH) + "x" + str(MAIN_WINDOW_HEIGHT))
root.resizable(width=FALSE, height=FALSE)

lf1 = LabelFrame(root, text="test1", width=LF_WIDTH, height=LF_HEIGHT)
lf1.grid(row=0, column=0)

root.update()


root.mainloop()
