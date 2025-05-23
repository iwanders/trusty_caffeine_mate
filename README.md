# Trusty Caffeine MATE

Caffeine didn't work for me in Ubuntu MATE 14.04 (Trusty Tahr), I could not be
bothered with [patching](https://bugs.launchpad.net/caffeine/+bug/1462186) it so
I implemented it myself. Also works on Ubuntu MATE 16.04 (Xenial Xerus),
Ubuntu MATE 18.04 (Bionic Beaver) and Ubuntu MATE 20.04 (Focal Fossa), and Debian 12 (Bookworm).


This is a Python application indicator which does exactly what it needs to do:
it provides a notification icon that allows you to inhibit the screensaver.

## How?

It works by calling `mate-screensaver-command -i` in a subprocess which inhibits
the screensaver. An interrupt signal is sent to the process when Caffeine is
disabled. It also disables dpms through `xset`.

### Bionic Beaver 18.04
It depends on the `python-appindicator` package, so that needs to be installed
via `apt-get install python-appindicator`.
In Ubuntu Mate 18.04 (Bionic Beaver) the coffee cup icon requires installing the
`faenza-icon-theme` package (`apt-get install faenza-icon-theme`). Use the `bionic`
branch for a version that's completely compatible with Bionic.

### Focal Fossa 20.04
The Python module `appindicator` has been deprecated in favour of; `gir1.2-appindicator3-0.1`.
The coffee cup symbol also still requires the `faenza-icon-theme` to be installed, use the `focal`
branch for Focal.

### Debian Bookworm 12
The library `gir1.2-appindicator3-0.1` has been deprecated in favour of `gir1.2-ayatanaappindicator3-0.1`.
Minor changes to the import statement were necessary, the coffee cup symbol can still be installed with
the `faenza-icon-theme` package. This was flaky initially as sometimes this script would get started
before the `mate-screensaver` started, making the `--enabled` flag problematic, this now comes with
a default delay before it enables of 30 seconds to prevent this race condition.
