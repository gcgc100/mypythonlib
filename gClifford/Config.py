#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# import ConfigParser
import configparser
import os
from gClifford.Singleton import Singleton
import gClifford.osAddon as osAddon

cwd = os.getcwd()


class Config(metaclass=Singleton):
    """docstring for Config"""
    _config = None

    def __init__(self):
        """docstring for __init__"""
        global _config
        # _config = ConfigParser.RawConfigParser()
        _config = configparser.ConfigParser()
        self._configFilepath = "config/config.cfg"
        if not os.path.isfile(self._configFilepath):
            os.makedirs("config", exist_ok=False)
            config = _config
            config['DEFAULT'] = {}
            with open(self._configFilepath, 'w') as configfile:
                config.write(configfile)
            print("init config OK")
        else:
            _config.read(self._configFilepath)

    # def __getattr__(self, key):
    #     global _config
    #     try:
    #         return _config['DEFAULT'][key]
    #     except KeyError:
    #         raise AttributeError(r"'Dict' object has no attribute '%s'" % key)
    #
    # def __setattr__(self, key, value):
    #     __import__('pdb').set_trace()
    #     raise AttributeError("Readonly")

    @property
    def config(self):
        """The config property."""
        global _config
        return _config
    
    def write(self):
        config = self.config
        with open(self._configFilepath, 'w') as configfile:
            config.write(configfile)
            

    def reload(self, name=None):
        """

        """
        global _config
        # _config = ConfigParser.RawConfigParser()
        _config = configparser.ConfigParser()
        if name is None:
            name = self._configFilepath
        if not os.path.isfile(name):
            config = _config
            config['DEFAULT'] = {}
            with open(name, 'w') as configfile:
                config.write(configfile)
        else:
            _config.read(name)
            
def __getattr__(name):
    if name == "config":
        return Config().config
    elif name == "defaultConfig":
        return Config().config["DEFAULT"]
    else:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
#
if __name__ == '__main__':
    import doctest
    doctest.testmod()
