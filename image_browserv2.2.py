import tkinter as tk
from tkinter import ttk, Scrollbar,VERTICAL,Frame,W,E,S,N,Button
from tkinter import filedialog as fd
from tkinter import messagebox as ms
import time
import os
import sys
import PIL
from PIL import ImageTk, Image



Image.MAX_IMAGE_PIXELS = None  

class Image_browser:
    def __init__(self, root):
        # self. is our root window
        self.root = root
        # Canvas Size
        self.area = (700, 500)
        # Creates All Of Our Widgets
        self.setup_gui(self.area)
        self.img = None
        self.button = Button(
            self.root,
            text="get image directory",
            bd=12,
            bg="lavender",
            command=self.list_files,
        )
        self.button.grid(row=13, column=8)
        self.button = Button(
            self.root,
            text="new directory",
            bd=10,
            bg="lavender",
            command=self.newdirlist,
        )
        self.button.grid(row=16, column=8)
        self.path = "/home/jh/Pictures"
        self.file = None
        self.data =[]
    def setup_gui(self, area):
        self.area = area
        self.tree = ttk.Treeview(self.root, columns=("Size", "Type", "Modified"))
        self.tree.heading("#0", text="File Name")
        self.tree.heading("Size", text="Size (KB)")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Modified", text="Last Modified")
        self.tree.grid(row=0, column=0, rowspan=15, sticky="nswe")

        # Replace Scrollbar to work with Treeview
        self.sc = Scrollbar(self.root, orient=VERTICAL, command=self.tree.yview)
        self.sc.grid(row=0, rowspan=15, column=3, sticky='ns')
        self.tree.configure(yscrollcommand=self.sc.set)
        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.tree
  
       

        self.canvas = tk.Canvas(
            self.root,
            height=self.area[1],
            width=self.area[0],
            bg="black",
            bd=10,
            relief="ridge",
        )
        self.canvas.grid(row=2, column=1)
        txt = """
    0                             !
                No Image
        """
        # Text On Canvas Saying No Current Image Open.
        self.wt = self.canvas.create_text(
            self.area[0] / 2 - 270,
            self.area[1] / 2,
            text=txt,
            font=("", 30),
            fill="white",
        )
        self.frame = Frame(self.root, bg="white", padx=10, pady=10)
        btn_open = tk.Button(
            self.frame,
            text="Open New Image",
            bd=2,
            fg="white",
            bg="black",
            font=("", 15),
            command=self.make_image,
        )
        btn_open.grid(row=8, column=11)
        self.frame.grid(row=1, column=2)
        # Status Bar
        self.status = tk.Label(
            self.root,
            text="Image Browser    Current Image: None",
            bg="gray",
            font=("Ubuntu", 15),
            bd=2,
            fg="black",
            relief="sunken",
            anchor=W,
        )
        self.status.grid(row=0, column=1)
        self.list_files

    def treeview_sort_column(self, tv, col, reverse):
        # Extract the data from the column and pair it with the row id
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        # Sort the list in the desired order (ascending or descending)
        l.sort(reverse=reverse)

        # Rearrange the items in the Treeview based on the sorted order
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # Toggle the sorting order for the next click
        tv.heading(col, command=lambda: self.treeview_sort_column(tv, col, not reverse))


    def list_files(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

            
        # Define a list of image extensions
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

        # Add new files from the selected directory
        for file in os.listdir(self.path):
            file_path = os.path.join(self.path, file)
            file_size = os.path.getsize(file_path) // 1024  # Size in KB
            # Determine if the file is an image
            file_type = 'Image' if any(file.endswith(ext) for ext in image_extensions) else 'Other'
            modified_time = time.ctime(os.path.getmtime(file_path))

            self.tree.insert('', 'end', text=file, values=(file_size, file_type, modified_time))

        # Clear the current image display if there's any
        self.canvas.delete('all')
        self.status["text"] = "Image Browser    Current Image: None"

    def showcontent(self, event):
        selected_item = self.tree.selection()

        if selected_item:
            file_name = self.tree.item(selected_item[0], 'text')
            full_path = os.path.join(self.path, file_name)

            # Check if the path is a file and not a directory
            if os.path.isfile(full_path):
                try:
                    self.loaded_img = Image.open(full_path)
                    re = self.loaded_img.resize((700, 500), Image.Resampling.LANCZOS)
                    self.img = ImageTk.PhotoImage(re)
                    self.canvas.delete('all')
                    self.canvas.create_image(
                        self.area[0] / 2 + 10,
                        self.area[1] / 2 + 10,
                        anchor='center',
                        image=self.img,
                    )
                    self.status["text"] = "Image Browser   Current Image: " + full_path
                   
                except Exception as e:
                    ms.showerror("Error", f"Error loading image: {e}")
                    self.status["text"] = "Error loading image"
            else:
                ms.showinfo("Information", "Selected item is not an image file")
                self.status["text"] = "Selected item is not an image file"

    def newdirlist(self):
        new_path = fd.askdirectory()
        if new_path:
            try:
                self.path = new_path
                os.chdir(self.path)
                self.list_files()
                self.status["text"] = f"Directory changed to {self.path}"
            except Exception as e:
                ms.showerror("Error", f"Error accessing directory: {e}")


    def opensystem(self, event):
        x = self.tree.curselection()[0]
        os.system(self.tree.get(x))
        self.showcontent(event)


    def on_select(self, event):
        selected_item = self.tree.selection()
        self.showcontent(event)




    def open_folder(self):
        self.path = fd.askdirectory(title="Select Folder to open")
        os.listdir(self.path)
        flist = os.listdir()
        for item in flist:
            self.tree.insert(tk.END, item)
            self.data.append(item)

    def clear(self):
        self.tree.delete(END, 0)

        flist = os.listdir(self.path)
        for item in flist:
            self.tree.insert(tk.END, item)

    def make_image(self):
        try:
            # Specify file types
            filetypes = (
    ('PNG files', '*.png'),
    ('JPEG files', '*.jpg'),
    ('JPEG files', '*.jpeg'),
    ('GIF files', '*.gif'),
    ('BMP files', '*.bmp'),
    ('All files', '*.*')
)


            # Open File Dialog with specified image file types
            self.file = fd.askopenfilename(filetypes=filetypes)

            if self.file:  # Check if a file was selected
                self.loaded_img = Image.open(self.file)
                re = self.loaded_img.resize((700, 500), Image.Resampling.LANCZOS)
                self.img = ImageTk.PhotoImage(re)
                self.canvas.delete('all')
                self.canvas.create_image(
                    self.area[0] / 2 + 10,
                    self.area[1] / 2 + 10,
                    anchor='center',
                    image=self.img,
                )
                self.status["text"] = "Image Browser Current Image: " + self.file
        except Exception as e:
            print(f"Error loading image: {e}")
            self.status["text"] = "Error loading image"

               

    
if __name__== "__main__":
    root = tk.Tk()
    img = Image_browser(root)
    root.mainloop()
    
   
