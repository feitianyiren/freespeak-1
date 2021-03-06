# FreeSpeak - a GUI frontend to online translator engines
# freespeak/ui/manager.py
#
## Copyright (C) 2005, 2006, 2007, 2008, 2009  Luca Bruno <lethalman88@gmail.com>
##
## This file is part of FreeSpeak.
##   
## FreeSpeak is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.
##    
## FreeSpeak is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU Library General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.

"""
Translation manager UI
"""

import gtk

class Manager (gtk.Notebook):
    """
    A notebook for managing translation pages
    """
    def __init__ (self, application):
        gtk.Notebook.__init__ (self)
        self.set_scrollable (True)
        self.application = application

    def switch_to_latest (self):
        """
        Switch to the latest page of the notebook
        """
        self.set_current_page (-1)

    def close_current_translation (self):
        """
        Close the currently viewed translation
        """
        page_num = self.get_current_page ()
        self.remove_page (page_num)

    def add_translation (self, translation):
        """
        Append a new translation page
        """
        label = translation.get_label ()
        self.append_page (translation, label)
        translation.set_border_width (6)
        translation.show ()

    def remove_translation (self, translation):
        """
        Remove the given translation from the notebook
        """
        page_num = self.page_num (translation)
        self.remove_page (page_num)

__all__ = ['Manager']
