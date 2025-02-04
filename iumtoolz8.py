import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk, StringVar,Toplevel
from PIL import Image, ImageTk
import os
import subprocess
import sys
import time
from glob import glob
import json

BOOKMARK_FILE = "bookmarks.json"
Image.MAX_IMAGE_PIXELS = None



class ImageToolApp:
    def __init__(self, root):
        self.root = root
       
        self.notebook = ttk.Notebook(self.root)
        self.notebook.grid(row=1,column=1)
        self.json_file = BOOKMARK_FILE
        self.image_paths = []
        self.selected_images = []
        self.current_img_path = None
        self.merged_image = None  # Fixing the reference issue
        self.json_file = BOOKMARK_FILE
        self.path_var = StringVar()
        self.bookmarks = self.load_bookmarks()
        # File Frame
        self.frm1 = tk.Frame(self.notebook, height=44,width=600)
        self.frm1.grid(row=0, column=0, columnspan=3)
        self.frm2 = tk.Frame(self.notebook, height=44,width=600)
        self.frm2.grid(row=0, column=1, columnspan=3)
        self.frm3 = tk.Frame(self.notebook, height=44,width=600)
        self.frm3.grid(row=0, column=2, columnspan=3)
        self.frm4 = tk.Frame(self.notebook, height=44,width=600)
        self.frm4.grid(row=0, column=3, columnspan=3)
        self.frm5 = tk.Frame(self.notebook, height=44,width=600)
        self.frm5.grid(row=0, column=4, columnspan=3)
        self.frm6 = tk.Frame(self.notebook, height=44,width=600)
        self.frm6.grid(row=0, column=6, columnspan=3)

        self.notebook.add(self.frm1, text="Navgation")
        self.notebook.add(self.frm2, text="Controls")
        self.notebook.add(self.frm3, text="Thumbnails")  
        self.notebook.add(self.frm4, text="FileInfo")
        self.notebook.add(self.frm5, text="Merger")
        self.notebook.add(self.frm6, text="Image Edite")

        self.dir_path = tk.Entry(self.frm1, bd=11, bg="wheat", textvariable=self.path_var, width=50)
        self.dir_path.grid(row=0, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        self.dir_path.insert(0, os.getcwd())
       

        # Buttons in File Frame
        tk.Button(self.frm1, bd=8, bg="cyan", text="Use Path", command=self.use_path).grid(row=2, column=0)
        tk.Button(self.frm1, bd=8, bg="light green", text="Browse", command=self.browse_path).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(self.frm1, bd=8, bg="light blue", text="Save Bookmark", command=self.add_bookmark).grid(row=2, column=2, padx=5, pady=5)
        tk.Button(self.frm1, bd=8, bg="light yellow", text="Delete Bookmark", command=self.delete_bookmark).grid(row=2, column=3, padx=5, pady=5)

        # Bookmarks Combobox
        self.bookmark_var = StringVar()
        self.bookmark_combo = ttk.Combobox(self.frm1, textvariable=self.bookmark_var, values=list(self.load_bookmarks().keys()))
        self.bookmark_combo.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
        self.bookmark_combo.bind("<<ComboboxSelected>>", self.select_bookmark)

        tk.Button(self.frm1, bd=10, bg="orange", text="Open Selected Path", command=self.open_selected_path).grid(row=3, column=2, padx=5, pady=5)
        
        # Additional Widgets (example: Thumbnails and Information areas)
        self.canvas = tk.Canvas(self.frm3, bg="white")
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.scrollbar = tk.Scrollbar(self.frm3, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")

        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.frame_thumbnails = tk.Frame(self.canvas, bg="white")
        self.canvas.create_window((0, 0), window=self.frame_thumbnails, anchor="nw")

        # Configure resizing
        self.frm3.grid_rowconfigure(0, weight=1)
        self.frm3.grid_columnconfigure(0, weight=1)

        self.frame_thumbnails.bind("<Configure>", lambda e: self.canvas.config(scrollregion=self.canvas.bbox("all")))
        self.progress_bar = ttk.Progressbar(self.frm3, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.grid(row=2, column=0, columnspan=3, pady=5)
                # Frame for additional buttons
        self.frame_buttons = tk.Frame(self.frm2)
        self.frame_buttons.grid(row=6, column=0, columnspan=3, sticky="ew", padx=10, pady=10)

        # Buttons for all functionalities
        self.btn_get_images = tk.Button(self.frame_buttons, bd=8, bg="light green", text="Get Images", 
                                        command=self.get_images)
        self.btn_get_images.grid(row=0, column=0, padx=5, pady=5)

        self.btn_convert_to_png = tk.Button(self.frame_buttons, bd=8, bg="light blue", text="Convert to PNG", 
                                            command=self.convert_to_png)
        self.btn_convert_to_png.grid(row=0, column=1, padx=5, pady=5)

        self.btn_build_sprite_sheet = tk.Button(self.frame_buttons, bd=8, bg="gold", text="Build Sprite Sheet", 
                                                command=self.build_sprite_sheet)
        self.btn_build_sprite_sheet.grid(row=0, column=2, padx=5, pady=5)

        self.btn_merge_images = tk.Button(self.frame_buttons, bd=8, bg="orange", text="Merge Images", 
                                          command=self.merge_images)
        self.btn_merge_images.grid(row=1, column=0, padx=5, pady=5)

        self.btn_save_merged_image = tk.Button(self.frame_buttons, bd=8, bg="pink", text="Save Merged Image", 
                                               command=self.save_merged_image)
        self.btn_save_merged_image.grid(row=1, column=1, padx=5, pady=5)

        self.btn_display_merged_image = tk.Button(self.frame_buttons, bd=8, bg="purple", text="Display Merged Image", 
                                                  command=lambda: self.display_merged_image(self.merged_image))
        self.btn_display_merged_image.grid(row=1, column=2, padx=5, pady=5)

        self.btn_select_image = tk.Button(self.frame_buttons, bd=8, bg="cyan", text="Select Image", 
                                          command=lambda: self.select_image(self.current_img_path))
        self.btn_select_image.grid(row=2, column=0, padx=5, pady=5)

        self.btn_load_thumbnails = tk.Button(self.frame_buttons, bd=8, bg="red", text="Load Thumbnails", 
                                             command=self.load_thumbnail)
        self.btn_load_thumbnails.grid(row=2, column=1, padx=5, pady=5)

        self.var_recursive = tk.BooleanVar(value=False)
        self.mode_label = tk.Label(self.frm2, text="Mode: Flat Directory")
        self.mode_label.grid(row=9, column=0)
        self.check_recursive = tk.Checkbutton(self.frame_buttons,text="Recursive View",variable=self.var_recursive,command=self.update_mode_label)
        self.check_recursive.grid(row=10, column=1, padx=5)
      
        self.frame_thumbnails = tk.Frame(self.frm3, bg="white")
        self.frame_thumbnails.grid(row=0, column=0, sticky="nsew")

        # Configure scrollable area
        self.scrollbar = tk.Scrollbar(self.frm3, orient="vertical", command=self.canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.config(yscrollcommand=self.scrollbar.set)
        self.lbl_info = tk.Label(self.frm4, text="File Info", anchor="w")
        self.lbl_info.grid(row=0, column=0, sticky="w", pady=5)

        self.txt_info = tk.Text(self.frm4,bd=7, height=8, width=40, wrap="word")
        self.txt_info.grid(row=1, column=0, sticky="nsew")

        self.lbl_selected = tk.Label(self.frm4,bd=10, text="Selected Images")
        self.lbl_selected.grid(row=2, column=0, sticky="w", pady=5)

    def browse_path(self):
        """Browse and set a directory path."""
        path = filedialog.askdirectory(title="Select Directory")
        if path:
            self.path_var.set(path)
            self.adjust_entry_width()

    def adjust_entry_width(self):
        """Dynamically adjust the width of the entry widget based on path length."""
        path_length = len(self.path_var.get())
        self.dir_path.config(width=max(50, path_length))

    def add_bookmark(self):
        """Add a new bookmark for the current path."""
        path = self.path_var.get()
        if not path or not os.path.exists(path):
            messagebox.showerror("Invalid Path", "The selected path does not exist!")
            return

        name = simpledialog.askstring("Bookmark Name", "Enter a name for the bookmark:")
        if not name:
            messagebox.showwarning("Invalid Name", "Bookmark name cannot be empty!")
            return

        if name in self.bookmarks:
            overwrite = messagebox.askyesno("Overwrite Bookmark", f"Bookmark '{name}' already exists. Overwrite?")
            if not overwrite:
                return

        self.bookmarks[name] = path
        self.update_bookmarks()
        messagebox.showinfo("Bookmark Added", f"Bookmark '{name}' saved successfully.")

    def save_bookmarks(self):
        """Save bookmarks to a JSON file."""
        try:
            with open(self.json_file, "w") as file:
                json.dump(self.bookmarks, file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save bookmarks: {e}")

    def delete_bookmark(self):
        """Delete the selected bookmark."""
        selected = self.bookmark_var.get()
        if selected in self.bookmarks:
            del self.bookmarks[selected]
            self.update_bookmarks()
            messagebox.showinfo("Bookmark Deleted", f"Bookmark '{selected}' deleted successfully.")
        else:
            messagebox.showwarning("Invalid Selection", "No valid bookmark selected.")

    def select_bookmark(self, event=None):
        """Select a bookmark from the dropdown and update the path."""
        selected = self.bookmark_var.get()
        if selected in self.bookmarks:
            self.path_var.set(self.bookmarks[selected])
            self.adjust_entry_width()

    def open_selected_path(self):
        """Open the selected path or display an error."""
        path = self.path_var.get()
        if os.path.exists(path):
            try:
                self.get_images()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open path: {e}")
        else:
            messagebox.showerror("Error", "The selected path does not exist.")

    def use_path(self):
        """Set and use the current path."""
        path = self.path_var.get()
        if os.path.exists(path):
            try:
                self.open_path(path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to use path: {e}")

    @staticmethod
    def open_path(path):
        """Open a directory in the system's file explorer."""
        try:
            if sys.platform == "win32":
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.run(["open", path], check=True)
            elif sys.platform.startswith("linux"):
                subprocess.run(["xdg-open", path], check=True)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open path: {e}")

    def load_bookmarks(self):
        """Load bookmarks from a JSON file."""
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                messagebox.showerror("Error", "Bookmarks file is corrupted. Resetting bookmarks.")
                return {}
        return {}

    def update_bookmarks(self):
        """Update the bookmarks dropdown and save the bookmarks."""
        self.bookmark_combo['values'] = list(self.bookmarks.keys())
        self.save_bookmarks()

    def load_images(self, directory):
        """Search for image files in the directory and update the UI."""
        extensions = ('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif', '*.tiff', '*.webp', '*.avif')

        self.image_paths = []
        search_pattern = '**/*' if self.var_recursive.get() else '*'

        for ext in extensions:
            self.image_paths.extend(glob(os.path.join(directory, search_pattern, ext), recursive=self.var_recursive.get()))

        if not self.image_paths:
            messagebox.showinfo("No Images Found", "No images were found in the selected directory.")
        else:
            self.display_thumbnails()

    
    def get_images(self):
        path = self.path_var.get()
        if os.path.exists(path):
            try:
                self.open_path(path)
                self.load_images(path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open path: {e}")
        else:
            messagebox.showerror("Error", f"Path '{path}' does not exist.")
    def load_images(self, directory):
        extensions = ('*.png', '*.jpg', '*.jpeg', '*.bmp', '*.gif', '*.tiff', '*.webp', '*.avif')
        search_pattern = '**/*' if self.var_recursive.get() else '*'

        self.image_paths = []
        for ext in extensions:
            self.image_paths.extend(glob(os.path.join(directory, search_pattern, ext), recursive=self.var_recursive.get()))

        converted_files = []
        for file_path in self.image_paths:
            if file_path.endswith((".webp", ".avif")):
                try:
                    img = Image.open(file_path)
                    png_path = os.path.splitext(file_path)[0] + ".png"
                    img.save(png_path, format="PNG")
                    converted_files.append(png_path)
                except Exception as e:
                    print(f"Error converting {file_path}: {e}")

        # Update image paths to include converted PNGs
        self.image_paths.extend(converted_files)

        if not self.image_paths:
            messagebox.showinfo("No Images Found", "No images found in the selected directory.")
            return

        self.display_thumbnails()
            
           
    def display_thumbnails(self):
        self.progress_bar["maximum"] = len(self.image_paths)
        self.thumbnail_index = 0  # Keep track of the current index
        self.load_thumbnail()
    def load_thumbnail(self):
        """Load a single thumbnail and schedule the next one."""
        if self.thumbnail_index < len(self.image_paths):
            img_path = self.image_paths[self.thumbnail_index]
            try:
                img = Image.open(img_path)
                img.thumbnail((100, 100))  # Create a thumbnail
                tk_img = ImageTk.PhotoImage(img)

                frame = tk.Frame(self.frame_thumbnails, bd=2, relief="ridge")
                frame.grid(row=self.thumbnail_index // 6, column=self.thumbnail_index % 6, padx=5, pady=5)

                lbl_img = tk.Label(frame, image=tk_img)
                lbl_img.image = tk_img  # Keep a reference
                lbl_img.grid(row=0, column=0)

                lbl_info = tk.Label(frame, text=os.path.basename(img_path), wraplength=100, anchor="w")
                lbl_info.grid(row=1, column=0, sticky="ew")

                lbl_img.bind("<Enter>", lambda e, path=img_path: self.show_file_info(path))
                lbl_img.bind("<Button-1>", lambda e, path=img_path: self.select_image(path))
                lbl_img.bind("<Double-1>", lambda e, path=img_path: self.add_to_selection(path))

                self.progress_bar.step(1)  # Update progress bar

            except Exception as e:
                print(f"Error loading image {img_path}: {e}")

            # Schedule the next thumbnail
            self.thumbnail_index += 1
            self.canvas.update_idletasks()
            self.progress_bar.update_idletasks()
            self.root.after(10, self.load_thumbnail)
        else:
            # Reset progress bar and update scroll region
            self.progress_bar["value"] = 0
            self.frame_thumbnails.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

  

    def select_image(self, img_path):
        """Set the selected image and show its details."""
        self.show_file_info(img_path)
        self.current_img_path = img_path

    def show_file_info(self, img_path):
        """Display file details in the information area."""
        if os.path.exists(img_path):
            file_size = os.path.getsize(img_path) / 1024  # KB
            last_modified = time.ctime(os.path.getmtime(img_path))
            info_text = f"Path: {img_path}\nSize: {file_size:.2f} KB\nLast Modified: {last_modified}"
            self.txt_info.delete(1.0, tk.END)
            self.txt_info.insert(tk.END, info_text)

    def update_mode_label(self):
        """Update the mode label and reload images."""
        mode = "Recursive Directory" if self.var_recursive.get() else "Flat Directory"
        self.mode_label.config(text=f"Mode: {mode}")
        self.get_images()
    def merge_images(self):
        """Merge selected images side by side."""
        if len(self.selected_images) < 2:
            messagebox.showwarning("Not Enough Images", "Select at least two images to merge.")
            return

        try:
            # Open images and calculate dimensions
            images = [Image.open(img) for img in self.selected_images]
            total_width = sum(img.width for img in images)
            max_height = max(img.height for img in images)

            # Create a blank image with the calculated dimensions
            merged_image = Image.new('RGB', (total_width, max_height))
            x_offset = 0

            for img in images:
                merged_image.paste(img, (x_offset, 0))
                x_offset += img.width

            self.merged_image = merged_image
            self.display_merged_image(merged_image)

            messagebox.showinfo("Success", "Images merged successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge images: {e}")

    def display_merged_image(self, image):
        """Display the merged image in the canvas."""
        self.canvas.delete("all")
        resized_image = image.resize((800, 600))  # Adjust size for display
        tk_img = ImageTk.PhotoImage(resized_image)
        self.canvas.create_image(400, 300, anchor=tk.CENTER, image=tk_img)
        self.canvas.image = tk_img

    def save_merged_image(self):
        """Save the merged image to a file."""
        if self.merged_image is None:
            messagebox.showerror("Error", "No merged image to save.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")]
        )
        if file_path:
            try:
                self.merged_image.save(file_path)
                messagebox.showinfo("Success", "Merged image saved successfully.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save merged image: {e}")

    def build_sprite_sheet(self):
        """Build a sprite sheet from selected images."""
        if not self.selected_images:
            messagebox.showwarning("No Images Selected", "Select images to create a sprite sheet.")
            return

        try:
            columns = simpledialog.askinteger("Sprite Sheet", "Enter the number of columns:", minvalue=1)
            if not columns:
                return

            rows = (len(self.selected_images) + columns - 1) // columns
            img_width, img_height = Image.open(self.selected_images[0]).size

            sprite_sheet = Image.new('RGBA', (img_width * columns, img_height * rows))
            for idx, img_path in enumerate(self.selected_images):
                img = Image.open(img_path)
                row, col = divmod(idx, columns)
                sprite_sheet.paste(img, (col * img_width, row * img_height))

            self.merged_image = sprite_sheet
            self.display_merged_image(sprite_sheet)

            messagebox.showinfo("Sprite Sheet Created", "Sprite sheet created successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create sprite sheet: {e}")

    def convert_to_png(self):
        """Convert selected images to PNG format."""
        file_paths = filedialog.askopenfilenames(
            title="Select Images to Convert",
            filetypes=[("Image files", "*.webp *.avif *.bmp"), ("All files", "*.*")]
        )
        if not file_paths:
            return

        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            messagebox.showwarning("No Directory Selected", "Output directory not selected.")
            return

        success_count = 0
        error_files = []

        for file_path in file_paths:
            try:
                img = Image.open(file_path)
                base_name = os.path.basename(file_path)
                name, _ = os.path.splitext(base_name)
                output_path = os.path.join(output_dir, f"{name}.png")
                img.save(output_path, format="PNG")
                success_count += 1
            except Exception as e:
                print(f"Error converting {file_path}: {e}")
                error_files.append(file_path)

        message = f"Successfully converted {success_count} files to PNG."
        if error_files:
            message += f"\nFailed to convert {len(error_files)} files."
        messagebox.showinfo("Conversion Summary", message)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1400x800")
    app = ImageToolApp(root)
    root.mainloop()


