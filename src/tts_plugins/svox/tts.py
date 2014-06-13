#! /usr/bin/env python
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

import subprocess
from pkg_manager import get_install_packages, install_packages
from message_view import show_message
from nls import _

def get_voice(text):
    wav_file = "/tmp/deepin-translator-svox.wav"
    subprocess.Popen(["pico2wave", "-w", wav_file, text]).wait()
    return [wav_file]

def get_phonetic_symbol(text):
    return ""
    
def check_before_voice():
    need_install_packages = get_install_packages(["libttspico-utils"])
    if len(need_install_packages) > 0:
        show_message(_("Package SVOX is required to enable pronunciation"), _("Cancel"), _("Install"), lambda : install_packages(need_install_packages))
        return False
    else:
        return True
