# Trusty Caffeine MATE

Caffeine didn't work for me in Ubuntu MATE 14.04 (Trusty Tahr), I could not be
bothered with [patching](https://bugs.launchpad.net/caffeine/+bug/1462186) it so
I implemented it myself. Also works on Ubuntu MATE 16.04 (Xenial Xerus) and
Ubuntu MATE 18.04 (Bionic Beaver).


This is a Python application indicator which does exactly what it needs to do:
it provides a notification icon that allows you to inhibit the screensaver.

## How?

It works by calling `mate-screensaver-command -i` in a subprocess which inhibits
the screensaver. An interrupt signal is sent to the process when Caffeine is
disabled. It also disables dpms through `xset`.

It depends on the `python-appindicator` package, so that needs to be installed
via `apt-get install python-appindicator`. The icon is already available on your
system.

### Bionic Beaver 18.04
In Ubuntu Mate 18.04 (Bionic Beaver) the coffee cup icon requires installing the
`faenza-icon-theme` package (`apt-get install faenza-icon-theme`).

### Focal Fossa 20.04
The Python module `appindicator` has been deprecated in favour of;
- `gir1.2-appindicator3-0.1`


