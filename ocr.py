#! /usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Wang Yong
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

from PIL import Image
from xutils import screen_width, screen_height, conn, root
import pyocr
import pyocr.builders
import re
import xcb
import xcb.xproto

screenshot_width = 600
screenshot_height = 100

def filter_punctuation(text):
    return re.sub("[^A-Za-z_-]", " ", text)

def ocr_word(mouse_x, mouse_y):
    # Ocr word under cursor.
    x = max(mouse_x - screenshot_width / 2, 0) 
    y = max(mouse_y - screenshot_height / 2, 0)
    width = min(mouse_x + screenshot_width / 2, screen_width) - x
    height = min(mouse_y + screenshot_height / 2, screen_height) - y
                    
    scale = 2
    tool = pyocr.get_available_tools()[0]
    lang = "eng"
        
    output_format = xcb.xproto.ImageFormat.ZPixmap
    plane_mask = 2**32 - 1
    
    reply = conn.core.GetImage(
        output_format, 
        root, 
        x,
        y,
        width,
        height,
        plane_mask).reply()
    image_data = reply.data.buf()
    image = Image.frombuffer("RGBX", (width, height), image_data, "raw", "BGRX").convert("RGB")
    
    word_boxes = tool.image_to_string(
        image.convert("L").resize((width * scale, height * scale)),
        lang=lang,
        builder=pyocr.builders.WordBoxBuilder())
    
    cursor_x = (mouse_x - x) * scale
    cursor_y = (mouse_y - y) * scale
    
    for word_box in word_boxes[::-1]:
        ((left_x, left_y), (right_x, right_y)) = word_box.position
        if (left_x <= cursor_x <= right_x and left_y <= cursor_y <= right_y):
            word = filter_punctuation(word_box.content)
            return (mouse_x, mouse_y, word)
        
    return None    
