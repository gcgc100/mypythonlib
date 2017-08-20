#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Set the __metaclass__ of the class to Singleton to make it a singleton class.
"""

class Singleton(type):

    def __init__(cls, name, bases, dict):
        super(Singleton, cls).__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kw):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kw)
        return cls._instance
