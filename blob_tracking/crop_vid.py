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

## @file crop_vid.py Script for cropping video.

import argparse
import cv2
from threading import Thread
import sys


class DisplayImageThread (Thread):
    def __init__(self, image, window_name):
        Thread.__init__(self)
        self.image = image
        self.window_name = window_name
        self.exit_flag = False

    def run(self):
        while not self.exit_flag:
            # Display image.
            cv2.imshow(self.window_name, self.image)
            # Wait.
            cv2.waitKey(250)

        cv2.destroyWindow(self.window_name)

    def update_image(self, image):
        self.image = image

    def close_window(self):
        self.exit_flag = True


def crop_frame(frame, extents):
    return frame[extents[2]:extents[3], extents[0]:extents[1]]


def ask_user_about_extents(extents):
    # Dictionary of valid responses.
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}

    # Query string.
    prompt = "Do you want to use these extents" + str(extents) + "? [Y/n/left-px right-px top-px bottom-px]: "

    while True:
        # Get choice.
        choice = raw_input(prompt).lower()

        # Check to see if the choice is a number.
        try:
            splitted_choice = choice.split()
            extents = [int(x) for x in splitted_choice]

            # Return the new extents.
            return False, extents

        except ValueError:
            # If it wasn't a number, check to see if it was a valid choice.
            if choice == '':
                return True, extents
            elif choice in valid:
                return valid[choice], extents
            else:
                print('Invalid response.')


def prompt_and_crop(filename, extents):
    # Flag returned to indicate that the video should be croppped.
    crop_good = False
    # Open video.
    cap = cv2.VideoCapture(filename)

    if cap.isOpened():
        # Get frame.
        ret, frame = cap.read()

        # If the frame was valid, crop and display image.
        if ret:
            # Show cropped image.
            image_window = DisplayImageThread(crop_frame(frame, extents), "Cropped Image")
            image_window.start()

            # Prompt the user until they are happy with the angle.
            while not crop_good:
                # Show image and prompt user.
                image_window.update_image(crop_frame(frame, extents))
                crop_good, new_extents = ask_user_about_extents(extents)

                # Was the user happy with the cropping? Not if the extents didn't get changed.
                if not crop_good and new_extents is extents:
                    # Things didn't work out.
                    break

                # Update the new extents.
                extents = new_extents

            image_window.close_window()
            image_window.join()

    return crop_good, extents


def main():
    # Get command line args.
    parser = argparse.ArgumentParser()
    parser.add_argument('in_file', metavar='input-video-file-name',
                        help='name of the video file to rotate')
    parser.add_argument('x1', metavar='left-pixel',
                        help='pixel on the left side of the image to crop to')
    parser.add_argument('x2', metavar='right-pixel',
                        help='pixel on the right side of the image to crop to')
    parser.add_argument('y1', metavar='top-pixel',
                        help='pixel on the top of the image to crop to')
    parser.add_argument('y2', metavar='bottom-pixel',
                        help='pixel on the bottom of the image to crop to')
    parser.add_argument('-y', action='store_true',
                        help='check cropping by displaying sample image')
    args = parser.parse_args()

    # Get video file.
    cap = cv2.VideoCapture(args.in_file)

    if cap.isOpened():
        # Read video frame
        ret, frame = cap.read()
    cap.release()

    # Store and check crop is valid.
    rows, cols, ch = frame.shape
    # Image extents [x1, x2, y1, y2]
    extents = [0, cols, 0, rows]

    print "Video extents are: " + str(extents)

    try:
        extents[0] = int(args.x1)
        extents[1] = int(args.x2)
        extents[2] = int(args.y1)
        extents[3] = int(args.y2)
        crop_good = True
    except ValueError:
        crop_good = False

    # Check rotation result with user.
    if args.y:
        crop_good, extents = prompt_and_crop(args.in_file, extents)

    # Check to see if the user was happy with the rotation.
    if crop_good:
        # Get video file.
        cap = cv2.VideoCapture(args.in_file)
        # Create the writer.
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        width = extents[1] - extents[0]
        height = extents[3] - extents[2]
        out = cv2.VideoWriter('out.avi', fourcc, int(cap.get(cv2.CAP_PROP_FPS)), (width, height))

        # Get total number of frames for progress bar.
        n_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        while cap.isOpened():
            # Read video frame
            ret, frame = cap.read()

            # Check to see if frame is valid
            if not ret:
                break

            # Rotate frame and write it.
            frame = crop_frame(frame, extents)
            out.write(frame)

            # Get progress percentage.
            percent = cap.get(cv2.CAP_PROP_POS_FRAMES)/n_frames
            # Start from beginning of line.
            sys.stdout.write('\r')
            # Print status.
            sys.stdout.write("[%-20s] %d%%" % ('='*int(20.0*percent), 100.0*percent))
            sys.stdout.flush()

        # Newline for command prompt.
        print '\n'
        cap.release()
        out.release()

    # Clean up.
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
