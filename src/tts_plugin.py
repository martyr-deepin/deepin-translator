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

from PyQt5.QtCore import pyqtSlot, QObject
import os
from model import Model
from deepin_utils.config import Config
from deepin_utils.core import is_true
from deepin_utils.file import get_parent_dir
from nls import LANGUAGE

class TtsPlugin(QObject):
    
    def __init__(self):
        QObject.__init__(self)
        
        self.plugin_config_name = "config.ini"
        self.plugin_module_name = "tts.py"
        self.plugin_dir = os.path.join(get_parent_dir(__file__), "tts_plugins")
        
        self.scan_plugin_info()
        
    def get_plugin_file(self, plugin_name):
        return os.path.join(self.plugin_dir, plugin_name, self.plugin_module_name)
    
    def get_voice_engines(self, src_lang, connected=True):
        engine_list = []
        if self.engine_dict.has_key(src_lang):
            engine_list += self.engine_dict[src_lang]
            
        voice_list = engine_list + self.engine_list
        voice_list = sorted(voice_list, key=lambda (name, display_name, priority, need_network): priority, reverse=True)
        
        return map(lambda (name, display_name, priority, need_network): (name, display_name), 
                   filter(lambda (name, display_name, priority, need_network): need_network == connected, voice_list))
    
    @pyqtSlot(str, result="QVariant")
    def get_voice_model(self, src_lang):
        self.voice_model = Model(self.get_voice_engines(src_lang))
        return self.voice_model
    
    def scan_plugin_info(self):
        self.engine_list = []
        self.engine_dict = {}
        
        for plugin_name in os.listdir(self.plugin_dir):
            plugin_config_file = os.path.join(self.plugin_dir, plugin_name, self.plugin_config_name)
            plugin_config = Config(plugin_config_file)
            plugin_config.load()
            
            language = LANGUAGE.replace("_", "-")
            plugin_display_name = plugin_config.get("Plugin Info", "name[%s]" % language) or plugin_config.get("Plugin Info", "name[en]")
            
            need_network = is_true(plugin_config.get("Voice Info", "need_network"))
            support_all_language = is_true(plugin_config.get("Voice Info", "support_all_language"))
            support_languages_info = plugin_config.get("Voice Info", "support_languages")
            priority = plugin_config.get("Voice Info", "priority")
            if support_languages_info == None:
                support_languages = []
            else:
                support_languages = support_languages_info.split(",")
                
            if support_all_language:
                self.engine_list.append((plugin_name, plugin_display_name, priority, need_network))
            else:
                self.update_dict(self.engine_dict, support_languages, plugin_name, plugin_display_name, priority, need_network)

    def update_dict(self, info_dict, languages, plugin_name, plugin_display_name, priority, need_network):
        for language in languages:
            if not info_dict.has_key(language):
                info_dict[language] = []
                
            info_list = info_dict[language]    
            info_list.append((plugin_name, plugin_display_name, priority, need_network))
