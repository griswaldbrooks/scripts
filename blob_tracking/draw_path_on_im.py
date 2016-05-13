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

## @file draw_path_on_im.py Script for drawing a path on an image.

import cv2
import numpy as np
import argparse


def main():
    # Get command line args.
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file')
    parser.add_argument('path_file')
    args = parser.parse_args()

    # Read image.
    im = cv2.imread(args.image_file)

    # Load path.
    path = np.loadtxt(args.path_file, delimiter=',')
    path = path.reshape((-1, 1, 2)).astype(np.int32)

    # Draw lines.
    cv2.polylines(im, [path], False, (0, 255, 255))

    cv2.imshow("Path", im)
    cv2.waitKey(0)

if __name__ == '__main__':
    main()
