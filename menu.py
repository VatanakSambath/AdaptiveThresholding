import tkinter
from tkinter import *
from tkinter import filedialog as fd
from PIL import Image, ImageTk
import adaptiveThreshholding as at
import imageEnhancement
import cv2
import time

app = Tk()
app.title('Image Binarization')
app.geometry('680x400')
app.eval('tk::PlaceWindow . center')
app.resizable(False, False)
frm = Frame(app)
image = ""
imagePath = ""

menubar = Menu(app)
app.config(menu=menubar)

originalImageTitle = tkinter.Label(app, text="Original Image with Enhancement")
originalImageTitle.pack(pady=15, padx=0)
originalImageTitle.pack_forget()
lblImage = Label(app)
lblImage.pack(pady=0, padx=0)
lblImage.pack_forget()

binarizeImageTitle = tkinter.Label(app, text="Image after binarization")
binarizeImageTitle.pack(pady=15, padx=0)
binarizeImageTitle.pack_forget()
lblImageUpdate = Label(app)
lblImageUpdate.pack(pady=0)
lblImageUpdate.pack_forget()

file_menu = Menu(menubar)
file_menu = Menu(menubar, tearoff=False)
tool_menu = Menu(menubar)
tool_menu = Menu(menubar, tearoff=False)
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
    originalImageTitle.pack(pady=15, padx=0)
    img.thumbnail((630, 630))
    img = ImageTk.PhotoImage(img)
    lblImage.configure(image=img)
    lblImage.image = img
    lblImage.pack()
    # showinfo(title='Selected File', message=filename)

def setImage(outImage):
    outImage.thumbnail((630, 630))
    img = ImageTk.PhotoImage(outImage)
    lblImage.configure(image=img)
    lblImage.image = img

def adaptive_threshholding(image):
    outImg = at.bradley_roth_numpy(image, False)
    if outImg:
        binarizeImageTitle.pack(pady=10, padx=0)
        outImg.thumbnail((630, 630))
        img = ImageTk.PhotoImage(outImg)
        lblImageUpdate.configure(image=img)
        lblImageUpdate.image = img
        lblImageUpdate.pack(pady=0)

def otsu_with_adaptiveThresholding(image, imagePath):
    if not image:
        return tkinter.messagebox.showinfo(title="Info", message="Please load image first before apply any methods")
    else:
        img = cv2.imread(imagePath)
        grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh, binaryImg = cv2.threshold(grayImg, 0, 255, cv2.THRESH_OTSU)
        outImg = at.bradley_roth_numpy(image, False, None, thresh)
        binarizeImageTitle.pack(pady=10, padx=0)
        outImg.thumbnail((630, 630))
        img = ImageTk.PhotoImage(outImg)
        lblImageUpdate.configure(image=img)
        lblImageUpdate.image = img
        lblImageUpdate.pack(pady=0)

def erosion_adaptive_threshholding(image):
    if image:
        outImg = at.bradley_roth_numpy(image, True)
        binarizeImageTitle.pack(pady=10, padx=0)
        outImg.thumbnail((630, 630))
        img = ImageTk.PhotoImage(outImg)
        lblImageUpdate.configure(image=img)
        lblImageUpdate.image = img
        lblImageUpdate.pack(pady=0)

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

def clearEnhancement(imgPath):
    if imgPath:
        img = Image.open(imgPath)
        global image
        image = Image.open(imgPath).convert('L')
        img.thumbnail((630, 630))
        img = ImageTk.PhotoImage(img)
        lblImage.configure(image=img)
        lblImage.image = img
    else:
        return tkinter.messagebox.showinfo(title="Info", message="Please load image first before clear any methods")

menubar.add_cascade(label="File", menu=file_menu, underline=0)
menubar.add_cascade(label="Tools", menu=tool_menu, underline=0)
menubar.add_cascade(label="Enhancement", menu=enhance_menu, underline=0)
menubar.add_cascade(label="Binarization", menu=binarize_menu, underline=0)

file_menu.add_command(label='Load Image', command=select_file)
file_menu.add_command(label='Exit', command=app.destroy)

enhance_menu.add_command(label='Gaussian Blurring', command=lambda: gaussian_enhancement(imagePath), underline=0)
enhance_menu.add_command(label='Bilateral Blurring', command=lambda: bilateral_enhancement(imagePath), underline=0)
enhance_menu.add_command(label='Median Blurring', command=lambda: median_threshholding(imagePath), underline=0)

binarize_menu.add_command(label='Adaptive Thresholding', command=lambda: adaptive_threshholding(image), underline=0)
binarize_menu.add_command(label='Erosion & Adaptive Thresholding', command=lambda: erosion_adaptive_threshholding(image), underline=0)
binarize_menu.add_command(label='Otsu & Adaptive Thresholding', command=lambda: otsu_with_adaptiveThresholding(image, imagePath), underline=0)

tool_menu.add_command(label='Clear Enhancement', command=lambda: clearEnhancement(imagePath), underline=0)


def main():
    # start a program
    app.mainloop()


if __name__ == "__main__":
    main()
