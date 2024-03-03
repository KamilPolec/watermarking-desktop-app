from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageEnhance, ImageTk


def browse():
    global img
    global image
    global wide_img
    f_path = askopenfilename(initialdir="/",
                             title="Select File",
                             filetypes=(("JPG files", "*.jpg*"), ("JPEG files", "*.jpeg*"), ("PNG files", "*.png*"), ("All Files", "*.*"),))
    wide_img = Image.open(f_path)
    img = Image.open(f_path)
    if img.width > 2000 or img.height > 2000:
        width, height = img.width / 4, img.height / 4
        img = img.resize((int(width), int(height)))
    else:
        width, height = img.width / 4, img.height / 4
        img = img.resize((int(width), int(height)))
    image = ImageTk.PhotoImage(img)
    photo_to_watermark['image'] = image


def watermark_img():
    global wide_img
    im1 = wide_img
    im2 = Image.open("watermark-example.png")

    im2 = im2.resize(im1.size)
    im1.putalpha(256)
    im2.putalpha(48)

    new = Image.alpha_composite(im1=im1, im2=im2)

    brightness_factor = 1.2  # Increase brightness by 50%
    enhancer = ImageEnhance.Brightness(new)
    im_watermarked = enhancer.enhance(brightness_factor)

    im_watermarked.show()
    wide_img = im_watermarked


def save_img():
    global wide_img
    wide_img.save(fp="Watermarked_image.png")


root = Tk()
root.title("Watermarking Program")

content = ttk.Frame(root, padding="12")
content.grid(column=0, row=0, sticky="N, W, E, S")

photo_to_watermark = ttk.Label(content)
photo_to_watermark.grid(column=0, row=0, columnspan=3)
img = Image.open("forest.jpg")
wide_img = Image.open("forest.jpg")
# print(int(img.height))
img = img.resize((1000, 450))
image = ImageTk.PhotoImage(img)
photo_to_watermark['image'] = image


ttk.Button(content, text="Upload Image", command=browse).grid(column=0, row=1, sticky="S")

ttk.Button(content, text="Watermark", command=watermark_img).grid(column=1, row=1, sticky="S")
ttk.Button(content, text="Save Image", command=save_img).grid(column=2, row=1, sticky="S")

root.mainloop()
