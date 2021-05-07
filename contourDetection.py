import cv2
import numpy as np
import os
import time
import utility

# -- Empty function as fill parameter ---

def empty(a):
    pass

# --- Load in images. If not loaded, use Edge detection script

if os.path.isfile('data/Gates_Original.npy'):
    images = np.load('data/Gates_Original.npy', allow_pickle=True)
else:
    print("Please use the edge_detection script to convert jpgs to npy")


# --- Setting parameters for settings & slider screen

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 240)    # Set size of settings window
cv2.createTrackbar("Treshold1", "Parameters",450,700,empty)
cv2.createTrackbar("Treshold2", "Parameters",300,700,empty)
cv2.createTrackbar("AreaMin", "Parameters", 2000, 20000, empty)
cv2.createTrackbar("AreaMax", "Parameters", 7000, 20000, empty)

# --- Settings for Dilation to remove Noise
kernel = np.ones((5,5))

def getContours(img, imgContour):
    extraVariable, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # -- Target x and y coordinate
    target_coordinate_x = 0.5 * 300
    target_coordinate_y = 0.5 * 315
    x_coordinates = []  # Save x coordinates of boxes
    y_coordinates = []  # Save y-coordinates of boxes

    for cnt in contours:
        area = cv2.contourArea(cnt)
        areaMin = cv2.getTrackbarPos("AreaMin", "Parameters")
        areaMax = cv2.getTrackbarPos("AreaMax", "Parameters")
        if areaMin < area < areaMax:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, closed=True)        # Approximates the shape of the
            x, y, w, h = cv2.boundingRect(approx)
            x_coordinates.append(x)
            y_coordinates.append(y)
            cv2.rectangle(imgContour, (x,y), (x+w, y+h), (0,255,0), 5)
            # cv2.putText(imgContour, "Points: " + str(len(approx)), (x + w + 20, y + 20), cv2.FONT_HERSHEY_COMPLEX,
            #             .7, (0,255,0), 2)
            # cv2.putText(imgContour, "Areas: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX,
            #             .7, (0,255,0), 2)

        if len(x_coordinates) > 0:
            target_coordinate_x = np.mean(x_coordinates)
            target_coordinate_y = np.mean(y_coordinates)
        else:
            target_coordinate_x = 0.5 * 300
            target_coordinate_y = 0.5 * 315

    print("The target coordinate in x is now: ", target_coordinate_x)
    print("The target coordinate in y is now: ", target_coordinate_y)

#Scan through all fotos
for i in range(len(images)):
    points = []
    live_image = images[i]
    imgContour = live_image.copy()
    imgOriginal = live_image.copy()

    imgContrast = cv2.addWeighted(live_image, 1, live_image, 0, 0)
    e1 = cv2.getTickCount()
    imgGaussian = cv2.GaussianBlur(imgContrast, (7, 7), 1)
    e2 = cv2.getTickCount()
    time = (e2 - e1) / cv2.getTickFrequency()
    print("Time for Gaussian: ", time)

    e1 = cv2.getTickCount()
    imgBilateral = cv2.bilateralFilter(imgContrast, 9, 75, 75)
    e2 = cv2.getTickCount()
    time = (e2 - e1) / cv2.getTickFrequency()
    print("Time for Bilateral: ", time)

    e1 = cv2.getTickCount()
    imgRotmask = cv2.medianBlur(imgContrast, 5)
    e2 = cv2.getTickCount()
    time = (e2 - e1) / cv2.getTickFrequency()
    print("Time for Median: ", time)
    imgGray = cv2.cvtColor(imgBilateral, cv2.COLOR_BGR2GRAY)

    treshold1 = cv2.getTrackbarPos("Treshold1", "Parameters")
    treshold2 = cv2.getTrackbarPos("Treshold2", "Parameters")
    imgUint = (imgGray * 255).astype(np.uint8)
    imgCanny = cv2.Canny(imgUint, treshold1, treshold2)
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)
    getContours(imgDil, imgContour)



    # Displaying the results side to side
    StackedImages = utility.stackImages(([imgOriginal, imgGaussian, imgCanny],
                                        [imgBilateral, imgRotmask, imgContour]), 0.6)
    cv2.imshow("Stacked Images", StackedImages)

    # cv2.imshow("Result", imgContour)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # time.sleep(0.1)
    cv2.waitKey(0)






