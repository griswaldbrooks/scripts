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

## @file rotate_vid.py Script for rotating video by number of degrees.

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


def rotate_frame(frame, angle):
    # Rotate frame
    rows, cols, ch = frame.shape
    R = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    return cv2.warpAffine(frame, R, (cols, rows))


def ask_user_about_angle(angle):
    # Dictionary of valid responses.
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}

    # Query string.
    prompt = "Do you want to use this angle[" + str(angle) + "]? [Y/n/new angle in degrees]: "

    while True:
        # Get choice.
        choice = raw_input(prompt).lower()

        # Check to see if the choice is a number.
        try:
            angle = int(choice)
            # Return the new angle.
            return False, angle

        except ValueError:
            # If it wasn't a number, check to see if it was a valid choice.
            if choice == '':
                return True, angle
            elif choice in valid:
                return valid[choice], angle
            else:
                print('Invalid response.')


def prompt_and_rotate(filename, angle):
    # Flag returned to indicate that the video should be rotated.
    rotation_good = False
    # Open video.
    cap = cv2.VideoCapture(filename)

    if cap.isOpened():
        # Get frame and rotate.
        ret, frame = cap.read()

        # If the frame was valid, rotate and display image.
        if ret:
            # Show rotated image.
            image_window = DisplayImageThread(rotate_frame(frame, angle), "Rotated Image")
            image_window.start()

            # Prompt the user until they are happy with the angle.
            while not rotation_good:
                # Show image and prompt user.
                image_window.update_image(rotate_frame(frame, angle))
                rotation_good, new_angle = ask_user_about_angle(angle)

                # Was the user happy with the angle? Not if the angle didn't get changed.
                if not rotation_good and new_angle is angle:
                    # Things didn't work out.
                    break

                # Update the new angle.
                angle = new_angle

            image_window.close_window()
            image_window.join()

    return rotation_good, angle


def main():
    # Get command line args.
    parser = argparse.ArgumentParser()
    parser.add_argument('in_file', metavar='input-video-file-name',
                        help='name of the video file to rotate')
    parser.add_argument('angle', metavar='angle',
                        help='angle in degrees to rotate the video')
    parser.add_argument('-y', action='store_true',
                        help='check angle by displaying sample image')
    args = parser.parse_args()

    # Store and check angle is valid.
    try:
        angle = int(args.angle)
        angle_good = True
    except ValueError:
        angle_good = False

    # Check rotation result with user.
    if args.y:
        angle_good, angle = prompt_and_rotate(args.in_file, angle)

    # Check to see if the user was happy with the rotation.
    if angle_good:
        # Get video file.
        cap = cv2.VideoCapture(args.in_file)
        # Create the writer.
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
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
            frame = rotate_frame(frame, angle)
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
