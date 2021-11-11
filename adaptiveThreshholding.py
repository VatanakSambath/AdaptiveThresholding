import tkinter
import numpy as np
from PIL import Image
import cv2
from ctypes import *


def bradley_roth_numpy(image, isErosion, s=None, t=None):
    if not image:
        return tkinter.messagebox.showinfo(title="Info", message="Please load image first before apply any methods")
    else:
        # Convert image to numpy array
        img = np.array(image).astype(np.float)

        # Default window size is round(cols/8)
        if s is None:
            s = np.round(img.shape[1] / 8)

        # Default threshold is 15% of the total
        # area in the window
        if t is None:
            t = 23.0
        print("threshold value: " + str(t))
        # Compute integral image
        intImage = np.cumsum(np.cumsum(img, axis=1), axis=0)

        # Define grid of points
        (rows, cols) = img.shape[:2]
        (X, Y) = np.meshgrid(np.arange(cols), np.arange(rows))

        # Make into 1D grid of coordinates for easier access
        X = X.ravel()
        Y = Y.ravel()

        # Ensure s is even so that we are able to index into the image
        # properly
        s = s + np.mod(s, 2)

        # Access the four corners of each neighbourhood
        x1 = X - s / 2
        x2 = X + s / 2
        y1 = Y - s / 2
        y2 = Y + s / 2

        # Ensure no coordinates are out of bounds
        x1[x1 < 0] = 0
        x2[x2 >= cols] = cols - 1
        y1[y1 < 0] = 0
        y2[y2 >= rows] = rows - 1

        # Ensures coordinates are integer
        x1 = x1.astype(np.int)
        x2 = x2.astype(np.int)
        y1 = y1.astype(np.int)
        y2 = y2.astype(np.int)

        # Count how many pixels are in each neighbourhood
        count = (x2 - x1) * (y2 - y1)

        # Compute the row and column coordinates to access
        # each corner of the neighbourhood for the integral image
        f1_x = x2
        f1_y = y2
        f2_x = x2
        f2_y = y1 - 1
        f2_y[f2_y < 0] = 0
        f3_x = x1 - 1
        f3_x[f3_x < 0] = 0
        f3_y = y2
        f4_x = f3_x
        f4_y = f2_y

        # Compute areas of each window
        sums = intImage[f1_y, f1_x] - intImage[f2_y, f2_x] - intImage[f3_y, f3_x] + intImage[f4_y, f4_x]

        # Compute thresholded image and reshape into a 2D grid
        out = np.ones(rows * cols, dtype=np.bool)
        out[img.ravel() * count <= sums * (100.0 - t) / 100.0] = False

        # Also convert back to uint8
        out = 255 * np.reshape(out, (rows, cols)).astype(np.uint8)
        outImage = Image.fromarray(out)
        outImage.save("adaptiveThresholdImage.jpg")

        if isErosion is True:
            #apply Morphological Transformations (Dilation)
            img = cv2.imread("adaptiveThresholdImage.jpg", 0)
            kernel = np.ones((2, 2), np.uint8)
            #erosion
            out = cv2.erode(img, kernel, iterations=1)
            #dilation
            # dilation = cv2.dilate(img, kernel, iterations=1)
            #outImage = Image.fromarray(out)
            #outImage.show()
        #else:
            #outImage.show()
            # Return PIL image back to user
        return Image.fromarray(out)


def adaptive_thresh(input_img):
    h, w, _ = input_img.shape
    S = w / 8
    s2 = S / 2
    T = 23.0

    # integral img
    int_img = np.zeros_like(input_img, dtype=np.uint32)
    # for col in range(w):
    #     for row in range(h):
    #         int_img[row, col] = input_img[0:row, 0:col].sum()
    for col in range(w):
        sumn = 0
        for row in range(h):
            sumn += sum(input_img[row, col])
            if col == 0:
                int_img[row, col] = sumn
            else:
                int_img[row, col] = input_img[row - 1, col] + sumn
    #output img
    out_img = np.zeros_like(input_img)

    for col in range(w):
        for row in range(h):
            # SxS region
            y0 = int(max(row - s2, 0))
            y1 = int(min(row + s2, h - 1))
            x0 = int(max(col - s2, 0)) #i
            x1 = int(min(col + s2, w - 1)) #i
            count = (y1 - y0) * (x1 - x0)
            sum_ = int_img[y1, x1] - int_img[y0, x1 - 1] - int_img[x1 - 1, y1] + int_img[x0 - 1, y1 - 1]
            value = input_img[row, col] * count <= sum_ * (100. - T) / 100.
            if value.all():
                out_img[row, col] = 0
            else:
                out_img[row, col] = 255

    return Image.fromarray(out_img)


if __name__ == '__main__':
    # img = Image.open('image.jpg').convert('L')
    # out = bradley_roth_numpy(img)
    image = cv2.imread('001_nl_b334_051_01.jpg')
    image = cv2.GaussianBlur(image, (5, 5), cv2.BORDER_DEFAULT)
    out = adaptive_thresh(image)
    out.show()
    out.save('output.jpg')
