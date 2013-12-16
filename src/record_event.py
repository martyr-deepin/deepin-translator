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

from PyQt5.QtCore import QObject, pyqtSignal
from xutils import get_event_data, record_event, check_valid_event
import threading

class RecordEvent(QObject, threading.Thread):
    
    capture_event = pyqtSignal("QVariant")
    
    def __init__(self, parent=None):
        QObject.__init__(self, parent)
        self.setDaemon(True)
        
    def record_callback(self, reply):
        check_valid_event(reply)
     
        data = reply.data
        while len(data):
            event, data = get_event_data(data)
            self.capture_event.emit(event)
            print "########### ", event
            
    def run(self):
        record_event(self.record_callback)
