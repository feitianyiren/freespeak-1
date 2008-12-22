import gtk

class IntroButton (gtk.Button):
    def __init__ (self, text, description, stock):
        gtk.Button.__init__ (self)

        self.set_name ("intro-button")
        self.set_focus_on_click (False)
        self.set_relief (gtk.RELIEF_NONE)
        self.set_property ('can-focus', False)

        image = gtk.image_new_from_stock (stock, gtk.ICON_SIZE_DIALOG)
        image.show ()
        label = gtk.Label ()
        label.set_markup ("<b><u><span color='blue'>%s</span></u></b>" % text)
        label.set_alignment (0, 0.5)
        label.show ()
        hbox = gtk.HBox ()
        hbox.set_border_width (12)
        hbox.pack_start (image, False, padding=12)
        hbox.pack_start (label, False, padding=12)
        hbox.show ()
        self.add (hbox)

class Intro (gtk.Alignment):
    def __init__ (self, application, manager):
        gtk.Alignment.__init__ (self, 0.5, 0.5, 0, 0)
        self.application = application
        self.manager = manager

        self.setup_layout ()
        self.setup_manager ()
        self.setup_text ()
        self.setup_web ()
        self.setup_suggestions ()
        self.setup_help ()

        self.connect ('expose-event', self.on_expose)

    def on_expose (self, widget, event):
        style = self.get_style ()
        allocation = self.vbox.get_allocation ()
        x, y = allocation.x-12, allocation.y-12
        width, height = allocation.width+24, allocation.height+24
        style.paint_box (event.window, gtk.STATE_PRELIGHT, gtk.SHADOW_ETCHED_IN, event.area, self, None,
                         x, y, width, height)

    def setup_layout (self):
        self.set_border_width (12)
        self.vbox = gtk.VBox (homogeneous=True)
        self.vbox.show ()
        self.add (self.vbox)
        self.size_group = gtk.SizeGroup (gtk.SIZE_GROUP_HORIZONTAL)

    def setup_manager (self):
        self.manager.hide ()
        self.manager.connect ('page-added', self.on_page_added)
        self.manager.connect ('page-removed', self.on_page_removed)

    def setup_text (self):
        button = IntroButton ("Make a text translation", "", gtk.STOCK_NEW)
        button.show ()
        self.size_group.add_widget (button)
        self.vbox.pack_start (button)

    def setup_web (self):
        button = IntroButton ("Make a web page translation", "", gtk.STOCK_NETWORK)
        button.show ()
        self.size_group.add_widget (button)
        self.vbox.pack_start (button)

    def setup_suggestions (self):
        button = IntroButton ("Request translation suggestions", "", gtk.STOCK_SELECT_FONT)
        button.show ()
        self.size_group.add_widget (button)
        self.vbox.pack_start (button)

    def setup_help (self):
        button = IntroButton ("Getting started", "Getting started", gtk.STOCK_HELP)
        button.show ()
        self.size_group.add_widget (button)
        self.vbox.pack_start (button)

    # Events

    def on_page_added (self, *args):
        self.hide ()
        self.manager.show ()

    def on_page_removed (self, notebook, *args):
        if notebook.get_n_pages () == 0:
            self.manager.hide ()
            self.show ()
