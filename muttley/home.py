"""
 Muttley
 A small business companion.

 Author: Andres Basile
 License: GPL v3

"""
from os.path import exists
from re import compile, IGNORECASE
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GdkPixbuf
from gettext import gettext as _
from muttley.pos import Pos

@Gtk.Template(filename="data/ui/home.ui")
class Home(Gtk.ApplicationWindow):
    __gtype_name__ = "Home"
    ui_open = Gtk.Template.Child()
    ui_bar = Gtk.Template.Child()

    def __init__(self, **kwargv):
        """ Init
        """
        super(Home, self).__init__(**kwargv)
        # Internals
        self.that = kwargv['application']
        self.pos = None
        self.inv_cache = None
        # Init
        self.ui_open.connect(
            'clicked',
            self.that._open
        )

    def file_image_load(self, barcode):
        try:
            img = GdkPixbuf.Pixbuf.new_from_file_at_size(
                "{0}/{1}.jpg".format(self.dir_images.get_path(), barcode),
                200,
                200
            )
        except Exception as e:
            img = None
        return img

    def file_load(self, file_uri):
        try:
            self.file_inventory = Gio.File.new_for_uri(file_uri)
        except Exception as e:
            print(e)
        else:
            self.inv_cache = {}
            self.dir_sales = self.file_inventory.resolve_relative_path('../sales')
            self.dir_images = self.file_inventory.resolve_relative_path('../images')
            _, gcontent, _ = self.file_inventory.load_contents()
            for row in gcontent.decode('utf-8').split("\n"):
                col = row.rstrip().split(',')
                try:
                   barcode = str(col[0])
                   description = str(col[1])
                   price = float(col[2])
                except Exception:
                    pass
                else:
                    self.inv_cache[barcode] = {
                       'description': description,
                       'price': price,
                       'image': self.file_image_load(barcode)
                    }
            if not self.pos:
                self.pos = Pos()
                self.ui_bar.add_titled(self.pos, 'pos', "POS")
            self.pos.load(self.inv_cache)
            self.pos.ui_inv_search.grab_focus()

