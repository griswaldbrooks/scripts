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
from numpy import linalg as la
from nodes import Node
# from node_maps import createMap1
from node_maps import createMapFromImage
from view_map import printMap
from view_map import viewMap


class AStarNode(Node):
    def __init__(self, node):
        self._state = node.get_state()
        self._neighbors = node.get_neighbors()
        self._fscore = float("inf")
        self._gscore = float("inf")

    def set_fscore(self, score):
        self._fscore = score

    def set_gscore(self, score):
        self._gscore = score

    def get_fscore(self):
        return self._fscore

    def get_gscore(self):
        return self._gscore

    def get_cost(self):
        return self.get_fscore()


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
        # return 0

    def cost_to_node(self, node1, node2):
        return la.norm(node1.get_state() - node2.get_state())

    def in_closed_set(self, node):
        # return any((node == c_node).all() for c_node in self._closed)
        try:
            self._closed.index(node)
            return True
        except Exception:
            return False

    def in_open_set(self, node):
        # return any((node == c_node).all() for c_node in self._open)
        try:
            self._open.index(node)
            return True
        except Exception:
            return False

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
            self._map.append(c_node)

            # Is this the goal?
            if c_node == self._goal_state:
                # Reconstruct the path.
                self._goal_state = c_node
                self._generate_path()
                return

            # Add it to the closed set.
            self._closed.append(c_node)

            # Check to see if neighbors need to be expanded or cost updated.
            c_neighbors = c_node.get_neighbors()

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
                    # bn_node = [node for node in self._open if node == an_node]
                    # if bn_node[0].get_gscore() >= an_node.get_gscore():
                    #     bn_node[0] = an_node
                    b_ndx = self._open.index(an_node)
                    if self._open[b_ndx].get_gscore() >= an_node.get_gscore():
                        self._open[b_ndx] = an_node


def main():

    # Get a map.
    # map = createMap1()
    map = createMapFromImage('Simple_maze_small1.png')

    # TODO: Convert to coordinates.
    # n_s = [node for node in map if node == Node([0, 0])]
    # n_s = n_s[0]
    # n_f = [node for node in map if node == Node([1, 4])]
    # n_f = n_f[0]
    n_s = [node for node in map if node == Node([85, 5])]
    n_s = n_s[0]
    n_f = [node for node in map if node == Node([38, 42])]
    n_f = n_f[0]

    print("Start Node: " + str(n_s.get_state()))

    # Find path.
    s = Searcher()
    # s.add_map(map)
    s.set_start(n_s)
    s.set_goal(n_f)
    s.find_path()

    print s.path_length()
    # printMap(s._path)
    viewMap(s._map, path=s._path)

if __name__ == '__main__':
    main()
