#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import unittest
from sklearn.datasets import fetch_20newsgroups
import gClifford.tfIdf as tfIdf

class TestTfIdf(unittest.TestCase):

    """Test case docstring."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_tfidf(self):
        categories = ['alt.atheism', 'talk.religion.misc', 'comp.graphics', 'sci.space']
        newsgroups_train = fetch_20newsgroups(subset='train', 
                categories=categories)
        vectors = tfIdf.tfIdf(newsgroups_train.data[:200])
