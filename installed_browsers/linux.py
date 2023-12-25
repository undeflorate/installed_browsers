import os
import re
import subprocess
import sys
from typing import Iterator, Optional

from xdg.DesktopEntry import DesktopEntry

from .common import Browser, Version, OS

# tuple of possible browsers
# desktop entry name may be different: "chromium_chromium.desktop" or "chromium-browser.desktop"
POSSIBLE_BROWSERS = (
    ("chrome", ("google-chrome",)),
    ("chromium", ("chromium", "chromium_chromium", "chromium-browser")),
    ("firefox", ("firefox", "firefox_firefox")),
    ("ms-edge", ("microsoft-edge",)),
    ("opera", ("opera_opera",)),
    ("opera-beta", ("opera-beta_opera-beta",)),
    ("opera-developer", ("opera-developer_opera-developer",)),
    ("brave", ("brave-browser", "brave_brave")),
    ("brave-beta", ("brave-browser-beta",)),
    ("brave-nightly", ("brave-browser-nightly",))
)

# tuple of browser locations
# $XDG_DATA_HOME and $XDG_DATA_DIRS are not always set
BROWSER_LOCATIONS = (
    "~/.local/share/applications",
    "/usr/share/applications",
    "/var/lib/snapd/desktop/applications",
)

# set version pattern with dot separation
VERSION_PATTERN = re.compile(r"\b(\S+\.\S+)\b")


# get all installed browsers
def browsers() -> Iterator[Browser]:
    match sys.platform:
        case OS.LINUX:
            for browser, desktop_entries in POSSIBLE_BROWSERS:
                for application_dir in BROWSER_LOCATIONS:
                    for desktop_entry in desktop_entries:
                        path = os.path.join(application_dir, f"{desktop_entry}.desktop")
                        if not os.path.isfile(path):
                            continue
                        entry = DesktopEntry(path)
                        executable_path = entry.getExec()
                        if executable_path.lower().endswith(" %u"):
                            executable_path = executable_path[:-3].strip()
                        version = subprocess.getoutput(f"{executable_path} --version 2>&1").strip()
                        match = VERSION_PATTERN.search(version)
                        if match:
                            version = match[0]
                        yield Browser(
                            name=browser, description=entry.getName(), version=version, location=executable_path
                        )


# get details of a browser
def get_details_of(name) -> Optional[Browser]:
    match sys.platform:
        case OS.LINUX:
            for browser, desktop_names in (browser_record for browser_record in POSSIBLE_BROWSERS
                                           if browser_record[0] == name):
                for desktop_name in desktop_names:
                    for application_dir in BROWSER_LOCATIONS:
                        path = os.path.join(application_dir, f"{desktop_name}.desktop")
                        if not os.path.isfile(path):
                            continue
                        entry = DesktopEntry(path)
                        executable_path = entry.getExec()
                        if executable_path.lower().endswith(" %u"):
                            executable_path = executable_path[:-3].strip()
                        version = subprocess.getoutput(f"{executable_path} --version 2>&1").strip()
                        match = VERSION_PATTERN.search(version)
                        if match:
                            version = match[0]
                        yield Browser(
                            name=browser, description=entry.getName(), version=version, location=executable_path
                        )


# retrieve browser version
def get_version_of(name) -> Optional[Version]:
    match sys.platform:
        case OS.LINUX:
            for browser, desktop_names in (browser_record for browser_record in POSSIBLE_BROWSERS
                                           if browser_record[0] == name):
                for desktop_name in desktop_names:
                    for application_dir in BROWSER_LOCATIONS:
                        path = os.path.join(application_dir, f"{desktop_name}.desktop")
                        if not os.path.isfile(path):
                            continue
                        entry = DesktopEntry(path)
                        executable_path = entry.getExec()
                        if executable_path.lower().endswith(" %u"):
                            executable_path = executable_path[:-3].strip()
                        version = subprocess.getoutput(f"{executable_path} --version 2>&1").strip()
                        match = VERSION_PATTERN.search(version)
                        if match:
                            version = match[0]
                        yield Version(
                            version=version
                        )
            yield "Browser is not installed."


# check if the given browser is installed
def do_i_have_installed(name):
    match sys.platform:
        case OS.LINUX:
            for browser, desktop_names in (browser_record for browser_record in POSSIBLE_BROWSERS
                                           if browser_record[0] == name):
                for desktop_name in desktop_names:
                    for application_dir in BROWSER_LOCATIONS:
                        path = os.path.join(application_dir, f"{desktop_name}.desktop")
                        if not os.path.isfile(path):
                            continue
                        entry = DesktopEntry(path)
                        if entry:
                            return True
            return False


# get default browser
def what_is_the_default_browser() -> Optional[str]:
    match sys.platform:
        case OS.LINUX:
            cmd = "xdg-settings get default-web-browser".split()
            if cmd:
                default_browser = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().strip()
            else:
                default_browser = "No browser is set to default."
            return default_browser
