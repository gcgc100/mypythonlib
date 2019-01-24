#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest, time

import gClifford.setTools as setTools


class TestSetTools(unittest.TestCase):

    """Test setTools module"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_merge_set_from_pairs(self):
        pairs = [[1,2], [2,3], [1,3], [4,5], [6,7], [5,9]]
        print(setTools.merge_set_from_pairs(pairs))
