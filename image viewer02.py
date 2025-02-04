import tkinter as tk
from tkinter import filedialog as fd
from tkinter.filedialog import askopenfilename


from tkinter import *
from PIL import Image, ImageTk
import os

root = Tk()
root.geometry("600x600")


def resize_image(root, copy_image, label1):
    new_height = 600
    new_width = 600
    image = copy_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    label1.configure(image=photo)
    label1.image = photo


def next():
    global n
    global itemslist
    n = (n+1) % len(itemslist)
    img1 = itemslist[n]

    image = Image.open(path+"/"+img1)
    copy_image = image.copy()
    photo = ImageTk.PhotoImage(image)

    label = Label(root, image=photo)
    label.bind('<configure>', resize_image(root, copy_image, label1))
    label.pack()


def previous():
    global n
    global itemslist
    n = (n-1) % len(itemslist)
    img1 = itemslist[n]

    image = Image.open(path+"/"+img1)
    copy_image = image.copy()
    photo = ImageTk.PhotoImage(image)

    label2 = Label(root, image=photo)
    label2.bind('<configure>', resize_image(root, copy_image, label1))
    label2.pack()

# defining open_file_chooser function
def open_file_chooser():
    filename = askopenfilename()
    print("You have selected : %s" % filename)

def open_path_chooser():
    path = fd.askdirectory()
    print("You have selected : %s" % filename)


# creating an instance of Tk
root = tk.Tk()
root.title("Example")

# Button : Open
open = tk.Button(root, text = "Open", command = open_path_chooser)
open.pack()


n = 0
path = 
itemslist = os.listdir(path)
img1 = itemslist[n]

image = Image.open(path+"/"+img1)
copy_image = image.copy()
photo = ImageTk.PhotoImage(image)

label1 = Label(root, image=photo)
label1.bind('<configure>', resize_image(root, copy_image, label1))
label1.pack()

btn1 = Button(root, text="next", width=5, height=10, command=next)
btn1.place(x=570, y=150)

btn2 = Button(root, text="prev", width=5, height=10, command=previous)
btn1.place(x=0, y=150)
btn3 = Button(root, text="next", width=5, height=10, command=open_file_chooser)
btn3.place(x=670, y=250)

root.mainloop()
