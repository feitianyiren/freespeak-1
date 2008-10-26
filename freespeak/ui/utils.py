import gtk
import gobject

class ScrolledWindow (gtk.ScrolledWindow):
    def __init__ (self, child):
        gtk.ScrolledWindow.__init__ (self)
        self.set_policy (gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.set_shadow_type (gtk.SHADOW_ETCHED_IN)
        self.add (child)

class Frame (gtk.Frame):
    def __init__ (self, label_text):
        gtk.Frame.__init__ (self)
        label = gtk.Label ()
        label.set_markup ("<b>"+label_text+"</b>")
        label.show ()
        self.set_property ('label-xalign', 0)
        self.set_label_widget (label)
        self.set_shadow_type (gtk.SHADOW_NONE)

    def add (self, widget):
        alignment = gtk.Alignment ()
        alignment.set_property ('top-padding', 6)
        alignment.set_property ('left-padding', 12)
        alignment.set_property ('xscale', 1)
        alignment.set_property ('yscale', 1)
        alignment.add (widget)
        alignment.show ()
        return gtk.Frame.add (self, alignment)

class Progress (gtk.ProgressBar):
    def __init__ (self):
        gtk.ProgressBar.__init__ (self)
        self.running = False
        self.set_pulse_step (0.01)

    def pulse_idle (self):
        self.pulse ()
        return self.running

    def start (self):
        assert not self.running
        self.running = True
        gobject.timeout_add (10, self.pulse_idle)

    def stop (self):
        self.running = False

def error (message, parent=None):
    """
    Run an message dialog for an error
    """
    dialog = gtk.MessageDialog(parent,
                               gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
    dialog.run ()
    dialog.destroy()

def warning (message, parent=None):
    """
    Run an message dialog for a warning
    """
    dialog = gtk.MessageDialog(parent,
                               gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_WARNING, gtk.BUTTONS_OK, message)
    dialog.run ()
    dialog.destroy()
            
def question(self, message, parent=None):
    """
    Ask a question and return the response of the message dialog
    @param msg: The message to be shown
    @param parent: Specify the transient parent
    @return: Dialog response
    """
    dialog = gtk.MessageDialog(parent,
                               gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                               gtk.MESSAGE_QUESTION, gtk.BUTTONS_NONE, msg)
    dialog.add_buttons(gtk.STOCK_YES, gtk.RESPONSE_YES,
                       gtk.STOCK_NO, gtk.RESPONSE_NO) 
    dialog.set_default_response(gtk.RESPONSE_NO)
    response = dialog.run()
    dialog.destroy()
    return response
