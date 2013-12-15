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

from utils import encode_params

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
        
def get_voice(text, tl="en"):
    if not isinstance(text, unicode):
        text = text.decode("utf-8", "ignore")
        
    results = []    
    contents = group(text, 54)
    for c in contents:
        results.append(google_voice("".join(c), tl=tl))
    return results    

def google_voice(text, tl="en", encoding="UTF-8"):
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
