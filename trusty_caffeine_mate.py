#!/usr/bin/env python

import appindicator  # install via apt-get install python-appindicator
import argparse
import gtk
import signal
import subprocess
import sys

#  Copyright (c) 2016, Ivor Wanders
#  MIT License, see the LICENSE.md file.


class Caffeine:
    def __init__(self, light_theme=False, debug=False, show_quit=False,
                 start_enabled=False):
        # create and setup the indicator
        self.ind = appindicator.Indicator(
                                      "trusty-caffeine",
                                      "caffeine-cup-empty",
                                      appindicator.CATEGORY_SYSTEM_SERVICES)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.ind.set_attention_icon("caffeine-cup-full")

        # use the appropriate icon
        if (light_theme):
            self.ind.set_icon_theme_path(
                "/usr/share/icons/matefaenza/status/22/")
        else:
            self.ind.set_icon_theme_path(
                "/usr/share/icons/matefaenzagray/status/22/")

        # create the menu
        self.menu = gtk.Menu()

        self.activate_item = gtk.MenuItem("Activate")
        self.activate_item.connect("activate", self.toggle)
        self.activate_item.show()
        self.menu.append(self.activate_item)

        # add the quit option if need be.
        if (show_quit):
            self.quit_item = gtk.MenuItem("Quit")
            self.quit_item.connect("activate", self.quit)
            self.quit_item.show()
            self.menu.append(self.quit_item)

        # add the menu
        self.ind.set_menu(self.menu)

        # set default state
        self.activated = False
        self.proc = None

        # if enabled, activate it.
        if (start_enabled):
            self.activate()

        # if we run in debug mode, call the debug method every 100ms
        if (debug):
            gtk.timeout_add(100, self.debug)

    def activate(self):
        # change the menu text and the indicator state
        self.activate_item.set_label("Deactivate")
        self.ind.set_status(appindicator.STATUS_ATTENTION)

        # create the subprocess
        self.proc = subprocess.Popen(['mate-screensaver-command', '-i'],
                                     stdout=subprocess.PIPE)

        # You could also change this command for example for redshift:
        # self.proc = Popen(['redshift', '-l', '52.22:6.89',
        #                     '-t', '5500:4000'], stdout=PIPE)

        self.activated = True

    def deactivate(self):
        # if we have a process send the interrupt signal
        if (self.proc):
            self.proc.send_signal(signal.SIGINT)
            # Lets assume that the process actually quits from an interrupt.

        # update the menu text
        self.activate_item.set_label("Activate")
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.activated = False

    def toggle(self, widget):
        # This method is called when the menu item is clicked.
        if (self.activated):
            self.deactivate()
        else:
            self.activate()

    def debug(self):
        # prints None if the process is active, exit code otherwise.
        if (self.proc):
            print(self.proc.poll())
            print(self.proc.returncode)
        else:
            print("No process")
        return True

    def main(self):
        gtk.main()

    def quit(self, widget):
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Caffeine indicator')
    parser.add_argument('--debug', default=False, action="store_true",
                        help="Whether to print the status every 100ms.")
    parser.add_argument('--lighttheme', default=False, action="store_true",
                        help="Use the light theme's icon.")
    parser.add_argument('--showquit', default=False, action="store_true",
                        help="Show the quit option in the menu.")
    parser.add_argument('--enabled', default=False, action="store_true",
                        help="Should it start with the inhibit active?.")

    args = parser.parse_args()

    indicator = Caffeine(light_theme=args.lighttheme,
                         debug=args.debug,
                         show_quit=args.showquit,
                         start_enabled=args.enabled)

    indicator.main()
