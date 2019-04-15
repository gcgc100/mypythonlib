#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import unittest

import gClifford.myCluster as clu

class TestMyCluster(unittest.TestCase):

    """Test myCluster"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_KMeans(self):
        print(clu.myCluster().cluster(3))

    def test_KMeanShift(self):
        print(clu.myCluster().cluster(3, cluster=clu.myCluster.MeanShiftCluster))
        
    def test_DBSCAN(self):
        print(clu.myCluster().cluster(3, cluster=clu.myCluster.DBSCANCluster))

    def test_Birch(self):
        print(clu.myCluster().cluster(3, cluster=clu.myCluster.BirchCluster))
        
        
