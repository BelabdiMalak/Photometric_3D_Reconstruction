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