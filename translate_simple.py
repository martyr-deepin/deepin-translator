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

from __future__ import unicode_literals
from translate_interface import TranslateInterface
from netlib import public_curl, urlencode
from xmltodict import parse as xml_parse
from auto_object import AutoQObject
from ocr import ocr_word
from xutils import get_pointer_coordiante

class TranslateSimple(TranslateInterface):
    
    def __init__(self):
        TranslateInterface.__init__(self, "TranslateSimple.qml")
        
    def get_voice(self, text, lang):
        url = "http://dict.youdao.com/dictvoice"
        data = { "keyfrom" : "deskdict.mini.word", "audio" : text, "client" : "deskdict", "id" : "cee84504d9984f1b2", "vendor": "unknown", 
                 "in" : "YoudaoDict", "appVer" : "5.4.46.5554", "appZengqiang" : 0, "type" : lang}
        return "%s?%s" % (url, urlencode(data))
    
    def get_suggest(self, text):
        data = { "type" : "DESKDICT", "num" : 10, "ver" : 2.0, "le": "eng", "q" : text }
        ret = public_curl.request("http://dict.youdao.com/suggest", data)
        doc =  xml_parse(ret)
        try:
            return doc['suggest']['items']['item']
        except:
            return None
        
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
        
    def get_translate(self, text):
        if not text:
            return
        
        if isinstance(text, unicode):
            text = text.encode("utf-8")
    
        data = { "keyfrom" : "deskdict.mini", "q" : text, "doctype" : "xml", "xmlVersion" : 8.2,
                 "client" : "deskdict", "id" : "cee84504d9984f1b2", "vendor": "unknown", 
                 "in" : "YoudaoDict", "appVer" : "5.4.46.5554", "appZengqiang" : 0, "le" : "eng", "LTH" : 40}
        ret = public_curl.request("http://dict.youdao.com/search", data)
        ret = xml_parse(ret)
        
        yodaodict = ret['yodaodict']
        
        self.translate_info.keyword = text    
        self.translate_info.ukphone = None
        self.translate_info.usphone = None
        self.translate_info.trans = None
        self.translate_info.uslink = None
        self.translate_info.uklink = None
            
        try:
            word = yodaodict['basic']['simple-dict']['word']
        except Exception: 
            pass
        else:    
            ukphone = word.get("ukphone", None)
            if ukphone:
                self.translate_info.ukphone = ukphone
                self.translate_info.uklink = self.get_voice(text, 1)
                
            usphone = word.get("usphone", None)
            if usphone:
                self.translate_info.usphone = usphone
                self.translate_info.uslink = self.get_voice(text, 2)
                
            trs = word["trs"]["tr"]
            if isinstance(trs, list):
                ret = "<br>".join(item['l']['i'] for item in trs)
            else:    
                ret = trs['l']['i']
            self.translate_info.trans = ret            
        
        try:
            ret = yodaodict['yodao-web-dict']['web-translation']
        except:    
            return
        
        if isinstance(ret, list):
            ret = ret[0]
        
        trans = ret['trans']
        if isinstance(trans, list):
            web_trans = "|".join(item["value"] for item in trans)
        else:    
            web_trans = trans['value']
        self.translate_info.webtrans = web_trans
