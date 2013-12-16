#! /usr/bin/env python
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
import imp
from tts_plugin import TtsPlugin
from config import setting_config
from deepin_utils.net import is_network_connected

tts_plugin = TtsPlugin()
voice_simple = imp.load_source("voice_simple", tts_plugin.get_plugin_file(setting_config.get_translate_config("word_voice_engine")))
voice_long = imp.load_source("voice_long", tts_plugin.get_plugin_file(setting_config.get_translate_config("words_voice_engine")))
word_voice_model = tts_plugin.get_voice_model(setting_config.get_translate_config("src_lang"))
words_voice_model = tts_plugin.get_voice_model(setting_config.get_translate_config("src_lang"))

def get_voice(text, voice):
    if is_network_connected():
        return voice.get_voice(text)
    else:
        voice_engines = tts_plugin.get_voice_engines(setting_config.get_translate_config("src_lang"), False)
        voice_engine_names = map(lambda (name, display_name): name, voice_engines)
        if len(voice_engine_names) > 0:
            local_simple = imp.load_source("local_simple", tts_plugin.get_plugin_file(voice_engine_names[0]))
            return local_simple.get_voice(text)
        else:
            return []
        
def get_voice_simple(text):
    global voice_simple
    return get_voice(text, voice_simple)

def get_voice_long(text):
    global voice_long
    return get_voice(text, voice_long)
    
class TtsInterface(QObject):
    
    def __init__(self):
        QObject.__init__(self)

    @pyqtSlot()    
    def update_word_voice_module(self):
        global voice_simple
        voice_simple = imp.load_source("voice_simple", tts_plugin.get_plugin_file(setting_config.get_translate_config("word_voice_engine")))
    
    @pyqtSlot()    
    def update_words_voice_module(self):
        global voice_long
        voice_long = imp.load_source("voice_long", tts_plugin.get_plugin_file(setting_config.get_translate_config("words_voice_engine")))
            
    @pyqtSlot()    
    def update_voice_with_src_lang(self):
        voice_engines = tts_plugin.get_voice_engines(setting_config.get_translate_config("src_lang"))
        voice_engine_names = map(lambda (name, display_name): name, voice_engines)
        word_voice_model.setAll(voice_engines)
        words_voice_model.setAll(voice_engines)
        current_word_voice_engine = setting_config.get_translate_config("word_voice_engine")
        current_words_voice_engine = setting_config.get_translate_config("words_voice_engine")
            
        if current_word_voice_engine not in voice_engine_names:
            setting_config.update_translate_config("word_voice_engine", voice_engine_names[0])
            self.update_word_voice_module()
        
        if current_words_voice_engine not in voice_engine_names:
            setting_config.update_translate_config("words_voice_engine", voice_engine_names[0])
            self.update_words_voice_module()

tts_interface = TtsInterface()
