# Gate Contour Detection with Minimum Area Noise Filtering 
## Final xxx Assignment

This project is an assignment for the xxx course on the TU Delft, and proposes a method for racing drones to detect gates. It combines contour detection and colour masking. Additionally, it uses area calculations to remove noise. 

## Installation & Getting Started

### 0. Directory Management

It is very important that you keep the same hierarchy of folders as suggested in this project! That means **for the algorithm to work, you must**:

- Put the real images inside data/Gates_Original folder
- Put the masked images inside data/Gate_Masked folder 
- Put the csv in the Gates_Csv folder 

You should create the folder yourself if it's not there yet (or change the paths accordingly). 

### 1. Download Packages 

It is advised to set up a seperate Anaconda virtual environment. The following imports are used and are thus required.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the following imports.

```bash
import numpy
import cv2
import numpy as np
import os
Import time
from PIL import Image
```

### 2. Run the main file and main algorithm

The core of this repository consists of the following three files. 

**Main.py** should be run first (!). It calls the utility script which crops and then converts images to numpy arrays. When prompted, please press enter to then run the color detection algorithm. 

**Utility.py** can remain untouched by the user. Utility functions contains functions that are called from other scripts. Contains the following definitions: ```def stackImages()``` to display the images together without matplotlib and ```def convertJpgToNpy()``` to convert images to numpy arrays as preprocessing. 

**orangeDetector.py** is the final script, which the report builds upon (used for data analysis). It is called from the main automatically. Note that the program takes about 10 seconds to start up! The code shows you several thresholds you can work with; the recommended settings are set as initial guesses.

Important note: **hold down enter to play the images** after each other!

### 3. Optional: Run the alternative algorithm of your choice

The winning algorithm is automatically ran, as shown above. The other four can be ignored for grading purposes, as they were outperformed during exploration phase. Still, they are interesting to consider and so are left in this repo. They can be ran by executing them individually. 

1. **chessBoardFinder.py** uses the opencv built in chess board detector. As shapes of square patterns are irregular, this function does not perform well on the corners and is thus not recommended to be used. 

2. **cornerFinder.py** is essentially a custom chess board detector. It uses open cv’s harris corner detection to find the edges of the gates. Because it checks for contrasting colors which shift in y- and x, it always gives false positives on the lamps.

3. **contourDetection.py** essentially the same as the winning orangeDetector algorithm, but without the colour masking. More lightweight, but more prone to false positives.

4. **verticalFiltering.py** filters for vertical edges and finds the midpoints.

### 4. Choose optimal settings during runtime

Assuming you are running the winning orangeDetector.py, you will be presented (alongside the visual stacked images), a slider menu. Here, the following can be adjusted.

First, the color_parameters tell you the range (0-255) in which the color masking works. Please set a lower and upper bound for Blue, Green and Red, respectively.

Second, the noise_parameter bar lets you select the minimum (and maximum) area for a contour to be considered a unity. This way you can filter out noise of objects which are too small.

[![Settings-And-Parameters.jpg](https://i.postimg.cc/fTGWfVvQ/Settings-And-Parameters.jpg)](https://postimg.cc/jLhrsd9M)

## Results & Visuals

The following results can be obtained. We see size screens:

1. Original image
2. Blurred image
3. Colour masked image
4. Colour masked image
5. Image after 1 iteration of dilation
6. Detected contours, written over the original image


[![Results-Drone-Racing.jpg](https://i.postimg.cc/SN2N96CG/Results-Drone-Racing.jpg)](https://postimg.cc/7f4k8TBC)

The csv file given gives us the corner points of the gate. The output of this script, instead returns the centre of the gate, as this is the location the drone should go (it is the average of the two boxes). In the code, the output is inscribed in a target_coordinate_x and target_coordinate_y variables.

# Data Analysis

To verify whether the target coordinate was correct, an excel file has been added in Gates_Csv. The file is called dataAnalysis.xlsx, and compares the target coordinate found by the algorithm with that computed directly from the corner points.

## Support

If stuck, or if any questions arise, feel free to send an email to e.b.vanbaasbank@student.tudelft.nl

## Roadmap
Idea for future releases, the following would be planned:

- Generating ROC curves
- Train custom gate images with YOLO 

## Authors and acknowledgment

A thanks to professors guidoAI, JuSquare and dewagter.

## License
[MIT](https://choosealicense.com/licenses/mit/)

## University
[![rsz-tudelft-klein.png](https://i.postimg.cc/dQGW41rc/rsz-tudelft-klein.png)](https://postimg.cc/F1sgKhTT) 









