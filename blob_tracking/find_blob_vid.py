#!/usr/bin/env python
#
# Software Licence Agreement (MIT)
#
# Copyright (c) 2016 Griswald Brooks
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
# CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
#

##
# @author Griswald Brooks

## @file find_blob_vid.py Script for finding color blob in video.

import cv2
import numpy as np
import argparse
import matplotlib.pyplot as plt


def main():
    # Get command line args.
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file')
    args = parser.parse_args()

    # Get video file.
    cap = cv2.VideoCapture(args.image_file)

    # Surrogate datatypes for scatter plot.
    # TODO: Get rid of this.
    all_keypoints_x = []
    all_keypoints_y = []

    while(cap.isOpened()):

        # Read video frame
        ret, frame = cap.read()

        # Check to see if frame is valid
        if not ret:
            break

        # Rotate frame -90 degrees
        rows, cols, ch = frame.shape
        R = cv2.getRotationMatrix2D((cols/2, rows/2), -90, 1)
        frame = cv2.warpAffine(frame, R, (cols, rows))

        # Convert BGR to HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # define range of orange color in HSV
        lower_orange = np.array([0, 75, 75])
        upper_orange = np.array([7, 255, 255])

        # Threshold the HSV image to get only orange colors
        mask = cv2.inRange(hsv, lower_orange, upper_orange)

        # Do a closing and opening to filter out holes and spots
        close_kernel = np.ones((15, 15), np.uint8)
        open_kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, close_kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, open_kernel)

        # Setup SimpleBlobDetector parameters.
        params = cv2.SimpleBlobDetector_Params()

        # Change thresholds
        params.minThreshold = 10
        params.maxThreshold = 255
        params.minDistBetweenBlobs = 10

        # Filter by Color.
        params.filterByColor = True
        params.blobColor = 255
        # Filter by Area.
        params.filterByArea = True
        params.minArea = 160
        # params.maxArea = 280

        # # Filter by Circularity
        params.filterByCircularity = False
        # params.minCircularity = 0.1

        # # Filter by Convexity
        params.filterByConvexity = False
        # params.minConvexity = 0.87

        # # Filter by Inertia
        params.filterByInertia = False
        # params.minInertiaRatio = 0.01

        # Set up the detector with default parameters.
        detector = cv2.SimpleBlobDetector_create(params)

        # Detect blobs.
        keypoints = detector.detect(mask)

        for keypoint in keypoints:
            print keypoint.pt
            all_keypoints_x.append(keypoint.pt[0])
            all_keypoints_y.append(keypoint.pt[1])

         # Bitwise-AND mask and original image
        frame_masked = cv2.bitwise_and(frame, frame, mask=mask)

        # Draw detected blobs as red circles.
        # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
        im_with_keypoints = cv2.drawKeypoints(frame_masked, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

        # Show keypoints
        cv2.imshow("Keypoints", im_with_keypoints)
        # cv2.imshow("Mask", mask)
        cv2.waitKey(10)

    # Save keypoints.
    np.savetxt('path.positions', np.transpose([all_keypoints_x, all_keypoints_y]), delimiter=',')

    # Plot keypoints.
    plt.scatter(np.asarray(all_keypoints_x), np.asarray(all_keypoints_y), color='b')
    plt.show()

if __name__ == '__main__':
    main()
