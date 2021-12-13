import os
import tkinter
from tkinter import *
from tkinter import filedialog as fd

import numpy as np
from PIL import Image, ImageTk
from skimage.color import rgb2gray

import adaptiveThreshholding as at
import imageEnhancement
import cv2
from skimage import color, data, restoration
from matplotlib import pyplot as plt, pyplot

app = Tk()
app.title('Image Binarization Apply on Palm Leaf Menuscripts')
app.geometry('680x400')
app.eval('tk::PlaceWindow . center')
#app.resizable(False, False)
frm = Frame(app)

image = ""
imagePath = ""
OIT = StringVar()
OIT.set("Original Image")
BIT = StringVar()

menubar = Menu(app)
app.config(menu=menubar)

originalImageTitle = tkinter.Label(app, textvariable=OIT)
originalImageTitle.pack(pady=15, padx=0)
originalImageTitle.pack_forget()
lblImage = Label(app)
lblImage.pack(pady=0, padx=0)
lblImage.pack_forget()

binarizeImageTitle = tkinter.Label(app, textvariable=BIT)
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
about_menu = Menu(menubar)
about_menu = Menu(menubar, tearoff=False)


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


def save_image(image):
    img = ImageTk.PhotoImage(image)
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(dir_path, "save-image")
    if not os.path.exists(path):
        os.mkdir(path)
    image.save(os.path.join(dir_path, "save-image","save_image.jpg"))
    tkinter.messagebox.showinfo(title="Info", message="Image saved")



def setImage(outImage):
    outImage.thumbnail((630, 630))
    img = ImageTk.PhotoImage(outImage)
    lblImage.configure(image=img)
    lblImage.image = img


def adaptive_threshholding(img):
    if not img:
        return tkinter.messagebox.showinfo(title="Info", message="Please load image first before apply any methods")
    else:
        outImg = at.bradley_roth_numpy(img, False)
        global image
        image = outImg
        BIT.set("Binarization with Adaptive Thresholding")
        binarizeImageTitle.pack(pady=10, padx=0)
        outImg.thumbnail((630, 630))
        img = ImageTk.PhotoImage(outImg)
        lblImageUpdate.configure(image=img)
        lblImageUpdate.image = img
        lblImageUpdate.pack(pady=0)


def otsu_with_adaptiveThresholding(image, imagePath): #has some problem with thresholding value
    if not image:
        return tkinter.messagebox.showinfo(title="Info", message="Please load image first before apply any methods")
    else:
        BIT.set("Binarization with Otsu and Adaptive Thresholding")
        #img = cv2.imread(imagePath, cv2.IMREAD_GRAYSCALE)
        img = cv2.imread(imagePath)
        grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        #print(grayImg)
        thresh, binaryImg = cv2.threshold(grayImg, 0, 255,cv2.THRESH_BINARY, cv2.THRESH_OTSU)
        print(thresh)
        outImg = at.bradley_roth_numpy(image, False, None, thresh)
        # global image
        # image = outImg
        binarizeImageTitle.pack(pady=10, padx=0)
        outImg.thumbnail((630, 630))
        img = ImageTk.PhotoImage(outImg)
        lblImageUpdate.configure(image=img)
        lblImageUpdate.image = img
        lblImageUpdate.pack(pady=0)

        # plt.subplot(3, 3, 3 + 1), plt.imshow(binaryImg, 'gray')
        # plt.show()
        #cv2.imshow("image",grayImg)


def erosion_adaptive_threshholding(img):
    if not img:
        return tkinter.messagebox.showinfo(title="Info", message="Please load image first before apply any methods")
    else:
        BIT.set("Binarization with Adaptive Thresholding and apply Erosion")
        outImg = at.bradley_roth_numpy(img, True)
        global image
        image = outImg
        binarizeImageTitle.pack(pady=10, padx=0)
        outImg.thumbnail((630, 630))
        img = ImageTk.PhotoImage(outImg)
        lblImageUpdate.configure(image=img)
        lblImageUpdate.image = img
        lblImageUpdate.pack(pady=0)


