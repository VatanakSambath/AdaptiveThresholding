from tkinter import *
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import adaptiveThreshholding as at
import imageEnhancement
import cv2
import numpy as np

app = Tk()
app.title('Image Processing')
app.geometry('650x400')
app.eval('tk::PlaceWindow . center')
app.resizable(False, False)
frm = Frame(app)
image = ""
imagePath = ""

menubar = Menu(app)
app.config(menu=menubar)

lblImage = Label(app)
lblImage.pack(pady=120)

file_menu = Menu(menubar)
file_menu = Menu(menubar, tearoff=False)
enhance_menu = Menu(menubar)
enhance_menu = Menu(menubar, tearoff=False)
binarize_menu = Menu(menubar)
binarize_menu = Menu(menubar, tearoff=False)


def select_file():
    filetypes = (('JPG Files', '*.jpg'), ('PNG Files', '*.png'), ('JPEG Files', '*.jpeg'), ('All files', '*.*'))
    filename = fd.askopenfilename(title='Open a file', initialdir='C:/Users/Gaming Store/Downloads/palmleaf_doc_img_v_beta/', filetypes=filetypes)
    global imagePath
    imagePath = filename
    img = Image.open(filename)
    imgnew = Image.open(filename).convert('L')
    global image
    image = imgnew
    # img = img.resize(300, 300)
    img.thumbnail((450, 450))
    img = ImageTk.PhotoImage(img)
    lblImage.configure(image=img)
    lblImage.image = img
    # showinfo(title='Selected File', message=filename)

def setImage(outImage):
    outImage.thumbnail((450, 450))
    img = ImageTk.PhotoImage(outImage)
    lblImage.configure(image=img)
    lblImage.image = img

def adaptive_threshholding(image):
    outImg = at.bradley_roth_numpy(image)
    # outImg.thumbnail((450, 450))
    # img = ImageTk.PhotoImage(outImg)
    # lblImage.configure(image=img)
    # lblImage.image = img

def bilateral_enhancement(img):
    outImg = imageEnhancement.adaptive_bilateral(img)
    if outImg:
        setImage(outImg)
        global image
        image = Image.open('enhanceImage.jpg').convert('L')

def gaussian_enhancement(img):
    outImg = imageEnhancement.gaussianBlur(img)
    if outImg:
        setImage(outImg)
        global image
        image = Image.open('enhanceImage.jpg').convert('L')

def median_threshholding(img):
    outImg = imageEnhancement.medianBlur(img)
    if outImg:
        setImage(outImg)
        global image
        image = Image.open('enhanceImage.jpg').convert('L')

menubar.add_cascade(label="File", menu=file_menu, underline=0)
menubar.add_cascade(label="Enhancement", menu=enhance_menu, underline=0)
menubar.add_cascade(label="Binarization", menu=binarize_menu, underline=0)

file_menu.add_command(label='Load Image', command=select_file)
file_menu.add_command(label='Exit', command=app.destroy)

enhance_menu.add_command(label='Gaussian Blurring', command=lambda: gaussian_enhancement(imagePath), underline=0)
enhance_menu.add_command(label='Bilateral Blurring', command=lambda: bilateral_enhancement(imagePath), underline=0)
enhance_menu.add_command(label='Median Blurring', command=lambda: median_threshholding(imagePath), underline=0)

binarize_menu.add_command(label='Adaptive Thresholding', command=lambda: adaptive_threshholding(image), underline=0)
binarize_menu.add_command(label='Otsu & Adaptive Thresholding', command=lambda: adaptive_threshholding(image), underline=0)


def main():
    # start a program
    app.mainloop()


if __name__ == "__main__":
    main()
