#! /usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2013 Deepin, Inc.
#               2011 ~ 2013 Wang Yong
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
from nls import LANGUAGE

init_lang = LANGUAGE.replace("_", "-")
if init_lang in ["zh-CN"]:
    init_word_dict = "youdao"
    init_word_voice = "youdao"
    init_words_voice = "google"
else:
    init_word_dict = "google_simple"
    init_word_voice = "google"
    init_words_voice = "google"

DEFAULT_CONFIG = [
    ("trayicon", 
     [("pause", False),
      ("toggle_speech", True),
      ("key_trigger_select", False),
      ]),
    ("translate",
     [("src_lang", "en"),
      ("dst_lang", init_lang),
      ("word_engine", init_word_dict),
      ("words_engine", "google_long"),
      ("word_voice_engine", init_word_voice),
      ("words_voice_engine", init_words_voice),
      ]),
    ]

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
            
    @pyqtSlot(str, bool)        
    def update_trayicon_config(self, config_id, config_value):
        with self.config.save_config():
            self.config.set("trayicon", config_id, config_value)

    @pyqtSlot(str, str)        
    def update_translate_config(self, config_id, config_value):
        with self.config.save_config():
            self.config.set("translate", config_id, config_value)
            
    @pyqtSlot(str, result=bool)        
    def get_trayicon_config(self, option):
        return is_true(self.config.get_config("trayicon", option))
    
    @pyqtSlot(str, result=str)
    def get_translate_config(self, option):
        return self.config.get_config("translate", option)
            
setting_config = SettingConfig()
