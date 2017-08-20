#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Config
import os
import shutil

secretConfig = Config.Config()
if not os.path.isfile("config/secret.secret"):
    shutil.copy("config/config.cfg", "config/secret.secret")
secretConfig.reload("config/secret.secret")

