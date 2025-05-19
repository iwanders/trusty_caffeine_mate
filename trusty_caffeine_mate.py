#!/usr/bin/env python3

import gi
gi.require_version('AyatanaAppIndicator3', '0.1')
from gi.repository import AyatanaAppIndicator3 as appindicator
from gi.repository import GLib, Gtk

import argparse
import signal
import subprocess
import sys
import os
import time

#  Copyright (c) 2016, Ivor Wanders
#  MIT License, see the LICENSE.md file.

class Caffeine:
    def __init__(self, light_theme=False, debug=False, show_quit=False,
                 start_enabled=False, enable_delay=30.0, verbose=False):
        self.verbose = verbose
        self.print(f"{time.time()}: startup")
        # create and setup the indicator
        self.ind = appindicator.Indicator.new(
                                      "trusty-caffeine",
                                      "caffeine-cup-empty",
                                      appindicator.IndicatorCategory.SYSTEM_SERVICES)
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
        self.ind.set_attention_icon("caffeine-cup-full")

        found_theme = False
        # use the appropriate icon
        if (light_theme):
            self.ind.set_icon_theme_path(
                "/usr/share/icons/matefaenza/status/22/")
        else:
            # matefaenzagray was renamed to matefaenzadark in Xenial.
            # In Bionic it is called Faenza-Dark, install the faenza-icon-theme
            # package to make it available.
            dark_themes = ["matefaenzagray", "matefaenzadark", "Faenza-Dark"]
            for t in dark_themes:
                d = os.path.join("/usr", "share", "icons", t, "status", "22")
                if (os.path.isdir(d)):
                    self.ind.set_icon_theme_path(d)
                    found_theme = True
                    break

        if (not found_theme):
            print("Ubuntu 18.04 / 20.04 doesn't have the icon installed by default.")
            print("Use 'apt-get install faenza-icon-theme' to install the icon")

        # create the menu
        self.menu = Gtk.Menu()

        self.activate_item = Gtk.MenuItem(label="Activate")
        self.activate_item.connect("activate", self.toggle)
        self.activate_item.show()
        self.menu.append(self.activate_item)

        # add the quit option if need be.
        if (show_quit):
            self.quit_item = Gtk.MenuItem(label="Quit")
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
            delay_in_ms = int(enable_delay * 1000.0)
            self.print(f"{time.time()}: start_enabled for {delay_in_ms} ms")
            # Trigger the timer on the delay.
            self.enable_timer = GLib.timeout_add(delay_in_ms, self.timed_activate)

        # if we run in debug mode, call the debug method every 100ms
        if (debug):
            GLib.timeout_add(100, self.debug)

    def print(self, *args, **kwargs):
        if self.verbose:
            print(*args, **kwargs)
            sys.stdout.flush()

    def timed_activate(self):
        self.print(f"{time.time()}: timed_activate")
        GLib.source_remove(self.enable_timer)
        self.enable_timer = None
        self.activate()

    def activate(self):
        self.print(f"{time.time()}: activated")
        # change the menu text and the indicator state
        self.activate_item.set_label("Deactivate")
        self.ind.set_status(appindicator.IndicatorStatus.ATTENTION)

        # Disable dpms
        subprocess.call(['xset', 's', 'off', '-dpms']) #, 's', 'noblank'

        # create the subprocess to block mate's screensaver.
        self.proc = subprocess.Popen(['mate-screensaver-command', '-i',
                                      '--reason', "Trusty caffeine mate is active",
                                      '-n', 'trusty caffeine mate'],
                                     stdout=subprocess.PIPE)

        # You could also change this command for example for redshift:
        # self.proc = Popen(['redshift', '-l', '52.22:6.89',
        #                     '-t', '5500:4000'], stdout=PIPE)

        self.activated = True

    def deactivate(self):
        self.print(f"{time.time()}: deactivated")
        # if we have a process send the interrupt signal
        if (self.proc):
            self.proc.send_signal(signal.SIGINT)
            # Lets assume that the process actually quits from an interrupt.
            subprocess.call(['xset', 's', 'on', '+dpms']) #, 's', 'blank'

        # update the menu text
        self.activate_item.set_label("Activate")
        self.ind.set_status(appindicator.IndicatorStatus.ACTIVE)
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
        Gtk.main()

    def quit(self, widget):
        sys.exit(0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Caffeine indicator')
    parser.add_argument('--debug', default=False, action="store_true",
                        help="Whether to print the status every 100ms.")
    parser.add_argument('--verbose', default=False, action="store_true",
                        help="Whether to print state transitions.")
    parser.add_argument('--lighttheme', default=False, action="store_true",
                        help="Use the light theme's icon.")
    parser.add_argument('--showquit', default=False, action="store_true",
                        help="Show the quit option in the menu.")
    parser.add_argument('--enabled', default=False, action="store_true",
                        help="Should it start with the inhibit active?.")

    parser.add_argument('--enable-delay', default=30.0,
                        help="Delay before disabling the screensaver, only used when --enabled is"
                             "set, defaults to %(default)s", type=float
                        )

    args = parser.parse_args()

    indicator = Caffeine(light_theme=args.lighttheme,
                         debug=args.debug,
                         show_quit=args.showquit,
                         start_enabled=args.enabled,
                         enable_delay=args.enable_delay,
                         verbose=args.verbose,
                        )

    indicator.main()
