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

## @file node_maps.py Module for creating test maps.

from nodes import Node
import numpy as np
from PIL import Image


def createMap1():
    # Define nodes.
    n0 = Node([0, 0])
    # n1 = Node([0, 1])
    n2 = Node([0, 2])
    n3 = Node([0, 3])
    n4 = Node([0, 4])
    n5 = Node([1, 0])
    # n6 = Node([1, 1])
    n7 = Node([1, 2])
    # n8 = Node([1, 3])
    n9 = Node([1, 4])
    n10 = Node([2, 0])
    n11 = Node([2, 1])
    n12 = Node([2, 2])
    # n13 = Node([2, 3])
    n14 = Node([2, 4])
    n15 = Node([3, 0])
    n16 = Node([3, 1])
    n17 = Node([3, 2])
    n18 = Node([3, 3])
    n19 = Node([3, 4])

    # Build map.
    n0.add_neighbor(n5)

    n5.add_neighbor(n0)
    n5.add_neighbor(n10)

    n10.add_neighbor(n5)
    n10.add_neighbor(n11)
    n10.add_neighbor(n15)

    n15.add_neighbor(n10)
    n15.add_neighbor(n16)

    n11.add_neighbor(n10)
    n11.add_neighbor(n12)
    n11.add_neighbor(n16)

    n16.add_neighbor(n11)
    n16.add_neighbor(n17)
    n16.add_neighbor(n15)

    n12.add_neighbor(n7)
    n12.add_neighbor(n17)
    n12.add_neighbor(n11)

    n17.add_neighbor(n12)
    n17.add_neighbor(n18)
    n17.add_neighbor(n16)

    n18.add_neighbor(n17)
    n18.add_neighbor(n19)

    n19.add_neighbor(n18)
    n19.add_neighbor(n14)

    n14.add_neighbor(n19)
    n14.add_neighbor(n9)

    n9.add_neighbor(n4)
    n9.add_neighbor(n14)

    n4.add_neighbor(n9)
    n4.add_neighbor(n3)

    n3.add_neighbor(n4)
    n3.add_neighbor(n2)

    n2.add_neighbor(n3)
    n2.add_neighbor(n7)

    n7.add_neighbor(n2)
    n7.add_neighbor(n12)

    return [n0, n2, n3, n4, n5, n7, n9, n10, n11, n12, n14, n15, n16, n17, n18, n19]


def getValidNeighbors(node, arr_map):
    # Get matrix dimensions and generate valid indices.
    map_dim = np.shape(arr_map)
    node_state = node.get_state()
    neighbor_states = []

    possible_states = [[node_state[0], node_state[1] - 1],
                       [node_state[0], node_state[1] + 1],
                       [node_state[0] - 1, node_state[1]],
                       [node_state[0] + 1, node_state[1]]]

    for state in possible_states:
        if state[0] >= 0 and state[0] < map_dim[0] and state[1] >= 0 and state[1] < map_dim[1]:
            if arr_map[state[0]][state[1]] > 0:
                neighbor_states.append(np.array([state[0], state[1]]))

    return neighbor_states


def createMapFromImage(image_path):
    # Convert image to matrix.
    im = Image.open(image_path)
    arr_map = np.array(im)

    # Get the node indices. Zeros are obstacles.
    n_indices = np.where(arr_map > 0)
    n_indices = np.matrix([n_indices[0], n_indices[1]]).T

    # Create nodes.
    # node_set = set()
    node_set = list()
    dim = np.shape(n_indices)
    for idx in range(0, dim[0]):
        node_set.append(Node(n_indices[idx].A.squeeze()))
        # node_set.add(Node(n_indices[idx].A.squeeze()))

    print(str(len(node_set)) + " nodes added.")

    # Find neighbors.
    num = float(len(node_set))
    idx = float(0)
    for node in node_set:
        idx += 1.0
        print("Percentage: " + str(idx/num))
        neighbor_states = getValidNeighbors(node, arr_map)
        if neighbor_states:
            for state in neighbor_states:
                n_node = Node(state)
                # n_node = [cand_node for cand_node in node_set if (cand_node.get_state() == state).all()]
                # if n_node:
                #     node.add_neighbor(n_node[0])
                n_idx = node_set.index(n_node)
                if n_idx:
                    node.add_neighbor(node_set[n_idx])

    return node_set


def main():
    m = createMapFromImage('Simple_maze_small1.png')
    from view_map import viewMap
    viewMap(m)

if __name__ == '__main__':
    main()
