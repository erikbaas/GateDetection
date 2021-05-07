import cv2
import numpy as np
import os
import time
import utility

frameWidth = 640
frameHeight = 480
cap = cv2.VideoCapture(0)
cap.set(3, frameWidth)
cap.set(4, frameHeight)

def empty(a):
    pass

# --- Load in images. If not loaded, use Edge detection script

if os.path.isfile('data/Gates_Original.npy'):
    images = np.load('data/Gates_Original.npy', allow_pickle=True)
else:
    print("Please use the edge_detection script to convert jpgs to npy")

# --- Setting parameters for optimal Canny
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 640, 240)    # Set size of settings window
cv2.createTrackbar("treshold_dst","Parameters",1,60,empty)         # In percentages
cv2.createTrackbar("blocksize","Parameters",2,40,empty)
cv2.createTrackbar("ksize","Parameters",19,30,empty)
cv2.createTrackbar("harrisparameter","Parameters",15,50,empty)            # In percentages


# --- Settings for kernel size
ksize = 3

#Scan through all fotos
for i in range(len(images)):
    points = []
    live_image = images[i]
    imgOriginal = live_image.copy()
    imgOverwritten = live_image.copy()

    imgContrast = cv2.addWeighted(live_image, 1, live_image, 0, 0)
    imgGaussian = cv2.GaussianBlur(imgContrast, (7, 7), 1)
    imgGray = cv2.cvtColor(imgGaussian, cv2.COLOR_BGR2GRAY)

    treshold_dst = cv2.getTrackbarPos("treshold_dst", "Parameters")
    treshold_dst = treshold_dst / 100.
    blocksize = cv2.getTrackbarPos("blocksize", "Parameters")
    # This block of code ensures that the harris parameter is always odd and below 31
    ksize_unchecked = cv2.getTrackbarPos("ksize", "Parameters")
    if (ksize_unchecked % 2) == 1 and ksize_unchecked < 32:
        ksize = ksize_unchecked             # Only allows odd numbers
    harrisparameter = cv2.getTrackbarPos("harrisparameter", "Parameters")
    harrisparameter = harrisparameter / 100.

    print("The treshold dst, blocksize, kernel size and harrisparameter k are: " , treshold_dst, blocksize, ksize, harrisparameter)

    imgUint = (imgGray * 255).astype(np.uint8)

    # Perform Harris and Image Dilation
    imgFloat32 = np.float32(imgGray)
    dst = cv2.cornerHarris(imgFloat32, blocksize, ksize, harrisparameter)
    dst = cv2.dilate(dst, None)
    imgOverwritten[dst > treshold_dst * dst.max()] = [255, 0, 0]                # Write red dots

    if cv2.waitKey(0) & 0xff == 27:
        cv2.destroyAllWindows()

    # Displaying the results side to side
    StackedImages = utility.stackImages(([imgOriginal, imgGaussian],
                                        [imgGray, imgOverwritten]), 0.6)
    cv2.imshow("Stacked Images", StackedImages)

    # cv2.imshow("Result", imgContour)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # time.sleep(0.1)
    cv2.waitKey(0)




