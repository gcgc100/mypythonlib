#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import shutil
from gClifford import osAddon


class TestOsAddon(unittest.TestCase):

    """Test osAddon module"""

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree("./gClifford/tests/dataForTest/output")
        os.mkdir("./gClifford/tests/dataForTest/output")

    def setUp(self):
        outputdir = "./gClifford/tests/dataForTest/output"
        if not os.path.isdir(outputdir):
            os.mkdir(outputdir)

    def tearDown(self):
        pass

    def test_ensure_dir(self):
        osAddon.ensure_dir("testDir/test")
        os.rmdir("testDir")
        osAddon.ensure_dir("test.md")
        osAddon.ensure_dir("./test")

    def test_get_size(self):
        self.assertEqual(osAddon.get_size(
            os.path.dirname(os.path.abspath(__file__))+"/testSize"), 1775)

    def test_smartCopy(self):
        testdata = "./gClifford/tests/dataForTest/"
        src = testdata+"a.txt"
        output = testdata+"output"
        osAddon.smartCopy(src, output)
        with self.assertRaises(IOError):
            osAddon.smartCopy(src, testdata+"notexist")
        osAddon.smartCopy(src, output)
        self.assertEqual(len(os.listdir(output)), 2)
        osAddon.smartCopy(src, output)
        self.assertEqual(len(os.listdir(output)), 3)
        with self.assertRaises(IOError):
            osAddon.smartCopy(testdata+"b.txt", output)


if __name__ == "__main__":
    unittest.main()
