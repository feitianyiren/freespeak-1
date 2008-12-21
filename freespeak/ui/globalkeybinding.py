# FreeSpeak - a GUI frontend to online translator engines
# freespeak/globalkeybinding.py
#
## Copyright (C) 2005, 2006, 2007, 2008  Luca Bruno <lethalman88@gmail.com>
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

from Xlib.display import Display
from Xlib import X
import gobject
import gconf
import gtk.gdk
import threading

class GlobalKeyBinding (gobject.GObject, threading.Thread):
    __gsignals__ = {
        'activate': (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, ()),
        }

    def __init__ (self, application, key):
        gobject.GObject.__init__ (self)
        threading.Thread.__init__ (self)
        self.setDaemon (True)

        self.application = application
        self.gconf_key = key

        self.application.config.client.notify_add (self.application.config.dir+"/"+self.gconf_key,
                                                   self.on_key_changed)
        self.keymap = gtk.gdk.keymap_get_default ()
        self.display = Display ()
        self.screen = self.display.screen ()
        self.root = self.screen.root

        self.map_modifiers ()

    def map_modifiers (self):
        gdk_modifiers = (gtk.gdk.CONTROL_MASK, gtk.gdk.SHIFT_MASK, gtk.gdk.MOD1_MASK,
                         gtk.gdk.MOD2_MASK, gtk.gdk.MOD3_MASK, gtk.gdk.MOD4_MASK, gtk.gdk.MOD5_MASK,
                         gtk.gdk.SUPER_MASK, gtk.gdk.HYPER_MASK)
        self.known_modifiers_mask = 0
        for modifier in gdk_modifiers:
            # Do you know how to handle unknown "Mod*" keys?
            # They are usually Locks and something like that
            if "Mod" not in gtk.accelerator_name (0, modifier):
                self.known_modifiers_mask |= modifier

    def on_key_changed (self, *args):
        self.regrab ()

    def regrab (self):
        self.ungrab ()
        self.grab ()

    def grab (self):
        accelerator = self.application.config.get (self.gconf_key)
        keyval, modifiers = gtk.accelerator_parse (accelerator)
        if not accelerator or (not keyval and not modifiers):
            self.keycode = None
            self.modifiers = None
            return
        self.keycode = self.keymap.get_entries_for_keyval(keyval)[0][0]
        self.modifiers = int (modifiers)
        return self.root.grab_key (self.keycode, X.AnyModifier, True, X.GrabModeAsync, X.GrabModeSync)

    def ungrab (self):
        if self.keycode:
            self.root.ungrab_key (self.keycode, X.AnyModifier, self.root)
        
    def idle (self):
        # Clipboard requests will hang without locking the GDK thread
        gtk.gdk.threads_enter ()
        self.emit ("activate")
        gtk.gdk.threads_leave ()
        return False

    def run (self):
        self.running = True
        wait_for_release = False
        while self.running:
            event = self.display.next_event ()
            if event.detail == self.keycode and event.type == X.KeyPress and not wait_for_release:
                modifiers = event.state & self.known_modifiers_mask
                if modifiers == self.modifiers:
                    wait_for_release = True
                    self.display.allow_events (X.AsyncKeyboard, event.time)
                else:
                    self.display.allow_events (X.ReplayKeyboard, event.time)
            elif event.detail == self.keycode and wait_for_release:
                if event.type == X.KeyRelease:
                    wait_for_release = False
                    gobject.idle_add (self.idle)
                self.display.allow_events (X.AsyncKeyboard, event.time)
            else:
                self.display.allow_events (X.ReplayKeyboard, event.time)

    def stop (self):
        self.running = False
        self.ungrab ()
        self.display.close ()
