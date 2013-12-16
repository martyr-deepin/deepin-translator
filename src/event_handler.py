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

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from Xlib import X
from threading import Timer
from xutils import get_keyname, delete_selection, is_ctrl_key, is_alt_key
import commands
from config import setting_config
from dict_interface import get_translate_simple

class EventHandler(QObject):
    
    press_alt = pyqtSignal()
    release_alt = pyqtSignal()    
    press_ctrl = pyqtSignal()
    release_ctrl = pyqtSignal()
    
    press_esc = pyqtSignal()
    
    cursor_stop = pyqtSignal()

    left_button_press = pyqtSignal(int, int, int)
    right_button_press = pyqtSignal(int, int, int)    
    wheel_press = pyqtSignal()
    
    translate_selection = pyqtSignal(int, int, str)
    
    def __init__(self):
        QObject.__init__(self)

        self.press_alt_flag = False
        self.press_ctrl_flag = False

        self.stop_timer = None
        self.stop_delay = 0.05
        
        self.press_alt_timer = None
        self.press_alt_delay = 0.3

        self.press_ctrl_timer = None
        self.press_ctrl_delay = 0.3
        
        # Delete selection first.
        delete_selection()
        
    def is_view_visible(self):
        view = get_translate_simple()
        if view == None:
            return False
        else:
            return view.isVisible()
        
    def is_cursor_in_view_area(self):
        view = get_translate_simple()
        if view == None:
            return False
        else:
            return view.in_translate_area()
        
    @pyqtSlot("QVariant")    
    def handle_event(self, event):
        print "*****************"
        if event.type == X.KeyPress:
            keyname = get_keyname(event)
            
            if not is_alt_key(keyname):
                self.try_stop_timer(self.press_alt_timer)
            elif not is_ctrl_key(keyname):
                self.try_stop_timer(self.press_ctrl_timer)
        
            if is_alt_key(keyname):
                self.press_alt_flag = True
                
                if not setting_config.get_trayicon_config("pause"):
                    print "Press alt", not self.is_view_visible() or not self.is_cursor_in_view_area()
                    if not self.is_view_visible() or not self.is_cursor_in_view_area():
                        self.press_alt_timer = Timer(self.press_alt_delay, lambda : self.press_alt.emit())
                        self.press_alt_timer.start()
            elif is_ctrl_key(keyname):
                self.press_ctrl_flag = True
                
                if not setting_config.get_trayicon_config("pause"):
                    print "Press ctrl", not self.is_view_visible() or not self.is_cursor_in_view_area()
                    if not self.is_view_visible() or not self.is_cursor_in_view_area():
                        self.press_ctrl_timer = Timer(self.press_ctrl_delay, lambda : self.press_ctrl.emit())
                        self.press_ctrl_timer.start()
            elif keyname in ["Escape"]:
                self.press_esc.emit()
        elif event.type == X.KeyRelease:
            keyname = get_keyname(event)
            if is_alt_key(keyname):
                self.press_alt_flag = False
                self.release_alt.emit()
            elif is_ctrl_key(keyname):
                self.press_ctrl_flag = False
                self.release_ctrl.emit()
        elif event.type == X.ButtonPress:
            if event.detail == 1:
                self.left_button_press.emit(event.root_x, event.root_y, event.time)
            elif event.detail == 3:
                self.right_button_press.emit(event.root_x, event.root_y, event.time)
            elif event.detail == 5:
                self.wheel_press.emit()
        elif event.type == X.ButtonRelease:
            print "Button release", not self.is_view_visible() or not self.is_cursor_in_view_area()
            if not self.is_view_visible() or not self.is_cursor_in_view_area():
                if not setting_config.get_trayicon_config("pause"):
                    if not setting_config.get_trayicon_config("key_trigger_select") or self.press_ctrl_flag:
                        selection_content = commands.getoutput("xsel -p -o")
                        delete_selection()
                        
                        if len(selection_content) > 1 and not selection_content.isspace():
                            self.translate_selection.emit(event.root_x, event.root_y, selection_content)
            # Delete clipboard selection if user selection in visible area to avoid next time to translate those selection content.
            elif self.is_view_visible() and self.is_cursor_in_view_area():
                delete_selection()
        elif event.type == X.MotionNotify:
            self.try_stop_timer(self.stop_timer)
        
            if not setting_config.get_trayicon_config("pause"):
                self.stop_timer = Timer(self.stop_delay, lambda : self.emit_cursor_stop(event.root_x, event.root_y))
                self.stop_timer.start()                    
                    
    def emit_cursor_stop(self, mouse_x, mouse_y):
        if self.press_alt_flag and (not self.is_view_visible() or not self.is_cursor_in_view_area()):
            self.cursor_stop.emit()

    def try_stop_timer(self, timer):
        if timer and timer.is_alive():
            timer.cancel()
