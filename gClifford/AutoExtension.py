#!/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

from pathlib import Path
# import tempfile
import json
import functools
from urllib.parse import urlparse
from urllib.parse import parse_qs

class AutoExtension(object):
    
    def __init__(self, crxPath, driverPath=None):
        self.extensionCrxPath = crxPath
        self.driverPath = driverPath
        # self.tmpUserData = tempfile.mkdtemp()

    def initSelenium(self, disableCache=True, customOption=None):
        driver_path = self.driverPath
        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # chrome_options.add_argument('--disable-gpu')
        chrome_options.add_extension(str(self.extensionCrxPath))
        # chrome_options.add_argument(self.tmpUserData)
        if customOption is not None:
            assert callable(customOption)
            chrome_options = customOption(chrome_options)
        if driver_path is None:
            s = Service()
        else:
            s = Service(executable_path=driver_path)
        driver = webdriver.Chrome(options=chrome_options, service=s) #打开扩展posta 
        if disableCache:
            driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled":True})
        self.driver = driver
        
        driver.get("chrome://extensions")
        # shadow = driver.execute_script('return document.getElementsByTagName("extensions-manager")[0].shadowRoot')
        shadow1 = driver.find_element(by=By.CSS_SELECTOR, value="extensions-manager")
        shadow2 = shadow1.shadow_root.find_element(by=By.CSS_SELECTOR, value="extensions-item-list")
        shadow3 = shadow2.shadow_root.find_element(by=By.CSS_SELECTOR, value="extensions-item")
        detailBut = shadow3.shadow_root.find_element(by=By.CSS_SELECTOR, value="#detailsButton")
        detailBut.click()
        
        o = urlparse(driver.current_url)
        self._extensionId = parse_qs(o.query)["id"][0]
        
        shadow1 = driver.find_element(by=By.CSS_SELECTOR, value="extensions-manager")
        shadow2 = shadow1.shadow_root.find_element(by=By.CSS_SELECTOR, value="extensions-detail-view")
        load_path = shadow2.shadow_root.find_element(by=By.CSS_SELECTOR, value="#load-path")
        self._extensionLoadPath = load_path.find_element(by=By.CSS_SELECTOR, value="a").text


    def openOptionUI(self):
        self.driver.get("chrome-extension://{}/{}".format(self.extensionId, self.Manifest["options_ui"]["page"]))

    @property
    def name(self):
        """The name property."""
        return self.Manifest["name"]

    @property
    def description(self):
        """The description property."""
        return self.Manifest["description"]

    @property
    def extensionId(self):
        """The extensionId property."""
        return self._extensionId

    @property
    def permissions(self):
        """The permissions property."""
        return self.Manifest["permissions"]

    @property
    def web_accessible_resources(self):
        """The web_accessible_resources property."""
        return self.Manifest["web_accessible_resources"]
    
    @property
    @functools.lru_cache(maxsize=None)
    def ContentScripts(self):
        """The ContentScripts property."""
        csRet = []
        for cs in self.Manifest["content_scripts"]:
            for cs_file in cs["js"]:
                csItem = cs.copy()
                csItem["js"] = Path(self._extensionLoadPath) / cs_file
            csRet.append(csItem)
        return csRet

    @property
    @functools.lru_cache(maxsize=None)
    def BackgroundScripts(self):
        """The BackgroundScripts property."""
        bsRet = []
        for bs in self.Manifest["background"]["scripts"]:
            bsRet.append(Path(self._extensionLoadPath) / bs)
        return bsRet

    @property
    @functools.lru_cache(maxsize=None)
    def Manifest(self):
        """The Manifest property."""
        with open(Path(self._extensionLoadPath) / "manifest.json", "r") as f:
            manifest = json.load(f)
        return manifest
