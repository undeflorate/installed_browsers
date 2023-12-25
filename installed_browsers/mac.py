import os
import plistlib
import subprocess
import sys
from typing import Iterator, Optional

from .common import Browser, Version, OS

# tuple of possible browsers
POSSIBLE_BROWSERS = (
    ("chrome", "com.google.Chrome", "KSVersion"),
    ("chrome-canary", "com.google.Chrome.canary", "KSVersion"),
    ("chromium", "org.chromium.Chromium", "CFBundleShortVersionString"),
    ("firefox", "org.mozilla.firefox", "CFBundleShortVersionString"),
    ("firefox-developer", "org.mozilla.firefoxdeveloperedition", "CFBundleShortVersionString"),
    ("firefox-nightly", "org.mozilla.nightly", "CFBundleShortVersionString"),
    ("safari", "com.apple.Safari", "CFBundleShortVersionString"),
    ("opera", "com.operasoftware.Opera", "CFBundleVersion"),
    ("opera-beta", "com.operasoftware.OperaNext", "CFBundleVersion"),
    ("opera-developer", "com.operasoftware.OperaDeveloper", "CFBundleVersion"),
    ("msedge", "com.microsoft.edgemac", "CFBundleVersion"),
    ("msedge-beta", "com.microsoft.edgemac.Beta", "CFBundleVersion"),
    ("msedge-dev", "com.microsoft.edgemac.Dev", "CFBundleVersion"),
    ("msedge-canary", "com.microsoft.edgemac.Canary", "CFBundleVersion"),
    ("brave", "com.brave.Browser", "CFBundleVersion"),
    ("brave-beta", "com.brave.Browser.beta", "CFBundleVersion"),
    ("brave-dev", "com.brave.Browser.dev", "CFBundleVersion"),
    ("brave-nightly", "com.brave.Browser.nightly", "CFBundleVersion"),
)


# get all installed browsers
def browsers() -> Iterator[Browser]:
    match sys.platform:
        case OS.MAC:
            for browser, bundle_id, version_string in POSSIBLE_BROWSERS:
                paths = subprocess.getoutput(f'mdfind "kMDItemCFBundleIdentifier == {bundle_id}"').splitlines()
                for path in paths:
                    with open(os.path.join(path, "Contents/Info.plist"), "rb") as f:
                        plist = plistlib.load(f)
                        executable_name = plist.get("CFBundleExecutable")
                        executable = os.path.join(path, "Contents/MacOS", executable_name)
                        description = plist.get("CFBundleDisplayName") or plist.get("CFBundleName", browser)
                        version = plist[version_string]
                        yield Browser(
                            name=browser,
                            description=description,
                            version=version,
                            location=executable if browser != "safari" else path
                        )


# get details of a browser
def get_details_of(name) -> Optional[Browser]:
    match sys.platform:
        case OS.MAC:
            for browser, bundle_id, version_string in (browser_record for browser_record in POSSIBLE_BROWSERS
                                                       if browser_record[0] == name):
                paths = subprocess.getoutput(f'mdfind "kMDItemCFBundleIdentifier == {bundle_id}"').splitlines()
                for path in paths:
                    with open(os.path.join(path, "Contents/Info.plist"), "rb") as f:
                        plist = plistlib.load(f)
                        executable_name = plist.get("CFBundleExecutable")
                        executable = os.path.join(path, "Contents/MacOS", executable_name)
                        description = plist.get("CFBundleDisplayName") or plist.get("CFBundleName", browser)
                        version = plist[version_string]
                        yield Browser(
                            name=browser,
                            description=description,
                            version=version,
                            location=executable if browser != "safari" else path
                        )


# retrieve browser version
def get_version_of(name) -> Optional[Version]:
    match sys.platform:
        case OS.MAC:
            for browser, bundle_id, version_string in (browser_record for browser_record in POSSIBLE_BROWSERS
                                                       if browser_record[0] == name):
                paths = subprocess.getoutput(f'mdfind "kMDItemCFBundleIdentifier == {bundle_id}"').splitlines()
                for path in paths:
                    with open(os.path.join(path, "Contents/Info.plist"), "rb") as f:
                        plist = plistlib.load(f)
                        version = plist[version_string]
                        yield Version(
                            version=version
                        )
            yield "Browser is not installed."


# check if the given browser is installed
def do_i_have_installed(name):
    match sys.platform:
        case OS.MAC:
            for browser, bundle_id, version_string in (browser_record for browser_record in POSSIBLE_BROWSERS
                                                       if browser_record[0] == name):
                paths = subprocess.getoutput(f'mdfind "kMDItemCFBundleIdentifier == {bundle_id}"').splitlines()
                for path in paths:
                    with open(os.path.join(path, "Contents/Info.plist"), "rb") as f:
                        plist = plistlib.load(f)
                        executable_name = plist.get("CFBundleExecutable")
                        if executable_name:
                            return True
            return False


# get default browser
def what_is_the_default_browser() -> Optional[str]:
    match sys.platform:
        case OS.MAC:
            # cmd = "xdg-settings get default-web-browser".split()
            # if cmd:
            #     default_browser = subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode().strip()
            # else:
            #     default_browser = "No browser is set to default."
            # return default_browser
            return "This function is not yet supported."
