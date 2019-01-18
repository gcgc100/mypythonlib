#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest

from gClifford.mylogging import logger
import gClifford.mylogging as l
import shutil
import os


class TestMyLogging(unittest.TestCase):

    """Test mylogging module"""

    def setUp(self):
        if os.path.exists("log"):
            print ("log directory already exists, delete or move"
                   " log directory and run test again")

    def tearDown(self):
        if os.path.exists("log"):
            shutil.rmtree("log")

    def test_logfile(self):
        logger.debug("1 test")
        return
        print(l.ROOT_DIR)
        with open("log/log.log") as f:
            text = f.read()
            self.assertTrue(text.endswith("DEBUG, 1 test\n"))

    def test_contextLog(self):
        class t(object):
            @l.contextLog(logger)
            def func(self):
                print("inside func")

        t().func()


if __name__ == "__main__":
    unittest.main()
