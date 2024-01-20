import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os
from datetime import datetime

Image.MAX_IMAGE_PIXELS = None 





class ImageTileSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Tile Splitter")

        # Instance variables
        self.auto_create_dir = tk.BooleanVar()

        # Setup the GUI
        self.setup_gui()

    def setup_gui(self):
        # Image selection
        tk.Label(self.root, text="Image Path:").grid(row=0, column=0)
        self.entry_image_path = tk.Entry(self.root, width=50)
        self.entry_image_path.grid(row=0, column=1)
        tk.Button(self.root, text="Browse", command=self.select_image).grid(row=0, column=2)

        # Tile size inputs
        tk.Label(self.root, text="Tile Width:").grid(row=1, column=0)
        self.entry_tile_width = tk.Entry(self.root)
        self.entry_tile_width.grid(row=1, column=1)
        tk.Label(self.root, text="Tile Height:").grid(row=2, column=0)
        self.entry_tile_height = tk.Entry(self.root)
        self.entry_tile_height.grid(row=2, column=1)

        # Output directory selection
        tk.Label(self.root, text="Output Directory:").grid(row=3, column=0)
        self.entry_output_dir = tk.Entry(self.root, width=50)
        self.entry_output_dir.grid(row=3, column=1)
        tk.Button(self.root, text="Browse", command=lambda: self.entry_output_dir.insert(0, filedialog.askdirectory())).grid(row=3, column=2)

        # Checkbox for auto-creating output directory
        tk.Checkbutton(self.root, text="Auto-create Output Directory", variable=self.auto_create_dir).grid(row=4, column=0)

        # Split button
        tk.Button(self.root, text="Split Image", command=self.split_image).grid(row=4, column=1)

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

        # Ensure all inputs are provided
        if not (image_path and tile_width and tile_height and output_dir) and not self.auto_create_dir.get():
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            image = Image.open(image_path)
            img_width, img_height = image.size

            if self.auto_create_dir.get():
                output_dir = os.path.join("output_tiles", datetime.now().strftime("%Y%m%d_%H%M%S"))
                os.makedirs(output_dir, exist_ok=True)
            else:
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)

            tile_number = 0
            for i in range(0, img_width, tile_width):
                for j in range(0, img_height, tile_height):
                    box = (i, j, i + tile_width, j + tile_height)
                    tile = image.crop(box)
                    tile_filename = f'tile_{tile_number}.png'
                    tile.save(os.path.join(output_dir, tile_filename))
                    tile_number += 1
            
            messagebox.showinfo("Success", f"Image split into {tile_number} tiles successfully!")

        except Exception as e:
            messagebox.showerror("Error", str(e))

# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageTileSplitterApp(root)
    root.mainloop()
