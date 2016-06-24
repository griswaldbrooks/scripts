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

## @file view_map.py Module for visualizing Node maps.

import matplotlib.pyplot as plt
from matplotlib import collections as mc
from node_maps import createMap1
import numpy as np


def printMap(map):
    for node in map:
        print("Node State: " + str(node.get_state()))
        print("Neighbors: ")
        for neighbor in node.get_neighbors():
            print("     Node State: " + str(neighbor.get_state()))


def viewMap(map, path=[]):
    # Edge segments.
    map_edges = []
    path_edges = []

    # Node colormap.
    cm = plt.get_cmap('jet')
    for node in map:
        # Add vertices.
        # Rows are x coordinates. Cols are y.
        s = node.get_state()

        # Get vertex cost and color.
        c = node.get_cost()
        # TODO: Maps need a way to be asked what the min and max costs are.
        cost_range = [0, 1000]
        color_range = [0.0, 1.0]
        node_color = cm(np.interp(c, cost_range, color_range))
        plt.plot(s[0], s[1], 'o', c=node_color, markersize=5)

        # Add edges.
        for n_node in node.get_neighbors():
            s_n = n_node.get_state()
            map_edges.append([s, s_n])

    for node in path:
        try:
            p_node = node.get_predecessor()

            # Add edge.
            if p_node:
                path_edges.append([node.get_state(), p_node.get_state()])
        except Exception:
            pass

    map_edge_col = mc.LineCollection(map_edges)
    path_edge_col = mc.LineCollection(path_edges, linewidth=5, label="Path")
    plt.gca().add_collection(map_edge_col)
    plt.gca().add_collection(path_edge_col)
    plt.margins(0.1)
    plt.legend(loc='upper right', shadow=True, fontsize='large', numpoints=1)
    # Set colorbars for nodes.
    sm = plt.cm.ScalarMappable(cmap=cm, norm=plt.Normalize(vmin=0, vmax=1000))
    sm._A = []
    colorbar = plt.colorbar(sm, shrink=0.9, pad=0.02)
    colorbar.set_label('Node Cost')

    plt.show()


def main():

    # Get a map.
    map = createMap1()

    printMap(map)
    viewMap(map)

if __name__ == '__main__':
    main()
