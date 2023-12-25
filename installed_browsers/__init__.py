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
        case OS.WINDOWS:
            yield from windows.browsers()
        case OS.MAC:
            yield from mac.browsers()
        case _:
            print("This operation system is not yet supported.")


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
    return linux.do_i_have_installed(name)


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
    for found in (entity for entity in linux.get_details_of(name) if entity is not None):
        return found


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
    for found in (entity for entity in linux.get_version_of(name) if entity is not None):
        return found


def what_is_the_default_browser():
    """
    Shows the default browser in system - if there is any.

    :return: Default browser information.
    """
    return linux.what_is_the_default_browser()
