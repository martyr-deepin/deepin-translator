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

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from config import setting_config
from window import Window
import os
from deepin_utils.file import get_parent_dir
from xutils import screen_width, screen_height
    
class SettingView(Window):
    
    updateLang = pyqtSignal()

    def __init__(self):
        Window.__init__(self)
    
        from tts_interface import (word_voice_model, words_voice_model, tts_interface)
        from dict_interface import (source_lang_model, dest_lang_model, 
                                    word_translate_model, words_translate_model,
                                    dict_interface)

        self.qml_context.setContextProperty("dictInterface", dict_interface)
        self.qml_context.setContextProperty("ttsIntreface", tts_interface)
        self.qml_context.setContextProperty("sourceLangModel", source_lang_model)
        self.qml_context.setContextProperty("destLangModel", dest_lang_model)
        self.qml_context.setContextProperty("wordTranslateModel", word_translate_model)
        self.qml_context.setContextProperty("wordsTranslateModel", words_translate_model)
        self.qml_context.setContextProperty("wordVoiceModel", word_voice_model)
        self.qml_context.setContextProperty("wordsVoiceModel", words_voice_model)
        self.qml_context.setContextProperty("screenWidth", screen_width)
        self.qml_context.setContextProperty("screenHeight", screen_height)
        self.qml_context.setContextProperty("windowView", self)
        self.qml_context.setContextProperty("settingConfig", setting_config)
        self.setSource(QtCore.QUrl.fromLocalFile(os.path.join(get_parent_dir(__file__), 'SettingView.qml')))

setting_view = SettingView()
