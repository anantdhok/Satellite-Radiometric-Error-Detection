import cv2
import numpy as np
import imutils

threshold = 15


class Detection:
    def __init__(self):
        self.image = cv2.imread('Testcases/Test.png')
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        (self.h, self.w) = self.getDimensions(self.image)
        self.errors = list()

    def getDimensions(self, image):
        (h, w) = image.shape[:2]
        return (h, w)

    def adjustResolution(self):
        self.image = imutils.resize(self.image, width=int(self.h + 1))
        self.image = imutils.resize(self.image, height=int(self.w + 1))

    def getNeighbors(self, x, y):
        ops = [-1, 0, +1]
        pixels = list()
        for opy in ops:
            for opx in ops:
                if (opy == y and opx == x):
                    continue
                try:
                    pixels.append(self.image[x + opx][y + opy])
                except:
                    pass
        return pixels

    def pixelDropout(self):
        data = self.image
        for i in range(self.h):
            for j in range(self.w):
                if (i == 0 or j == 0):
                    continue
                pixel = data[i, j]
                try:
                    neighbors = self.getNeighbors(i, j)
                    average = sum(neighbors)/len(neighbors)
                except:
                    pixel = average
                if (abs(average - pixel) > threshold):
                    self.errors.append("PixelDropout : at x = " + str(j) + " and y = " + str(i))

    def printErrors(self):
        for i in self.errors:
            print(i)


verify = Detection()
verify.adjustResolution()
verify.pixelDropout()
verify.printErrors()

cv2.imshow('Image', verify.image)
cv2.waitKey(0)
cv2.destroyAllWindows()
