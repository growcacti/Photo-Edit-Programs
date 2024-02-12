import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageChops, ImageTk
import numpy as np
import os

def ssim(img1, img2):
    """Simplified SSIM calculation between two images."""
    c1, c2 = (0.01 * 255)**2, (0.03 * 255)**2
    mean1, mean2 = img1.mean(), img2.mean()
    std1, std2 = img1.std(), img2.std()
    covariance = np.mean((img1 - mean1) * (img2 - mean2))
    ssim_index = ((2 * mean1 * mean2 + c1) * (2 * covariance + c2)) / ((mean1**2 + mean2**2 + c1) * (std1**2 + std2**2 + c2))
    return ssim_index

class ImageComparerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Comparer")
        self.geometry("800x600")
        self.image1_path = tk.StringVar()
        self.image2_path = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        tk.Button(self, text="Open Image 1", command=lambda: self.load_image(1)).grid(row=0, column=0, padx=10, pady=10)
        tk.Label(self, textvariable=self.image1_path).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(self, text="Open Image 2", command=lambda: self.load_image(2)).grid(row=1, column=0, padx=10, pady=10)
        tk.Label(self, textvariable=self.image2_path).grid(row=1, column=1, padx=10, pady=10)
        tk.Button(self, text="Show Diff Image", command=self.diff_image).grid(row=2, column=0, padx=10, pady=10)
        self.info = tk.Text(self, height=5, width=30)
        self.info.grid(row=4, column=0, columnspan=2, pady=10)
        self.img_label1 = tk.Label(self)
        self.img_label1.grid(row=3, column=0, padx=10, pady=10)
        self.img_label2 = tk.Label(self)
        self.img_label2.grid(row=3, column=1, padx=10, pady=10)
        self.img_label_diff = tk.Label(self)
        self.img_label_diff.grid(row=3, column=2, padx=10, pady=10)

    def update_image_label(self, img_path, label_widget):
        img = Image.open(img_path)
        img.thumbnail((200, 200))
        photo = ImageTk.PhotoImage(img)
        label_widget.config(image=photo)
        label_widget.image = photo

    def load_image(self, image_number):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif *.bmp")])
        if file_path:
            if image_number == 1:
                self.image1_path.set(file_path)
                self.update_image_label(file_path, self.img_label1)
            else:
                self.image2_path.set(file_path)
                self.update_image_label(file_path, self.img_label2)

    def diff_image(self):
        if self.image1_path.get() and self.image2_path.get():
            im1 = Image.open(self.image1_path.get()).convert('L')
            im2 = Image.open(self.image2_path.get()).convert('L')
            im1 = im1.resize(im2.size)
            diff = ImageChops.difference(im1, im2)
            diff = diff.point(lambda x: x * 10)
            diff_path = "diff.png"
            diff.save(diff_path)
            self.update_image_label(diff_path, self.img_label_diff)
            self.calculate_ssim(im1, im2)
            self.rmse(im1, im2)
        else:
            messagebox.showerror("Error", "Please select both images first.")

    def calculate_ssim(self, im1, im2):
        img1 = np.array(im1)
        img2 = np.array(im2)
        s = ssim(img1, img2)
        self.info.insert(tk.END, f"SSIM: {s}\n")

    def rmse(self, im1, im2):
        pixels1 = np.array(im1)
        pixels2 = np.array(im2)
        differences = pixels1 - pixels2
        squared_diff = np.square(differences)
        mean_squared_diff = np.mean(squared_diff)
        rmse_val = np.sqrt(mean_squared_diff)
        self.info.insert(tk.END, f"RMSE: {rmse_val}\n")

if __name__ == "__main__":
    app = ImageComparerApp()
    app.mainloop()
