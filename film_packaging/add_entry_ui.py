from tkinter import *

from db_parse import *

MAIN_WINDOW_WIDTH = 600
MAIN_WINDOW_HEIGHT = 600
PADDING = 10


root = Tk()
root.geometry(str(MAIN_WINDOW_WIDTH) + "x" + str(MAIN_WINDOW_HEIGHT))
root.resizable(width=FALSE, height=FALSE)
root.update()

root.mainloop()
