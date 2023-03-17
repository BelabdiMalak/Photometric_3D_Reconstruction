import cv2 as cv
import numpy as np


# Extract light directions & intensities from files and store them in a matrix
def fileToMatrix(path):
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        matrixString = [line.split(' ') for line in lines]
        matrix = [[float(item) for item in line] for line in matrixString]
    return matrix


# From a mask image, return a binary matrix (image) were 1 defines a pixel of the object, 0 a pixel of the background
def binaryMatrix(path):
    mask = cv.imread(path, cv.IMREAD_UNCHANGED)
    if mask is None: 
        print('Couldn\'t load the mask object')
    else:
        binaryMask = np.zeros(mask.shape, np.uint8)
        cv.threshold(mask, 0, 1, cv.THRESH_BINARY, binaryMask)
        cv.imwrite("data/binaryMask.png", binaryMask)
        print(binaryMask[100])
