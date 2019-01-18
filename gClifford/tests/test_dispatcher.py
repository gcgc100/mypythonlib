#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest, time

from gClifford import dispatcher as disp

class TestDispatcher(unittest.TestCase):
    """Test dispatcher"""
    count = 0
    def target(self):
        self.count = 5
        print("I should appear after 5s")
    def target2(self):
        self.count = 10
        print("I should appear after 10s")
    def test_dispatch_basic(self):
        """Test dispatch function"""
        h = disp.dispatch(self.target, delaytime=5)
        self.assertEqual(self.count, 0)
        time.sleep(3)
        self.assertEqual(self.count, 0)
        time.sleep(3)
        self.assertEqual(self.count, 5)
        self.count = 0
        h = disp.dispatch(self.target, delaytime=5)
        h.cancelTheDelayTask()
        time.sleep(6)
        self.assertEqual(self.count, 0)
    
    def test_dispatch_parral(self):
        h1 = disp.dispatch(self.target, delaytime=5)
        h2 = disp.dispatch(self.target2, delaytime=3)
        self.assertEqual(self.count, 0)
        time.sleep(4)
        self.assertEqual(self.count, 10)
        time.sleep(3)
        self.assertEqual(self.count, 5)
        self.count = 0

    def test_dispatch_paralAndCancel(self):
        h1 = disp.dispatch(self.target, delaytime=5)
        h2 = disp.dispatch(self.target2, delaytime=3)
        self.assertEqual(self.count, 0)
        h2.cancelTheDelayTask()
        time.sleep(4)
        self.assertEqual(self.count, 0)
        time.sleep(3)
        self.assertEqual(self.count, 5)
        self.count = 0

    def test_dispatch_closure(self):
        outer = [0,]
        def closure():
            outer
            outer[0] = 10
        disp.dispatch(closure, delaytime=3)
        self.assertEqual(outer[0], 0)
        time.sleep(5)
        self.assertEqual(outer[0], 10)
