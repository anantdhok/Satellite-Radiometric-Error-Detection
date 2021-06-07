import cv2
import numpy as np
import imutils

threshold = 60  # 60 for optimal results


class Detection:
    def __init__(self):
        self.image = cv2.imread('Testcases/Test3.png')
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        (self.h, self.w) = self.getDimensions(self.image)
        self.errors = list()

    def validate(self):
        self.pixelDropout()
        if (len(self.errors) > 0):
            for e in self.errors:
                self.lineDropout(e[2], e[1])

    def getDimensions(self, image):
        (h, w) = image.shape[:2]
        return (h, w)

    def adjustResolution(self):
        self.image = imutils.resize(self.image, width=int(self.w))
        self.image = imutils.resize(self.image, height=int(self.h))

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
        for r in range(self.w):
            for c in range(self.h):
                if (r == 0 or c == 0 or r == self.h-1 or c == self.w-1):
                    continue
                try:
                    pixel = data[r, c]
                    neighbors = self.getNeighbors(r, c)
                    average = sum(neighbors)/len(neighbors)
                except:
                    pixel = average
                if (abs(average - pixel) > threshold):
                    self.errors.append(['Pixel Dropout', r, c])

    def lineDropout(self, r, c):
        data = self.image
        (einl, einc) = (0, 0)
        for i in range(self.w):
            try:
                neighbors = self.getNeighbors(r, i)
                average = sum(neighbors)/len(neighbors)
            except:
                continue
            if (abs(average - data[r, i]) > threshold):
                einl += 1  # Error in Line
        for i in range(self.h):
            try:
                neighbors = self.getNeighbors(i, c)
                average = sum(neighbors)/len(neighbors)
            except:
                continue
            if (abs(average - data[i, c]) > threshold):
                einc += 1  # Error in Column
        if (einl != 0 or einc != 0):
            self.replaceErrors(einl, einc, r, c)

    def replaceErrors(self, line, coln, r, c):
        temp = list()
        if (line/self.w > 0.75):
            for i, e in enumerate(verify.errors):
                if e[1] != r:  # Eliminate close errors
                    if e[1] != r-1:
                        if e[1] != r+1:
                            temp.append(e)
            verify.errors = temp
            self.errors.append(['Line Dropout', c, None])
        if (coln/self.h > 0.75):
            for i, e in enumerate(verify.errors):
                if e[2] != c:  # Eliminate close errors
                    if e[2] != c-1:
                        if e[2] != c+1:
                            temp.append(e)
            verify.errors = temp
            self.errors.append(['Column Dropout', None, r])
        del temp

    def printErrors(self):
        for i in self.errors:
            print(i)


verify = Detection()
verify.adjustResolution()
verify.validate()
verify.printErrors()

cv2.imshow('Image', verify.image)
cv2.imwrite("Result.png", verify.image)
cv2.waitKey(0)
cv2.destroyAllWindows()
