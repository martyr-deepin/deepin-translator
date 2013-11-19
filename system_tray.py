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
from xutils import get_pointer_coordiante
from deepin_menu.menu import Menu

class SystemTrayIcon(QSystemTrayIcon):
    
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.activated.connect(self.on_activated) 
        
    @pyqtSlot(str)
    def click_menu(self, menu_id):
        print menu_id
        if menu_id:
            qApp.quit()
        
    def on_activated(self, reason):
        if reason == QSystemTrayIcon.Context:
            (mouse_x, mouse_y) = get_pointer_coordiante()
            menu = Menu([
                    ("about", "关于"),
                    ("src_lang", "原始语言"),
                    ("dst_lang", "目标语言"),
                    ("quit", "退出"),
                    ])
            menu.itemClicked.connect(self.click_menu)
            menu.showDockmenu(mouse_x - 67, mouse_y - 140)
