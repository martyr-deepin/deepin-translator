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

from PyQt5.QtGui import QIcon
from PyQt5.QtQuick import QQuickItem
from PyQt5.QtWidgets import QApplication
from event import RecordEvent
from system_tray import SystemTrayIcon
from translate_long import TranslateLong
from translate_simple import TranslateSimple
from unique_service import UniqueService
import signal
import sys  
import threading
    
APP_DBUS_NAME = "com.deepin.ocr"    
APP_OBJECT_NAME = "/com/deepin/ocr"

if __name__ == "__main__":
    uniqueService = UniqueService(APP_DBUS_NAME, APP_OBJECT_NAME)

    app = QApplication(sys.argv)  
    trayIcon = SystemTrayIcon(QIcon("image/icon.png"), app)
    trayIcon.show()
    
    translate_simple = TranslateSimple()
    translate_long = TranslateLong()
    
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    rootObject = translate_simple.rootObject()
    
    def show_translate(x, y, text):
        if len(filter(lambda word: word != "", (text.split(" ")))) > 1:
            translate_long.show_translate(x, y, text)
        else:
            translate_simple.show_translate(x, y, text)
            
    def hide_translate():
        if not translate_simple.in_translate_area():
            translate_simple.hide_translate()

        if not translate_long.in_translate_area():
            translate_long.hide_translate()
        
    record_event = RecordEvent(translate_simple)
    record_event.press_ctrl.connect(translate_simple.translate_cursor_word)
    record_event.wheel_press.connect(hide_translate)
    record_event.left_button_press.connect(hide_translate)
    record_event.right_button_press.connect(hide_translate)
    record_event.cursor_stop.connect(translate_simple.show_translate)
    record_event.translate_selection.connect(show_translate)
    
    thread = threading.Thread(target=record_event.filter_event)
    thread.setDaemon(True)
    thread.start()

    sys.exit(app.exec_())
