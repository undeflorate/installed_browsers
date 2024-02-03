import fnmatch
import sys
from typing import Iterator, Optional

from . import linux, mac, windows
from .common import Browser, Version, OS

__all__ = ["Browser",
           "browsers",
           "do_i_have_installed",
           "give_me_details_of",
           "get_version_of",
           "what_is_the_default_browser"]


def browsers() -> Iterator[Browser]:
    """
    Iterates over installed browsers.

    :return: Iterator of Tuple of browser key and browser information.
    """
    match sys.platform:
        case OS.LINUX:
            yield from linux.browsers()
        case OS.MAC:
            yield from mac.browsers()
        case OS.WINDOWS:
            yield from windows.browsers()
        case _:
            yield Browser(
                name="exception", description="This operating system is not yet supported.", version="", location=""
            )


def what_is_the_default_browser():
    """
    Shows the default browser in system - if there is any.

    :return: Default browser information.
    """
    match sys.platform:
        case OS.LINUX:
            return linux.what_is_the_default_browser()
        case OS.MAC:
            return mac.what_is_the_default_browser()
        # case OS.WINDOWS: Windows is not yet supported.


def do_i_have_installed(name: str):
    """
    Checks if the provided browser is installed in system.

    Parameters:
                Possible browser entries / parameters\n
                for Linux:\n
                chrome, chromium, firefox, ms-edge, opera, opera-beta, opera-developer,
                brave, brave-beta, brave-nightly\n
                for macOS:\n
                chrome, chrome-canary, chromium, firefox, firefox-developer, firefox-nightly,
                safari, opera, opera-beta, opera-developer, ms-edge, ms-edge-beta, ms-edge-dev, ms-edge-canary,
                brave, brave-beta, brave-dev, brave-nightly\n
                for Windows:\n
                chrome, chrome-canary, chromium, firefox, firefox-developer, firefox-nightly,
                opera, opera-beta, opera-developer, ms-edge, ms-edge-beta, ms-edge-dev, ms-edge-canary, ms-ie,
                brave, brave-beta, brave-nightly
    :return: True or False depending on the browser is installed or not.
    """
    match sys.platform:
        case OS.LINUX:
            return linux.do_i_have_installed(name)
        case OS.MAC:
            return mac.do_i_have_installed(name)
        # case OS.WINDOWS: Windows is not yet supported.


def give_me_details_of(name: str) -> Optional[Browser]:
    """
    Retrieve browser details if the provided browser is installed in system.

    Parameters:
                Possible browser entries / parameters\n
                for Linux:\n
                chrome, chromium, firefox, ms-edge, opera, opera-beta, opera-developer,
                brave, brave-beta, brave-nightly\n
                for macOS:\n
                chrome, chrome-canary, chromium, firefox, firefox-developer, firefox-nightly,
                safari, opera, opera-beta, opera-developer, ms-edge, ms-edge-beta, ms-edge-dev, ms-edge-canary,
                brave, brave-beta, brave-dev, brave-nightly\n
                for Windows:\n
                chrome, chrome-canary, chromium, firefox, firefox-developer, firefox-nightly,
                opera, opera-beta, opera-developer, ms-edge, ms-edge-beta, ms-edge-dev, ms-edge-canary, ms-ie,
                brave, brave-beta, brave-nightly
    :return: Dictionary containing browser name, description, desktop version and location.
    """
    match sys.platform:
        case OS.LINUX:
            for found in (entity for entity in linux.get_details_of(name) if entity is not None):
                return found
        case OS.MAC:
            for found in (entity for entity in mac.get_details_of(name) if entity is not None):
                return found
        # case OS.WINDOWS: Windows is not yet supported.


def get_version_of(name: str) -> Optional[Version]:
    """
    Retrieve browser version if the provided browser is installed in system.

    Parameters:
                Possible browser entries / parameters\n
                for Linux:\n
                chrome, chromium, firefox, ms-edge, opera, opera-beta, opera-developer,
                brave, brave-beta, brave-nightly\n
                for macOS:\n
                chrome, chrome-canary, chromium, firefox, firefox-developer, firefox-nightly,
                safari, opera, opera-beta, opera-developer, ms-edge, ms-edge-beta, ms-edge-dev, ms-edge-canary,
                brave, brave-beta, brave-dev, brave-nightly\n
                for Windows:\n
                chrome, chrome-canary, chromium, firefox, firefox-developer, firefox-nightly,
                opera, opera-beta, opera-developer, ms-edge, ms-edge-beta, ms-edge-dev, ms-edge-canary, ms-ie,
                brave, brave-beta, brave-nightly
    :return: Browser description and version.
    """
    match sys.platform:
        case OS.LINUX:
            for found in (entity for entity in linux.get_version_of(name) if entity is not None):
                return found
        case OS.MAC:
            for found in (entity for entity in mac.get_version_of(name) if entity is not None):
                return found
        # case OS.WINDOWS: Windows is not yet supported.
