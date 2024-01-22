import tkinter as tk
from tkinter import ttk, Scrollbar,VERTICAL,Frame,W,E,S,N,Button 
from tkinter.filedialog import askopenfilename,asksaveasfilename,askdirectory
from tkinter import simpledialog
from tkinter import messagebox as ms
import time
import os
import sys
import PIL
from PIL import ImageTk, Image
from datetime import datetime
import threading

Image.MAX_IMAGE_PIXELS = None  
WHITE = (255,255,255)


def multi_img_file_resizer(parent):
    infostr =""" the small app will resize every image in a folder to the same percentage,
    an example input is 0.30 is 30%"""
    def resize_images(input_folder, resize_factor):
        output_folder = os.path.join(input_folder, 'resized_output')
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        for file in os.listdir(input_folder):
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_path = os.path.join(input_folder, file)
                try:
                    with Image.open(img_path) as img:
                        # Resizing the image
                        new_size = tuple(int(dim * resize_factor) for dim in img.size)
                        resized_img = img.resize(new_size, Image.Resampling.LANCZOS)
                        # Saving the resized image
                        resized_img.save(os.path.join(output_folder, file))
                        print(f"Resized and saved: {file}")
                except Exception as e:
                    print(f"Error processing {file}: {e}")

    def select_folder():
        folder_selected = askdirectory()
        if folder_selected:
            resize_factor = simpledialog.askfloat("Resize Factor", "Enter resize factor (e.g., 0.8 for 80%):", minvalue=0.1, maxvalue=1.0)
            if resize_factor:
                resize_images(folder_selected, resize_factor)

    
    select_button = tk.Button(parent, text="Select Folder and Resize Images", command=select_folder)
    select_button.grid(row=8, column=1)

class MenuBar(tk.Menu):
    def __init__(self, parent):
        tk.Menu.__init__(self, parent)
        self.parent = parent
        self.file_menu = tk.Menu(self, tearoff=0)
        self.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", underline=1, command=None) 
        self.file_menu.add_command(label="Open", command=self.open_image)
        self.file_menu.add_command(label="Save As", command=self.save_image)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=None)#self.parent.quit
        self.file_menu.add_command(label="   ", command=None)
        self.edit_menu = tk.Menu(self)
        self.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Flip", command=self.flip_image)
        self.edit_menu.add_command(label="Rotate", command=self.rotate_image)
        self.edit_menu.add_command(label="Blur", command=self.blur_image)
        self.edit_menu.add_command(label="Sharpen", command=self.sharpen_image)

      
        
        
        
        self.view_menu = tk.Menu(self)
        self.cursor_menu = tk.Menu(self)
        self.format_menu = tk.Menu(self)
        self.tool_menu = tk.Menu(self)

    def open_image(self):
        file_path = askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tiff *.ico")])
        if file_path:
            self.loaded_image = Image.open(file_path)
            self.update_image()
    def copyshift_image(self):
        self.current_image = image_browser.get_current_image()
        nb.set_image_on_edit_tab(self.current_image)
        
    def save_image(self):
        if self.loaded_image:
            file_path = asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
            if file_path:
                self.loaded_image.save(file_path)

    def update_image(self):
        if self.loaded_image:
            photo = ImageTk.PhotoImage(self.loaded_image)
            self.canvas.config(image=photo)
            self.label.image = photo

    def flip_image(self):
        if self.loaded_image:
            self.loaded_image = self.loaded_image.transpose(Image.FLIP_LEFT_RIGHT)
            self.update_image()
    def rotate_image(self):
        if self.loaded_image:
            degrees = self.rotate_scale.get()  # Get the value from the scale widget
            self.loaded_image = self.loaded_image.rotate(degrees)
            self.update_image()
    def blur_image(self):
        if self.loaded_image:
            self.loaded_image = self.loaded_image.filter(ImageFilter.BLUR)
            self.update_image()

    def sharpen_image(self):
        if self.loaded_image:
            enhancer = ImageEnhance.Sharpness(self.loaded_image)
            self.loaded_image = enhancer.enhance(2.0)
            self.update_image()


    def brighten(self):
        try:
            brightness = float(value)
            enhanced_image = ImageEnhance.Brightness(original_image).enhance(brightness)
            updated_image = ImageTk.PhotoImage(enhanced_image)
            label.config(image=updated_image)
            label.image = updated_image
            brightness_scale = tk.Scale(parent, from_=0.1, to=2.0, resolution=0.1, orient="horizontal", label="Brightness", command=update_brightness)
            brightness_scale.set(1.0)  # Initial brightness value
            brightness_scale.grid(row=10,column=4)

        except ValueError as e:
            print(e)
