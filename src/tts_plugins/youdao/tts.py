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

from utils import encode_params
import requests
from pyquery import PyQuery

VOICE_UK = 1
VOICE_US = 2

def get_voice_type(text):
    data = { "keyfrom" : "deskdict.mini", "q" : text, "doctype" : "xml", "xmlVersion" : 8.2,
             "client" : "deskdict", "id" : "cee84504d9984f1b2", "vendor": "unknown", 
             "in" : "YoudaoDict", "appVer" : "5.4.46.5554", "appZengqiang" : 0, "le" : "eng", "LTH" : 40}
    ret = requests.get("http://dict.youdao.com/search", params=data).text
    if isinstance(ret, unicode):
        ret = ret.encode('utf-8')
    pq = PyQuery(ret, parser="xml")
    
    try:    
        if pq.find('usphone').text() == None:
            return VOICE_UK
    except: 
        pass
    
    return VOICE_US
        
def get_voice(text):
    url = "http://dict.youdao.com/dictvoice"
    data = { "keyfrom" : "deskdict.mini.word", "audio" : text, "client" : "deskdict", "id" : "cee84504d9984f1b2", "vendor": "unknown", 
             "in" : "YoudaoDict", "appVer" : "5.4.46.5554", "appZengqiang" : 0, "type" : get_voice_type(text)}
    
    return ["%s?%s" % (url, encode_params(data))]

def check_before_voice():
    return True