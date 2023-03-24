import cv2 as cv
import numpy as np


# Extract light directions & intensities from files and store them in a matrix
def fileToMatrix(path):
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        matrixString = [line.split(' ') for line in lines]
        matrix = [[float(item) for item in line] for line in matrixString]
    return matrix


# Extract the images names from a file
def imgNames(path):
    with open(path, 'r', encoding='utf-8') as file:
        names = file.readlines()
        return [name.strip('\n') for name in names]
    

# From a mask image, return a binary matrix were 1 defines a pixel of the object, 0 a pixel of the background
def binaryMask(path):
    mask = cv.imread(path, cv.IMREAD_UNCHANGED)
    if mask is None: 
        print('Couldn\'t load the mask object')
    else:
        binaryMask = np.zeros(mask.shape, np.uint8)
        cv.threshold(mask, 0, 1, cv.THRESH_BINARY, binaryMask)
        cv.imwrite("data/binaryMask.png", binaryMask)
        print(binaryMask[100])


# Return a table(96,h*w) containing all the images after treatment
def loadImages(imagesPath, intensitiesPath):
    lightIntensities = fileToMatrix(intensitiesPath)
    i = 0
    images=[]
    for name in imgNames(imagesPath):
        img = cv.imread("data/"+name, cv.IMREAD_UNCHANGED)
        if img is None:
            print('Couldn\'t load '+ name + 'image')
        else: 
            h, w, c = img.shape
            # unit16 => Float32
            imgNormalized = cv.normalize(img, None, 0, 1, cv.NORM_MINMAX, dtype=cv.CV_32F)
            imgNormalized[:,:,0] = imgNormalized[:,:,0] / lightIntensities[i][2]
            imgNormalized[:,:,1] = imgNormalized[:,:,1] / lightIntensities[i][1]
            imgNormalized[:,:,2] = imgNormalized[:,:,2] / lightIntensities[i][0] 
            imgGreyScale = cv.cvtColor(imgNormalized, cv.COLOR_BGR2GRAY)
            # image dimension: (h, w, c) => (h*w,)
            images.append(imgGreyScale.flatten())
            i+=1
    return images


# Get the normal vector (x,y,z) of every pixel of all images (313344 pixels)
def needleMap(directionsPath, intensitiesPath,imagesPath):
    # get the inverse of light directions matrix (from 96*3 to 3*96)
    lightDirectionsInv = np.linalg.pinv(fileToMatrix(directionsPath))
    images = loadImages(imagesPath,intensitiesPath)
    normals = np.dot(lightDirectionsInv, images)
    return normals
