import cv2 as cv
import numpy as np


# Extract light directions & intensities from files and store them in a matrix
def fileToMatrix(path):
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        matrixString = [line.split(' ') for line in lines]
        matrix = [[float(item) for item in line] for line in matrixString]
    return matrix


def fileNames(path):
    with open(path, 'r', encoding='utf-8') as file:
        names = file.readlines()
        return [name.strip('\n') for name in names]
    


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

def loadImages(imagesPath, intensitiesPath):
    lightIntensities = fileToMatrix(intensitiesPath)
    i = 0
    for name in fileNames(imagesPath):
        img = cv.imread("data/"+name, cv.IMREAD_UNCHANGED)
        if img is None:
            print('Couldn\'t load '+ name + 'image')
        else: 
            print(i)
            imgNormalized = cv.normalize(img, None, 0, 1, cv.NORM_MINMAX, dtype=cv.CV_32F)
            h, w, c = img.shape
            print(len(lightIntensities))
            imgNormalized[:,:,0] = imgNormalized[:,:,0] / lightIntensities[i][2]
            imgNormalized[:,:,1] = imgNormalized[:,:,1] / lightIntensities[i][1]
            imgNormalized[:,:,2] = imgNormalized[:,:,2] / lightIntensities[i][0] 
            i+=1
            imgGreyScale = cv.cvtColor(imgNormalized, cv.COLOR_BGR2GRAY)

loadImages('data/filenames.txt', 'data/light_intensities.txt')