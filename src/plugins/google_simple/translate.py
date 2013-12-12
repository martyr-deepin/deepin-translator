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
from utils import encode_params
import requests
from config import setting_config
import os

def group(seq, size): 
    def take(seq, n):
        for i in xrange(n):
            yield seq.next()

    if not hasattr(seq, 'next'):  
        seq = iter(seq)
    while True: 
        x = list(take(seq, size))
        if x:
            yield x
        else:
            break

class Translate(TranslateInterface):
    
    def __init__(self):
        TranslateInterface.__init__(self, os.path.join(os.path.dirname(__file__), "Translate.qml"))
        

    def init_translate_info(self):
        TranslateInfo = AutoQObject(
            ("translate", str),
            ("voices", 'QVariant'),
            ("fixed", str),
          name="TranslateInfo")
        self.translate_info = TranslateInfo()        
        
    def parse_dummy_list(self, dlist):
        while ",," in dlist or "[," in dlist:
            dlist = dlist.replace(",,", ",None,").replace("[,", "[None,")
        try:    
            return eval(dlist)
        except SyntaxError:
            return []
        
    def get_word_translate(self, glist):
        
        def parse_list(word_list):
            try:
                title = word_list[0]
                content = ";".join(word_list[1])
                return "%s: %s" % (title, content)
            except:
                return None
        
        try:
            noun_list = glist[1][0]
        except:    
            noun = None
        else:    
            noun = parse_list(noun_list)
            
        try:    
            verb_list = glist[1][1]
        except:
            verb = None
        else:    
            verb = parse_list(verb_list)
            
        if not noun and not verb:
            return self.get_sample_result(glist)
        
        ret = []
        if noun is not None:
            ret.append(noun)
        if verb is not None:    
            ret.append(verb)
        return "<br/>".join(ret)    
     
    def get_sample_result(self, glist):
        try:
            return  ''.join([dl[0] for dl in glist[0]])
        except:
            return "翻译失败"
    
    def google_translate(self, text, sl="auto", tl="zh-CN", encoding="UTF-8"):
        target_language = tl
        source_language = sl
        input_encoding = output_encoding = encoding
        data = dict(client="t",
                    hl="zh-CN",
                    sl=source_language,
                    tl=target_language,
                    ie=input_encoding,
                    oe=output_encoding,
                    otf=1,
                    ssel=0,
                    pc=1,
                    uptl=target_language,
                    sc=2,
                    q=text)    
        url = "http://translate.google.cn/translate_a/t"
        dummy_list = requests.get(url, params=data).text
        plist = self.parse_dummy_list(dummy_list)
        result = self.get_word_translate(plist)
        return result.decode(encoding)
    
    @classmethod
    def get_google_voices(cls, text, tl="en"):
        if not isinstance(text, unicode):
            text = text.decode("utf-8", "ignore")
            
        results = []    
        contents = group(text, 54)
        for c in contents:
            results.append(cls.google_voice("".join(c), tl=tl))
        return results    
    
    
    @classmethod
    def google_voice(cls, text, tl="en", encoding="UTF-8"):
        url = "http://translate.google.cn/translate_tts"
        text = text.encode("utf-8", "ignore")
        data = dict(ie=encoding,
                    tl=tl,
                    total=1,
                    idx=0,
                    textlen=len(text),
                    prev="input",
                    q=text
                    )
        args = encode_params(data)
        return "%s?%s" % (url, args)
        
    def translate_cursor_word(self):
        (mouse_x, mouse_y) = get_pointer_coordiante()
        ocrword = ocr_word(mouse_x, mouse_y)
        if ocrword:
            self.show_translate(mouse_x, mouse_y, ocrword)
    
    @pyqtSlot(str)
    def get_translate(self, text):
        self.translate_info.voices = self.get_google_voices(
            text,
            tl=setting_config.get_translate_config("src_lang"),
            )
        self.translate_info.translate = self.google_translate(
            text,
            tl=setting_config.get_translate_config("dst_lang"),
            )
