# FreeSpeak - a GUI frontend to online translator engines
# freespeak/ui/about.py
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
About FreeSpeak
"""

import gtk
from freespeak import defs

class About (gtk.AboutDialog):
    """
    About dialog
    """
    def __init__ (self, application):
        gtk.AboutDialog.__init__ (self)
        self.application = application

        self.set_name ("FreeSpeak")
        self.set_version (defs.VERSION)
        self.set_comments (_("A free frontend to online translator engines")) 
        self.set_license ("""
        FreeSpeak is free software; you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation; either version 2 of the License, or
        (at your option) any later version.
        
        FreeSpeak is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU Library General Public License for more details.
        
        You should have received a copy of the GNU General Public License
        along with this program; if not, write to the Free Software
        Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301, USA.
        """)
        # TODO: this must not be application-wide
        gtk.about_dialog_set_url_hook (self.on_url, "")
        gtk.about_dialog_set_email_hook (self.on_url, "mailto:")
                          
        self.set_website_label ("http://freespeak.berlios.de/")
        self.set_website ("http://freespeak.berlios.de/")
        self.set_authors (["Luca Bruno\t<lethalman88@gmail.com>"])
        logo = self.application.icon_theme.load_icon ('freespeak', 64, 0)
        self.set_logo (logo)
        self.set_artists (["Coviello Giuseppe\t<immigrant@email.it>"])
        self.set_translator_credits ("Luca Bruno\t<lethalman88@gmail.com>")
                                     
        self.set_copyright ("Copyright (C) 2005, 2006, 2007, 2008, 2009  Luca Bruno <lethalman88@gmail.com>")

        self.connect ('response', self.on_response)
        self.show_all()

    # Events

    def on_url (self, w, url, data):
        """
        URL hook for about dialogs
        """
        gtk.show_uri (self.window.get_screen(), data+url, 0)

    def on_response (self, *w):
        """
        Dialog response
        """
        self.destroy ()
