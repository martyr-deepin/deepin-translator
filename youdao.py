#! /usr/bin/env python
# -*- coding: utf-8 -*-


from __future__ import unicode_literals

from netlib import public_curl, urlencode
from xmltodict import parse as xml_parse
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
                self.__dict__['_'+key] = kwargs.get(key, val())
 
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


SimpleInfo = AutoQObject(("keyword", str),
                         ("ukphone", str),
                         ("usphone", str),
                         ("uklink", str),
                         ("uslink", str),
                         ("webtrans", str),                         
                         ("trans", str),
                         ("weba", str),
                         name="SimpleInfo")


simpleinfo = SimpleInfo()

'''


'''

def get_voice(text, lang):
    url = "http://dict.youdao.com/dictvoice"
    data = { "keyfrom" : "deskdict.mini.word", "audio" : text, "client" : "deskdict", "id" : "cee84504d9984f1b2", "vendor": "unknown", 
             "in" : "YoudaoDict", "appVer" : "5.4.46.5554", "appZengqiang" : 0, "type" : lang}
    return "%s?%s" % (url, urlencode(data))

def get_suggest(text):
    data = { "type" : "DESKDICT", "num" : 10, "ver" : 2.0, "le": "eng", "q" : text }
    ret = public_curl.request("http://dict.youdao.com/suggest", data)
    doc =  xml_parse(ret)
    try:
        return doc['suggest']['items']['item']
    except:
        return None
    
    
def get_simple(text):    
    if not text:
        return
    
    if isinstance(text, unicode):
        text = text.encode("utf-8")

    data = { "keyfrom" : "deskdict.mini", "q" : text, "doctype" : "xml", "xmlVersion" : 8.2,
             "client" : "deskdict", "id" : "cee84504d9984f1b2", "vendor": "unknown", 
             "in" : "YoudaoDict", "appVer" : "5.4.46.5554", "appZengqiang" : 0, "le" : "eng", "LTH" : 40}
    ret = public_curl.request("http://dict.youdao.com/search", data)
    ret = xml_parse(ret)
    
    yodaodict = ret['yodaodict']
    simpleinfo.keyword = text    
    
    simpleinfo.ukphone = None
    simpleinfo.usphone = None
    simpleinfo.trans = None
    simpleinfo.uslink = None
    simpleinfo.uklink = None
        
    try:
        word = yodaodict['basic']['simple-dict']['word']
    except Exception: 
        pass
    else:    
        ukphone = word.get("ukphone", None)
        if ukphone:
            simpleinfo.ukphone = "英[%s]" % ukphone
            simpleinfo.uklink = get_voice(text, 1)
            
        usphone = word.get("usphone", None)
        if usphone:
            simpleinfo.usphone = "美[%s]" % usphone
            simpleinfo.uslink = get_voice(text, 2)
            
        trs = word["trs"]["tr"]
        if isinstance(trs, list):
            ret = "<br>".join(item['l']['i'] for item in trs)
        else:    
            ret = trs['l']['i']
        simpleinfo.trans = ret            
    
    try:
        ret = yodaodict['yodao-web-dict']['web-translation']
    except:    
        return
    
    if isinstance(ret, list):
        ret = ret[0]
    
    trans = ret['trans']
    if isinstance(trans, list):
        web_trans = "|".join(item["value"] for item in trans)
    else:    
        web_trans = trans['value']
    simpleinfo.webtrans = web_trans
