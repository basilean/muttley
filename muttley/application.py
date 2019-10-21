"""

 Muttley
 A small business companion.

 Author: Andres Basile
 License: GPL v3

"""
from gettext import gettext as _
from gi import require_version
require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib, Gio, GdkPixbuf
from muttley.home import Home
from muttley.about import About
from muttley.file import File

UI_MENU="""
<?xml version="1.0" encoding="UTF-8"?>
<interface>
  <menu id="ui_menu">
    <section>
      <item>
        <attribute name="action">app.open</attribute>
        <attribute name="label" translatable="yes">_Open</attribute>
      </item>
    </section>
    <section>
      <item>
        <attribute name="action">app.about</attribute>
        <attribute name="label" translatable="yes">_About</attribute>
      </item>
      <item>
        <attribute name="action">app.quit</attribute>
        <attribute name="label" translatable="yes">_Quit</attribute>
        <attribute name="accel">&lt;Primary&gt;q</attribute>
    </item>
    </section>
  </menu>
</interface>
"""

class App(Gtk.Application):
    def __init__(self):
        super(App, self).__init__(
            application_id="ar.com.basile.muttley",
            flags=Gio.ApplicationFlags.HANDLES_COMMAND_LINE,
        )
        self.inv_file = None
        self.add_main_option("file", ord("f"), GLib.OptionFlags.NONE,
                             GLib.OptionArg.STRING, "Inventory CSV file.", None)

    def do_startup(self):
        Gtk.Application.do_startup(self)
        builder = Gtk.Builder.new_from_string(UI_MENU, -1)
        self.set_app_menu(builder.get_object("ui_menu"))
        self.do_app_menu()

    def do_activate(self):
        self.home = Home(application=self)
        self.home.present()
        if self.inv_file:
            self.home.file_load(self.inv_file)

    def do_command_line(self, command_line):
        options = command_line.get_options_dict()
        options = options.end().unpack()
        if options.get("file"):
            self.inv_file = options["file"]
        self.activate()
        return 0

    def do_app_menu(self):
        actions = [
            ('about', self._about),
            ('quit', self._quit),
            ('open', self._open),
        ]
        for name, func in actions:
            action = Gio.SimpleAction.new(name, None)
            action.connect('activate', func)
            self.add_action(action)

    def _open(self, *argv):
        inventory = File(transient_for=self.home)
        reply = inventory.run()
        if reply == Gtk.ResponseType.OK:
            self.inv_file = inventory.get_uri()
            self.home.file_load(self.inv_file)
        inventory.destroy()

    def _about(self, *argv):
        about = About(transient_for=self.home)
        about.present()

    def _quit(self, *argv):
        self.home.destroy()
