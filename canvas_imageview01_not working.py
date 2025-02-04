import tkinter as tk
import glob
import os
from tkinter import filedialog

cd = os.getcwd()
print(cd)


from PIL import Image
import os


def listimg():
    path = "/home/jh/Desktop/imagefolder"
    lst_files = []
    for f in os.listdir(path):
        if f.endswith(".png") or f.endswith(".PNG"):
            lst_files = [f]
    w = 800
    h = 600


def insertfiles():
    for filename in glob.glob("*.png"):
        lst.insert(1, filename)


def showimg(event):
    n = lst.curselection()
    filename = lst.get(n)
    img = tk.PhotoImage(file=filename)
    w, h = img.width(), img.height()
    print(filename)
    canvas.image = img
    canvas.config(width=w, height=h)
    canvas.create_image(0, 0, image=img, anchor=tk.NW)


listimg()
root = tk.Tk()
root.geometry("800x600+300+50")
lst = tk.Listbox(root, width=20)
lst.pack(side="left", fill=tk.BOTH, expand=0)
lst.bind("<<ListboxSelect>>", showimg)
insertfiles()
canvas = tk.Canvas(root)
canvas.pack()
listimg()


root.mainloop()