def bilateral_enhancement(img):
    if not img:
        return tkinter.messagebox.showinfo(title="Info", message="Please load image first before apply any methods")
    else:
        outImg = imageEnhancement.adaptive_bilateral(img)
        OIT.set("Original Image with Bilateral Filtering")
        setImage(outImg)
        global image
        image = Image.open('enhanceImage.jpg').convert('L')


def gaussian_enhancement(img):
    if not img:
        return tkinter.messagebox.showinfo(title="Info", message="Please load image first before apply any methods")
    else:
        outImg = imageEnhancement.gaussianBlur(img)
        OIT.set("Original Image with Gussian Filtering")
        setImage(outImg)
        global image
        image = Image.open('enhanceImage.jpg').convert('L')


def median_enhancement(img):
    if not img:
        return tkinter.messagebox.showinfo(title="Info", message="Please load image first before apply any methods")
    else:
        outImg = imageEnhancement.medianBlur(img)
        OIT.set("Original Image with Median Filtering")
        setImage(outImg)
        global image
        image = Image.open('enhanceImage.jpg').convert('L')


def wiener_enhancement(img):
    if not img:
        return tkinter.messagebox.showinfo(title="Info", message="Please load image first before apply any methods")
    else:
        imgnew = rgb2gray(plt.imread(img))
        #img = color.rgb2gray(data.astronaut())
        from scipy.signal import convolve2d
        psf = np.ones((5, 5)) / 4
        print(psf)
        img = convolve2d(imgnew, psf, 'same')
        img += 0.1 * img.std() * np.random.standard_normal(imgnew.shape)
        deconvolved_img = restoration.wiener(img, psf, 50)
        #cv2.imshow('', deconvolved_img)
        deconvolved_img = cv2.convertScaleAbs(deconvolved_img, alpha=255.0)
        cv2.imwrite('enhanceImage.jpg', deconvolved_img)
        #pyplot.imsave('enhanceImage.jpg', deconvolved_img)
        OIT.set("Original Image with Wiener Filtering")
        img = Image.open('enhanceImage.jpg')
        setImage(img)
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
        OIT.set("Image After Clear the enhancement method")
    else:
        return tkinter.messagebox.showinfo(title="Info", message="Please load image first before clear any methods")


def about():
    return tkinter.messagebox.showinfo(title="Info", message="Image saved")


menubar.add_cascade(label="File", menu=file_menu, underline=0)
menubar.add_cascade(label="Tools", menu=tool_menu, underline=0)
menubar.add_cascade(label="Enhancement", menu=enhance_menu, underline=0)
menubar.add_cascade(label="Binarization", menu=binarize_menu, underline=0)
menubar.add_cascade(label="Help", menu=about_menu, underline=0)

file_menu.add_command(label='Load Image', command=select_file)
file_menu.add_command(label='Save Image', command=lambda: save_image(image), underline=0)
file_menu.add_command(label='Exit', command=app.destroy)

enhance_menu.add_command(label='Gaussian Filtering', command=lambda: gaussian_enhancement(imagePath), underline=0)
enhance_menu.add_command(label='Bilateral Filtering', command=lambda: bilateral_enhancement(imagePath), underline=0)
enhance_menu.add_command(label='Median Filtering', command=lambda: median_enhancement(imagePath), underline=0)
enhance_menu.add_command(label='Wiener Filtering', command=lambda: wiener_enhancement(imagePath), underline=0)

binarize_menu.add_command(label='Adaptive Thresholding', command=lambda: adaptive_threshholding(image), underline=0)
binarize_menu.add_command(label='Erosion & Adaptive Thresholding', command=lambda: erosion_adaptive_threshholding(image), underline=0)
binarize_menu.add_command(label='Otsu & Adaptive Thresholding', command=lambda: otsu_with_adaptiveThresholding(image, imagePath), underline=0)

tool_menu.add_command(label='Clear Enhancement', command=lambda: clearEnhancement(imagePath), underline=0)

about_menu.add_command(label='About', command=lambda: about(), underline=0)


def main():
    # start a program
    app.mainloop()


if __name__ == "__main__":
    main()
