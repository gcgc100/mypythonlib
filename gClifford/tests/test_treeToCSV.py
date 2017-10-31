#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os

from gClifford.treeToCSV import tree_to_CSV


class TreeNode(object):

    """Docstring for TreeNode. """

    def __init__(self, data, parent=None):
        """TODO: to be defined1. """
        self.__children = []
        self.__data = data
        self.__parent = parent

    def __str__(self):
        return self.__data

    @property
    def children(self):
        """children property getter
        """
        return self.__children

    @children.setter
    def children(self, children):
        """children property setter
        """
        self.__children = children

    @property
    def parent(self):
        """parent property getter
        """
        return self.__parent

    @parent.setter
    def parent(self, parent):
        """parent property setter
        """
        self.__parent = parent


class TestTreeToCSV(unittest.TestCase):

    """Test treeToCSV module"""

    def setUp(self):
        self.testTmpDir = "./gClifford/tests/dataForTest/tmp"
        self.treeRoot = TreeNode("a")
        for i in range(10):
            self.treeRoot.children.append(TreeNode("b%s" % i, self.treeRoot))
        if not os.path.isdir(self.testTmpDir):
            os.mkdir(self.testTmpDir)

    def tearDown(self):
        pass

    def test_tree_to_csv(self):
        with open(os.path.join(self.testTmpDir, "test.csv"), "w") as f:
            tree_to_CSV(self.treeRoot, f, header=["1", "2"])
