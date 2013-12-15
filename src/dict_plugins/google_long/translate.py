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
from auto_object import AutoQObject
from translate_window import TranslateWindow
import requests
from config import setting_config
import os
from deepin_utils.file import get_parent_dir
from utils import safe_eval
from tts_interface import get_voice_long

class Translate(TranslateWindow):
    
    def __init__(self):
        TranslateWindow.__init__(self, os.path.join(get_parent_dir(__file__), "Translate.qml"))
        

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
            return safe_eval(dlist)
        except SyntaxError:
            return []
     
    def get_sample_result(self, glist):
        '''
        翻译详细: a[5]
        
        原始字符:      a[5][<i>][0]
        句子ID:       a[5][<i>][1]
        可选翻译:      a[5][<i>][2] | 判断长度， 取每一列表的[0], 取出翻译后字符: a[5][<i>][2][0][0]
        字符位置(pos): a[5][<i>][3] | 取出[0], 并判断是否为None     
    
        In [104]: print a[4][1]
        ['reparents', [5], 1, 0, 1000, 1, 2, 0]
    
        In [105]: print a[5][1]
        ['reparents', 5, [['reparents', 1000, 1, 0]], [[13, 22]], '']    
    
        '''    
        try:
            return  ''.join([dl[0] for dl in glist[0]])
        except:
            return "翻译失败"
    
    def google_translate(self, text, sl="auto", tl="zh-CN", encoding="UTF-8"):
        target_language = tl
        source_language = sl
        input_encoding = output_encoding = encoding
        data = dict(client="t",
                    hl=tl,
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
        result = self.get_sample_result(plist)
        return result.decode(encoding)
        
    @pyqtSlot(str)
    def get_translate(self, text):
        self.translate_info.voices = get_voice_long(text)
        self.translate_info.translate = self.google_translate(
            text,
            tl=setting_config.get_translate_config("dst_lang"),
            )
