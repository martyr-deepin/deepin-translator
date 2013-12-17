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

import os
from PyQt5 import QtCore
from PyQt5.QtCore import QCoreApplication
if os.name == 'posix':
    QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads, True)
    
from PyQt5.QtWidgets import QApplication
from unique_service import UniqueService
import signal
import sys  
import constant
    
APP_DBUS_NAME = "com.deepin.ocr"    
APP_OBJECT_NAME = "/com/deepin/ocr"

if __name__ == "__main__":
    uniqueService = UniqueService(APP_DBUS_NAME, APP_OBJECT_NAME)

    app = QApplication(sys.argv)  
    
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    from dict_interface import get_translate_simple, get_translate_long
    
    def show_translate(x, y, text):
        if len(filter(lambda word: word != "", (text.split(" ")))) > 1:
            translate_long = get_translate_long()
            if translate_long:
                translate_long.show_translate(x, y, text)
        else:
            translate_simple = get_translate_simple()
            if translate_simple:
                translate_simple.show_translate(x, y, text)
            
    def hide_translate():
        translate_simple = get_translate_simple()
        if translate_simple:
            if translate_simple.isVisible() and not translate_simple.in_translate_area():
                translate_simple.hide_translate()

        translate_long = get_translate_long()
        if translate_long:
            if translate_long.isVisible() and not translate_long.in_translate_area():
                translate_long.hide_translate()
            
    def handle_press_alt():
        translate_simple = get_translate_simple()
        if translate_simple:
            translate_simple.translate_cursor_word()
            
    def translate_cursor_word():
        translate_simple = get_translate_simple()
        if translate_simple:
            translate_simple.translate_cursor_word()
            
    from record_event import RecordEvent
    from event_handler import EventHandler
    
    event_handler = EventHandler()
    event_handler.press_esc.connect(hide_translate)
    event_handler.press_alt.connect(handle_press_alt)
    event_handler.wheel_press.connect(hide_translate)
    event_handler.left_button_press.connect(hide_translate)
    event_handler.right_button_press.connect(hide_translate)
    event_handler.translate_selection.connect(show_translate)
    event_handler.cursor_stop.connect(translate_cursor_word)
    
    from setting_view import setting_view
    from system_tray import SystemTrayIcon
    tray_icon = SystemTrayIcon(app)
    tray_icon.show()
    (constant.TRAYAREA_TOP, constant.TRAYAREA_BOTTOM) = tray_icon.get_trayarea()
    tray_icon.showSettingView.connect(setting_view.showNormal)
    
    record_event = RecordEvent()
    record_event.capture_event.connect(event_handler.handle_event)
    record_event.start()

    sys.exit(app.exec_())
