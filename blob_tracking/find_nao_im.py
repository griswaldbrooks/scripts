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

## @file find_blob_im.py Script for finding the Nao's orange colors in image.

import cv2
import numpy as np
import argparse


def main():
    # Get command line args.
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file', metavar='image-file-name',
                        help='name of the image to find Nao in')
    args = parser.parse_args()

    # Read image
    im = cv2.imread(args.image_file)

    # Convert BGR to HSV
    im = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

    # define range of orange color in HSV
    lower_orange = np.array([0, 75, 75])
    upper_orange = np.array([7, 255, 255])

    # Threshold the HSV image to get only orange colors
    mask = cv2.inRange(im, lower_orange, upper_orange)

    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Change thresholds
    params.minThreshold = 10
    params.maxThreshold = 255

    # Filter by Color and Area.
    params.filterByColor = True
    params.filterByArea = True
    params.filterByCircularity = False
    params.filterByConvexity = False
    params.filterByInertia = False

    params.blobColor = 255
    params.minArea = 160

    # Set up the detector with default parameters.
    detector = cv2.SimpleBlobDetector_create(params)

    # Detect blobs.
    keypoints = detector.detect(mask)

    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    im_with_keypoints = cv2.drawKeypoints(im, keypoints, np.array([]), (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    # Show keypoints
    cv2.imshow("Keypoints", im_with_keypoints)

    cv2.waitKey(0)

if __name__ == '__main__':
    main()
