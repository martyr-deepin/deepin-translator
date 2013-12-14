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

import os
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
if os.name == 'posix':
    QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads, True)
    
from PyQt5.QtCore import pyqtSlot, QObject
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication
from event import RecordEvent
from system_tray import SystemTrayIcon
from unique_service import UniqueService
import signal
import sys  
import threading
from config import setting_config
from window import Window
from xutils import screen_width, screen_height
from model import LanguageModel
from plugin import Plugin
import imp
from deepin_utils.file import get_parent_dir
import constant
    
APP_DBUS_NAME = "com.deepin.ocr"    
APP_OBJECT_NAME = "/com/deepin/ocr"

def change_engine(engine_module, module_name, engine_name):
    # We need hide view before change engine.
    engine_module.hide_translate()
    engine_module = imp.load_source(module_name, plugin.get_plugin_file(setting_config.get_translate_config(engine_name))).Translate()

class TranslateInfo(QObject):

    @pyqtSlot()
    def update_translate_engine(self):
        global translate_simple
        global translate_long
        global word_translate_model
        global words_translate_model
        
        word_engines = plugin.get_word_engines(setting_config.get_translate_config("src_lang"), setting_config.get_translate_config("dst_lang"))
        words_engines = plugin.get_words_engines(setting_config.get_translate_config("src_lang"), setting_config.get_translate_config("dst_lang"))
        word_engine_names = map(lambda (name, display_name): name, word_engines)
        words_engine_names = map(lambda (name, display_name): name, words_engines)
        
        current_word_engine = setting_config.get_translate_config("word_engine")
        current_words_engine = setting_config.get_translate_config("words_engine")
        
        word_translate_model.setAll(word_engines)    
        words_translate_model.setAll(words_engines)    
        
        if current_word_engine not in word_engine_names:
            setting_config.update_translate_config("word_engine", word_engine_names[0])
            change_engine(translate_simple, "translate_simple", "word_engine")
            
        if current_words_engine not in words_engine_names:
            setting_config.update_translate_config("words_engine", words_engine_names[0])
            change_engine(translate_long, "translate_long", "words_engine")
            
    @pyqtSlot()
    def update_word_module(self):
        global translate_simple
        change_engine(translate_simple, "translate_simple", "word_engine")

    @pyqtSlot()   
    def update_words_module(self):
        global translate_long
        change_engine(translate_long, "translate_long", "words_engine")
    
if __name__ == "__main__":
    uniqueService = UniqueService(APP_DBUS_NAME, APP_OBJECT_NAME)

    app = QApplication(sys.argv)  
    tray_icon = SystemTrayIcon(QIcon(os.path.join(get_parent_dir(__file__), "image", "trayicon.png")), app)
    tray_icon.show()
    (constant.TRAYAREA_TOP, constant.TRAYAREA_BOTTOM) = tray_icon.get_trayarea()
    
    plugin = Plugin()
    
    source_lang_model = LanguageModel()
    dest_lang_model = LanguageModel()

    word_engine_name = setting_config.get_translate_config("word_engine")
    words_engine_name = setting_config.get_translate_config("words_engine")
    translate_simple = imp.load_source("translate_simple", plugin.get_plugin_file(word_engine_name)).Translate()
    translate_long = imp.load_source("translate_long", plugin.get_plugin_file(words_engine_name)).Translate()
    word_translate_model = plugin.get_word_model(setting_config.get_translate_config("src_lang"), setting_config.get_translate_config("dst_lang"))
    words_translate_model = plugin.get_words_model(setting_config.get_translate_config("src_lang"), setting_config.get_translate_config("dst_lang"))
    
    translate_info = TranslateInfo()
    
    setting_view = Window()
    setting_view.qml_context.setContextProperty("sourceLangModel", source_lang_model)
    setting_view.qml_context.setContextProperty("destLangModel", dest_lang_model)
    setting_view.qml_context.setContextProperty("plugin", plugin)
    setting_view.qml_context.setContextProperty("wordTranslateModel", word_translate_model)
    setting_view.qml_context.setContextProperty("wordsTranslateModel", words_translate_model)
    setting_view.qml_context.setContextProperty("screenWidth", screen_width)
    setting_view.qml_context.setContextProperty("screenHeight", screen_height)
    setting_view.qml_context.setContextProperty("windowView", setting_view)
    setting_view.qml_context.setContextProperty("settingConfig", setting_config)
    setting_view.qml_context.setContextProperty("translateInfo", translate_info)
    setting_view.setSource(QtCore.QUrl.fromLocalFile(os.path.join(get_parent_dir(__file__), 'SettingView.qml')))
    
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    rootObject = translate_simple.rootObject()
    
    def show_translate(x, y, text):
        if len(filter(lambda word: word != "", (text.split(" ")))) > 1:
            translate_long.show_translate(x, y, text)
        else:
            translate_simple.show_translate(x, y, text)
            
    def hide_translate():
        if translate_simple.isVisible() and not translate_simple.in_translate_area():
            translate_simple.hide_translate()

        if translate_long.isVisible() and not translate_long.in_translate_area():
            translate_long.hide_translate()
            
    def handle_press_alt():
        translate_simple.translate_cursor_word()
            
    record_event = RecordEvent(translate_simple)
    record_event.press_esc.connect(hide_translate)
    record_event.press_alt.connect(handle_press_alt)
    record_event.wheel_press.connect(hide_translate)
    record_event.left_button_press.connect(hide_translate)
    record_event.right_button_press.connect(hide_translate)
    record_event.translate_selection.connect(show_translate)
    
    tray_icon.showSettingView.connect(setting_view.showNormal)
    
    thread = threading.Thread(target=record_event.filter_event)
    thread.setDaemon(True)
    thread.start()

    sys.exit(app.exec_())