class ScrollableNotebook(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set the geometry and title if desired
        self.geometry("1800x800")
        self.title("Image Manager App v3")
        

        menu = MenuBar(self)  # 'menu' is defined here
        self.config(menu=menu)  # Set the menu for the ScrollableNotebook window

       
        notebook_frame = tk.Frame(self, width=600,height=600)
        notebook_frame.grid(row=0, column=0,rowspan=4,columnspan=4, sticky="nsew")

        # Configure the grid to expand the frame
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

       
        self.canvas = tk.Canvas(notebook_frame, width=600,height=600)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Add a scrollbar to the frame
        scrollbar = ttk.Scrollbar(notebook_frame, orient="horizontal", command=self.canvas.xview)
        scrollbar.grid(row=23, column=0, sticky="ew")
        self.canvas.configure(xscrollcommand=scrollbar.set)

        # Configure the notebook frame grid
        notebook_frame.grid_rowconfigure(0, weight=1)
        notebook_frame.grid_columnconfigure(0, weight=1)

        # Create a frame inside the canvas to hold the notebook
        notebook_frame_inside = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=notebook_frame_inside, anchor='nw')


        # Configure grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create and place the notebook
        self.nb = ttk.Notebook(self)
        self.nb.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # Add tabs to the notebook
        self.frm1 = ttk.Frame(self.nb)
        self.nb.add(self.frm1, text="Image_Browser")
        self.frm2 = ttk.Frame(self.nb)
        self.nb.add(self.frm2, text="Image Edit")
        self.ctrl_frm = ttk.Frame(self.frm2, width=50, height=35)
        self.ctrl_frm.grid(row=0, column=7)
        self.canvas2 = tk.Canvas(self.frm2,height=800, width=1200, bg="WHITE", bd=10)
        self.canvas2.grid(row=2, column=1)
        self.zoom_slider = tk.Scale(self.ctrl_frm, from_=1, to=10, orient="horizontal", label="Zoom", command=self.zoom_image)
        self.zoom_slider.set(1)  # Initial zoom level
        self.zoom_slider.grid(row=0, column=2)
        self.image_browser = Image_browser(self.frm1, self.canvas2)
        self.frm3 = ttk.Frame(self.nb)
        self.nb.add(self.frm3, text="Bulk Resize")
        self.frm4 = ttk.Frame(self.nb)
        self.bulk_resize = multi_img_file_resizer(self.frm3)
        self.nb.add(self.frm4, text="Image Spliter")
        self.split_tiles = ImageTileSplitterApp(self.frm4)
        nb_frm = tk.Frame(self, width=1200, height=200)
        nb_frm.grid(row=0, column=0, sticky="nsew")
        self.frm5 = ttk.Frame(self.nb)
        self.nb.add(self.frm5, text="Img proof edit1")
        self.ctrl_frm5 = ttk.Frame(self.frm5, width=50, height=35)
        self.ctrl_frm5.grid(row=0, column=7)
        self.frm6 = ttk.Frame(self.nb)
        self.nb.add(self.frm6, text="Image Edit")
        self.ctrl_frm6 = ttk.Frame(self.frm6, width=50, height=35)
        self.ctrl_frm6.grid(row=0, column=7)
        self.frm7 = ttk.Frame(self.nb)
        self.nb.add(self.frm7, text="Image Edit")
        self.ctrl_frm7 = ttk.Frame(self.frm7, width=50, height=35)
        self.ctrl_frm7.grid(row=0, column=7)
        self.frm8 = ttk.Frame(self.nb)
        self.nb.add(self.frm8, text="Image Edit")
        self.ctrl_frm8 = ttk.Frame(self.frm8, width=50, height=35)
        self.ctrl_frm8.grid(row=0, column=7)
        self.nb.bind("<<NotebookTabChanged>>", self.on_tab_changed)

    def zoom_image(self, zoom_level):
        # This function will be called when the zoom slider is adjusted
        if self.image_browser.loaded_img:
            # Calculate the new size based on the zoom level
            zoom_factor = float(zoom_level)
            width, height = self.image_browser.loaded_img.size
            new_size = (int(width * zoom_factor), int(height * zoom_factor))

            # Resize the image and update the canvas
            resized_img = self.image_browser.loaded_img.resize(new_size, Image.Resampling.LANCZOS)

            self.img_on_canvas = ImageTk.PhotoImage(resized_img)
            self.canvas2.create_image(600, 400, image=self.img_on_canvas, anchor='center')  # Adjust position as needed
            self.canvas2.image = self.img_on_canvas
            
    def on_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.nb.add(frame, text=title)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def on_tab_changed(self, event=None):
        selected_index = self.nb.index(self.nb.select())
        if selected_index == 1:  # Assuming this index corresponds to Image Edit tab
            self.canvas2 = menu.loaded_image
 
        else:
            self.canvas = None  # or any default widget
    def can_respond(self, widget):
        # Check if the widget is enabled
        if str(widget['state']) == 'disabled':
            return False

        # Check if the widget is visible
        if not widget.winfo_ismapped():
            return False

        # Check for specific content conditions

        if some_specific_condition(content):  # Replace with your condition
            return False

        # Check if the widget has focus
        if widget is not self.focus_get():
            return False

        return True




