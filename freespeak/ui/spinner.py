"""
    ui/spinner.py
    Fri Jun 14 13:41:56 2004
    Copyright (C) 2005-2006-2007-2008  Luca Bruno <lethalman88@gmail.com>
    http://www.italianpug.org
   
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Library General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
"""

import gtk
import gobject

from freespeak import utils

class Spinner (gtk.Image):
    PIXELS = 16
    TIMEOUT = 80 # ms

    animation = []
    animation_last = 0

    @classmethod
    def setup_animation (cls, application):
        icons = application.icon_theme.load_icon ("process-working", gtk.ICON_SIZE_DIALOG, 0)
        for y in range (5):
            for x in range (7):
                pixbuf = gtk.gdk.Pixbuf (gtk.gdk.COLORSPACE_RGB, True, 8, cls.PIXELS, cls.PIXELS)
                icons.copy_area (x*cls.PIXELS, y*cls.PIXELS, cls.PIXELS, cls.PIXELS,
                                 pixbuf, 0, 0)
                cls.animation.append (pixbuf)
        cls.animation_last = len (cls.animation) - 1

    def __init__ (self, application, idle_pixbuf):
        gtk.Image.__init__ (self)
        self.application = application

        self.idle_pixbuf = idle_pixbuf
        self.setup_animation (application)
        self.set_from_pixbuf (self.idle_pixbuf)

    def _rotate (self):
        self.set_from_pixbuf (self.animation[self.icon_num])
        if self.icon_num >= self.animation_last:
            self.icon_num = 0
        else:
            self.icon_num += 1
        return True

    @utils.syncronized
    def start (self):
        self.icon_num = 0
        self.source = gobject.timeout_add (self.TIMEOUT, self._rotate)

    @utils.syncronized
    def stop (self):
        gobject.source_remove (self.source)
        self.set_from_pixbuf (self.idle_pixbuf)