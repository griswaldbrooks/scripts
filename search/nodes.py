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

## @file nodes.py Module for creating state nodes.

import numpy as np


class Node:
    def __init__(self, state):
        self._state = np.array(state)
        self._neighbors = []
        self._predecessor = None

    def __eq__(self, node):
        return (self.get_state() == node.get_state()).all()

    def __hash__(self):
        return hash(tuple(self._state))

    def get_neighbors(self):
        return self._neighbors

    def get_state(self):
        return self._state

    def get_cost(self):
        return float("inf")

    def set_state(self, state):
        self._state = np.array(state)

    def add_neighbor(self, neighbor):
        self._neighbors.append(neighbor)

    def set_predecessor(self, anode):
        self._predecessor = anode

    def get_predecessor(self):
        return self._predecessor
