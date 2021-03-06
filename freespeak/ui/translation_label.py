# FreeSpeak - a GUI frontend to online translator engines
# freespeak/ui/translation.py
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
Classes for creating a full-featured notebook translation tab
"""

import gtk

from freespeak.ui.spinner import Spinner
import freespeak.ui.utils as uiutils

class TranslationLabel (gtk.HBox):
    """
    The label contains a pixbuf, a label and a close button.
    Also a popup menu is available if the user right clicks the tab.
    If the user double clicks the tab label, it becomes an entry able to change
    the label of the tab.
    """
    ui_string = """<ui>
        <popup name="PopupMenu">
            <menuitem action="Close" />
        </popup>
    </ui>"""

    def __init__ (self, application, translation):
        gtk.HBox.__init__ (self, spacing=2)
        self.application = application
        self.translation = translation

        self.title = 'Unnamed'
        self.is_custom = False

        self.setup_icon ()
        self.setup_label ()
        self.setup_entry ()
        self.setup_menu ()
        self.setup_event_box ()
        self.setup_close ()
        self.be_label ()

        self.pack_start (self.icon)
        self.pack_start (self.event_box)
        self.pack_start (self.close, False, padding=4)

    def setup_icon (self):
        """
        Setup the spinner icon
        """
        self.icon = Spinner (self.application, None)
        self.icon.show ()

    def setup_label (self):
        """
        Setup the label
        """
        self.label = gtk.Label ()
        self.label.show ()

    def setup_entry (self):
        """
        Setup the entry that will take place for modifying the label
        """
        self.entry = gtk.Entry ()
        self.entry_focus_out = self.entry.connect ('focus-out-event',
                                                   self.on_entry_activate)
        self.entry_activate_handler = self.entry.connect ('activate',
                                                          self.on_entry_activate)
        self.entry.show ()

    def setup_event_box (self):
        """
        The event box needed to grab events for the child widgets
        """
        self.event_box = gtk.EventBox ()
        self.event_box.set_visible_window (False)
        self.event_box.connect ('button-press-event',
                                self.on_event_box_button_press_event)
        self.event_box.connect ('key-press-event',
                                self.on_event_box_key_press_event)
        self.event_box.show ()

    def setup_close (self):
        """
        Setup the close tiny-button
        """
        self.close = uiutils.TinyButton (gtk.STOCK_CLOSE)
        self.close.set_tooltip_text (_("Close this translation"))
        self.close.connect ('clicked', self.on_close)
        self.close.show ()

    def setup_menu (self):
        """
        Setup the popup menu
        """
        self.action_group = gtk.ActionGroup ('PopupActions')
        actions = (
            ('Close', gtk.STOCK_CLOSE, None, None,
             _('Close this translation'), self.on_close),
            )
        self.action_group.add_actions (actions)
        self.ui = gtk.UIManager ()
        self.ui.insert_action_group (self.action_group, 0)
        self.ui.add_ui_from_string (self.ui_string)
        self.menu = self.ui.get_widget ("/PopupMenu")

    def drop_child (self):
        """
        Drop the event box child, which would be a label or an entry
        """
        child = self.event_box.get_child ()
        if child:
            self.event_box.remove (child)

    def be_label (self):
        """
        Drop the entry and become a label
        """
        self.drop_child ()
        self.label.set_text (self.title)
        self.event_box.add (self.label)

    def be_entry (self):
        """
        Drop the label and become an entry
        """
        self.drop_child ()
        self.entry.set_text (self.title)
        self.event_box.add (self.entry)

    def set_suggested_title (self, title):
        """
        Set the suggested title of the page
        """
        if not self.is_custom:
            self.title = title
            self.label.set_text (title)

    def start_loading (self):
        """
        Make the tab busy by animating the spinner
        """
        self.icon.start ()

    def stop_loading (self):
        """
        Stop animating the spinner
        """
        self.icon.stop ()

    # Events

    def on_event_box_button_press_event (self, event_box, event):
        """
        Handle both the double click and the right click
        """
        if event.type == gtk.gdk._2BUTTON_PRESS:
            self.be_entry ()
            self.entry.grab_focus ()
        elif event.type == gtk.gdk.BUTTON_PRESS and event.button == 3:
            self.menu.popup (None, None, None, event.button, event.time, None)

    def on_event_box_key_press_event (self, event_box, event):
        """
        Handle the ESC key as a good key for becoming back a label
        and reject the entry changes
        """
        # ESC key
        if event.keyval == 65307:
            self.entry.handler_block (self.entry_focus_out)
            self.be_label ()
            self.entry.handler_unblock (self.entry_focus_out)

    def on_entry_activate (self, entry, *args):
        """
        Accept changes when the user activates the entry
        """
        self.title = entry.get_text ()
        self.entry.handler_block (self.entry_focus_out)
        self.be_label ()
        self.entry.handler_unblock (self.entry_focus_out)

        self.is_custom = True

    def on_close (self, button):
        """
        Close the translation
        """
        self.translation.close ()

__all__ = ['TranslationLabel']
