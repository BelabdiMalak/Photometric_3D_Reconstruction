import matplotlib.pyplot as plt
import numpy as np
import cv2
import math


LIGHT_DIRECTIONS_PATH  = 'data/light_directions.txt'
LIGHT_INTENSITIES_PATH = 'data/light_intensities.txt'
IMAGES_NAMES_PATH = 'data/filenames.txt'
MASK_PATH = 'data/mask.png'
IMAGES_PATH = 'data/'


def load_light_info(file):
    return np.genfromtxt(file, delimiter=' ')


def load_mask():
    mask = cv2.imread(MASK_PATH, cv2.IMREAD_UNCHANGED)
    if mask is None: 
        print('Couldn\'t load the mask object')
    else:
        binary_mask = np.zeros(mask.shape, np.uint8)
        cv2.threshold(mask, 0, 1, cv2.THRESH_BINARY, binary_mask)
        return binary_mask 


def load_img_names():
    with open(IMAGES_NAMES_PATH, 'r', encoding='utf-8') as file:
        names = file.readlines()
        return [name.strip('\n') for name in names]


def normalize_img():
    intensities = load_light_info(LIGHT_INTENSITIES_PATH)
    i = 0
    images=[]
    for name in load_img_names():
        image = cv2.imread(IMAGES_PATH+name, cv2.IMREAD_UNCHANGED)
        if image is None:
            print('Couldn\'t load image:'+ name)
        else: 
            image = cv2.normalize(image, None, 0, 1, cv2.NORM_MINMAX, dtype=cv2.CV_32F)
            image[:,:,0] = image[:,:,0] / intensities[i][2]
            image[:,:,1] = image[:,:,1] / intensities[i][1]
            image[:,:,2] = image[:,:,2] / intensities[i][0] 
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            images.append(image.flatten())
            i+=1
    return images


def get_needle_map():
    s_i = np.linalg.pinv(load_light_info(LIGHT_DIRECTIONS_PATH))
    e = normalize_img()
    n = np.dot(s_i, e)
    return n


def img_2D_3D():
    needle_map = get_needle_map()
    mask = load_mask()
    h, w = mask.shape
    # Reshape image (3,h*w) => (3, h, w)
    i=0
    image = np.zeros((3,h,w), np.float32)
    for j in needle_map:
        image[i] = np.reshape(j, (-1,w))
        i+=1
    
    image2D = np.zeros((h,w,3), np.float32)
    for y in range(h):
        for x in range(w):
            image2D[y,x] = [image[0,y,x], image[1,y,x], image[2,y,x]]

    image3D = np.zeros((h,w,3),np.float32)
    for y in range(h):
        for x in range(w):
            if(mask[y,x]==1):
                n = math.sqrt(image2D[y,x,0]**2 + image2D[y,x,1]**2  + image2D[y,x,2]**2)
                for z in range(3):
                    image3D[y,x,z] = (float)(image2D[y,x,z])
                    image3D[y,x,z] = ((image3D[y,x,z])/n+1.)/2.
    return image2D, image3D


def main():
    image2D, image3D = img_2D_3D()
    
    fig, ax2D = plt.subplots()
    ax2D.imshow(image2D, cmap='gray')
    ax2D.set_title('2D object (RGB)')
    ax2D.set_xlabel('x axis')
    ax2D.set_ylabel('y axis')
    plt.show()

    fig, ax3D = plt.subplots()
    ax3D.imshow(image3D, cmap='gray')
    ax3D.set_title('3D object (Needle map & Z-coordinate)')
    ax3D.set_xlabel('x axis')
    ax3D.set_ylabel('y axis')
    plt.show()

if __name__ == '__main__':
	main()