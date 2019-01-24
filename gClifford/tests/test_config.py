#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import sys
import os
import shutil

import gClifford.tests.ModuleUsingConfig as mc
from gClifford import Config

class TestConfig(unittest.TestCase):

    """Test Config module"""

    @classmethod
    def setUpClass(cls):
        Config.Config()
        shutil.copyfile("config/config.cfg", "config/test.cfg")
        with open("config/config.cfg", "a") as f:
            f.write("name = config\n")
        with open("config/test.cfg", "a") as f:
            f.write("name = test\n")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree("config")

    def test_name(self):
        self.assertEqual(Config.Config().name, "config")
        Config.Config().reload("config/test.cfg")
        self.assertEqual(Config.Config().name, "test")
        Config.Config().reload("config/config.cfg")

    def test_config_in_module(self):
        Config.Config().reload("config/test.cfg")
        self.assertEqual(mc.printValue(), "test")
        Config.Config().reload("config/config.cfg")
        

if __name__ == "__main__":
    unittest.main()
