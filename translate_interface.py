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

from PyQt5 import QtCore, QtQuick
from PyQt5.QtGui import QSurfaceFormat, QColor
from PyQt5.QtQuick import QQuickView
from PyQt5.QtWidgets import qApp
from xutils import get_pointer_coordiante
import os

class TranslateInterface(QQuickView):
    
    def __init__(self, qml_file):
        QQuickView.__init__(self)
        
        self.window_offset_x = -50
        self.window_offset_y = 5

        surface_format = QSurfaceFormat()
        surface_format.setAlphaBufferSize(8)
        
        self.setColor(QColor(0, 0, 0, 0))
        self.setFlags(QtCore.Qt.Popup)
        self.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)
        self.setFormat(surface_format)
        
        self.qml_context = self.rootContext()
        self.init_translate_info()
        self.qml_context.setContextProperty("translateInfo", self.translate_info)
        self.qml_context.setContextProperty("windowView", self)
        self.qml_context.setContextProperty("qApp", qApp)
        
        self.setSource(QtCore.QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), qml_file)))
        
    def init_translate_info(self):
        print "NOTE: Your should implement this function to init translate information!"
        
    def get_translate(self, text):
        print "NOTE: Your should implement this function to update translate information!"
        
    def hide_translate(self):
        if not self.in_translate_area():
            self.hide()
    
    def in_translate_area(self):
        (mouse_x, mouse_y) = get_pointer_coordiante()
        return self.x() < mouse_x < self.x() + self.width() and self.y() < mouse_y < self.y() + self.height()

    def show_translate(self, x, y, text):
        self.setX(x + self.window_offset_x)
        self.setY(y + self.window_offset_y)
        self.showNormal()
        self.get_translate(text)
        self.rootObject().showTranslate()
    
