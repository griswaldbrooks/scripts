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

## @file animate_diff_drive.py Module for animating a differential drive planar robot given a path.

# The point here is I want to give an estimated path, a ground truth path, and a point map
# and see what the robot did.

from numpy import sin, cos, square, sqrt
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation


class AnimateDiffDrive:
    def __init__(self):
        self._est_path = []
        self._gnd_path = []
        self._map = []

    def set_estimated_path(self, robot_poses):
        self._est_path = robot_poses

    def set_ground_truth_path(self, robot_poses):
        self._gnd_path = robot_poses

    def set_map(self, point_map):
        self._map = point_map

    def animate(self):
        # Create figure.
        fig = plt.figure()
        ax = fig.add_subplot(111,
                             autoscale_on=False,
                             xlim=(-1.1, 1.1),
                             ylim=(-1.1, 1.1))
        ax.grid()

        # Create animator.
        ani = animation.FuncAnimation(fig,
                                      self._produce_plot,
                                      np.arange(1, len(x_t)),
                                      interval=dt * len(t),
                                      blit=True,
                                      init_func=self._init_animation)
        # Square the axes.
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

    def _init_animation():
        line_fr.set_data([], [])
        line_gt.set_data([], [])
        line_zt.set_data([], [])
        time_text.set_text('')

        return line_gt, line_fr, line_zt, time_text

    def _produce_plot(i):
        # Filtered linear velocity of the vehicle.
        v = sqrt(square(dx_t[i]) + square(dy_t[i]))
        # Filtered position of the vehicle.
        # Line segment indicates direction of fitlered theta
        # whose magnitude represents the linear velocity.
        thisx = [x_t[i],
                 ARROW_LEN * (v + 0.1) * cos(theta_t[i]) + x_t[i]]
        thisy = [y_t[i],
                 ARROW_LEN * (v + 0.1) * sin(theta_t[i]) + y_t[i]]
        # Ground truth position of the vehicle.
        this_x_s = [x_s[i], x_s[i]]
        this_y_s = [y_s[i], y_s[i]]
        # Sensed position of the vehicle.
        this_x_z = [x_z[i], x_z[i]]
        this_y_z = [y_z[i], y_z[i]]

        line_fr.set_data(thisx, thisy)
        line_gt.set_data(this_x_s, this_y_s)
        line_zt.set_data(this_x_z, this_y_z)
        time_text.set_text(time_template % (i * dt))

        return line_gt, line_fr, line_zt, time_text


    _arrow_len = 0.3



    # Grab the data out of the file.
    filter_log = np.genfromtxt(args.filter_results, delimiter=',')

    # State history.
    # Positions of diff drive vehicle.
    x_t = filter_log[:, 0]
    y_t = filter_log[:, 1]
    theta_t = filter_log[:, 2]
    # Velocities of diff drive vehicle.
    dx_t = filter_log[:, 3]
    dy_t = filter_log[:, 4]
    dtheta_t = filter_log[:, 5]

    # Timing results.
    t = filter_log[:, 6]
    dt = t[2] - t[1]

    if args.ground_truth is not None:
        gt_log = np.genfromtxt(args.ground_truth, delimiter=',')

        # State history.
        # Positions of diff drive vehicle.
        x_s = gt_log[:, 0]
        y_s = gt_log[:, 1]
        theta_s = gt_log[:, 2]
        # Velocities of diff drive vehicle.
        dx_s = gt_log[:, 3]
        dy_s = gt_log[:, 4]
        dtheta_s = gt_log[:, 5]

    else:
        x_s = np.zeros((len(x_t), 1))
        y_s = np.zeros((len(x_t), 1))

    if args.sensor_data is not None:
        zt_log = np.genfromtxt(args.sensor_data, delimiter=',')

        # State history.
        # Positions of diff drive vehicle.
        x_z = zt_log[:, 0]
        y_z = zt_log[:, 1]
        theta_z = zt_log[:, 2]
        # Velocities of diff drive vehicle.
        dx_z = zt_log[:, 3]
        dy_z = zt_log[:, 4]
        dtheta_z = zt_log[:, 5]

    else:
        x_z = np.zeros((len(x_t), 1))
        y_z = np.zeros((len(x_t), 1))

    fig = plt.figure()
    ax = fig.add_subplot(111,
                         autoscale_on=False,
                         xlim=(-1.1, 1.1),
                         ylim=(-1.1, 1.1))
    ax.grid()

    line_fr, = ax.plot([], [], 'ro-', lw=2)
    line_zt, = ax.plot([], [], 'go-', lw=2)
    line_gt, = ax.plot([], [], 'bo-', lw=2)
    time_template = 'time = %.1fs'
    time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

    def init():
        line_fr.set_data([], [])
        line_gt.set_data([], [])
        line_zt.set_data([], [])
        time_text.set_text('')

        return line_gt, line_fr, line_zt, time_text

    def animate(i):
        # Filtered linear velocity of the vehicle.
        v = sqrt(square(dx_t[i]) + square(dy_t[i]))
        # Filtered position of the vehicle.
        # Line segment indicates direction of fitlered theta
        # whose magnitude represents the linear velocity.
        thisx = [x_t[i],
                 ARROW_LEN * (v + 0.1) * cos(theta_t[i]) + x_t[i]]
        thisy = [y_t[i],
                 ARROW_LEN * (v + 0.1) * sin(theta_t[i]) + y_t[i]]
        # Ground truth position of the vehicle.
        this_x_s = [x_s[i], x_s[i]]
        this_y_s = [y_s[i], y_s[i]]
        # Sensed position of the vehicle.
        this_x_z = [x_z[i], x_z[i]]
        this_y_z = [y_z[i], y_z[i]]

        line_fr.set_data(thisx, thisy)
        line_gt.set_data(this_x_s, this_y_s)
        line_zt.set_data(this_x_z, this_y_z)
        time_text.set_text(time_template % (i * dt))

        return line_gt, line_fr, line_zt, time_text

    ani = animation.FuncAnimation(fig,
                                  animate,
                                  np.arange(1, len(x_t)),
                                  interval=dt * len(t),
                                  blit=True,
                                  init_func=init)

    # Square the axes.
    plt.gca().set_aspect('equal', adjustable='box')
    plt.show()
