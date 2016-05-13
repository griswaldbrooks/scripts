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

## @file cluster_fit_points.py Script for clustering points and fitting curves to them.

import numpy as np
import argparse
import copy
from sklearn.cluster import DBSCAN
import matplotlib.pyplot as plt


class LabeledDataSet:
    def __init__(self, label):
        self._data = []
        self._label = label

    def setLabel(self, label):
        self._label = label

    def getLabel(self):
        return self._label

    def append(self, sample):
        self._data.append(sample)

    def getData(self):
        return copy.deepcopy(self._data)


def main():
    # Get command line args.
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args()

    # Load data.
    data = np.loadtxt(args.filename, delimiter=',')
    ##############################################################################
    # Compute DBSCAN
    db = DBSCAN(eps=10, min_samples=10).fit(data)
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    print('Estimated number of clusters: %d' % n_clusters_)

    # Split into different sets.
    labeled_sets = [LabeledDataSet(label) for label in xrange(n_clusters_)]
    print set(labels)
    for sample, label in zip(data, labels):
        if label != -1:
            labeled_sets[label].append(sample)

    # Curve fit each set.
    for labeled_set in labeled_sets:
        # Get the data and format it for polyfit.
        sample_set = np.array(labeled_set.getData())

        # Create function.
        coeff = np.polyfit(sample_set[:, 0], sample_set[:, 1], 5)
        curve = np.poly1d(coeff)

        xp = np.linspace(min(sample_set[:, 0]), max(sample_set[:, 0]), 1000)
        plt.plot(xp, curve(xp), '-')
        plt.ylim(0, 600)
        plt.xlim(200, 1000)

        np.savetxt('label' + str(labeled_set.getLabel()) + '.sample_set', np.transpose([sample_set[:, 0], sample_set[:, 1]]), delimiter=',')
        np.savetxt('label' + str(labeled_set.getLabel()) + '.poly_points', np.transpose([xp, curve(xp)]), delimiter=',')
    ##############################################################################
    # Plot result
    # Black removed and is used for noise instead.
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'

        class_member_mask = (labels == k)

        xy = data[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=3)

        xy = data[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
                 markeredgecolor='k', markersize=1)

    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show()

if __name__ == '__main__':
    main()
