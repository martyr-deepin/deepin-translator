#! /usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Hou Shaohui, Wang Yong
# 
# Author:     Hou Shaohui <houshao55@gmail.com>
# Maintainer: Hou Shaohui <houshao55@gmail.com>
#             Wang Yong <lazycat.manatee@gmail.com>
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

from PyQt5.QtCore import pyqtSlot
from auto_object import AutoQObject
from translate_interface import TranslateInterface
import os
import commands
from message_view import show_message
from pkg_manager import get_install_packages, install_packages
from deepin_utils.file import get_parent_dir
from nls import _

class Translate(TranslateInterface):
    
    def __init__(self):
        TranslateInterface.__init__(self, os.path.join(get_parent_dir(__file__), "Translate.qml"))
        self.need_install_packages = []

    def init_translate_info(self):
        TranslateInfo = AutoQObject(
            ("translate", str),
            ("fixed", str),
          name="TranslateInfo")
        self.translate_info = TranslateInfo()        
        
    def check_before_translate(self):
        self.need_install_packages = get_install_packages(["stardict", "sdcv", "stardict-xdict-ce-gb", "stardict-xdict-ec-gb"])
        if len(self.need_install_packages) > 0:
            show_message(_("Need install sdcv package to enable translate feature"), _("Cancel"), _("Install"), self.install_sdcv)
            return False
        else:
            return True
        
    @pyqtSlot(str)
    def get_translate(self, text):
        self.translate_info.translate = '\n'.join(commands.getoutput("sdcv %s" % text).split("\n")[1::])
        
    @pyqtSlot()    
    def install_sdcv(self):
        install_packages(self.need_install_packages)
