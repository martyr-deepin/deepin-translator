#! /usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2013 Deepin, Inc.
#               2011 ~ 2013 Wang Yong
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
from config import setting_config
from constant import LANGUAGE_OCR_DICT
from message_view import show_message
from nls import _
from pkg_manager import get_install_packages, install_packages
import constant
import ImageEnhance

screenshot_width = 600
screenshot_height = 100

def filter_punctuation(text):
    src_lang = setting_config.get_translate_config("src_lang")
    if src_lang in ["eng"]:
        return re.sub("[^A-Za-z_-]", " ", text).strip()
    else:
        return text

def ocr_log(src_lang):
    print "%s is not support" % src_lang
        
def ocr_word(mouse_x, mouse_y):
    # Return None if occur unsupported language.
    src_lang = setting_config.get_translate_config("src_lang")
    if not LANGUAGE_OCR_DICT.has_key(src_lang):
        show_message(_("Sorry, screen ocr not support %s yet") % _(src_lang), _("Cancel"), _("Ok, I know"), lambda : ocr_log(src_lang))
        return None

    # Return None if found any ocr package need install before continue. 
    ocr_pkg_name = LANGUAGE_OCR_DICT[src_lang]
    pkg_names = get_install_packages([ocr_pkg_name])
    if len(pkg_names):
        show_message(_("Need install OCR package to enable translate feature"), _("Cancel"), _("Install"), lambda : install_packages(pkg_names))
        return None
    
    # Return None if mouse at trayicon area.
    if constant.TRAYAREA_TOP < mouse_y < constant.TRAYAREA_BOTTOM:
        return None

    # Ocr word under cursor.
    lang = ocr_pkg_name.split("tesseract-ocr-")[1].replace("-", "_")
    x = max(mouse_x - screenshot_width / 2, 0) 
    y = max(mouse_y - screenshot_height / 2, 0)
    width = min(mouse_x + screenshot_width / 2, screen_width) - x
    height = min(mouse_y + screenshot_height / 2, screen_height) - y
                    
    scale = 2
    tool = pyocr.get_available_tools()[0]
        
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
    
    # Get screenshot image data.
    image_data = reply.data.buf()
    image = Image.frombuffer("RGBX", (width, height), image_data, "raw", "BGRX").convert("RGB")
    
    # First make image grey and scale bigger.
    image = image.convert("L").resize((width * scale, height * scale))
    
    # image.save("old.png")       # debug
    # Second enhance image with contrast and sharpness.
    image = ImageEnhance.Contrast(image).enhance(1.5)
    
    # I found uncomment below code have better result. ;)
    # image = ImageEnhance.Sharpness(image).enhance(2.0)
    
    # image.save("new.png")       # debug
    
    word_boxes = tool.image_to_string(
        image,
        lang=lang,
        builder=pyocr.builders.WordBoxBuilder())
    
    cursor_x = (mouse_x - x) * scale
    cursor_y = (mouse_y - y) * scale
    
    for word_box in word_boxes[::-1]:
        print word_box.content
        ((left_x, left_y), (right_x, right_y)) = word_box.position
        if (left_x <= cursor_x <= right_x and left_y <= cursor_y <= right_y):
            word = filter_punctuation(word_box.content)
            # print "'%s'" % word
            # Return None if ocr word is space string.
            if word.isspace():
                return None
            else:
                return word
        
    return None    
