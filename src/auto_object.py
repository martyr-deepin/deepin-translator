#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2013 Deepin, Inc.
#               2011 ~ 2013 Hou Shaohui
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

def AutoQObject(*class_def, **kwargs):
    '''
    Car = AutoQObject(
             ('model', str),
             ('brand', str),
             ('year', int),
             ('inStock', bool),
             name='Car'
          )
          
 
    c = Car(model='Fiesta', brand='Ford', year=1337)
    print c.model, c.brand, c.year, c.inStock
    print c
 
    c.inStock = True
 
    print c.model, c.brand, c.year, c.inStock
    print c          
    '''
    class Object(QtCore.QObject):
        def __init__(self, **kwargs):
            QtCore.QObject.__init__(self)
            for key, val in class_def:
                if callable(val):
                    value = val()
                else:    
                    value = ""
                self.__dict__['_'+key] = kwargs.get(key, value)
 
        def __repr__(self):
            values = ('%s=%r' % (key, self.__dict__['_'+key]) \
                    for key, value in class_def)
            return '<%s (%s)>' % (kwargs.get('name', 'QObject'), ', '.join(values))
 
        for key, value in class_def:
            nfy = locals()['_nfy_'+key] = QtCore.pyqtSignal()
 
            def _get(key):
                def f(self):
                    return getattr(self, '_'+key)
                return f
 
            def _set(key):
                def f(self, value):
                    setattr(self, '_'+key, value)
                    getattr(self, "_nfy_"+key).emit()                    
                return f
 
            set_func = locals()['_set_'+key] = _set(key)
            get_func = locals()['_get_'+key] = _get(key)
 
            locals()[key] = QtCore.pyqtProperty(value, get_func, set_func, notify=nfy)
 
    return Object


