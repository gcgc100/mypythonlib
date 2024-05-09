#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import shutil
import pytest
from pathlib import Path

import gClifford.tests.ModuleUsingConfig as mc
from gClifford import Config

class TestConfig():

    """Test Config module"""

    @pytest.fixture
    def config(self):
        Path("config").mkdir(exist_ok=True)
        _configFile = "config/config.cfg"
        _testFile = "config/test.cfg"
        with open(_configFile, "a") as f:
            f.write("[DEFAULT]\n")
            f.write("name = config\n")
        with open(_testFile, "a") as f:
            f.write("[DEFAULT]\n")
            f.write("name = test\n")
        yield None
        Path(_configFile).unlink()
        Path(_testFile).unlink()
        shutil.rmtree("config")
            
    def test_name(self, config):
        assert Config.defaultConfig.get("name") == "config"
        Config.Config().reload("config/test.cfg")
        assert Config.defaultConfig.get("name") == "test"
        assert Config.Config().config["DEFAULT"]["name"] == "test"
        Config.Config().reload("config/config.cfg")

    def test_config_in_module(self, config):
        Config.Config().reload("config/test.cfg")
        assert mc.printValue() == "test"
        Config.Config().reload("config/config.cfg")
