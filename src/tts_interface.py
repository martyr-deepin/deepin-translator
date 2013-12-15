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

import os
import imp
from deepin_utils.file import get_parent_dir
from tts_plugin import TtsPlugin
from config import setting_config

tts_plugin = TtsPlugin()
word_voice_engine_name = setting_config.get_translate_config("word_voice_engine")
words_voice_engine_name = setting_config.get_translate_config("words_voice_engine")
voice_simple = imp.load_source("voice_simple", tts_plugin.get_plugin_file(word_voice_engine_name)).get_voice
voice_long = imp.load_source("voice_long", tts_plugin.get_plugin_file(words_voice_engine_name)).get_voice
word_voice_model = tts_plugin.get_voice_model(setting_config.get_translate_config("src_lang"))
words_voice_model = tts_plugin.get_voice_model(setting_config.get_translate_config("src_lang"))
    
def get_tts_interface(tts_name):
    path = os.path.join(get_parent_dir(__file__), "tts_plugins", tts_name, "tts.py")
    voice_plugin = imp.load_source("voice_plugin", path)
    return voice_plugin.get_voice

def update_word_voice_module():
    global voice_simple
    voice_simple = imp.load_source("voice_simple", tts_plugin.get_plugin_file(word_voice_engine_name)).get_voice

def update_words_voice_module():
    global voice_long
    voice_long = imp.load_source("voice_long", tts_plugin.get_plugin_file(words_voice_engine_name)).get_voice
        
def update_voice_with_src_lang():
    voice_engines = tts_plugin.get_voice_engines(setting_config.get_translate_config("src_lang"))
    voice_engine_names = map(lambda (name, display_name): name, voice_engines)
    word_voice_model.setAll(voice_engines)
    words_voice_model.setAll(voice_engines)
    current_word_voice_engine = setting_config.get_translate_config("word_voice_engine")
    current_words_voice_engine = setting_config.get_translate_config("words_voice_engine")
        
    if current_word_voice_engine not in voice_engine_names:
        setting_config.update_translate_config("word_voice_engine", voice_engine_names[0])
        update_word_voice_module()
    
    if current_words_voice_engine not in voice_engine_names:
        setting_config.update_translate_config("words_voice_engine", voice_engine_names[0])
        update_words_voice_module()
