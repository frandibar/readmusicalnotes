# GNU Solfege - free ear training software
# Copyright (C) 2005, 2006, 2007 Tom Cato Amundsen
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin ST, Fifth Floor, Boston, MA  02110-1301  USA

import os
import sys
import locale

def _get_home_dir():
    ''' Try to find user's home directory, otherwise return current directory.'''
    path1 = os.path.expanduser("~")
    try:
        path2 = os.environ["HOME"]
    except KeyError:
        path2 = ""
    try:
        path3 = os.environ["USERPROFILE"]
    except KeyError:
        path3 = ""

    if not os.path.exists(path1):
        if not os.path.exists(path2):
            if not os.path.exists(path3):
                return os.getcwd()
            else: return path3
        else: return path2
    else: return path1


def get_home_dir():
    if sys.platform == 'win32':
        enc = sys.getfilesystemencoding()
        if enc is None or enc == "":
            enc = "iso-8859-1"
        try:
            return _get_home_dir().decode(enc)
        except UnicodeDecodeError:
            try:
                return _get_home_dir().decode(locale.getpreferredencoding())
            except UnicodeDecodeError:
                return _get_home_dir().decode("iso-8859-1")
    else:
        # linux user names can only be ascii chars.
        return _get_home_dir().decode("iso-8859-1")

def expanduser(s):
    return s.replace("~", get_home_dir())
