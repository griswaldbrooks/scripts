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

## @file draw_path_on_vid.py Script for drawing a path on an image.

import cv2
import numpy as np
import argparse


def main():
    # Get command line args.
    parser = argparse.ArgumentParser()
    parser.add_argument('video_file')
    parser.add_argument('path_file')
    parser.add_argument('scatter_file')
    args = parser.parse_args()

    # Load path.
    path = np.loadtxt(args.path_file, delimiter=',')
    path = path.reshape((-1, 1, 2)).astype(np.int32)

    # Check for scatter path.
    if args.scatter_file is not None:
        scatter = np.loadtxt(args.scatter_file, delimiter=',')
        scatter = scatter.reshape((-1, 1, 2)).astype(np.int32)

    # Get video file.
    cap = cv2.VideoCapture(args.video_file)

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

        # Draw lines.
        cv2.polylines(frame, [path], False, (0, 0, 255), thickness=2)
        if args.scatter_file is not None:
            cv2.polylines(frame, [scatter], False, (255, 0, 0), thickness=2)

        cv2.imshow("Path", frame)
        cv2.waitKey(10)

if __name__ == '__main__':
    main()
