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

from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtQuick, QtWidgets
from PyQt5.QtGui import QSurfaceFormat, QColor
from PyQt5.QtQuick import QQuickView
from PyQt5.QtWidgets import qApp
from xutils import get_pointer_coordiante
from ocr import ocr_word
import os
from config import setting_config
from deepin_utils.file import get_parent_dir
from tts_interface import get_voice_modules

class TranslateWindow(QQuickView):

    hided = QtCore.pyqtSignal()
    
    def __init__(self, qml_file):
        QQuickView.__init__(self)
        
        surface_format = QSurfaceFormat()
        surface_format.setAlphaBufferSize(8)
        
        self.setColor(QColor(0, 0, 0, 0))
        self.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)
        self.setFormat(surface_format)
        
        self.setFlags(QtCore.Qt.Popup)
        
        self.qml_context = self.rootContext()
        
        self.init_translate_info()
        
        self.qml_context.setContextProperty("translateInfo", self.translate_info)
        self.qml_context.setContextProperty("windowView", self)
        self.qml_context.setContextProperty("settingConfig", setting_config)
        self.qml_context.setContextProperty("qApp", qApp)
        
        self.setSource(QtCore.QUrl.fromLocalFile(os.path.join(get_parent_dir(__file__), qml_file)))
        
    def init_translate_info(self):
        print "NOTE: Your should implement function 'init_translate_info' to init translate information!"
        
    @pyqtSlot(str)    
    def get_translate(self, text):
        print "NOTE: Your should implement function 'get_translate' to update translate information!"
        
    def check_before_translate(self):    
        return True
        
    def hide_translate(self):
        if self.isVisible() and not self.in_translate_area():
            self.hided.emit()
            self.hide()
    
    def in_translate_area(self):
        (mouse_x, mouse_y) = get_pointer_coordiante()
        return self.x() < mouse_x < self.x() + self.width() and self.y() < mouse_y < self.y() + self.height()

    def show_translate(self, x, y, text):
        if self.check_before_translate():
            voice_modules = get_voice_modules()
            for voice_module in voice_modules:
                if not voice_module.check_before_voice():
                    return
                
            self.rootObject().showTranslate(x, y, text)

    def translate_cursor_word(self):
        (mouse_x, mouse_y) = get_pointer_coordiante()
        ocrword = ocr_word(mouse_x, mouse_y)
        if ocrword:
            self.show_translate(mouse_x, mouse_y, ocrword)
    
    @pyqtSlot(str)
    def save_to_clipboard(self, text):
        QtWidgets.QApplication.clipboard().setText(text)

    
