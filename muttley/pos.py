from os.path import exists
from re import compile, IGNORECASE
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GdkPixbuf
from gettext import gettext as _

@Gtk.Template(filename="data/ui/pos.ui")
class Pos(Gtk.Box):
    """ Class
    """
    __gtype_name__ = "Pos"
    ui_inv_search = Gtk.Template.Child()
    ui_inv_list = Gtk.Template.Child()
    ui_inv_list_view = Gtk.Template.Child()
    ui_item_img = Gtk.Template.Child()
    ui_item_barcode = Gtk.Template.Child()
    ui_item_description = Gtk.Template.Child()
    ui_item_price = Gtk.Template.Child()
    ui_item_qty = Gtk.Template.Child()
    ui_tkt_list = Gtk.Template.Child()
    ui_tkt_list_view = Gtk.Template.Child()
    ui_tkt_total = Gtk.Template.Child()
    ui_tkt_done = Gtk.Template.Child()

    def __init__(self, *args, **kwargs):
        """ Init
        """
        super(Pos, self).__init__(*args, **kwargs)
        self.inventory = {}
        self.ticket = {}
        self.ui_inv_search.connect(
            'activate',
            self.inv_search
        )
        self.ui_inv_list_view.connect(
            'row-activated',
            self.inv_item_select
        )
        self.ui_item_qty.connect(
            'value-changed',
            self.item_set_qty
        )
        self.ui_tkt_list_view.connect(
            'row-activated',
            self.tkt_item_select
        )
        self.ui_tkt_done.connect(
            'clicked',
            self.tkt_done
        )

    def load(self, inventory):
        self.inventory = inventory
        self.ticket = {}
        self.ui_inv_list.clear()
        self.ui_tkt_list.clear()
        self.item_unset()
        self.ui_tkt_total.set_text("0.0")

    def inv_search(self, event):
        """ Inventory Search
        """
        text = event.get_text()
        event.set_text(str())
        if self.inventory.get(text):
            self.item_set(text, 1)
            self.item_set_qty(None)
        else:
            self.ui_inv_list.clear()
            regex = compile(
                text,
                flags=IGNORECASE
            )
            for key, item in self.inventory.items():
                if regex.search(item['description']):
                    self.ui_inv_list.append(row=(
                        key,
                        self.inventory[key]['description'],
                        self.inventory[key]['price'],
                        self.inventory[key]['image']
                    ))

    def inv_item_select(self, view, path, column):
        """ Inventory Item Select
        """
        model = view.get_model()
        self.item_set(model[path][0], 1)
        self.item_set_qty(None)

    def item_set(self, barcode, qty=0):
        """ Item Set
        """
        if self.ticket.get(barcode):
            qty += self.ui_tkt_list.get_value(
                       self.ticket[barcode], 3
                   )
        self.ui_item_barcode.set_text(str(barcode))
        self.ui_item_description.set_text(
            self.inventory[barcode]['description']
        )
        self.ui_item_price.set_text(
            str(self.inventory[barcode]['price'])
        )
        self.ui_item_img.set_from_pixbuf(
            self.inventory[barcode]['image']
        )
        self.ui_item_qty.set_value(qty)
        self.ui_item_qty.set_sensitive(True)

    def item_set_qty(self, event):
        if self.ui_item_barcode.get_text():
            self.tkt_item_set(
                self.ui_item_barcode.get_text(),
                self.ui_item_qty.get_value()
            )

    def item_unset(self):
        self.ui_item_img.set_from_pixbuf(None)
        self.ui_item_barcode.set_text(str())
        self.ui_item_description.set_text(str())
        self.ui_item_price.set_text(str())
        self.ui_item_qty.set_value(0)
        self.ui_item_qty.set_sensitive(False)

    def tkt_item_set(self, barcode, num):
        tkt = self.ticket
        item = self.inventory[barcode]
        tkt_list = self.ui_tkt_list
        tkt_total = self.ui_tkt_total
        total = float(tkt_total.get_text())
        if tkt.get(barcode):
            qty = tkt_list.get_value(tkt[barcode], 3)
            total -= qty * item['price']
            if num == 0:
                tkt_list.remove(tkt[barcode])
                del tkt[barcode]
            else:
                tkt_list.set_value(tkt[barcode], 3, num)
                tkt_list.set_value(
                    tkt[barcode],
                    4,
                    num * item['price']
                )
                total += num * item['price']
        else:
            tkt[barcode] = tkt_list.append(row=(
                barcode,
                item['description'],
                item['price'],
                num,
                item['price']
            ))
            total += num * item['price']
        tkt_total.set_text(str(total))

    def tkt_item_select(self, view, path, column):
        model = view.get_model()
        self.item_set(model[path][0])

    def tkt_done(self, event):
        self.ticket = {}
        self.ui_tkt_list.clear()
        self.ui_tkt_total.set_text("0.0")
        self.item_unset()

