#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ConfigParser
import os
from Singleton import Singleton
import osAddon

cwd = os.getcwd()


class Config(object):
    """docstring for Config"""
    __metaclass__ = Singleton
    _config = None

    def __init__(self):
        """docstring for __init__"""
        global _config
        _config = ConfigParser.RawConfigParser()
        if not os.path.isfile("config/config.cfg"):
            osAddon.ensure_dir("config/config.cfg")
            config = _config
            config.add_section('config')
            with open('config/config.cfg', 'wb') as configfile:
                config.write(configfile)
            print "init config OK"
        else:
            _config.read("config/config.cfg")

    def __getattr__(self, key):
        global _config
        try:
            return _config.get('config', key)
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        raise AttributeError("Readonly")

    def reload(self, name="config/config.cfg"):
        """

        """
        global _config
        _config = ConfigParser.RawConfigParser()
        if not os.path.isfile(name):
            config = _config
            config.add_section('config')
            with open(name, 'wb') as configfile:
                config.write(configfile)
        else:
            _config.read(name)

if __name__ == '__main__':
    import doctest
    doctest.testmod()
