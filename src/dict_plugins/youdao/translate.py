#! /usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2013 Deepin, Inc.
#               2011 ~ 2013 Hou Shaohui, Wang Yong
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
import requests
from translate_window import TranslateWindow
from auto_object import AutoQObject
from models import suggestModel, historyModel
from pyquery import PyQuery
import os
from deepin_utils.file import get_parent_dir
from tts_interface import get_voice_simple, get_phonetic_symbol

class Translate(TranslateWindow):
    
    def __init__(self):
        TranslateWindow.__init__(self, os.path.join(get_parent_dir(__file__), "Translate.qml"))
        
    def init_translate_info(self):
        TranslateInfo = AutoQObject(
            ("keyword", str),
            ("phonetic", str),
            ("voices", 'QVariant'),
            ("webtrans", str),                         
            ("trans", str),
            ("weba", str),
            name="TranslateInfo")
        self.translate_info = TranslateInfo()
        
        self.qml_context.setContextProperty("suggestModel", suggestModel)
        self.qml_context.setContextProperty("historyModel", historyModel)
        
    def wrap_web_trans(self, pq):
        tran_lines = [PyQuery(e).text() for e in pq.find('web-translation:first')('trans value')]
        
        result_lines = [""]
        for tran_line in tran_lines:
            current_line = result_lines[-1]
            if len(current_line) + len(tran_line) > 30:
                result_lines.append(tran_line)
            else:
                result_lines[-1] += tran_line + "; "
                
        for (index, result_line) in enumerate(result_lines):        
            result_lines[index] = "w. " + result_lines[index]
                
        return '\n'.join(result_lines)        
    
    @pyqtSlot(str)    
    def get_translate(self, text):
        if not text:
            return
        
        if isinstance(text, unicode):
            text = text.encode("utf-8")
    
        data = { "keyfrom" : "deskdict.mini", "q" : text, "doctype" : "xml", "xmlVersion" : 8.2,
                 "client" : "deskdict", "id" : "cee84504d9984f1b2", "vendor": "unknown", 
                 "in" : "YoudaoDict", "appVer" : "5.4.46.5554", "appZengqiang" : 0, "le" : "eng", "LTH" : 40}
        
        ret = requests.get("http://dict.youdao.com/search", params=data).text
        if isinstance(ret, unicode):
            ret = ret.encode('utf-8')
            
        pq = PyQuery(ret, parser="xml")
        self.translate_info.keyword = text    
        self.translate_info.trans = None
        self.translate_info.voices = None
        
        self.translate_info.trans = '\n'.join([PyQuery(e).text() for e in pq('trs i')])
        self.translate_info.voices = get_voice_simple(text)
        self.translate_info.phonetic = get_phonetic_symbol(text)
        self.translate_info.webtrans = self.wrap_web_trans(pq)
        
