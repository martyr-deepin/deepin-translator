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
import requests
from utils import encode_params
from translate_interface import TranslateInterface
from xmltodict import parse as xml_parse
from models import suggestModel
from auto_object import AutoQObject
from ocr import ocr_word
from xutils import get_pointer_coordiante
from pyquery import PyQuery

class TranslateSimple(TranslateInterface):
    
    def __init__(self):
        TranslateInterface.__init__(self, "TranslateSimple.qml")
        
    def get_voice(self, text, lang):
        url = "http://dict.youdao.com/dictvoice"
        data = { "keyfrom" : "deskdict.mini.word", "audio" : text, "client" : "deskdict", "id" : "cee84504d9984f1b2", "vendor": "unknown", 
                 "in" : "YoudaoDict", "appVer" : "5.4.46.5554", "appZengqiang" : 0, "type" : lang}
        return "%s?%s" % (url, encode_params(data))
    
    def translate_cursor_word(self):
        (mouse_x, mouse_y) = get_pointer_coordiante()
        ocr_info = ocr_word(mouse_x, mouse_y)
        if ocr_info:
            self.show_translate(*ocr_info)
    
    def init_translate_info(self):
        TranslateInfo = AutoQObject(
            ("keyword", str),
            ("ukphone", str),
            ("usphone", str),
            ("uklink", str),
            ("uslink", str),
            ("webtrans", str),                         
            ("trans", str),
            ("weba", str),
            name="TranslateInfo")
        self.translate_info = TranslateInfo()
        
        self.qml_context.setContextProperty("suggestModel", suggestModel)
        
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
        self.translate_info.ukphone = None
        self.translate_info.usphone = None
        self.translate_info.trans = None
        self.translate_info.uslink = None
        self.translate_info.uklink = None
        
        self.translate_info.trans = '<br>'.join([PyQuery(e).text() for e in pq('trs i')])
        
        # ukphone
        try: self.translate_info.ukphone = pq.find('ukphone').text()
        except: pass    
        else: self.translate_info.uklink = self.get_voice(text, 1)            
            
        # usphone
        try: self.translate_info.usphone = pq.find('usphone').text()
        except: pass    
        else: self.translate_info.uslink = self.get_voice(text, 2)
        
        # web translations
        self.translate_info.webtrans = "web. " + "; ".join([ PyQuery(e).text() for e in pq.find('web-translation:first')('trans value')])
        
