#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
from deepin_utils.file import get_parent_dir

PROGRAM_NAME = "deepin-translator"

_home = os.path.expanduser('~')
xdg_cache_home = os.environ.get('XDG_CACHE_HOME') or \
            os.path.join(_home, '.cache')

xdg_config_home = os.environ.get('XDG_CONFIG_HOME') or \
            os.path.join(_home, '.config')

def get_cache_file(path):
    ''' get cache file. '''
    cachefile = os.path.join(xdg_cache_home, PROGRAM_NAME, path)
    cachedir = get_parent_dir(cachefile)
    if not os.path.isdir(cachedir):
        os.makedirs(cachedir)
    return cachefile    

def get_config_file(path):
    ''' get config file. '''
    configfile = os.path.join(xdg_config_home, PROGRAM_NAME, path)
    configdir = get_parent_dir(configfile)
    if not os.path.isdir(configdir):
        os.makedirs(configdir)
    return configfile    
