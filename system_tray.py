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

from PyQt5.QtWidgets import qApp, QSystemTrayIcon
from PyQt5.QtCore import pyqtSlot
from deepin_menu.menu import Menu

class SystemTrayIcon(QSystemTrayIcon):
    
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.activated.connect(self.on_activated) 
        
    @pyqtSlot(str)
    def click_menu(self, menu_id):
        if menu_id == "quit":
            qApp.quit()
        
    def on_activated(self, reason):
        if reason == QSystemTrayIcon.Context:
            geometry = self.geometry()
            mouse_x = int(geometry.x() / 2 + geometry.width() / 2)
            mouse_y = int(geometry.y() / 2)
            self.menu = Menu([
                    ("toggle_word", "暂停取词"),
                    ("toggle_speecn", "取词后发音"),
                    None,
                    ("key_trigger_ocr", "按Ctrl键屏幕取词"),
                    ("key_trigger_select", "按Alt键翻译选区"),
                    None,
                    ("select_translate_engine", "选择翻译引擎"),
                    None,
                    ("about", "关于"),
                    ("quit", "退出"),
                    ])
            self.menu.itemClicked.connect(self.click_menu)
            self.menu.showDockMenu(mouse_x, mouse_y)
