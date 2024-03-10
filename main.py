import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilenames
from PIL import Image, ImageTk
import numpy as np


THUMBNAIL_SIZE = (250, 250)


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Watermarking App")


class WatermarkApp(ttk.Frame):
    def __init__(self, container):
        super().__init__()
        self.container = container
        self.grid(padx=12, pady=12, column=0, row=0, sticky="N, W, E, S")
        # Thumbnail image
        self.thumbnail_img_list = []
        self.thumbnail_img = Image.open("placeholder.png")
        self.thumbnail_img.thumbnail(THUMBNAIL_SIZE)
        self.thumbnail_img = ImageTk.PhotoImage(self.thumbnail_img)
        col = 0
        row = -1
        for n in range(0, 9):
            if n % 3 == 0:
                row += 1
                col = 0
            self.thumbnail_label = ttk.Label(self, name=f"thumbnail{n + 1}")
            self.thumbnail_label.grid(column=col, row=row)
            self.thumbnail_label['image'] = self.thumbnail_img
            self.thumbnail_img_list.append(self.thumbnail_img)
            col += 1

        # Image being manipulated by Pillow
        self.images_to_watermark = []
        self.unedited_images = None
        self.watermarked_imgs = []
        # Buttons
        ttk.Button(self, text="Choose Images", command=self.browse).grid(column=0, row=3, sticky="S")
        ttk.Button(self, text="Watermark", command=self.watermark_imgs).grid(column=1, row=3, sticky="S")
        ttk.Button(self, text="Save All", command=self.save_img).grid(column=2, row=3, sticky="S")
        self.options_var = tk.StringVar()
        quick_options = ttk.Combobox(self, textvariable=self.options_var)
        quick_options["values"] = ("Centre", "Corner", "Edge", "Fill", "Repeating")
        quick_options["state"] = "readonly"
        quick_options.current(newindex=1)
        quick_options.grid(column=1, row=4, pady=5)

    def browse(self):
        f_path = askopenfilenames(initialdir="/",
                                  title="Choose Images",
                                  filetypes=(
                                      ("All Files", "*.*"), ("JPG files", "*.jpg*"), ("JPEG files", "*.jpeg*"),
                                      ("PNG files", "*.png*"),
                                  ))
        if f_path == "":
            pass
        else:
            self.images_to_watermark = [Image.open(img_path) for i, img_path in enumerate(f_path)]
            self.change_thumbnails(self.images_to_watermark)
            self.unedited_images = self.images_to_watermark.copy()

    def watermark_imgs(self):
        if self.images_to_watermark != self.unedited_images:
            self.images_to_watermark = self.unedited_images.copy()
            self.watermark_imgs()
        else:
            self.watermarked_imgs.clear()
            watermark = Image.open("watermark-example.png")
            watermark_opacity = watermark.copy()
            watermark_opacity.putalpha(90)
            watermark.paste(watermark_opacity, watermark)

            for og_img in self.images_to_watermark:
                img = og_img.copy()
                img.putalpha(255)
                watermark.thumbnail((img.width // 4, img.height // 4))
                wm_width, wm_height = watermark.width, watermark.height
                options_dic = {"Centre": ((img.width - wm_width) // 2,
                                          (img.height - wm_height) // 2),
                               "Corner": (0, 0),
                               "Edge": (0, (img.height - wm_height) // 2)}
                if self.options_var.get() == "Fill":
                    watermark = watermark.resize(img.size)
                    img.alpha_composite(im=watermark)
                elif self.options_var.get() == "Repeating":
                    splits = 4
                    arr = np.array(img)
                    h, w = arr.shape[:2]
                    h, w = (h // splits), (w // splits)
                    width, height = (w - wm_width) // 2, (h - wm_height) // 2
                    for _ in range(1, ((splits*splits) + 1)):
                        img.alpha_composite(im=watermark, dest=(width, height))
                        width += w
                        if _ % splits == 0:
                            height += h
                            print(width, height)
                            width = (w - wm_width) // 2
                else:
                    img.alpha_composite(im=watermark, dest=options_dic[self.options_var.get()])
                self.watermarked_imgs.append(img)

            self.change_thumbnails(self.watermarked_imgs)
            self.images_to_watermark.clear()

    def save_img(self):
        for index, img in enumerate(self.watermarked_imgs):
            img.save(fp=f"Watermarked_images/watermarked_image{index}.png")

    def change_thumbnails(self, img_list):
        self.thumbnail_img_list = self.thumbnail_img_list[:9]
        for n in range(1, 10):
            self.nametowidget(f"thumbnail{n}")['image'] = self.thumbnail_img_list[0]
        for index, img in enumerate(img_list):
            self.thumbnail_img = img.copy()
            self.thumbnail_img.thumbnail(THUMBNAIL_SIZE)
            bg_img = Image.new("RGB", (250, 250), (221, 221, 221))

            overlay_width, overlay_height = self.thumbnail_img.size
            bg_width, bg_height = bg_img.size
            offset_x = (bg_width - overlay_width) // 2
            offset_y = (bg_height - overlay_height) // 2

            bg_img.paste(self.thumbnail_img, (offset_x, offset_y))
            self.thumbnail_img = bg_img
            self.thumbnail_img = ImageTk.PhotoImage(self.thumbnail_img)
            self.thumbnail_img_list.append(self.thumbnail_img)
            if index < 9:
                self.nametowidget(f"thumbnail{index + 1}")['image'] = self.thumbnail_img


if __name__ == "__main__":
    app = App()
    WatermarkApp(app)
    app.mainloop()
