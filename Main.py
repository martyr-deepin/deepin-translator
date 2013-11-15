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
from PyQt5 import QtCore, QtQuick
from PyQt5.QtCore import pyqtSlot, QObject, pyqtSignal
from PyQt5.QtDBus import QDBusConnection, QDBusInterface
from PyQt5.QtGui import QSurfaceFormat, QColor
from PyQt5.QtQuick import QQuickView
from PyQt5.QtWidgets import QApplication, qApp
from Xlib import X, XK, display
from Xlib.ext import record
from Xlib.protocol import rq
from youdao import simpleinfo, get_simple
import os
import pyocr
import pyocr.builders
import re
import signal
import sys  
import threading
import time
import xcb
import xcb.xproto

APP_DBUS_NAME = "com.deepin.ocr"    
APP_OBJECT_NAME = "/com/deepin/ocr"

conn = xcb.connect()
screen = conn.get_setup().roots[0]
root = screen.root
screen_width = screen.width_in_pixels
screen_height = screen.height_in_pixels
screenshot_width = 600
screenshot_height = 100
root = screen.root
        
class UniqueService(QObject):

    uniqueTrigger = pyqtSignal()    
    
    @pyqtSlot()
    def unique(self):
        self.uniqueTrigger.emit()
        
def filter_punctuation(text):
    return re.sub("[^A-Za-z_-]", " ", text)

def ocr_word(mouse_x, mouse_y):
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

local_dpy = display.Display()
record_dpy = display.Display()
press_ctrl = False

class RecordEvent(QObject):
    
    press_ctrl = pyqtSignal()    
    release_ctrl = pyqtSignal()    
    
    def lookup_keysym(self, keysym):
        for name in dir(XK):
            if name[:3] == "XK_" and getattr(XK, name) == keysym:
                return name[3:]
        return "[%d]" % keysym
     
    def record_callback(self, reply):
        global press_ctrl
        
        if reply.category != record.FromServer:
            return
        if reply.client_swapped:
            print "* received swapped protocol data, cowardly ignored"
            return
        
        # Not an event
        if not len(reply.data) or ord(reply.data[0]) < 2:
            return
     
        data = reply.data
        while len(data):
            event, data = rq.EventField(None).parse_binary_value(data, record_dpy.display, None, None)
     
            if event.type == X.KeyPress:
                keyname = self.lookup_keysym(local_dpy.keycode_to_keysym(event.detail, 0))
                if keyname in ["Control_L", "Control_R"]:
                    press_ctrl = True
                    self.press_ctrl.emit()
            elif event.type == X.KeyRelease:
                keyname = self.lookup_keysym(local_dpy.keycode_to_keysym(event.detail, 0))
                if keyname in ["Control_L", "Control_R"]:
                    press_ctrl = False
                    self.release_ctrl.emit()
                
    def filter_event(self):
        ctx = record_dpy.record_create_context(
                0,
                [record.AllClients],
                [{
                        'core_requests': (0, 0),
                        'core_replies': (0, 0),
                        'ext_requests': (0, 0, 0, 0),
                        'ext_replies': (0, 0, 0, 0),
                        'delivered_events': (0, 0),
                        'device_events': (X.KeyPress, X.ButtonRelease),
                        'errors': (0, 0),
                        'client_started': False,
                        'client_died': False,
                }])
         
        record_dpy.record_enable_context(ctx, self.record_callback)
        record_dpy.record_free_context(ctx)

class MonitorMotionEvent(QObject):
    
    cursor_start = pyqtSignal()    
    cursor_move = pyqtSignal()    
    cursor_stop = pyqtSignal(int, int, str)

    def filter_event(self):
        last_mouse_x = -1
        last_mouse_y = -1
        last_mouse_time = 0
        stop_delay = 0.2
        stop_flag = False
        
        while True:
            mouse_time = time.time()
            
            pointer = conn.core.QueryPointer(root).reply()
            mouse_x = pointer.root_x
            mouse_y = pointer.root_y
            
            if last_mouse_x != mouse_x or last_mouse_y != mouse_y:
                if mouse_time - last_mouse_time > stop_delay:
                    # print "* Start: %s, %s" % (mouse_x, mouse_y)
                    
                    self.cursor_start.emit()
                else:
                    # print "* Move: %s, %s" % (mouse_x, mouse_y)
                    
                    self.cursor_move.emit()
            
                last_mouse_x = mouse_x
                last_mouse_y = mouse_y
                last_mouse_time = mouse_time
                
                stop_flag = False
            else:
                if not stop_flag and mouse_time - last_mouse_time > stop_delay:
                    stop_flag = True
                    print "Stop: %s, %s" % (mouse_x, mouse_y)
                    
                    if press_ctrl:
                        ocr_info = ocr_word(mouse_x, mouse_y)
                        if ocr_info:
                            self.cursor_stop.emit(*ocr_info)
                    
            time.sleep(0.01)
        
        # We should disconnect connection when don't need it anymore.
        conn.disconnect()

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
    
    view.setSource(QtCore.QUrl.fromLocalFile(os.path.join(os.path.dirname(__file__), 'Main.qml')))
    
    uniqueService.uniqueTrigger.connect(view.showFullScreen)
    
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    
    rootObject = view.rootObject()
    
    def show_translate(x, y, text):
        view.showNormal()
        view.setX(x + 10)
        view.setY(y + 10)
        get_simple(text)
        
    def translate_cursor_word():
        pointer = conn.core.QueryPointer(root).reply()
        mouse_x = pointer.root_x
        mouse_y = pointer.root_y
        ocr_info = ocr_word(mouse_x, mouse_y)
        show_translate(*ocr_info)
    
    motion_event = MonitorMotionEvent()
    motion_event.cursor_stop.connect(show_translate)
    threading.Thread(target=motion_event.filter_event).start()
    
    record_event = RecordEvent()
    record_event.press_ctrl.connect(translate_cursor_word)
    record_event.release_ctrl.connect(view.hide)
    threading.Thread(target=record_event.filter_event).start()

    sys.exit(app.exec_())
