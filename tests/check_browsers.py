import sys
from typing import Dict
from unittest.mock import ANY

import pytest

import installed_browsers

"""
These tests are based on what browsers exists in Github Actions virtual environments.
"""


@pytest.mark.parametrize(
    "browser",
    (
        pytest.param("chrome", id="chrome"),
        pytest.param("firefox", id="firefox"),
        pytest.param("safari", id="safari", marks=pytest.mark.skipif(sys.platform != "darwin", reason="osx-only")),
        pytest.param(
            "msedge", id="msedge", marks=pytest.mark.skipif(sys.platform == "linux", reason="osx-and-windows-only")
        ),
        pytest.param("msie", id="msie", marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only")),
    ),
)
def test_browsers(browser: str) -> None:
    available_browsers = [b["name"] for b in installed_browsers.browsers()]
    assert browser in available_browsers


@pytest.mark.parametrize(
    ("browser", "details"),
    (
        pytest.param(
            "chrome",
            {
                "name": "chrome",
                "description": "Google Chrome",
                "version": ANY,
                "location": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            },
            marks=pytest.mark.skipif(sys.platform != "darwin", reason="osx-only"),
            id="chrome-osx",
        ),
        pytest.param(
            "firefox",
            {
                "name": "firefox",
                "description": "Firefox",
                "version": ANY,
                "location": "/Applications/Firefox.app/Contents/MacOS/firefox"
            },
            marks=pytest.mark.skipif(sys.platform != "darwin", reason="osx-only"),
            id="firefox-osx",
        ),
        pytest.param(
            "safari",
            {
                "name": "safari",
                "description": "Safari",
                "version": ANY,
                "location": "/Applications/Safari.app"
            },
            marks=pytest.mark.skipif(sys.platform != "darwin", reason="osx-only"),
            id="safari-osx",
        ),
        pytest.param(
            "msedge",
            {
                "name": "msedge",
                "description": "Microsoft Edge",
                "version": ANY,
                "location": "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
            },
            marks=pytest.mark.skipif(sys.platform != "darwin", reason="osx-only"),
            id="msedge-osx",
        ),
        pytest.param(
            "chrome",
            {
                "name": "chrome",
                "description": "Google Chrome",
                "version": ANY,
                "location": "/usr/bin/google-chrome-stable"
            },
            marks=pytest.mark.skipif(sys.platform != "linux", reason="linux-only"),
            id="chrome-linux",
        ),
        pytest.param(
            "firefox",
            {
                "name": "firefox",
                "description": "Firefox Web Browser",
                "version": ANY,
                "location": "firefox"
            },
            marks=pytest.mark.skipif(sys.platform != "linux", reason="linux-only"),
            id="firefox-linux",
        ),
        pytest.param(
            "chrome",
            {
                "browser_type": "chrome",
                "display_name": "Google Chrome",
                "path": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only"),
            id="chrome-win32",
        ),
        pytest.param(
            "firefox",
            {
                "browser_type": "firefox",
                "display_name": "Mozilla Firefox",
                "path": r"C:\Program Files\Mozilla Firefox\firefox.exe",
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only"),
            id="firefox-win32",
        ),
        pytest.param(
            "msedge",
            {
                "browser_type": "msedge",
                "display_name": "Microsoft Edge",
                "path": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only"),
            id="msedge-win32",
        ),
        pytest.param(
            "msie",
            {
                "name": "msie",
                "description": "Internet Explorer",
                "version": ANY,
                "location": r"C:\Program Files\Internet Explorer\iexplore.exe"
            },
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only"),
            id="msie-win32",
        ),
    ),
)
def test_get(browser: str, details: Dict) -> None:
    assert installed_browsers.give_me_details_of(browser) == details
