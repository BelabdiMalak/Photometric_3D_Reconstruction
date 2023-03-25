import cv2 as cv
import numpy as np
import math


def fileToMatrix(path):
    with open(path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        matrixString = [line.split(' ') for line in lines]
        return [[float(item) for item in line] for line in matrixString]


def imgNames():
    with open('data/filenames.txt', 'r', encoding='utf-8') as file:
        names = file.readlines()
        return [name.strip('\n') for name in names]
    

def binaryMask():
    mask = cv.imread('data/mask.png', cv.IMREAD_UNCHANGED)
    if mask is None: 
        print('Couldn\'t load the mask object')
    else:
        binaryMask = np.zeros(mask.shape, np.uint8)
        cv.threshold(mask, 0, 1, cv.THRESH_BINARY, binaryMask)
        return binaryMask



def loadImages():
    lightIntensities = fileToMatrix('data/light_intensities.txt')
    i = 0
    images=[]
    for name in imgNames():
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
def needleMap():
    # get the inverse of light directions matrix (from 96*3 to 3*96)
    lightDirectionsInv = np.linalg.pinv(fileToMatrix('data/light_directions.txt'))
    images = loadImages()
    return np.dot(lightDirectionsInv, images)

def showImg2D():
    normalVectors = needleMap()
    mask = binaryMask()
    h,w = mask.shape
    i = 0
    
    image = np.zeros((3,h,w), np.float32)
    for line in normalVectors:
        matrix = np.reshape(line, (-1,w))
        image[i] = matrix
        i+=1

    # Reshape & show 2D image (RVB)
    img2D = np.zeros((h,w,3),np.float32)
    for y in range(h):
        for x in range(w):
            img2D[y,x] = [image[0,y,x], image[1,y,x], image[2,y,x]]
    
    cv.imshow('2D',img2D)

    img3D = np.zeros((h,w,3), np.float32)
    for y in range(h):
        for x in range(w):
            if(mask[y,x]==1):
                n = math.sqrt(img2D[y,x,0]**2 + img2D[y,x,1]**2  + img2D[y,x,2]**2)
                for z in range(3):
                    img3D[y,x,z] = (float)(img2D[y,x,z])
                    img3D[y,x,z] = ((img3D[y,x,z])/n+1.)/2.

    cv.imshow('3D',img3D)
    cv.waitKey(0)
    cv.destroyAllWindows(0)

