#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys, os
from gClifford import Singleton


class single(metaclass=Singleton.Singleton):

        """Singleton class"""
        # __metaclass__ = Singleton.Singleton

        def __init__(self):
                """for test """
                self.id = 10
                
        def getId(self):
            return self.id


class TestSingleton(unittest.TestCase):

        def test_singleton(self):
                self.assertEqual(single().id, 10)
                self.assertEqual(single().getId(), 10)
                single().id = 20
                self.assertEqual(single().id, 20)
                self.assertEqual(single().getId(), 20)

if __name__ == "__main__":
        unittest.main()
