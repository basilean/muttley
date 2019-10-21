from gi.repository import Gtk

@Gtk.Template(filename="data/ui/file.ui")
class File(Gtk.FileChooserDialog):
    __gtype_name__ = "File"

    def __init__(self, *args, **kwargs):
        """ Init
        """
        super(File, self).__init__(*args, **kwargs)
#        self.connect(
#            'response',
#            self._close
#        )

    def _close(self, model, extra):
        model.destroy()
