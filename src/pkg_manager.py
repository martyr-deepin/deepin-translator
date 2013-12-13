#! /usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (C) 2011 ~ 2012 Deepin, Inc.
#               2011 ~ 2012 Wang Yong
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

import commands
from PyQt5.QtDBus import QDBusConnection, QDBusInterface
        
def is_package_installed(pkg_name):
    # python-apt is better way to check package is whether installed.
    # But we use 'dpkg --get-selections' to avoid conflict with apt program, such as deepin software center.
    result = commands.getoutput("dpkg --get-selections %s" % pkg_name)
    return not result.startswith("dpkg: no packages found")

def get_install_packages(pkg_names):
    need_install_packages = []
    for pkg_name in pkg_names:
        if not is_package_installed(pkg_name):
            need_install_packages.append(pkg_name)
            
    return need_install_packages        

def install_packages(pkg_names):
    iface = QDBusInterface("com.linuxdeepin.softwarecenter", "/com/linuxdeepin/softwarecenter", '', QDBusConnection.systemBus())
    iface.asyncCall("install_pkg", pkg_names)
    commands.getoutput("deepin-software-center --page=install")
