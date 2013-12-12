#! /usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Hou Shaohui, Wang Yong
# 
# Author:     Hou Shaohui <houshao55@gmail.com>
# Maintainer: Hou Shaohui <houshao55@gmail.com>
#             Wang Yong <lazycat.manatee@gmail.com>
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
from auto_object import AutoQObject
from translate_interface import TranslateInterface
from xutils import get_pointer_coordiante
from ocr import ocr_word
import os
import commands

class Translate(TranslateInterface):
    
    def __init__(self):
        TranslateInterface.__init__(self, os.path.join(os.path.dirname(__file__), "Translate.qml"))

    def init_translate_info(self):
        TranslateInfo = AutoQObject(
            ("translate", str),
            ("fixed", str),
          name="TranslateInfo")
        self.translate_info = TranslateInfo()        
        
    def google_translate(self, text):
        return '\n'.join(commands.getoutput("sdcv %s" % text).split("\n")[1::])
    
    def translate_cursor_word(self):
        (mouse_x, mouse_y) = get_pointer_coordiante()
        ocrword = ocr_word(mouse_x, mouse_y)
        if ocrword:
            self.show_translate(mouse_x, mouse_y, ocrword)
    
    @pyqtSlot(str)
    def get_translate(self, text):
        self.translate_info.translate = self.google_translate(text)
