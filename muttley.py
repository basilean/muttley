#!/usr/bin/python3
"""

 Muttley
 A small business companion.

 Author: Andres Basile
 License: GPL v3

"""
from sys import argv
from signal import signal, SIGINT, SIG_DFL
import locale
import gettext
from muttley.application import App

def main():
    """ Main
    """
    localedir = "@localedir@"
    locale.bindtextdomain("muttley", localedir)
    locale.textdomain("muttley")
    gettext.bindtextdomain("muttley", localedir)
    gettext.textdomain("muttley")
    app = App()
    signal(SIGINT, SIG_DFL)
    return app.run(argv)

if __name__ == "__main__":
    exit(main())
