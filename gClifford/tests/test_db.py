#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
from os import path
sys.path.insert(0, path.join(path.dirname(path.abspath(__file__)), ".."))

import db

class TestDB(unittest.TestCase):

    """Test case docstring."""

    @classmethod
    def setUpClass(cls):
        db.create_engine("travis", "", "test")

    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        db.update("create table if not exists test (k VARCHAR(50), v VARCHAR(50), num INT(10));")
        pass

    def tearDown(self):
        db.update("drop table test;")
        pass

    def test_select_one(self):
        testdata = {"k": "key1", "v": "value1", "num": 12}
        db.insert('test', **testdata)
        row = db.select_one("select * from test where num=?", 12)
        self.assertEqual(row["k"], testdata["k"])

    def test_select_int(self):
        testdata = {"k": "key1", "v": "value1", "num": 12}
        db.insert('test', **testdata)
        retdata = db.select_int("select num from test where k=?", testdata["k"])
        self.assertEqual(retdata, 12)

    def test_select_int(self):
        testdata = {"k": "key1", "v": "value1", "num": 12}
        db.insert('test', **testdata)
        rows = db.select("select * from test")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["num"], 12)

    def test_update(self):
        testdata = {"k": "key1", "v": "value1", "num": 12}
        db.insert('test', **testdata)
        nkey = "key2"
        db.update("update test set k=? where num=?", nkey, 12)
        row = db.select_one("select * from test where num=?", 12)
        self.assertEqual(row["k"], nkey)
