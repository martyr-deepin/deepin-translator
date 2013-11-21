#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import collections
import threading
import fcntl
import cPickle
from urllib import urlencode

def to_key_val_list(value):
    """Take an object and test to see if it can be represented as a
    dictionary. If it can be, return a list of tuples, e.g.,

    ::

        >>> to_key_val_list([('key', 'val')])
        [('key', 'val')]
        >>> to_key_val_list({'key': 'val'})
        [('key', 'val')]
        >>> to_key_val_list('string')
        ValueError: cannot encode objects that are not 2-tuples.
    """
    if value is None:
        return None

    if isinstance(value, (str, bytes, bool, int)):
        raise ValueError('cannot encode objects that are not 2-tuples')

    if isinstance(value, collections.Mapping):
        value = value.items()

    return list(value)

def encode_params(data):
    """Encode parameters in a piece of data.

    Will successfully encode parameters when passed as a dict or a list of
    2-tuples. Order is retained if data is a list of 2-tuples but arbitrary
    if parameters are supplied as a dict.
    """

    if isinstance(data, (str, bytes)):
        return data
    elif hasattr(data, 'read'):
        return data
    elif hasattr(data, '__iter__'):
        result = []
        for k, vs in to_key_val_list(data):
            if isinstance(vs, basestring) or not hasattr(vs, '__iter__'):
                vs = [vs]
            for v in vs:
                if v is not None:
                    result.append(
                        (k.encode('utf-8') if isinstance(k, unicode) else k,
                         v.encode('utf-8') if isinstance(v, unicode) else v))
        return urlencode(result, doseq=True)
    else:
        return data

class ThreadFetch(threading.Thread):            
    
    def __init__(self, fetch_funcs, success_funcs=None, fail_funcs=None):
        super(ThreadFetch, self).__init__()
        self.setDaemon(True)
        self.fetch_funcs = fetch_funcs
        self.success_funcs = success_funcs
        self.fail_funcs = fail_funcs
        
    def run(self):    
        result = self.fetch_funcs[0](*self.fetch_funcs[1])
        if self.success_funcs:
            self.success_funcs[0](result, *self.success_funcs[1])
        
        # if result:
        #     if self.success_funcs:
        #         self.success_funcs[0](result, *self.success_funcs[1])
        # else:        
        #     if self.fail_funcs:
        #         self.fail_funcs[0](*self.fail_funcs[1])
    
def save_db(objs, fn):
    '''Save object to db file.'''
    try:
        f = open(fn + ".tmp", "w")
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        cPickle.dump(objs, f, cPickle.HIGHEST_PROTOCOL)
        f.close()
        os.rename(fn + ".tmp", fn)
    except:    
        pass
    
def load_db(fn):    
    '''Load object from db file.'''
    objs = None
    if os.path.exists(fn):
        f = open(fn, "rb")
        try:
            objs = cPickle.load(f)
        except:    
            try:
                shutil.copy(fn, fn + ".not-valid")
            except: pass    
            objs = None
        f.close()    
    return objs    
                
