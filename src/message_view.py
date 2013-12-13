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

from window import Window
from xutils import screen_width, screen_height
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
import os
from deepin_utils.file import get_parent_dir

class MessageView(Window):

    def __init__(self):
        Window.__init__(self)
        self.qml_context.setContextProperty("screenWidth", screen_width)
        self.qml_context.setContextProperty("screenHeight", screen_height)
        self.qml_context.setContextProperty("windowView", self)
        self.setSource(QtCore.QUrl.fromLocalFile(os.path.join(get_parent_dir(__file__), 'MessageBox.qml')))
        
    def set_action(self, action):
        self.action = action
        
    @pyqtSlot()    
    def execute_action(self):
        self.action()

message_view = None

def show_message(message, cancel, confirm, action):
    global message_view
    
    if message_view == None:
        message_view = MessageView()
        
    message_view.set_action(action)
    message_view.rootObject().showMessage(message, cancel, confirm)
