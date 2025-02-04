import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk, StringVar, Toplevel
from PIL import Image, ImageTk
import os
import subprocess
import sys
import time
from glob import glob
import json

BOOKMARK_FILE = "bookmarks.json"
Image.MAX_IMAGE_PIXELS = None


class ImageToolApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Tool Suite")
        self.geometry("1400x800")

        # Initialize attributes
        self.image_paths = []
        self.selected_images = []
        self.current_img_path = None
        self.json_file = BOOKMARK_FILE
        self.path_var = StringVar()
        self.file_frm = tk.Frame(self, width=200)
        self.file_frm.grid(row=0, column=0, columnspan=3)
        self.json_file = BOOKMARK_FILE
        self.top = Toplevel(self)
        # Load bookmarks from JSON
        self.bookmarks = self.load_bookmarks()
        self.dir_path = tk.Entry(
            self.file_frm, bd=11, bg="wheat", textvariable=self.path_var, width=50
        )
        self.dir_path.grid(row=0, column=0, columnspan=3, sticky="ew", padx=5, pady=5)
        self.dir_path.insert(0, os.getcwd())
        # tk.Buttons

        tk.Button(
            self.file_frm, bd=8, bg="cyan", text="Use Path", command=self.use_path
        ).grid(row=2, column=0)
        tk.Button(
            self.file_frm,
            bd=8,
            bg="light green",
            text="Browse",
            command=self.browse_path,
        ).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(
            self.file_frm,
            bd=8,
            bg="light blue",
            text="Save Bookmark",
            command=self.save_bookmarks,
        ).grid(row=2, column=2, padx=5, pady=5)
        tk.Button(
            self.file_frm,
            bd=8,
            bg="light yellow",
            text="Delete Bookmark",
            command=self.delete_bookmark,
        ).grid(row=2, column=3, padx=5, pady=5)

        # Bookmarks Combobox
        self.bookmark_var = StringVar()
        self.bookmark_combo = ttk.Combobox(
            self.file_frm,
            textvariable=self.bookmark_var,
            values=list(self.bookmarks.keys()),
        )
        self.bookmark_combo.grid(
            row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5
        )
        self.bookmark_combo.bind("<<ComboboxSelected>>", self.select_bookmark)

        # tk.Button to open the selected path
        tk.Button(
            self.file_frm,
            bd=10,
            bg="orange",
            text="Open Selected Path",
            command=self.open_selected_path,
        ).grid(row=3, column=2, padx=5, pady=5)
        tk.Button(
            self.file_frm,
            bd=8,
            bg="light pink",
            text="Add Bookmark",
            command=self.add_bookmark,
        ).grid(row=3, column=3, padx=5, pady=5)
        # Top frame for options

        self.mode_label = tk.Label(self.top, text="Mode: Flat Directory")
        self.mode_label.grid(row=0, column=0)

        self.progress_bar = ttk.Progressbar(
            self.top, orient="horizontal", length=400, mode="determinate"
        )
        self.progress_bar.grid(row=1, column=2)
        self.progress_label = tk.Label(self.top, text="if loading please wait...")
        self.progress_label.grid(row=2, column=2)

        self.canvas = tk.Canvas(
            self.top,
            bg="white",
            height=200,
            width=600,
            xscrollincrement=20,
            yscrollincrement=20,
        )
        self.canvas.grid(row=4, column=2, columnspan=8, rowspan=10, sticky="nsew")

        self.frame_thumbnails = tk.Frame(self.canvas, height=200, width=300)
        self.frame_thumbnails.grid(row=1, column=1, columnspan=3, rowspan=3)
        self.canvas.create_window((2, 2), window=self.frame_thumbnails)

        # Frame to hold thumbnails inside the canvas

        self.frame_thumbnails.grid_rowconfigure(0, weight=1)
        self.frame_thumbnails.grid_columnconfigure(0, weight=1)
        self.framebottom = tk.Frame(self)
        self.framebottom.grid(
            row=8, column=1, columnspan=2, sticky="ew", padx=10, pady=10
        )
        self.btn_browse = tk.Button(
            self.framebottom,
            bd=8,
            bg="azure",
            text="Get Images",
            command=self.get_images,
        )
        self.btn_browse.grid(row=0, column=0, padx=5)
        self.var_recursive = tk.BooleanVar(value=False)

        self.check_recursive = tk.Checkbutton(
            self.framebottom,
            text="Recursive View",
            variable=self.var_recursive,
            command=self.update_mode_label,
        )
        self.check_recursive.grid(row=0, column=1, padx=5)
        self.btn_view_full = tk.Button(
            self.framebottom,
            bd=8,
            bg="medium orchid",
            text="View Full Image",
            command=self.view_full_image,
        )
        self.btn_view_full.grid(row=0, column=2, padx=5)

        self.btn_unselect = tk.Button(
            self.framebottom,
            bd=8,
            bg="SeaGreen2",
            text="Unselect",
            command=self.unselect_image,
        )
        self.btn_unselect.grid(row=0, column=3, padx=5)

        self.btn_merge = tk.Button(
            self.framebottom,
            bd=8,
            bg="bisque",
            text="Merge Images",
            command=self.merge_images,
        )
        self.btn_merge.grid(row=0, column=4, padx=5)
        self.save_merge = tk.Button(
            self.framebottom,
            bd=8,
            bg="bisque",
            text="Savr Merged Image",
            command=self.save_merged_image,
        )
        self.save_merge.grid(row=0, column=7, padx=5)

        self.btn_sprite = tk.Button(
            self.framebottom,
            bd=8,
            bg="light steel blue",
            text="Build Sprite Sheet",
            command=self.build_sprite_sheet,
        )
        self.btn_sprite.grid(row=0, column=5, padx=5)
        self.btn_convert = tk.Button(
            self.framebottom,
            bd=6,
            bg="burlywood",
            text="Convert to PNG",
            command=self.convert_to_png,
        )
        self.btn_convert.grid(row=0, column=6, padx=5)
        self.frame_right = tk.Frame(self)
        self.frame_right.grid(row=5, column=3, sticky="nsew", padx=10, pady=10)

        self.lbl_info = tk.Label(self.frame_right, text="File Info", anchor="w")
        self.lbl_info.grid(row=0, column=5, sticky="w", pady=5)

        self.txt_info = tk.Text(self.frame_right, bd=7, height=8, width=40, wrap="word")
        self.txt_info.grid(row=1, column=6, sticky="nsew")

        self.lbl_selected = tk.Label(self.frame_right, bd=10, text="Selected Images")
        self.lbl_selected.grid(row=2, column=0, sticky="w", pady=5)

        self.listbox_selected = tk.Listbox(self.frame_right, bd=9, height=15, width=40)
        self.listbox_selected.grid(row=3, column=8, sticky="nsew")

        # Grid weight configuration
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame_right.grid_rowconfigure(1, weight=1)

    def browse_path(self):
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)
            self.adjust_entry_width()

    def adjust_entry_width(self):
        path_length = len(self.path_var.get())
        self.dir_path.config(width=max(50, path_length))

    def add_bookmark(self):
        path = self.path_var.get()
        if not path:
            messagebox.showwarning(
                "Save Bookmark", "No path selected to save as a bookmark!"
            )
            return

        if not os.path.exists(path):
            messagebox.showerror("Save Bookmark", "The selected path does not exist!")
            return

        # Prompt user for a custom name
        name = simpledialog.askstring("Bookmark Name", "Enter a name for the bookmark:")

        if not name:
            messagebox.showwarning("Save Bookmark", "Bookmark name cannot be empty!")
            return

        if name in self.bookmarks:
            overwrite = messagebox.askyesno(
                "Overwrite Bookmark",
                f"A bookmark with the name '{name}' already exists. Overwrite?",
            )
            if not overwrite:
                return

        self.bookmarks[name] = path
        self.update_bookmarks()
        messagebox.showinfo("Bookmark Saved", f"Bookmark '{name}' saved successfully.")

    def save_bookmarks(self):
        try:
            with open(self.json_file, "w") as file:
                json.dump(self.bookmarks, file)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save bookmarks: {e}")

    def delete_bookmark(self):
        selected = self.bookmark_var.get()
        if selected in self.bookmarks:
            del self.bookmarks[selected]
            self.update_bookmarks()
            messagebox.showinfo(
                "Bookmark Deleted", f"Bookmark '{selected}' deleted successfully."
            )

    def select_bookmark(self, event=None):
        selected = self.bookmark_var.get()
        if selected in self.bookmarks:
            self.path_var.set(self.bookmarks[selected])
            self.adjust_entry_width()

    def open_selected_path(self):
        path = self.path_var.get()
        if os.path.exists(path):
            try:
                self.get_images()
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open path: {e}")
        else:
            messagebox.showerror("Error", f"Path '{path}' does not exist.")

    def use_path(self):
        path = self.path_var.get()
        if os.path.exists(path):
            try:
                self.open_path(path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open path: {e}")

    @staticmethod
    def open_path(path):
        if sys.platform == "win32":
            os.startfile(path)  # Opens file or directory in Windows
        elif sys.platform == "darwin":
            subprocess.run(["open", path], check=True)  # macOS uses 'open'
        elif sys.platform.startswith("linux"):  # Check for Linux
            subprocess.run(["xdg-open", path], check=True)  # Linux uses 'xdg-open'
        else:
            raise OSError("Unsupported platform")

    def load_bookmarks(self):
        if os.path.exists(self.json_file):
            try:
                with open(self.json_file, "r") as file:
                    return json.load(file)
            except json.JSONDecodeError:
                messagebox.showerror(
                    "Error", "Failed to load bookmarks: Invalid JSON format."
                )
                return {}
        return {}

    def update_bookmarks(self):
        self.bookmark_combo["values"] = list(
            self.bookmarks.keys()
        )  # Update the dropdown
        self.save_bookmarks()  # Save changes to the JSON file

    def get_images(self):
        path = self.path_var.get()
        if os.path.exists(path):
            try:
                self.load_images(path)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open path: {e}")
        else:
            messagebox.showerror("Error", f"Path '{path}' does not exist.")

    def load_images(self, directory):
        extensions = (
            "*.png",
            "*.jpg",
            "*.jpeg",
            "*.bmp",
            "*.gif",
            "*.tiff",
            "*.webp",
            "*.avif",
        )

        self.image_paths = []
        if self.var_recursive.get():  # Recursive mode
            search_pattern = "**/*"
            for ext in extensions:
                self.image_paths.extend(
                    glob(os.path.join(directory, search_pattern, ext), recursive=True)
                )
        else:  # Flat mode
            for ext in extensions:
                self.image_paths.extend(
                    glob(os.path.join(directory, ext), recursive=False)
                )

        if not self.image_paths:
            messagebox.showinfo(
                "No Images Found", "No images found in the selected directory."
            )
            return

        self.display_thumbnails()

    def display_thumbnails(self):
        self.progress_bar["maximum"] = len(self.image_paths)
        self.thumbnail_index = 0  # Reset the thumbnail index

        # Update the scrollable canvas size
        self.frame_thumbnails.update_idletasks()
        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

        # Dynamically calculate thumbnails per row
        canvas_width = self.canvas.winfo_width()
        thumbnail_size = 140  # Thumbnail size (includes image and padding)
        self.thumbnails_per_row = max(1, canvas_width // thumbnail_size)

        # Clear existing thumbnails
        for widget in self.frame_thumbnails.winfo_children():
            widget.destroy()

        # Start loading thumbnails
        self.load_thumbnail()

    def load_thumbnail(self):
        """Load a single thumbnail and schedule the next one."""
        if self.thumbnail_index < len(self.image_paths):
            img_path = self.image_paths[self.thumbnail_index]
            try:
                img = Image.open(img_path)
                img.thumbnail((120, 120))  # Adjust thumbnail size
                tk_img = ImageTk.PhotoImage(img)

                # Create a frame for each thumbnail
                frame = tk.Frame(self.frame_thumbnails, bd=2, relief="ridge")
                frame.grid(
                    row=self.thumbnail_index // self.thumbnails_per_row,
                    column=self.thumbnail_index % self.thumbnails_per_row,
                    padx=10,
                    pady=10,
                )

                # Add the thumbnail image
                lbl_img = tk.Label(frame, image=tk_img)
                lbl_img.image = tk_img  # Prevent garbage collection
                lbl_img.grid(row=0, column=0, padx=5, pady=5)

                # Add the file name
                lbl_info = tk.Label(
                    frame,
                    text=os.path.basename(img_path),
                    wraplength=120,
                    anchor="center",
                )
                lbl_info.grid(row=1, column=0, padx=5, pady=5)

                ##                # Bind events for interactivity
                ##                lbl_img.bind("<Enter>", lambda e, path=img_path: self.show_file_info(path))
                ##                lbl_img.bind("<Button-1>", lambda e, path=img_path: self.select_image(path))
                ##                lbl_img.bind("<Double-1>", lambda e, path=img_path: self.add_to_selection(path))

                # Update progress bar
                self.progress_bar.step(1)
            except Exception as e:
                print(f"Error loading image {img_path}: {e}")

            # Schedule the next thumbnail
            self.thumbnail_index += 1
            self.after(10, self.load_thumbnail)  # Adjust delay as needed
        else:
            # Reset progress bar when done
            self.progress_bar["value"] = 0
            self.frame_thumbnails.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

            file_size = os.path.getsize(img_path) / 1024
            last_modified = time.ctime(os.path.getmtime(img_path))

            info_text = (
                f"Path: {img_path}\n"
                f"Size: {file_size:.2f} KB\n"
                f"Last Modified: {last_modified}"
            )

            self.txt_info.delete(1.0, tk.END)
            self.txt_info.insert(tk.END, info_text)
            self.current_img_path = img_path

    def select_image(self, img_path):
        self.show_file_info(img_path)
        self.current_img_path = img_path

    def add_to_selection(self, img_path):
        if img_path not in self.selected_images:
            self.selected_images.append(img_path)
            self.listbox_selected.insert(tk.END, os.path.basename(img_path))

    def unselect_image(self):
        selected_idx = self.listbox_selected.curselection()
        if not selected_idx:
            messagebox.showwarning("No Selection", "Select an image to unselect.")
            return

        selected_file = self.listbox_selected.get(selected_idx)
        self.listbox_selected.delete(selected_idx)
        self.selected_images = [
            img
            for img in self.selected_images
            if os.path.basename(img) != selected_file
        ]

    def view_full_image(self):
        if not self.current_img_path:
            messagebox.showwarning("No Image Selected", "Select an image to view.")
            return

        try:
            img = Image.open(self.current_img_path)
            top = tk.Toplevel(self)
            top.title("Full Image View")

            tk_img = ImageTk.PhotoImage(img)
            lbl_full_img = tk.Label(top, image=tk_img)
            lbl_full_img.image = tk_img
            lbl_full_img.pack()

            self.show_file_info(self.current_img_path)

        except Exception as e:
            messagebox.showerror("Error", f"Error opening image: {e}")

    def merge_images(self):
        if len(self.selected_images) < 2:
            messagebox.showwarning(
                "Not Enough Images", "Select at least two images to merge."
            )
            return

        images = [Image.open(img) for img in self.selected_images]
        total_width = sum(img.width for img in images)
        max_height = max(img.height for img in images)

        merged_image = Image.new("RGB", (total_width, max_height))
        x_offset = 0

        for img in images:
            merged_image.paste(img, (x_offset, 0))
            x_offset += img.width

        self.display_merged_image(merged_image)

    def display_merged_image(self, image):
        self.canvas.delete("all")  # Clear canvas
        img = image.resize((800, 600))
        tk_img = ImageTk.PhotoImage(img)
        self.canvas.create_image(400, 300, anchor=tk.CENTER, image=tk_img)
        self.canvas.image = tk_img

    def save_merged_image(self):
        if self.merged_image:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".jpg",
                filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")],
            )
            if file_path:
                self.merged_image.save(file_path)
                messagebox.showinfo("Success", "Image saved successfully!")
        else:
            messagebox.showerror("Error", "No merged image to save.")

    def build_sprite_sheet(self):
        if not self.selected_images:
            messagebox.showwarning(
                "No Images", "Select images to create a sprite sheet."
            )
            return

        try:
            columns = simpledialog.askinteger(
                "Columns", "Enter number of columns:", minvalue=1
            )
            if not columns:
                return

            rows = (len(self.selected_images) + columns - 1) // columns
            img_width, img_height = Image.open(self.selected_images[0]).size

            sprite_sheet = Image.new("RGBA", (img_width * columns, img_height * rows))
            for idx, img_path in enumerate(self.selected_images):
                img = Image.open(img_path)
                row, col = divmod(idx, columns)
                sprite_sheet.paste(img, (col * img_width, row * img_height))

            self.display_merged_image(sprite_sheet)
            messagebox.showinfo(
                "Sprite Sheet Complete", "Sprite sheet built successfully."
            )
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_mode_label(self):
        mode = "Recursive Directory" if self.var_recursive.get() else "Flat Directory"
        self.mode_label.config(text=f"Mode: {mode}")
        directory = self.path_var.get()
        if os.path.exists(directory):
            self.load_images(directory)
        else:
            messagebox.showerror("Error", "The directory path is invalid.")

    def update_view(self):
        """Reload images based on the current recursive setting."""
        directory = self.path_var.get()

        if os.path.exists(directory):
            self.load_images(directory)
        else:
            messagebox.showerror("Error", "The directory path is invalid.")

    def convert_to_png(self):
        # Ask the user to select files
        file_types = [("Image files", "*.webp *.avif"), ("All files", "*.*")]
        file_paths = filedialog.askopenfilenames(
            title="Select Images to Convert", filetypes=file_types
        )

        if not file_paths:
            return  # No files selected

        # Ask the user to choose a folder for saving converted images
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            messagebox.showwarning(
                "No Directory Selected", "Output directory not selected."
            )
            return

        success_count = 0
        error_files = []

        for file_path in file_paths:
            try:
                # Open the image and convert it to PNG
                img = Image.open(file_path)
                base_name = os.path.basename(file_path)
                name, _ = os.path.splitext(base_name)  # Remove the original extension
                output_path = os.path.join(output_dir, f"{name}.png")
                img.save(output_path, format="PNG")
                success_count += 1
            except Exception as e:
                print(f"Error converting {file_path}: {e}")
                error_files.append(file_path)

        # Show summary of the conversion process
        if success_count > 0:
            messagebox.showinfo(
                "Conversion Complete",
                f"Successfully converted {success_count} files to PNG.",
            )
        if error_files:
            messagebox.showerror(
                "Conversion Errors",
                f"Failed to convert the following files:\n{error_files}",
            )


if __name__ == "__main__":
    app = ImageToolApp()
    app.mainloop()