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

import threading
import sys  
from PyQt5.QtWidgets import QApplication, qApp
from PyQt5.QtQuick import QQuickView
from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal
from PyQt5.QtGui import QSurfaceFormat, QColor
from PyQt5 import QtCore, QtQuick
import os
from PIL import Image
import pyocr
import pyocr.builders
import re
from PyQt5.QtDBus import QDBusConnection, QDBusInterface

import xcb
import xcb.xproto
import signal
import time
import pyocr
import pyocr.builders

APP_DBUS_NAME = "com.deepin.ocr"    
APP_OBJECT_NAME = "/com/deepin/ocr"

class UniqueService(QObject):

    uniqueTrigger = pyqtSignal()    
    
    @pyqtSlot()
    def unique(self):
        self.uniqueTrigger.emit()
        
def filter_punctuation(text):
    return re.sub("[^A-Za-z_-]", " ", text)

class OCR(QObject):
    
    cursor_start = pyqtSignal()    
    cursor_move = pyqtSignal()    
    cursor_stop = pyqtSignal(int, int, str)

    def filter_event(self):
        conn = xcb.connect()
        screen = conn.get_setup().roots[0]
        root = screen.root
        screen_width = screen.width_in_pixels
        screen_height = screen.height_in_pixels
        screenshot_width = 600
        screenshot_height = 100
        root = screen.root
        scale = 2
        
        last_mouse_x = -1
        last_mouse_y = -1
        last_mouse_time = 0
        stop_delay = 0.2
        stop_flag = False
        
        tool = pyocr.get_available_tools()[0]
        lang = "eng"
        
        while True:
            mouse_time = time.time()
            pointer = conn.core.QueryPointer(root).reply()
            mouse_x = pointer.root_x
            mouse_y = pointer.root_y
            
            if last_mouse_x != mouse_x or last_mouse_y != mouse_y:
                if mouse_time - last_mouse_time > stop_delay:
                    print "* Start: %s, %s" % (mouse_x, mouse_y)
                    
                    self.cursor_start.emit()
                else:
                    print "* Move: %s, %s" % (mouse_x, mouse_y)
                    
                    self.cursor_move.emit()
            
                last_mouse_x = mouse_x
                last_mouse_y = mouse_y
                last_mouse_time = mouse_time
                
                stop_flag = False
            else:
                if not stop_flag and mouse_time - last_mouse_time > stop_delay:
                    stop_flag = True
                    print "Stop: %s, %s" % (mouse_x, mouse_y)
                    
                    # GetImage requires an output format as the first arg.  We want ZPixmap:
                    output_format = xcb.xproto.ImageFormat.ZPixmap
                    plane_mask = 2**32 - 1
                    x = max(mouse_x - screenshot_width / 2, 0) 
                    y = max(mouse_y - screenshot_height / 2, 0)
                    width = min(mouse_x + screenshot_width / 2, screen_width) - x
                    height = min(mouse_y + screenshot_height / 2, screen_height) - y
                    
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
                            
                            self.cursor_stop.emit(
                                mouse_x,
                                mouse_y,
                                word,
                                )
                            break
            
            time.sleep(0.01)
        
        # We should disconnect connection when don't need it anymore.
        conn.disconnect()
        
from youdao import simpleinfo, get_simple
    
if __name__ == "__main__":
    iface = QDBusInterface(APP_DBUS_NAME, APP_OBJECT_NAME, '', QDBusConnection.sessionBus())
    if iface.isValid():
        iface.call("unique")
        sys.exit(1)
    
    uniqueService = UniqueService()
    QDBusConnection.sessionBus().registerService(APP_DBUS_NAME)
    QDBusConnection.sessionBus().registerObject(APP_OBJECT_NAME, uniqueService, QDBusConnection.ExportAllSlots)

    app = QApplication(sys.argv)  
    
    view = QQuickView()
    surface_format = QSurfaceFormat()
    surface_format.setAlphaBufferSize(8)
    
    view.setColor(QColor(0, 0, 0, 0))
    view.setFlags(QtCore.Qt.FramelessWindowHint)
    view.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)
    view.setFormat(surface_format)
    
    qml_context = view.rootContext()
    qml_context.setContextProperty("simpleinfo", simpleinfo)
    qml_context.setContextProperty("windowView", view)
    qml_context.setContextProperty("qApp", qApp)
    
    view.setSource(QtCore.QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), 'test.qml')))
    # view.setMinimumSize(QSize(800, 600))
    
    uniqueService.uniqueTrigger.connect(view.showFullScreen)
    
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    rootObject = view.rootObject()
    
    def show_translate(x, y, text):
        view.showNormal()
        view.setX(x + 10)
        view.setY(y + 10)
        get_simple(text)
    
    ocr = OCR()
    ocr.cursor_stop.connect(show_translate)
    # ocr.cursor_stop.connect(rootObject.showTranslate)
    # ocr.cursor_start.connect(rootObject.hideTranslate)
    # ocr.cursor_move.connect(rootObject.hideTranslate)
    
    threading.Thread(target=ocr.filter_event).start()

    sys.exit(app.exec_())
