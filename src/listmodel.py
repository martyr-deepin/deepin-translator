#! /usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2013 Deepin, Inc.
#               2011 ~ 2013 Hou Shaohui, Wang Yong
# 
# Author:     Hou Shaohui <houshao55@gmail.com>
# Maintainer: Hou Shaohui <houshao55@gmail.com>
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

from PyQt5 import QtCore

class QObjectListModel(QtCore.QAbstractListModel):
    
    _roles = {}
    
    def __init__(self, parent=None):
        super(QObjectListModel, self).__init__(parent)
        self._data = []
        
    def roleNames(self):    
        return self._roles
    
    def rowCount(self, parent=QtCore.QModelIndex()):
        return self.size
    
    def setAll(self, data):
        self.beginResetModel()
        self._data = data
        self.endResetModel()
        self.dataChanged.emit(self.index(0), self.index(self.size-1), [])
        
    def data(self, index, role):
        if not index.isValid() or index.row() > self.size:
            return QtCore.QVariant()
        try:
            item = self._data[index.row()]
        except:
            return QtCore.QVariant()
        
        for r, name in self._roles.items():
            if r == role:
                getattr(item, name, QtCore.QVariant())
        return QtCore.QVariant()        
    
    def append(self, objs):
        if not isinstance(objs, list):
            objs = [ objs ]
        self.beginInsertRows(QtCore.QModelIndex(), self.size, self.size+len(objs)-1)    
        self._data.extend(objs)
        self.endInsertRows()
        
    def insert(self, i, objs):    
        if not isinstance(objs, list):
            objs = [ objs ]
        self.beginInsertRows(QtCore.QModelIndex(), i, i+len(objs)-1)    
        for obj in reversed(objs):
            self._data.insert(i, obj)
        self.endInsertRows()    
        
    def replace(self, obj, i=None):    
        if i is None:
            try:
                i = self.indexOf(obj)
            except ValueError:  
                i = None
        if i is None:        
            return
        self._data[i] = obj
        self.dataChanged.emit(self.index(i), self.index(i), [])
        
    def move(self, fromIndex, toIndex):    
        value = toIndex
        if toIndex > fromIndex:
            value += 1
        if not self.beginMoveRows(QtCore.QModelIndex(), fromIndex, fromIndex, QtCore.QModelIndex(), value):
            return
        self._data.insert(toIndex, self._data.pop(fromIndex))
        self.endMoveRows()
        
    def removeAt(self, i, count=1):    
        self.beginRemoveRows(QtCore.QModelIndex(), i, i + count - 1)
        for cpt in range(count):
            self._data.pop(i)
        self.endRemoveRows()
        
    def remove(self, obj):
        if not self.contains(obj):
            raise ValueError("QObjectListModel.remove(obj) : obj not in list")
        self.removeAt(self.indexOf(obj))
        
    def takeAt(self, i):
        self.beginRemoveRows(QtCore.QModelIndex(), i, i)
        obj = self._data.pop(i)
        self.endRemoveRows()
        return obj
    
    def clear(self):
        if not self._data:
            return
        self.beginRemoveRows(QtCore.QModelIndex(), 0, self.size - 1)
        self._data = []
        self.endRemoveRows()

    def contains(self, obj):
        return obj in self._data
        
    def indexOf(self, matchObj, fromIndex=0, positive=True):    
        index = self._data[fromIndex:].index(matchObj) + fromIndex
        if positive and index < 0:
            index += self.size
        return index
    
    def lastIndexOf(self, matchObj, fromIndex=-1, positive=True):
        r = list(self._data)
        r.reverse()
        index = - r[-fromIndex - 1:].index(matchObj) + fromIndex
        if positive and index < 0:
            index += self.size
        return index
    
    @property    
    def size(self):
        return len(self._data)
    
    @QtCore.pyqtSlot(result=bool)
    def isEmpty(self):
        return self.size == 0
    
    @QtCore.pyqtSlot(int, result="QVariant")
    def get(self, i):
        return self._data[i]
    
    def __iter__(self):
        """ Enables iteration over the list of objects. """
        return iter(self._data)

    def __len__(self):
        return self.size

    def __nonzero__(self):
        return self.size > 0

    def __getitem__(self, index):
        """ Enables the [] operator """
        return self._data[index]

