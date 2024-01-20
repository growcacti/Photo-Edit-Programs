from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps
import os

class PhotoEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Photo Editor")
        self.root.geometry("640x640")
        self.img_path = None
      
        self.create_widgets()
    
    def create_widgets(self):
        # Top controls
        self.blurr = Label(self.root, text="Blur:", font=("ariel 17 bold"))
        self.blurr.grid(row=0, column=0, sticky=W)
        self.v1 = IntVar()
        self.scale1 = ttk.Scale(self.root, from_=0, to=10, variable=self.v1, orient=HORIZONTAL)
        self.scale1.grid(row=0, column=1, sticky=W)
        # ... similar for brightness, contrast, etc.

        # Canvas in the middle
        self.canvas2 = Canvas(self.root, width="600", height="420", relief=RIDGE, bd=2)
        self.canvas2.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        # Bottom buttons
        self.btn1 = Button(self.root, text="Select Image", bg='black', fg='gold', font=('ariel 15 bold'), relief=GROOVE)
        self.btn1.grid(row=2, column=0, padx=10, pady=10)
        self.btn2 = Button(self.root, text="Save", bg='black', fg='gold', font=('ariel 15 bold'), relief=GROOVE)
        self.btn2.grid(row=2, column=1, padx=10, pady=10)
        self.btn3 = Button(self.root, text="Exit", bg='black', fg='gold', font=('ariel 15 bold'), relief=GROOVE)
        self.btn3.grid(row=2, column=2, padx=10, pady=10)



    def selected(self):
        img_path = filedialog.askopenfilename(initialdir=os.getcwd())
        self.img= Image.open(img_path)
        img.thumbnail((350, 350))
        # imgg = img.filter(ImageFilter.BoxBlur(0))
        img1 = ImageTk.PhotoImage(img)
        self.canvas2.create_image(300, 210, image=img1)
        self.canvas2.image = img1


    
    def blur(self, event):
        for m in range(0, v1.get() + 1):
            self.img= Image.open(img_path)
            img.thumbnail((350, 350))
            imgg = img.filter(ImageFilter.BoxBlur(m))
            img1 = ImageTk.PhotoImage(imgg)
            self.canvas2.create_image(300, 210, image=img1)
            self.canvas2.image = img1


    
    def brightness(self, event):
        for m in range(0, v2.get() + 1):
            self.img= Image.open(img_path)
            img.thumbnail((350, 350))
            imgg = ImageEnhance.Brightness(img)
            img2 = imgg.enhance(m)
            img3 = ImageTk.PhotoImage(img2)
            canvas2.create_image(300, 210, image=img3)
            canvas2.image = img3
          


  

 
       
    

# Main script
if __name__ == "__main__":
    root = Tk()
    app = PhotoEditor(root)
    root.mainloop()
