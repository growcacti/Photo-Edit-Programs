import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def split_image_into_tiles(image_path, tile_width, tile_height):
    image = Image.open(image_path)
    img_width, img_height = image.size

    tiles = []
    for i in range(0, img_width, tile_width):
        for j in range(0, img_height, tile_height):
            box = (i, j, i + tile_width, j + tile_height)
            tile = image.crop(box)
            tiles.append(tile)

    return tiles


def browse_file():
    filename = filedialog.askopenfilename(filetypes=(("PGN files", "*.pgn"), ("All files", "*.*")))
    entry_source_file.delete(0, tk.END)
    entry_source_file.insert(0, filename)

def start_splitting():
    input_file = entry_source_file.get()
    games_per_file = entry_games_per_file.get()
    try:
        games_per_file = int(games_per_file)
        split_pgn_file(input_file, games_per_file)
        messagebox.showinfo("Success", "The file has been split successfully.")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number of games per file.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Set up the GUI
root = tk.Tk()
root.title("PGN File Splitter")

tk.Label(root, text="Source PGN File:").grid(row=0, column=0)
entry_source_file = tk.Entry(root, width=50)
entry_source_file.grid(row=0, column=1)
button_browse = tk.Button(root, text="Browse", command=browse_file)
button_browse.grid(row=0, column=2)

tk.Label(root, text="Number of Games per File:").grid(row=1, column=0)
entry_games_per_file = tk.Entry(root)
entry_games_per_file.grid(row=1, column=1)

button_start = tk.Button(root, text="Start Splitting", command=start_splitting)
button_start.grid(row=2, column=1)

root.mainloop()
