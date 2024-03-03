import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageEnhance, ImageTk


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Watermarking App")


class Watermark(ttk.Frame):
    def __init__(self, container):
        super().__init__()
        self.grid(padx=12, pady=12, column=0, row=0, sticky="N, W, E, S")

        self.photo_to_watermark = ttk.Label(self)
        self.photo_to_watermark.grid(column=0, row=0, columnspan=3)
        self.img = Image.open("forest.jpg")
        self.wide_img = Image.open("forest.jpg")
        self.img = self.img.resize((1000, 450))
        self.image = ImageTk.PhotoImage(self.img)
        self.photo_to_watermark['image'] = self.image

        ttk.Button(self, text="Upload Image", command=self.browse).grid(column=0, row=1, sticky="S")
        ttk.Button(self, text="Watermark", command=self.watermark_img).grid(column=1, row=1, sticky="S")
        ttk.Button(self, text="Save Image", command=self.save_img).grid(column=2, row=1, sticky="S")

    def browse(self):
        f_path = askopenfilename(initialdir="/",
                                 title="Select File",
                                 filetypes=(
                                 ("JPG files", "*.jpg*"), ("JPEG files", "*.jpeg*"), ("PNG files", "*.png*"),
                                 ("All Files", "*.*"),))
        self.wide_img = Image.open(f_path)
        self.img = Image.open(f_path)
        if self.img.width > 1000 or self.img.height > 1000:
            width, height = self.img.width / 4, self.img.height / 4
            self.img = self.img.resize((int(width), int(height)))
        else:
            width, height = self.img.width / 4, self.img.height / 4
            self.img = self.img.resize((int(width), int(height)))
        self.image = ImageTk.PhotoImage(self.img)
        self.photo_to_watermark['image'] = self.image

    def watermark_img(self):
        im1 = self.wide_img
        im2 = Image.open("watermark-example.png")

        im2 = im2.resize(im1.size)
        im1.putalpha(256)
        im2.putalpha(48)

        new = Image.alpha_composite(im1=im1, im2=im2)

        brightness_factor = 1.2  # Increase brightness by 50%
        enhancer = ImageEnhance.Brightness(new)
        im_watermarked = enhancer.enhance(brightness_factor)

        im_watermarked.show()
        self.wide_img = im_watermarked

    def save_img(self):
        self.wide_img.save(fp="Watermarked_image.png")


if __name__ == "__main__":
    app = App()
    Watermark(app)
    app.mainloop()
