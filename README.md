# Trusty Caffeine MATE

Caffeine didn't work for me in Ubuntu MATE 14.04 (Trusty Tahr), I could not be
bothered with [patching](https://bugs.launchpad.net/caffeine/+bug/1462186) it so
I implemented it myself. Also works on Ubuntu MATE 16.04 (Xenial Xerus).

This is a Python application indicator which does exactly what it needs to do:
it provides a notification icon that allows you to inhibit the screensaver.

## How?

It works by calling `mate-screensaver-command -i` in a subprocess which inhibits
the screensaver. An interrupt signal is sent to the process when Caffeine is
disabled.

It depends on the `python-appindicator` package, so that needs to be installed
via `apt-get install python-appindicator`. The icon is already available on your
system.