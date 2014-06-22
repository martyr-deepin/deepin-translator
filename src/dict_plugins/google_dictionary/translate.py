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
import os
from deepin_utils.file import get_parent_dir
from tts_interface import get_voice_simple, get_phonetic_symbol
import json
import urllib
import re
            
class Translate(TranslateWindow):
    
    def __init__(self):
        TranslateWindow.__init__(self, os.path.join(get_parent_dir(__file__), "Translate.qml"))
        

    def init_translate_info(self):
        TranslateInfo = AutoQObject(
            ("text", str),
            ("translate", str),
            ("phonetic", str),
            ("voices", 'QVariant'),
            ("fixed", str),
          name="TranslateInfo")
        self.translate_info = TranslateInfo()        
        
    def asciirepl(self, match):
      return '\\u00' + match.group()[2:]
    
    def get_meaning(self, query):
        p = urllib.urlopen('http://www.google.com/dictionary/json?callback=a&q='+query+'&sl=en&tl=en&restrict=pr,de&client=te')
        page = p.read()[2:-10] #As its returned as a function call
        
        #To replace hex characters with ascii characters
        p = re.compile(r'\\x(\w{2})')
        ascii_string = p.sub(self.asciirepl, page)
    
        #Now decoding cleaned json response
        data = json.loads(ascii_string)
    
        all_meanings = dict()
        all_meanings['primaries'] = dict()
    
        if 'primaries' in data:
            #Creating list() for each types: adj, verb, noun
            for bunch in data['primaries']:
                #This list contains meanings and examples
                all_meanings['primaries'][bunch['terms'][0]['labels'][0]['text']] = list()
                means = all_meanings['primaries'][bunch['terms'][0]['labels'][0]['text']]
                
                for i in range(len(bunch['entries'])):
                    #Choosen meaning, others can be related
                    if bunch['entries'][i]['type'] != "meaning": continue
                    meaning = bunch['entries'][i]['terms'][0]['text']
                    try:    
                        example = list()
                        #Examples start with ZERO index
                        for i_ex in range(0, len(bunch['entries'][i]['entries'])):
                            example.append(bunch['entries'][i]['entries'][i_ex]['terms'][0]['text'])
                            
                    except:
                        example = None
                    means.append([meaning, example])
                    
        return all_meanings
        
    @pyqtSlot(str)
    def get_translate(self, text):
        means = self.get_meaning(text)
        translate_text = ""
        
        if means is not None:
            #Short Summary
            for sec in (means['primaries'].keys()):
                meanings = means['primaries'][sec]
                for m in meanings:
                    translate_text += "%s" % m[0]
                    try: 
                        for e in m[1]:
                            translate_text += "<ul><li> %s </li></ul>" % e
                    except: 
                        pass
                    
        self.translate_info.text = text
        self.translate_info.voices = get_voice_simple(text)
        self.translate_info.phonetic = get_phonetic_symbol(text)
        self.translate_info.translate = translate_text.strip()
        
    @pyqtSlot()    
    def clear_translate(self):
        self.translate_info.text = ""
        self.translate_info.translate = ""
