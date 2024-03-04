import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, askopenfilenames
from PIL import Image, ImageEnhance, ImageTk
from random import randint


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
        self.img_to_watermark = Image.open("forest.jpg")
        self.img = self.img.resize((1000, 450))
        self.image = ImageTk.PhotoImage(self.img)
        self.photo_to_watermark['image'] = self.image
        self.img_list = []
        self.watermarked_imgs = []
        ttk.Button(self, text="Upload Image", command=self.browse).grid(column=0, row=1, sticky="S")
        ttk.Button(self, text="Watermark", command=self.watermark_img).grid(column=1, row=1, sticky="S")
        ttk.Button(self, text="Save Image", command=self.save_img).grid(column=2, row=1, sticky="S")

    def browse(self):
        f_path = askopenfilenames(initialdir="/",
                                  title="Choose Images",
                                  filetypes=(
                                      ("JPG files", "*.jpg*"), ("JPEG files", "*.jpeg*"), ("PNG files", "*.png*"),
                                      ("All Files", "*.*"),))

        for img in f_path:
            self.img_to_watermark = Image.open(img)
            self.img_list.append(self.img_to_watermark)

        self.img = Image.open(f_path[0])
        if self.img.width > 1000 or self.img.height > 1000:
            width, height = self.img.width / 4, self.img.height / 4
            self.img = self.img.resize((int(width), int(height)))
        else:
            width, height = self.img.width / 4, self.img.height / 4
            self.img = self.img.resize((int(width), int(height)))
        self.image = ImageTk.PhotoImage(self.img)
        self.photo_to_watermark['image'] = self.image

    def watermark_img(self):
        watermark = Image.open("watermark-example.png")
        for img_to_watermark in self.img_list:
            watermark = watermark.resize(img_to_watermark.size)
            img_to_watermark.putalpha(256)
            watermark.putalpha(48)

            new = Image.alpha_composite(im1=img_to_watermark, im2=watermark)

            brightness_factor = 1.2  # Increase brightness by 50%
            enhancer = ImageEnhance.Brightness(new)
            im_watermarked = enhancer.enhance(brightness_factor)
            self.watermarked_imgs.append(im_watermarked)
            # im_watermarked.show()
        self.img_to_watermark = self.watermarked_imgs[0]

    def save_img(self):
        n = 1
        for img in self.watermarked_imgs:
            img.save(fp=f"Watermarked_images/watermarked_image{n}.png")
            n += 1


if __name__ == "__main__":
    app = App()
    Watermark(app)
    app.mainloop()
