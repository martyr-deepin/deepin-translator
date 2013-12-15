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

from listmodel import QObjectListModel
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSlot
from constant import LANGUAGES

class Model(QObjectListModel):
    
    nameRole = QtCore.Qt.UserRole + 1
    displayNameRole = QtCore.Qt.UserRole + 2
    
    _roles = {nameRole: "name", displayNameRole: "displayName"}
    
    def __init__(self, data, parent=None):
        QObjectListModel.__init__(self, parent)
        
        self.data_dict = dict(data)
        self.setAll(data)
        
    def data(self, index, role):
        if not index.isValid() or index.row() > self.size:
            return QtCore.QVariant()
        try:
            item = self._data[index.row()]
        except:
            return QtCore.QVariant()
        
        if role == self.nameRole:
            return item[0]
        elif role == self.displayNameRole:
            return item[1]
        
        return QtCore.QVariant()

    @pyqtSlot(str, result=str)        
    def getDisplayName(self, name):
        return self.data_dict[name]
    
    @pyqtSlot(str, result=int)
    def getNameIndex(self, name):
        try:
            return map(lambda (key, value): key, self._data).index(name)
        except:
            return 0

class LanguageModel(Model):
    def __init__(self, parent=None):
        Model.__init__(self, sorted(LANGUAGES, key=lambda (code, name): name), parent)
