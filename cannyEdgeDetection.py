#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 12:03:05 2021

@author: erikbaas

"""

import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy import ndimage
import os.path

# --- Load in images. If not loaded, use Edge detection script

if os.path.isfile('data/Gates_Original.npy'):
    images = np.load('data/Gates_Original.npy', allow_pickle=True)
else:
    print("Please use the edge_detection script to convert jpgs to npy")

# Set timer to measure execution speed
e1 = cv.getTickCount()

# # Remove 50 first images:
# images = images[50:]

# From the 1st image on, skip n photos each time and append back to list
# images = images[1::1]

# Setting:
vertical_kernel = cv.getStructuringElement(cv.MORPH_RECT, (1, 4))

rho = 1         # distance resolution in pixels of the Hough grid
theta = np.pi   # angular resolution in radians of the Hough grid
threshold = 15  # minimum number of votes (intersections in Hough grid cell)
min_line_length = 2  # minimum number of pixels making up a line
max_line_gap = 20  # maximum gap in pixels between connectable line segments

# Create figure:
plt.clf()
plt.figure(1)

# Do for all image:
for i in range(len(images)):
    points = []
    live_image = images[i]

    live_image = (live_image * 255).astype(np.uint8)

    # Superposition the images by itself to increase contrast
    live_image = cv.addWeighted(live_image, 1, live_image, 0, 0)

    live_image = cv.GaussianBlur(live_image, (7, 7), 1)

    # Open CV's canny edge detection:
    img_edges = cv.Canny(live_image, 300, 500)

    # Vertical edge detection:
    img_vertical = cv.morphologyEx(img_edges, cv.MORPH_OPEN, vertical_kernel, iterations=1)

    # Detect and draw lines:
    lines = cv.HoughLinesP(img_vertical, rho, theta, threshold, np.array([]), min_line_length, max_line_gap)

    # Create lines image and calculate center of line:
    img_lines = np.copy(live_image) * 0
    if type(lines) != type(None):
        for line in lines:
            for x1,y1,x2,y2 in line:
                cv.line(img_lines,(x1,y1),(x2,y2),(0,0,255),2)
                points.append([(x1+x2)/2,(y1+y2)/2])

    img_lines = cv.addWeighted(live_image, 1, img_lines, 1, 0)

    #Group points to objects using treshold:
    points = sorted(points)
    centers = []
    x_center = -1
    y_center = -1
    N = 0
    for p in points:
        if x_center == -1 or p[0] - x_center < 50:
            x_center = (x_center * N + p[0])/(N+1)
            y_center = (y_center * N + p[1])/(N+1)
            N += 1
        else:
                centers.append([x_center, y_center])
                x_center = -1
                y_center = -1
                N = 0
    if x_center != -1:
        centers.append([x_center, y_center])

    """ PLOTTING STUFF """
    #Plot images:
    plt.clf()

    plt.subplot(321)
    plt.text(0, -8, "Original image", fontsize=12)
    plt.imshow(images[i])

    plt.subplot(322)
    plt.text(0, -8, "Edge detection", fontsize=12)
    plt.imshow(img_edges)

    plt.subplot(323)
    plt.text(0, -8, "Vertical lines", fontsize=12)
    plt.imshow(img_vertical)

    plt.subplot(324)
    plt.text(0, -8, "Filtered lines and object mark", fontsize=12)
    for c in centers:
        plt.plot(c[0], c[1], 'go')
    plt.imshow(img_lines)

    # plt.subplot(325)
    # plt.text(0, -8, "Chessboard detection", fontsize=12)
    # plt.imshow(img_chesspoints)

    name = str("result/frame" + str(i) + ".png")
    #plt.savefig(name, dpi=300)
    plt.pause(0.0001)
#
# # Stop timer to measure execution speed
# e2 = cv.getTickCount()
# time = (e2 - e1) / cv.getTickFrequency()
# print(time)
#
