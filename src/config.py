#! /usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Wang Yong
# 
# Author:     Wang Yong <lazycat.manatee@gmail.com>
# Maintainer: Wang Yong <lazycat.manatee@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from PyQt5.QtCore import QObject, pyqtSlot
import os
from xdg import get_config_file
from deepin_utils.config import Config
from deepin_utils.core import is_true

DEFAULT_CONFIG = [
    ("trayicon", 
     [("pause", False),
      ("toggle_speech", True),
      ("key_trigger_ocr", True),
      ("key_trigger_select", False),
      ])]

class SettingConfig(QObject):
    
    def __init__(self):
        QObject.__init__(self)
        self.config_file = get_config_file("config.ini")
        
        if os.path.exists(self.config_file):
            self.config = Config(self.config_file, DEFAULT_CONFIG)
            self.config.load()
        else:
            self.config = Config(self.config_file, DEFAULT_CONFIG)
            self.config.write()
            print self.config.default_config
            
    def update_trayicon_config(self, config_id, config_value):
        with self.config.save_config():
            self.config.set("trayicon", config_id, config_value)
            
    @pyqtSlot(str, result=bool)        
    def get_trayicon_config(self, option):
        return is_true(self.config.get_config("trayicon", option))
            
setting_config = SettingConfig()
