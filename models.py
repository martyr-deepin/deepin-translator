#! /usr/bin/env python
# -*- coding: utf-8 -*-

import copy
from PyQt5 import QtCore

import requests
import utils

from xmltodict import parse as xml_parse

def get_suggest(text, num=10):
    data = { "type" : "DESKDICT", "num" : num, "ver" : 2.0, "le": "eng", "q" : text }
    ret = requests.get("http://dict.youdao.com/suggest", params=data).text
    doc =  xml_parse(ret)
    results = []
    try:
        data = doc['suggest']['items']['item']
        for item in data:
            if item.has_key("title") and item.has_key("explain"):
                results.append(dict(title=item["title"], explain=item["explain"]))
    except:
        return None
    else:
        if results:
            return results
        return None


class SuggestModel(QtCore.QAbstractListModel):
    TitleRole = QtCore.Qt.UserRole + 1
    ExplainRole = QtCore.Qt.UserRole + 2
    
    _roles = { TitleRole: "title", ExplainRole: "explain" }
    
    suggested = QtCore.pyqtSignal(int, object)
    finished = QtCore.pyqtSignal()

    
    def __init__(self, parent=None):
        super(SuggestModel, self).__init__(parent)
        self.suggestThreadId = 0
        self.suggested.connect(self.onSuggestedData)
        self._data = []
        
    def setSuggestData(self, data):
        self.beginResetModel()
        del self._data
        self._data = data        
        self.endResetModel()  
        self.finished.emit()
        
    def resetSuggestData(self):    
        self.beginResetModel()
        self.endResetModel()
        self.finished.emit()
                    
    def addSuggestData(self, suggest):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(suggest)
        self.endInsertRows()        
        
    @QtCore.pyqtSlot()
    def total(self):    
        return len(self._data)
        
    def removeSuggestData(self):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._data.pop()        
        self.endInsertRows()        
        
    def roleNames(self):
        return self._roles
        
    def rowCount(self, parent=QtCore.QModelIndex()):    
        return len(self._data)
    
    def data(self, index, role):

        if not index.isValid() or index.row() > len(self._data):
            return QtCore.QVariant()

        try:
            item = self._data[index.row()]
        except:
            return QtCore.QVariant()
        
        if role == self.TitleRole:
            return item.get("title", "")
        elif role == self.ExplainRole:
            return item.get("explain", "")
        return QtCore.QVariant()

    def parseSuggested(self, data):        
        if data is not None:
            self.setSuggestData(data)
        else:    
            self.resetSuggestData()
    
    def emitSuggesResult(self, data, threadId):        
        if threadId == self.suggestThreadId:
            self.suggested.emit(threadId, data)
            
    def onSuggestedData(self, threadId, data):        
        if threadId == self.suggestThreadId:
            self.parseSuggested(data)
            
    def asyncSuggest(self, suggestFunc, args):        
        self.suggestThreadId += 1
        thread_id = copy.deepcopy(self.suggestThreadId)
        utils.ThreadFetch(
            fetch_funcs=(suggestFunc, args),
            success_funcs=(self.emitSuggesResult, (thread_id,))).start()
        
    @QtCore.pyqtSlot(str)
    def suggest(self, text):    
        self.asyncSuggest(get_suggest, (text,))
        
    @QtCore.pyqtSlot(str, int)
    def suggestWithNum(self, text, num=10):    
        self.asyncSuggest(get_suggest, (text, num))
    
suggestModel = SuggestModel()        
