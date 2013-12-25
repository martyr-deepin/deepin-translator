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

from PyQt5.QtWidgets import qApp, QSystemTrayIcon
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5.QtGui import QIcon
from deepin_menu.menu import Menu, MenuSeparator, CheckboxMenuItem
from config import setting_config
from xutils import delete_selection, screen_height
from nls import _
from constant import LANGUAGES
from setting_view import setting_view
import os
from deepin_utils.file import get_parent_dir
from deepin_utils.core import is_true
from constant import QT_VERSION

class SystemTrayIcon(QSystemTrayIcon):
    
    showSettingView = pyqtSignal()
    
    def __init__(self, parent=None):
        QSystemTrayIcon.__init__(self, self.get_trayicon(), parent)
        self.activated.connect(self.on_activated) 
        
        self.menu_is_visible = False
        
    def set_trayicon(self):
        self.setIcon(self.get_trayicon())
        
    def get_trayicon(self):
        if is_true(setting_config.get_trayicon_config("pause")):
            icon_name = "pause_trayicon.png"
        else:
            icon_name = "trayicon.png"
            
        return QIcon(os.path.join(get_parent_dir(__file__), "image", icon_name))
    
    @pyqtSlot(str, bool)
    def click_menu(self, menu_id, state):
        if menu_id == "quit":
            qApp.quit()
        elif menu_id == "wizard":
            pass
        elif menu_id == "about":
            pass
        elif menu_id == "settings":
            self.showSettingView.emit()
        elif menu_id == "lang":
            src_lang = setting_config.get_translate_config("src_lang")
            dst_lang = setting_config.get_translate_config("dst_lang")
            setting_config.update_translate_config("src_lang", dst_lang)
            setting_config.update_translate_config("dst_lang", src_lang)
            
            self.menu.setItemText("lang", self.get_lang_value())
            
            setting_view.updateLang.emit()
        else:
            if menu_id == "pause":
                if not state:
                    delete_selection()
                
                self.set_menu_active(state)    
                
            setting_config.update_trayicon_config(menu_id, state)
            
            self.set_trayicon()
            
    def set_menu_active(self, state):
        self.menu.setItemActivity("toggle_speech", not state)
        self.menu.setItemActivity("key_trigger_select", not state)
        self.menu.setItemActivity("local_translate", not state)
        
    def get_lang_value(self):
        return (dict(LANGUAGES))[setting_config.get_translate_config("src_lang")] + " <=> " + (dict(LANGUAGES))[setting_config.get_translate_config("dst_lang")]
        
    def on_activated(self, reason):
        if not self.menu_is_visible:
            if reason in [QSystemTrayIcon.Context, QSystemTrayIcon.Trigger]:
                geometry = self.geometry()
                if QT_VERSION == "5.1":
                    mouse_x = int(geometry.x() / 2 + geometry.width() / 2)
                    mouse_y = int(geometry.y() / 2)
                else:
                    mouse_x = int(geometry.x() + geometry.width() / 2)
                    mouse_y = int(geometry.y())
                
                self.menu = Menu([
                        CheckboxMenuItem("pause", _("Pause translation popups"), 
                                         setting_config.get_trayicon_config("pause")),
                        CheckboxMenuItem("toggle_speech", _("Pronounce automatically"), 
                                         setting_config.get_trayicon_config("toggle_speech")),
                        CheckboxMenuItem("key_trigger_select", _("Only pop up while holding Ctrl key"), 
                                         setting_config.get_trayicon_config("key_trigger_select")),
                        CheckboxMenuItem("local_translate", _("Offline translation"),
                                         setting_config.get_trayicon_config("local_translate")),
                        MenuSeparator(),
                        CheckboxMenuItem("lang", self.get_lang_value(), showCheckmark=False),
                        MenuSeparator(),
                        ("settings", _("Settings")),
                        ("wizard", _("Wizard")),
                        MenuSeparator(),
                        ("quit", _("Exit")),
                        ])
                
                self.menu.itemClicked.connect(self.click_menu)
                self.menu.menuDismissed.connect(self.exit_menu)
                self.set_menu_active(setting_config.get_trayicon_config("pause"))
                if mouse_y > screen_height / 2:
                    self.menu.showDockMenu(mouse_x, mouse_y, cornerDirection="down")
                else:
                    self.menu.showDockMenu(mouse_x, mouse_y + geometry.height(), cornerDirection="up")
            
        self.menu_is_visible = not self.menu_is_visible
        
    @pyqtSlot()    
    def exit_menu(self):
        self.menu_is_visible = False
                    
    def get_trayarea(self):
        geometry = self.geometry()
        return (geometry.y() / 2, geometry.y() / 2 + geometry.height())
