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

## @file astar_rough.py Module for doing an astar search.

from copy import deepcopy
import numpy as np
from numpy import linalg as la


class Node:
    def __init__(self, state):
        self._state = np.array(state)
        self._neighbors = []

    def __eq__(self, node):
        return (self.get_state() == node.get_state()).all()

    def get_neighbors(self):
        return self._neighbors

    def get_state(self):
        return self._state

    def set_state(self, state):
        self._state = np.array(state)

    def add_neighbor(self, neighbor):
        self._neighbors.append(neighbor)


class AStarNode(Node):
    def __init__(self, node):
        self._state = node.get_state()
        self._neighbors = node.get_neighbors()
        self._fscore = float("inf")
        self._gscore = float("inf")
        self._predecessor = None

    def set_fscore(self, score):
        self._fscore = score

    def set_gscore(self, score):
        self._gscore = score

    def set_predecessor(self, anode):
        self._predecessor = anode

    def get_fscore(self):
        return self._fscore

    def get_gscore(self):
        return self._gscore

    def get_predecessor(self):
        return self._predecessor


class Searcher:
    def __init__(self):
        self._open = []
        self._closed = []
        self._map = []
        self._start_state = AStarNode(Node([float("inf"), float("inf")]))
        self._goal_state = AStarNode(Node([float("inf"), float("inf")]))
        # self._path_length = float("inf")
        self._path = []

    def add_map(self, map):
        self._map = deepcopy(map)

    def set_start(self, node):
        self._start_state = AStarNode(node)

    def set_goal(self, node):
        self._goal_state = AStarNode(node)

    def cost_to_goal(self, node):
        return la.norm(node.get_state() - self._goal_state.get_state())

    def cost_to_node(self, node1, node2):
        return la.norm(node1.get_state() - node2.get_state())

    def in_closed_set(self, node):
        return any((node == c_node).all() for c_node in self._closed)

    def in_open_set(self, node):
        return any((node == c_node).all() for c_node in self._open)

    def path_length(self):
        return len(self._path)

    def _generate_path(self):
        c_node = self._goal_state
        self._path.append(c_node)
        while not c_node == self._start_state:
            c_node = c_node.get_predecessor()
            self._path.append(c_node)

    def find_path(self):
        # Add start to open set.
        start_node = AStarNode(self._start_state)
        start_node.set_gscore(0)
        start_node.set_fscore(self.cost_to_goal(self._start_state))
        self._open.append(start_node)

        # If open list isn't empty.
        while self._open:
            # Put the cheapest node on top.
            self._open.sort(key=lambda node: node.get_fscore())

            # Expand node.
            c_node = self._open.pop(0)
            print("Current Node:" + str(c_node.get_state()))

            # Is this the goal?
            if c_node == self._goal_state:
                # Reconstruct the path.
                print("Made it!")
                self._goal_state = c_node
                self._generate_path()
                return

            # Add it to the closed set.
            self._closed.append(c_node)

            # Check to see if neighbors need to be expanded or cost updated.
            c_neighbors = c_node.get_neighbors()
            for neighbor in c_neighbors:
                print("     Neighbor Node: " + str(neighbor.get_state()))

            for n_node in c_neighbors:
                # If it's closed it doesn't need to be checked.
                if self.in_closed_set(n_node):
                    continue

                # Update cost and add to open.
                an_node = AStarNode(n_node)
                an_node.set_gscore(c_node.get_gscore() + self.cost_to_node(c_node, n_node))
                an_node.set_fscore(an_node.get_gscore() + self.cost_to_goal(an_node))
                an_node.set_predecessor(c_node)

                if not self.in_open_set(an_node):
                    self._open.append(an_node)
                else:
                    # Find the node in the open set.
                    bn_node = [node for node in self._open if node == an_node]
                    if bn_node[0].get_gscore() >= an_node.get_gscore():
                        bn_node[0] = an_node


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


def printMap(map):
    for node in map:
        print("Node State: " + str(node.get_state()))
        print("Neighbors: ")
        for neighbor in node.get_neighbors():
            print("     Node State: " + str(neighbor.get_state()))


def main():

    # Get a map.
    map = createMap1()

    # TODO: Convert to coordinates.
    n_s = [node for node in map if node == Node([0, 0])]
    n_s = n_s[0]
    n_f = [node for node in map if node == Node([1, 4])]
    n_f = n_f[0]

    print("Start Node: " + str(n_s.get_state()))

    # Find path.
    s = Searcher()
    s.add_map(map)
    s.set_start(n_s)
    s.set_goal(n_f)
    s.find_path()

    print s.path_length()
    printMap(s._path)   

if __name__ == '__main__':
    main()
