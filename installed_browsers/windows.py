import os
import sys
from typing import Iterator
# import winreg

from .common import Browser, Version, OS

# tuple of possible browsers
POSSIBLE_BROWSERS = {
    "Google Chrome": "chrome",
    "Google Chrome Canary": "chrome-canary",
    "Chromium": "chromium",
    "Mozilla Firefox": "firefox",
    "Firefox Developer Edition": "firefox-developer",
    "Firefox Nightly": "firefox-nightly",
    "Opera Stable": "opera",
    "Opera beta": "opera-beta",
    "Opera developer": "opera-developer",
    "Microsoft Edge": "msedge",
    "Microsoft Edge Beta": "msedge-beta",
    "Microsoft Edge Dev": "msedge-dev",
    "Microsoft Edge Canary": "msedge-canary",
    "Internet Explorer": "msie",
    "Brave": "brave",
    "Brave Beta": "brave-beta",
    "Brave Nightly": "brave-nightly",
}


# get all installed browsers
def browsers() -> Iterator[Browser]:
    match sys.platform:
        case OS.WINDOWS:
            import winreg
            yield from _win32_browsers_from_registry(winreg.HKEY_CURRENT_USER, winreg.KEY_READ)
            yield from _win32_browsers_from_registry(winreg.HKEY_LOCAL_MACHINE,
                                                     winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
            yield from _win32_browsers_from_registry(winreg.HKEY_LOCAL_MACHINE,
                                                     winreg.KEY_READ | winreg.KEY_WOW64_32KEY)


# get browsers from registry
def _win32_browsers_from_registry(tree: int, access: int) -> Iterator[Browser]:
    match sys.platform:
        case OS.WINDOWS:
            import winreg
            try:
                with winreg.OpenKey(tree, r"Software\Clients\StartMenuInternet", access=access) as hkey:
                    i = 0
                    while True:
                        try:
                            subkey = winreg.EnumKey(hkey, i)
                            i += 1
                        except OSError:
                            break
                        try:
                            description = winreg.QueryValue(hkey, subkey)
                            if not description or not isinstance(description, str):  # pragma: no cover
                                description = subkey
                        except OSError:  # pragma: no cover
                            description = subkey
                        try:
                            cmd = winreg.QueryValue(hkey, rf"{subkey}\shell\open\command")
                            cmd = cmd.strip('"')
                            os.stat(cmd)
                        except (OSError, AttributeError, TypeError, ValueError):  # pragma: no cover
                            continue
                        yield Browser(
                            name=POSSIBLE_BROWSERS.get(description, "unknown"),
                            description=description,
                            version="Not yet supported.",
                            # version=_get_file_version(cmd),
                            location=cmd
                        )
            except FileNotFoundError:
                pass


# get browser version
# def _get_file_version(path: str) -> str:
#     import win32api
#
#     info = win32api.GetFileVersionInfo(path, "\\")
#     ms = info["FileVersionMS"]
#     ls = info["FileVersionLS"]
#     return ".".join(map(str, (win32api.HIWORD(ms), win32api.LOWORD(ms), win32api.HIWORD(ls), win32api.LOWORD(ls))))
