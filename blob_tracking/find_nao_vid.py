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

## @file find_blob_vid.py Script for finding the Nao robot's orange colors in video.

import argparse
import cv2
import matplotlib.pyplot as plt
import numpy as np


def main():
    # Get command line args.
    parser = argparse.ArgumentParser()
    parser.add_argument('video_file')
    args = parser.parse_args()

    # Get video file.
    cap = cv2.VideoCapture(args.video_file)

    # Surrogate datatypes for scatter plot.
    # TODO: Get rid of this.
    all_keypoints_x = []
    all_keypoints_y = []

    # Setup SimpleBlobDetector.
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 10
    params.maxThreshold = 255
    params.minDistBetweenBlobs = 10

    # Filter by Color and Area.
    params.filterByColor = True
    params.filterByArea = True
    params.filterByCircularity = False
    params.filterByConvexity = False
    params.filterByInertia = False

    # Look for white blobs.
    params.blobColor = 255
    # Blobs can't be too small.
    params.minArea = 160

    # Set up the detector with default parameters.
    detector = cv2.SimpleBlobDetector_create(params)

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

        # define range of Nao's orange color in HSV
        lower_orange = np.array([0, 75, 75])
        upper_orange = np.array([7, 255, 255])

        # Threshold the HSV image to get only orange colors
        mask = cv2.inRange(hsv, lower_orange, upper_orange)

        # Do a closing and opening to filter out holes and spots
        close_kernel = np.ones((15, 15), np.uint8)
        open_kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, close_kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, open_kernel)

        # Detect blobs.
        keypoints = detector.detect(mask)

        for keypoint in keypoints:
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
        # cv2.waitKey(10)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    # Save keypoints.
    np.savetxt('path.positions', np.transpose([all_keypoints_x, all_keypoints_y]), delimiter=',')

    # Plot keypoints.
    plt.scatter(np.asarray(all_keypoints_x), np.asarray(all_keypoints_y), color='b')
    plt.show()

if __name__ == '__main__':
    main()
