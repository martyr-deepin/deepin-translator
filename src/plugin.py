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

from PyQt5.QtCore import pyqtSlot, QObject
import os
from model import Model
from deepin_utils.config import Config
from deepin_utils.core import is_true
import locale
from deepin_utils.file import get_parent_dir

class Plugin(QObject):
    
    def __init__(self):
        QObject.__init__(self)
        
        self.plugin_config_name = "config.ini"
        self.plugin_module_name = "translate.py"
        self.plugin_dir = os.path.join(get_parent_dir(__file__), "dict_plugins")
        
        self.scan_plugin_info()
        
    def get_plugin_file(self, plugin_name):
        return os.path.join(self.plugin_dir, plugin_name, self.plugin_module_name)
    
    @pyqtSlot(str, str, result="QVariant")
    def get_word_model(self, src_lang, dst_lang):
        self.word_model = Model(self.get_word_engines(src_lang, dst_lang))
        return self.word_model

    @pyqtSlot(str, str, result="QVariant")
    def get_words_model(self, src_lang, dst_lang):
        self.words_model = Model(self.get_words_engines(src_lang, dst_lang))
        return self.words_model
    
    def get_word_engines(self, src_lang, dst_lang):
        engine_list = []
        if self.word_dict.has_key(src_lang) and self.word_dict[src_lang].has_key(dst_lang):
            engine_list = self.word_dict[src_lang][dst_lang]
            
        return engine_list + self.word_all_list
    
    def get_words_engines(self, src_lang, dst_lang):
        engine_list = []
        if self.words_dict.has_key(src_lang) and self.words_dict[src_lang].has_key(dst_lang):
            engine_list = self.words_dict[src_lang][dst_lang]

        return engine_list + self.words_all_list    

    def scan_plugin_info(self):
        self.word_all_list = []
        self.words_all_list = []
        self.word_dict = {}
        self.words_dict = {}
        
        for plugin_name in os.listdir(self.plugin_dir):
            plugin_config_file = os.path.join(self.plugin_dir, plugin_name, self.plugin_config_name)
            plugin_config = Config(plugin_config_file)
            plugin_config.load()
            
            language = locale.getlocale()[0].replace("_", "-")
            plugin_display_name = plugin_config.get("Plugin Info", "name[%s]" % language) or plugin_config.get("Plugin Info", "name[en]")
            is_support_word = is_true(plugin_config.get("Language Info", "word_translate"))
            is_support_words = is_true(plugin_config.get("Language Info", "words_translate"))
            support_all_language = is_true(plugin_config.get("Language Info", "support_all_language"))
            two_way_translate = is_true(plugin_config.get("Language Info", "two_way_translate"))
            src_language = plugin_config.get("Language Info", "src_language")
            dst_language = plugin_config.get("Language Info", "dst_language")
            
            if is_support_word:
                if support_all_language:
                    self.word_all_list.append((plugin_name, plugin_display_name))
                else:
                    self.update_dict(self.word_dict, src_language, dst_language, plugin_name, plugin_display_name)
                    
                    if two_way_translate:
                        self.update_dict(self.word_dict, dst_language, src_language, plugin_name, plugin_display_name)    
                        
            if is_support_words:
                if support_all_language:
                    self.words_all_list.append((plugin_name, plugin_display_name))
                else:
                    self.update_dict(self.words_dict, src_language, dst_language, plugin_name, plugin_display_name)
                    
                    if two_way_translate:
                        self.update_dict(self.words_dict, dst_language, src_language, plugin_name, plugin_display_name)    
                        
    def update_dict(self, info_dict, first_key, second_key, plugin_name, plugin_display_name):
        if not info_dict.has_key(first_key):
            info_dict[first_key] = {}
            
        if not info_dict[first_key].has_key(second_key):
            info_dict[first_key][second_key] = []
            
        info_list = info_dict[first_key][second_key]
        info_list.append((plugin_name, plugin_display_name))    
