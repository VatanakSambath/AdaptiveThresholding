import tkinter
import cv2
from tkinter import *
from PIL import Image

def adaptive_bilateral(image):
    # Read the image.
    if not image:
        return tkinter.messagebox.showinfo(title="Info", message="Please load image first before apply any methods")
    else:
        img = cv2.imread(image)
        # Apply bilateral filter with d = 15,
        # sigmaColor = sigmaSpace = 75.
        bilateral = cv2.bilateralFilter(img, 15, 40, 40)
        outImage = Image.fromarray(bilateral)
        #outImage.show()
        # Save the output.
        cv2.imwrite('enhanceImage.jpg', bilateral)
        return outImage


def gaussianBlur(image):
    if not image:
        return tkinter.messagebox.showinfo(title="Info", message="Please load image first before apply any methods")
    else:
        image = cv2.imread(image)
        # Gaussian Blur
        Gaussian = cv2.GaussianBlur(image, (3, 3), 0)
        outImage = Image.fromarray(Gaussian)
        cv2.imwrite('enhanceImage.jpg', Gaussian)
        return outImage


def medianBlur(image):
    if not image:
        return tkinter.messagebox.showinfo(title="Info", message="Please load image first before apply any methods")
    else:
        image = cv2.imread(image)
        # Median Blur
        median = cv2.medianBlur(image, 5)
        outImage = Image.fromarray(median)
        cv2.imwrite('enhanceImage.jpg', median)
        return outImage

if __name__ == '__main__':
    #adaptive_bilateral('image.jpg')
    gaussianBlur('')
