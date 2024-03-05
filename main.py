import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilenames
from PIL import Image, ImageTk

THUMBNAIL_SIZE = (250, 250)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Watermarking App")


class Watermark(ttk.Frame):
    def __init__(self, container):
        super().__init__()
        self.container = container
        self.grid(padx=12, pady=12, column=0, row=0, sticky="N, W, E, S")
        # thumbnail image
        self.thumbnail_img = Image.open("placeholder.png")
        self.thumbnail_img.thumbnail(THUMBNAIL_SIZE)
        self.thumbnail_img = ImageTk.PhotoImage(self.thumbnail_img)
        for n in range(0, 3):
            self.thumbnail_label = ttk.Label(self, name=f"thumbnail{n + 1}")
            self.thumbnail_label.grid(column=n, row=0)
            self.thumbnail_label['image'] = self.thumbnail_img
        # Image being manipulated by Pillow
        self.img_to_watermark = Image.open("placeholder.png")
        self.img_list = []
        self.watermarked_imgs = []
        self.thumbnail_img_list = []
        # Buttons
        ttk.Button(self, text="Upload Image", command=self.browse).grid(column=0, row=1, sticky="S")
        ttk.Button(self, text="Watermark", command=self.watermark_img).grid(column=1, row=1, sticky="S")
        ttk.Button(self, text="Save Image", command=self.save_img).grid(column=2, row=1, sticky="S")

    def browse(self):
        f_path = askopenfilenames(initialdir="/",
                                  title="Choose Images",
                                  filetypes=(
                                      ("All Files", "*.*"), ("JPG files", "*.jpg*"), ("JPEG files", "*.jpeg*"),
                                      ("PNG files", "*.png*"),
                                  ))

        for index, img_path in enumerate(f_path):
            self.img_to_watermark = Image.open(img_path)
            self.img_list.append(self.img_to_watermark)

            self.thumbnail_img = Image.open(img_path)
            self.thumbnail_img.thumbnail(THUMBNAIL_SIZE)
            bg_img = Image.open("placeholder.png").copy()

            overlay_width, overlay_height = self.thumbnail_img.size
            bg_width, bg_height = bg_img.size
            offset_x = (bg_width - overlay_width) // 2
            offset_y = (bg_height - overlay_height) // 2

            bg_img.paste(self.thumbnail_img, (offset_x, offset_y))
            self.thumbnail_img = bg_img
            self.thumbnail_img = ImageTk.PhotoImage(self.thumbnail_img)
            self.thumbnail_img_list.append(self.thumbnail_img)
            if index + 1 < 4:
                self.nametowidget(f"thumbnail{index + 1}")['image'] = self.thumbnail_img

    def watermark_img(self):

        watermark = Image.open("watermark-example.png")
        watermark_opacity = watermark.copy()
        watermark_opacity.putalpha(90)
        watermark.paste(watermark_opacity, watermark)

        for img_to_watermark in self.img_list:
            img_to_watermark.putalpha(255)
            # watermark = watermark.resize((550, 550))
            img_to_watermark.alpha_composite(im=watermark, dest=(100, 100), source=(0, 0))
            self.watermarked_imgs.append(img_to_watermark)

        self.img_to_watermark = self.watermarked_imgs[0]

    def save_img(self):
        n = 1
        for index, img in enumerate(self.watermarked_imgs):
            img.save(fp=f"Watermarked_images/watermarked_image{n}.png")
            n += 1


if __name__ == "__main__":
    app = App()
    Watermark(app)
    app.mainloop()