class Image_browser:
    def __init__(self, parent, canvas2):
        self.parent = parent
        self.canvas2 = canvas2
        self.area = (700, 500)
        self.path = "/home/jh/Pictures"
        # Initialize Treeview
        self.tree = ttk.Treeview(self.parent, columns=("Size", "Type", "Modified"))
        self.tree.heading("#0", text="File Name", command=lambda: treeview_sort_column(self.tree, "#0", False))
        self.tree.heading("Size", text="Size (KB)", command=lambda: treeview_sort_column(self.tree, "Size", False))
        self.tree.heading("Type", text="Type", command=lambda: treeview_sort_column(self.tree, "Type", False))
        self.tree.heading("Modified", text="Last Modified", command=lambda: treeview_sort_column(self.tree, "Modified", False))

        # Scrollbar
        self.sc = Scrollbar(self.parent, orient=VERTICAL, command=self.tree.yview)
        self.sc.grid(row=0, rowspan=15, column=3, sticky='ns')
        self.tree.configure(yscrollcommand=self.sc.set)

        # Treeview grid placement
        self.tree.grid(row=0, column=0, rowspan=15, sticky="nswe")


        self.tree.bind('<<TreeviewSelect>>', self.on_select)
        self.canvas = tk.Canvas(
            self.parent,
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
        self.frame = Frame(self.parent, bg="white", padx=10, pady=10)
        btn_open = tk.Button(
            self.frame,
            text="Open New Image",
            bd=2,
            command=self.make_image,
        )
        btn_open.grid(row=3, column=11)
        self.frame.grid(row=1, column=2)
        self.copy_button = Button(self.frame, text="Copy to Edit Tab", command=self.copy_to_edit_tab)
        self.copy_button.grid(row=4, column=11)  # Adjust grid parameters as needed
        self.relist = tk.Button(
            self.frame,
            text="relist",
            bd=2,
            bg="lavender",
            command=self.list_files,
        )
        self.relist.grid(row=5, column=8)
        self.new_dir = tk.Button(
            self.frame,
            text="new dir",
            bd=2,
            bg="lavender",
            command=self.newdirlist,
        )
        self.new_dir.grid(row=6, column=8)
        # Status Bar
        self.status = tk.Label(
            self.parent,
            text="Image Browser    Current Image: None",)
        self.status.grid(row=0, column=1)

    
        self.list_files()


      
    def treeview_sort_column(tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # Rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # Reverse sort next time
        tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))
        
    def get_current_image(self):
        # This function returns the current loaded image
        if self.loaded_img:
            return self.loaded_img.copy()  # Return a copy of the image
        return None
    def list_files(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

            
        # Define a list of image extensions
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

        # Add new files from the selected directory
        for file in os.listdir(self.path):
            if file.endswith(tuple(image_extensions)):
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
        new_path = askdirectory()
        if new_path:
            try:
                self.path = new_path
                os.chdir(self.path)
                self.list_files()  # Populate the Treeview with files from the new directory
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
        self.path = askdirectory(title="Select Folder to open")
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
            self.file = askopenfilename(filetypes=filetypes)

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


        



    def copy_to_edit_tab(self):
        if self.loaded_img:  # Check if there's an image loaded
            photo = ImageTk.PhotoImage(self.loaded_img)
            nb.canvas2.create_image(800, 800, image=photo)  # Adjust position as needed
            nb.canvas2.image = photo  # Keep a reference



class ImageTileSplitterApp:
    def __init__(self, parent):
        self.parent = parent
       

        # Instance variables
        self.auto_create_dir = tk.BooleanVar()
        self.info = """This program will take a png file and split it up into tiles of desired
                       width and height sizes,
                      place new files into a folder. Be careful
                      how you use this, it can create a lot of files.
                      example is a 6400 X 6400 pixel size image and you want 64X64
                      you will get 100 separate images. Pieces of the original
                      """
        # Setup the GUI
        self.setup_gui()

    def setup_gui(self):
        # Image selection
        tk.Label(self.parent, text="Image Path:").grid(row=0, column=0)
        self.entry_image_path = tk.Entry(self.parent, width=50)
        self.entry_image_path.grid(row=0, column=1)
        tk.Button(self.parent, text="Browse", command=self.select_image).grid(row=0, column=2)
        # progress bar
        self.progress = ttk.Progressbar(self.parent, orient="horizontal", length=300, mode="determinate")
        self.progress.grid(row=5, column=0, columnspan=3, pady=10)
        # Tile size inputs
        tk.Label(self.parent, text="Tile Width:").grid(row=1, column=0)
        self.entry_tile_width = tk.Entry(self.parent)
        self.entry_tile_width.grid(row=1, column=1)
        tk.Label(self.parent, text="Tile Height:").grid(row=2, column=0)
        self.entry_tile_height = tk.Entry(self.parent)
        self.entry_tile_height.grid(row=2, column=1)

        # Output directory selection
        tk.Label(self.parent, text="Output Directory:").grid(row=3, column=0)
        self.entry_output_dir = tk.Entry(self.parent, width=50)
        self.entry_output_dir.grid(row=3, column=1)
        tk.Button(self.parent, text="Browse", command=lambda: self.entry_output_dir.insert(0, filedialog.askdirectory())).grid(row=3, column=2)

        # Checkbox for auto-creating output directory
        tk.Checkbutton(self.parent, text="Auto-create Output Directory", variable=self.auto_create_dir).grid(row=4, column=0)

        # Split button
        tk.Button(self.parent, text="Split Image", command=self.split_image).grid(row=4, column=1)
        tk.Label(self.parent, text = self.info).grid(row=9,column=0)
    def select_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.entry_image_path.delete(0, tk.END)
            self.entry_image_path.insert(0, file_path)

    def split_image(self):
        image_path = self.entry_image_path.get()
        tile_width = int(self.entry_tile_width.get())
        tile_height = int(self.entry_tile_height.get())
        output_dir = self.entry_output_dir.get()
        threading.Thread(target=self.process_image, args=(image_path, tile_width, tile_height, output_dir), daemon=True).start()
        
       
    def process_image(self, image_path, tile_width, tile_height, output_dir):
        try:
            # Open the image and get its size
            image = Image.open(image_path)
            img_width, img_height = image.size

            total_tiles = (img_width // tile_width) * (img_height // tile_height)
            self.progress['maximum'] = total_tiles

            tile_number = 0
            for i in range(0, img_width, tile_width):
                for j in range(0, img_height, tile_height):
                    box = (i, j, i + tile_width, j + tile_height)
                    tile = image.crop(box)

                    # If auto-create directory is selected
                    if self.auto_create_dir.get() and tile_number == 0:
                        output_dir = os.path.join("output_tiles", datetime.now().strftime("%Y%m%d_%H%M%S"))
                        os.makedirs(output_dir, exist_ok=True)

                    tile_filename = f'tile_{tile_number}.png'
                    tile.save(os.path.join(output_dir, tile_filename))

                    # Update progress bar
                    tile_number += 1
                    self.update_progress(tile_number)

            messagebox.showinfo("Success", f"Image split into {tile_number} tiles successfully!")
        except Exception as e:
            messagebox.showerror("Error", str(e))



    def update_progress(self, value):
        def _update():
            self.progress['value'] = value
        self.parent.after(0, _update)






























if __name__ == "__main__":
    
    nb = ScrollableNotebook()
    nb.mainloop()


