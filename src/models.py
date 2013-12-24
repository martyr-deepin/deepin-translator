#! /usr/bin/env python
# -*- coding: utf-8 -*-

import copy
from PyQt5 import QtCore

import requests
import utils
import xdg

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
        
    @QtCore.pyqtSlot(int, result=str)    
    def getTitle(self, index):
        return self._data[index]["title"]
        
    @QtCore.pyqtSlot(result=int)
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
    
    def emitSuggestResult(self, data, threadId):        
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
            success_funcs=(self.emitSuggestResult, (thread_id,))).start()
        
    @QtCore.pyqtSlot(str)
    def suggest(self, text):    
        self.asyncSuggest(get_suggest, (text,))
        
    @QtCore.pyqtSlot(str, int)
    def suggestWithNum(self, text, num=10):    
        self.asyncSuggest(get_suggest, (text, num))
    
suggestModel = SuggestModel()        


class KeyDict(dict):
    
    def __eq__(self, other):
        try:
            return self.owner == other.owner
        except:
            return False
        
    @property    
    def owner(self):
        return self.get("title")
        
    def __cmp__(self, other):    
        try:
            return cmp(self.owner, other.owner)
        except:
            return -1
            

class HistoryModel(QtCore.QAbstractListModel):
    TitleRole = QtCore.Qt.UserRole + 1
    ExplainRole = QtCore.Qt.UserRole + 2
    
    _roles = { TitleRole: "title", ExplainRole: "explain" }
    finished = QtCore.pyqtSignal()
    MAX_NUM = 5    
    
    def __init__(self, parent=None):
        super(HistoryModel, self).__init__(parent)
        self._db = xdg.get_cache_file("history.db")
        self._data = []
        
        # load db
        self.load()
        
    def load(self):    
        objs = utils.load_db(self._db)
        if objs:
            self._data = objs
    
    @QtCore.pyqtSlot()        
    def save(self):
        if self._data:
            utils.save_db(self._data, self._db)
        
    def setHistoryData(self, data):
        self.beginResetModel()
        del self._data
        self._data = data        
        self.endResetModel()  
        self.finished.emit()
        
    def resetHistoryData(self):    
        self.beginResetModel()
        self.endResetModel()
        self.finished.emit()
                    
    def addHistoryData(self, history):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._data.append(history)
        self.endInsertRows()        
        
    @QtCore.pyqtSlot(str, str, str)
    def addSearchData(self, title, explain, web):
        title = title.strip()
        explain = explain.split("<br>")[0]
        if not explain:
            explain = web
        
        explain = explain.split("\n")[0]
    
        kd = KeyDict(title=title, explain=explain)
        change = False
        if kd in self._data:
            idx = self._data.index(kd)
            if idx != 0:
                self._data.pop(idx)                
                self._data.insert(0, kd)
                change = True
        else:    
            self._data.insert(0, kd)
            change = True
            
        if change:    
            self.keepData()
            self.resetHistoryData()
            self.save()
            
    def keepData(self):        
        if len(self._data) > self.MAX_NUM:
            self._data = self._data[:self.MAX_NUM]
            
    @QtCore.pyqtSlot(int, result=str)    
    def getTitle(self, index):
        return self._data[index]["title"]
        
    @QtCore.pyqtSlot(result=int)
    def total(self):    
        return len(self._data)
        
    def removeHistoryData(self):
        self.beginInsertRows(QtCore.QModelIndex(), self.rowCount(), self.rowCount())
        self._data.pop()        
        self.endInsertRows()        
        
    def roleNames(self):
        return self._roles
    
    def rowCount(self, parent=QtCore.QModelIndex()):    
        return len(self._data[:self.MAX_NUM])
    
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

historyModel = HistoryModel()        
