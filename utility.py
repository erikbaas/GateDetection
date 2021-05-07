import cv2
import numpy as np
import os
import matplotlib.image as mpimg
from csv import writer

# This function clears the csv file with your found data in data/Gates_Csv
def clearCsvFile():
    f = open("data/Gates_Csv/cornersFound.csv", "w")
    f.truncate()
    f.close()

# This utility function writes the target coordinates to a CSV file
def append_list_as_row(file_name, list_of_elem):
    # Open file in append mode
    with open(file_name, 'a+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)


# Crops all photos to the same size and then saves it as NPY file
def convertJPGtoNPY():

    # Transfer images to npy array for faster processing
    if os.path.isfile('data/Gates_Original.npy'):
        images = np.load('data/Gates_Original.npy', allow_pickle=True)
        print('Npy files already created!')
    else:
        image_list = os.listdir('data/Gates_Original')
        images = []

        for i in image_list:
            path = str('data/Gates_Original/' + i)
            img = mpimg.imread(path)

            # Crop image to make them all same size [HEIGHT, WIDTH]
            img = img[55:355, 0:315]

            # Append back to list
            images.append(img)

        images = np.asarray(images)
        np.save('data/Gates_Original.npy', images)
        print("Images cropped and saved as Gates_Original.npy")

    # Transfer images to npy array for faster processing
    if os.path.isfile('data/Gates_Masked.npy'):
        images = np.load('data/Gates_Masked.npy', allow_pickle=True)
    else:
        image_list = os.listdir('data/Gates_Masked')
        images = []

        for i in image_list:
            path = str('data/Gates_Masked/' + i)
            img = mpimg.imread(path)

            # Crop image to make them all same size [HEIGHT, WIDTH]
            img = img[55:355, 0:315]

            # Append back to list
            images.append(img)

        images = np.asarray(images)
        np.save('data/Gates_Masked.npy', images)
        print("Images cropped and saved as Gates_Masked.npy")

    # Transfer images to npy array for faster processing
    if os.path.isfile('data/SandboxFiles.npy'):
        images = np.load('data/SandboxFiles.npy', allow_pickle=True)
    else:
        image_list = os.listdir('data/SandboxFiles')
        images = []

        for i in image_list:
            path = str('data/SandboxFiles/' + i)
            img = mpimg.imread(path)

            # Crop image to make them all same size [HEIGHT, WIDTH]
            # img = img[55:355, 0:315]

            # Append back to list
            images.append(img)

        images = np.asarray(images)
        np.save('data/SandboxFiles', images)
        print("Images cropped and saved as SandboxFiles.npy")

    return images

# Allows us to view photos side to side by stacking npy arrays next to each other
def stackImages(imgArray,scale,lables=[]):
    sizeW= imgArray[0][0].shape[1]
    sizeH = imgArray[0][0].shape[0]
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (sizeW, sizeH), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (sizeW, sizeH), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        print(eachImgHeight)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d][c])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables[d][c],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver