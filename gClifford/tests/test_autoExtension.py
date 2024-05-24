#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from os import path

from scipy.linalg import det
sys.path.insert(0, path.join(path.dirname(path.abspath(__file__)), ".."))

from pathlib import Path

from AutoExtension import AutoExtension


class TestAutoExtension(object):

    def setup_class(self):
        extPath = (Path(__file__).parent / "testdata/posta.crx").absolute()
        self.ae = AutoExtension(str(extPath))
    
    def test_initSelenium(self):
        self.ae.initSelenium()
        assert self.ae.extensionId == "celeboldlbeicnjbldldiaojcbmcfjka"
        assert self.ae.name == "posta"
        assert self.ae.description == "posta"
        assert "tabs" in self.ae.permissions
        
    def test_manifest(self):
        assert self.ae.Manifest['name'] == "posta"

    def test_backgroundScripts(self):
        assert Path(self.ae.BackgroundScripts[0]).name == "background.js"

    def test_contentScripts(self):
        assert Path(self.ae.ContentScripts[0]["js"]).name == "agent.js"
        
    def test_tmp(self):
        self.ae.openOptionUI()
        return
        self.ae.clickExtensionButton()


