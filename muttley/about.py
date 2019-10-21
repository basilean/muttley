from gi.repository import Gtk

@Gtk.Template(filename="data/ui/about.ui")
class About(Gtk.AboutDialog):
    __gtype_name__ = "About"

    def __init__(self, *args, **kwargs):
        """ Init
        """
        super(About, self).__init__(*args, **kwargs)
 #       self.connect(
 #           'response',
 #           self._close
 #       )

 #   def _close(self, model, extra):
 #       model.destroy()
