import cv2
import numpy as np
import os
import time
import utility

def colorDetection():

    # --- Load in images. If not loaded, recommend user to run the main script first.
    if os.path.isfile('data/Gates_Original.npy'):
        images = np.load('data/Gates_Original.npy', allow_pickle=True)
    else:
        print("Please use the main script once to convert jpgs to npy")

    # -- Empty function as fill parameter ---
    def empty(a):
        pass

    # --- Setting parameters for the settings & slider screen for color masking
    frameWidth = 640
    frameHeight = 480
    cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cv2.namedWindow("Color_Parameters")
    cv2.resizeWindow("Color_Parameters", 640, 240)  # Set size of the settings window
    cv2.createTrackbar("B_low", "Color_Parameters", 20, 255, empty)     # --- Note: ... initial guess, maxvalue, empty)
    cv2.createTrackbar("B_high", "Color_Parameters", 80, 255, empty)
    cv2.createTrackbar("G_low", "Color_Parameters", 70, 255, empty)
    cv2.createTrackbar("G_high", "Color_Parameters", 120, 255, empty)
    cv2.createTrackbar("R_low", "Color_Parameters", 210, 255, empty)
    cv2.createTrackbar("R_high", "Color_Parameters", 255, 255, empty)

    # --- Setting parameters for settings & slider screen
    frameWidth = 640
    frameHeight = 480
    cap = cv2.VideoCapture(0)
    cap.set(3, frameWidth)
    cap.set(4, frameHeight)
    cv2.namedWindow("Noise_Parameters")
    cv2.resizeWindow("Noise_Parameters", 640, 240)  # Set size of settings window
    cv2.createTrackbar("nr_dilations", "Noise_Parameters", 1, 3, empty)
    cv2.createTrackbar("AreaMin", "Noise_Parameters", 600, 20000, empty)
    cv2.createTrackbar("AreaMax", "Noise_Parameters", 7000, 20000, empty)

    # --- Settings for Dilation to remove Noise
    kernel = np.ones((5, 5))

    # Scan through all fotos
    for i in range(len(images)):
        live_image = images[i]
        # Make a copy to draw on
        imgContour = live_image.copy()
        # Make a copy to display the 'normal' photo later
        imgOriginal = live_image.copy()

        # Contrasting and blurring the photos
        imgContrast = cv2.addWeighted(live_image, 1, live_image, 0, 0)      # Add contrast to photo
        imgBilateral = cv2.bilateralFilter(imgContrast, 9, 75, 75)          # Used at the moment

        # Retrieve all variables fro the trackbar
        B_low = cv2.getTrackbarPos("B_low", "Color_Parameters")
        B_high = cv2.getTrackbarPos("B_high", "Color_Parameters")
        G_low = cv2.getTrackbarPos("G_low", "Color_Parameters")
        G_high = cv2.getTrackbarPos("G_high", "Color_Parameters")
        R_low = cv2.getTrackbarPos("R_low", "Color_Parameters")
        R_high = cv2.getTrackbarPos("R_high", "Color_Parameters")
        low_color = np.array([B_low, G_low, R_low])
        high_color = np.array([B_high, G_high, R_high])

        # Convert to UINT8 as opencv functions don't allow otherwise
        imgPreMask = (imgBilateral * 255).astype(np.uint8)

        # Perform the masking
        imgMask = cv2.inRange(imgPreMask, low_color, high_color)

        # Get Canny parameters from settings slider
        nr_dilations = cv2.getTrackbarPos("nr_dilations", "Noise_Parameters")

        # --- Start timer to measure execution speed
        # e1 = cv2.getTickCount()
        # Dilate image once to make contour tracking easier.
        imgDil = cv2.dilate(imgMask, kernel, iterations=nr_dilations)
        # e2 = cv2.getTickCount()
        # time = (e2 - e1) / cv2.getTickFrequency()
        # print("Time for dilation: ", time)
        # ---  Stop timer to measure execution speed^

        # Call the custom contour function
        getContours(imgDil, imgContour, i)

        # Displaying the results side to side with custom utility function
        StackedImages = utility.stackImages(([imgOriginal, imgBilateral, imgMask],
                                             [imgMask, imgDil, imgContour]), 0.6)
        cv2.imshow("Stacked Images", StackedImages)

        # Wait for enter press to continue
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # time.sleep(0.1)       # ALTERNATIVE to the waitkey: playing it slowly
        cv2.waitKey(0)


# ---- Function to get contours ----
def getContours(img, imgContour, i):

    # Use built in contour function
    extraVariable, contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # -- Target x and y coordinate
    target_coordinate_x = 0.5 * 300
    target_coordinate_y = 0.5 * 315
    x_coordinates = []  # Save x coordinates of boxes
    y_coordinates = []  # Save y-coordinates of boxes
    target_coordinates = [] # This is the message that gets sent to the CSV file in data

    # Check if areas are large enough to be considered a side of the pole. Removes noise.
    for cnt in contours:
        # Calculate Area
        area = cv2.contourArea(cnt)
        # Load in your set min and max area
        areaMin = cv2.getTrackbarPos("AreaMin", "Noise_Parameters")
        areaMax = cv2.getTrackbarPos("AreaMax", "Noise_Parameters")
        # Check if area is large enough to probably be part of the pole
        if areaMin < area < areaMax:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 7)         # Contour drawn in pink
            peri = cv2.arcLength(cnt, True)                                 # Calculate how long the perimeter is
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, closed=True)        # Approximates the shape of the perimeter
            x, y, w, h = cv2.boundingRect(approx)
            x_coordinates.append(x)
            y_coordinates.append(y)
            # Draw rectangle around shape
            cv2.rectangle(imgContour, (x,y), (x+w, y+h), (0,255,0), 5)      # Draws box around contours
            # Put text around shapes
            cv2.putText(imgContour, "Points: " + str(len(approx)), (x - 10, y + h + 40), cv2.FONT_HERSHEY_COMPLEX,
                        .7, (0,255,0), 2)
            cv2.putText(imgContour, "Areas: " + str(int(area)), (x - 10, y + h + 20), cv2.FONT_HERSHEY_COMPLEX,
                        .7, (0,255,0), 2)

    # Only if it sees TWO boxes it trusts its detection and takes the average of the coordinates as target.
    if 1 < len(x_coordinates) < 3:
        target_coordinate_x = int(np.floor(np.mean(x_coordinates) + 0.5*w))
        target_coordinate_y = int(np.floor(np.mean(y_coordinates) + 0.5*h))
        cv2.drawMarker(imgContour, (target_coordinate_x, target_coordinate_y), color=(100, 200, 200),
                       markerType=cv2.MARKER_CROSS, thickness=4)

    # Else it flies straight (middle of screen)
    else:
        target_coordinate_x = int(np.floor(0.5 * 300))
        target_coordinate_y = int(np.floor(0.5 * 315))

    # Append a list as new line to an existing csv file
    target_coordinates = [("img_"+str(i)+".png"), target_coordinate_x, target_coordinate_y]
    utility.append_list_as_row('data/Gates_Csv/cornersFound.csv', target_coordinates)

    # print("The target coordinate in x is now: ", target_coordinate_x)
    # print("The target coordinate in y is now: ", target_coordinate_y)
