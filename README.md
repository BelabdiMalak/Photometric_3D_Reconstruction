# Photometric 3D Reconstruction

## Introduction
Using 96 different images of a cat, I want to create its 3D object.

---

## Tools
OpenCV is the main Python Library used in computer vision (Image manipulation).

---

## To run the project (Linux)
1. Get sure that you have Python3 installed. In case not run this command : 
```shell
sudo apt-get install python3
```
2. Get sure you have Pip installed. If not run this command : 
```shell
sudo apt-get install python3sudo apt-get install python3
```
3. Install OpenCV library using this command : 
```shell
pip3 install opencv-python
```

4. Run the project running : 
```shell
python3 main.py
```
---
## Dataset
To implement this project, we used :
- 96 images of the same object taken by the same camera position but with different conditions
(positions and intensities) of the light source. These images are stored in RGB (BGR under
opencv) on 16 bits.
- A file contains the names of the 96 images already mentioned. (filenames.txt).
- A file contains the positions of the light sources. (light_directions.txt).
- A file contains the intensities of the light sources. (light_intensities.txt).
- An image contains the object's mask (mask.jpg).
---

## Steps 
To the 3D object I followed the following steps :
1. Normalize images values from **unit16** to **float32**, because the 96 images are too dark, normalization will make them clear. Add to that,we need float values to apply mathematical operations on our images. 
2. Divide each pixel by the correspending light intensity (shading correction in ImageJ to remove local fluorescent light intensity variations due to camera issues).
3. To make our calculations less complex, we convert images into grey scale (convey less information than RGB).
4. Get the normal vectors of all pixels of the object : 
5. Change the scale to [0-255].