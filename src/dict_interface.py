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
from dict_plugin import DictPlugin
from model import LanguageModel
import imp
from config import setting_config

dict_plugin = DictPlugin()

source_lang_model = LanguageModel()
dest_lang_model = LanguageModel()

word_engine_name = setting_config.get_translate_config("word_engine")
words_engine_name = setting_config.get_translate_config("words_engine")

translate_simple = imp.load_source("translate_simple", dict_plugin.get_plugin_file(word_engine_name)).Translate()
translate_long = imp.load_source("translate_long", dict_plugin.get_plugin_file(words_engine_name)).Translate()

word_translate_model = dict_plugin.get_word_model(setting_config.get_translate_config("src_lang"), setting_config.get_translate_config("dst_lang"))
words_translate_model = dict_plugin.get_words_model(setting_config.get_translate_config("src_lang"), setting_config.get_translate_config("dst_lang"))

class DictInterface(QObject):
    
    def __init__(self):
        QObject.__init__(self)

    @pyqtSlot(str)
    def update_translate_engine(self, option_type):
        global word_translate_model
        global words_translate_model
        
        word_engines = dict_plugin.get_word_engines(setting_config.get_translate_config("src_lang"), setting_config.get_translate_config("dst_lang"))
        words_engines = dict_plugin.get_words_engines(setting_config.get_translate_config("src_lang"), setting_config.get_translate_config("dst_lang"))
        
        word_engine_names = map(lambda (name, display_name): name, word_engines)
        words_engine_names = map(lambda (name, display_name): name, words_engines)
        
        current_word_engine = setting_config.get_translate_config("word_engine")
        current_words_engine = setting_config.get_translate_config("words_engine")
        
        word_translate_model.setAll(word_engines)    
        words_translate_model.setAll(words_engines)    
        
        if current_word_engine not in word_engine_names:
            setting_config.update_translate_config("word_engine", word_engine_names[0])
            self.update_word_module()
            
        if current_words_engine not in words_engine_names:
            setting_config.update_translate_config("words_engine", words_engine_names[0])
            self.update_words_module()
            
    @pyqtSlot()
    def update_word_module(self):
        global translate_simple
        change_engine(translate_simple, "translate_simple", "word_engine")
    
    @pyqtSlot()   
    def update_words_module(self):
        global translate_long
        change_engine(translate_long, "translate_long", "words_engine")
        
def change_engine(engine_module, module_name, engine_name):
    # We need hide view before change engine.
    engine_module.hide_translate()
    engine_module = imp.load_source(module_name, dict_plugin.get_plugin_file(setting_config.get_translate_config(engine_name))).Translate()
    
dict_interface = DictInterface()
