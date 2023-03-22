import tkinter as tk
from tkinter import ttk
import os


root = tk.Tk()
root.title("Kalkulator kalorii")
root.option_add("*tearOff", False)

#setting the theme of the app
style = ttk.Style(root)
file_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "forest-dark.tcl")
root.tk.call("source", file_path)
style.theme_use("forest-dark")

#positioning the window
height = 700
width = 500
screen_width = root.winfo_screenwidth()  
screen_height = root.winfo_screenheight() 
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry('%dx%d+%d+%d' % (width, height, x, y))

root.mainloop()