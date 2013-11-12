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

import sys  
from PyQt5.QtWidgets import QApplication, qApp
from PyQt5.QtQuick import QQuickView
from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal
from PyQt5.QtGui import QSurfaceFormat, QColor, QCursor
from PyQt5 import QtCore, QtQuick
import signal
import os
from PIL import Image
import pyocr
import pyocr.builders
import json
from PyQt5.QtCore import QBuffer, QIODevice
import cStringIO as StringIO
import re
from PyQt5.QtDBus import QDBusConnection, QDBusInterface
    
def filter_punctuation(text):
    return re.sub("[^A-Za-z]", "", text)
    
def pil_to_image(pixmap):
    strio = StringIO.StringIO()
        
    qbuffer = QBuffer()
    qbuffer.open(QIODevice.ReadWrite)
    pixmap.save(qbuffer, "png")
    strio.write(qbuffer.data())
    qbuffer.close()
        
    strio.seek(0)
    
    return Image.open(strio)
        
class OCR(QObject):

    def __init__(self):
        QObject.__init__(self)
        self.screenshot_width = 600
        self.screenshot_height = 100
        self.screen_width = app.primaryScreen().size().width()
        
    @pyqtSlot(result=str)
    def get_cursor_pos(self):
        point = QCursor.pos()
        return json.dumps((point.x(), point.y()))
        
    def _get_word_rect(self, mx, my, width, height):    
        try:
            x = mx - width / 2
            y = my - height / 2
            scale = 2
            
            tool = pyocr.get_available_tools()[0]
            lang = "eng"
            
            pixmap = app.primaryScreen().grabWindow(0, x, y, width, height).scaled(width * scale, height * scale)
            image = pil_to_image(pixmap)
            
            word_boxes = tool.image_to_string(
                image.convert("L"),
                lang=lang,
                builder=pyocr.builders.WordBoxBuilder())
            
            px = width / 2
            py = height / 2
            
            for word_box in word_boxes[::-1]:
                ((left_x, left_y), (right_x, right_y)) = word_box.position
                if (left_x <= px * scale <= right_x and left_y <= py * scale <= right_y):
                    return json.dumps((x + left_x / scale,
                                       y + left_y / scale,
                                       (right_x - left_x) / scale,
                                       (right_y - left_y) / scale,
                                       filter_punctuation(word_box.content),
                                       ))
            return None    
        except:
            return None
        
    @pyqtSlot(int, int, result=str)
    def get_word_rect(self, mx, my):
        for (w, h) in [(self.screenshot_width, self.screenshot_height),
                       (self.screen_width, self.screenshot_height),]:
            rect = self._get_word_rect(mx, my, w, h)
            if rect:
                return rect
            
        return ""
        
APP_DBUS_NAME = "com.deepin.ocr"    
APP_OBJECT_NAME = "/com/deepin/ocr"

class UniqueService(QObject):

    uniqueTrigger = pyqtSignal()    
    
    @pyqtSlot()
    def unique(self):
        self.uniqueTrigger.emit()
        
class Window(QQuickView):
    
    def __init__(self):
        QQuickView.__init__(self)
        
if __name__ == "__main__":
    iface = QDBusInterface(APP_DBUS_NAME, APP_OBJECT_NAME, '', QDBusConnection.sessionBus())
    if iface.isValid():
        iface.call("unique")
        sys.exit(1)
    
    uniqueService = UniqueService()
    QDBusConnection.sessionBus().registerService(APP_DBUS_NAME)
    QDBusConnection.sessionBus().registerObject(APP_OBJECT_NAME, uniqueService, QDBusConnection.ExportAllSlots)

    app = QApplication(sys.argv)  
    ocr = OCR()
    
    view = Window()
    surface_format = QSurfaceFormat()
    surface_format.setAlphaBufferSize(8)
    
    view.setColor(QColor(0, 0, 0, 0))
    view.setFlags(QtCore.Qt.FramelessWindowHint)
    view.setResizeMode(QtQuick.QQuickView.SizeRootObjectToView)
    view.setFormat(surface_format)
    
    qml_context = view.rootContext()
    qml_context.setContextProperty("windowView", view)
    qml_context.setContextProperty("qApp", qApp)
    qml_context.setContextProperty("ocr", ocr)
    
    view.setSource(QtCore.QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), 'Main.qml')))
    view.showFullScreen()
    
    uniqueService.uniqueTrigger.connect(view.showFullScreen)
    
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    sys.exit(app.exec_())
    
    
