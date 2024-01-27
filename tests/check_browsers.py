import subprocess
import sys
from typing import Dict
from unittest.mock import ANY
from unittest.mock import Mock
from unittest.mock import MagicMock, patch

import mock
import pytest

import installed_browsers

"""
These tests are based on what browsers exists in Github Actions virtual environments.
"""

DEFAULT_BROWSER = "firefox_firefox.desktop"
NO_DEFAULT_BROWSER = "No browser is set to default."
BROWSER_NOT_INSTALLED = "Browser is not installed."
OPERATING_SYSTEM_NOT_SUPPORTED = "This operating system is not yet supported."


@pytest.mark.parametrize(
    "browser",
    (
        pytest.param("chrome", id="chrome"),
        pytest.param("firefox", id="firefox"),
        pytest.param("safari", id="safari", marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only")),
        pytest.param(
            "msedge", id="msedge", marks=pytest.mark.skipif(sys.platform == "linux", reason="mac-and-windows-only")
        ),
        pytest.param("msie", id="msie", marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only")),
    ),
)
class TestBrowserInstallation:
    def test_installed_browsers(self, browser: str) -> None:
        available_browsers = [individual_browser["name"] for individual_browser in installed_browsers.browsers()]
        assert browser in available_browsers

    def test_browser_is_installed(self, browser: str) -> None:
        assert installed_browsers.do_i_have_installed(browser)

    @patch("os.path.isfile")
    def test_browser_is_not_installed(self, mock_isfile, browser: str) -> None:
        mock_isfile.return_value = False
        assert not installed_browsers.do_i_have_installed(browser)


@patch("sys.platform", "BDS")
def test_os_is_not_supported() -> None:
    for browsers in installed_browsers.browsers():
        assert browsers['description'] == OPERATING_SYSTEM_NOT_SUPPORTED


# @pytest.mark.parametrize(
#     "browser",
#     (
#         pytest.param("chrome", id="chrome"),
#         pytest.param("firefox", id="firefox"),
#         pytest.param("safari", id="safari", marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only")),
#         pytest.param(
#             "msedge", id="msedge", marks=pytest.mark.skipif(sys.platform == "linux", reason="mac-and-windows-only")
#         ),
#         pytest.param("msie", id="msie", marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only")),
#     ),
# )
# def test_installed_browser_existence(browser: str) -> None:
#     available_browsers = [individual_browser["name"] for individual_browser in installed_browsers.browsers()]
#     assert browser in available_browsers
#
#
# @pytest.mark.parametrize(
#     "browser",
#     (
#         pytest.param("chrome", id="chrome"),
#         pytest.param("firefox", id="firefox"),
#         pytest.param("safari", id="safari", marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only")),
#         pytest.param(
#             "msedge", id="msedge", marks=pytest.mark.skipif(sys.platform == "linux", reason="mac-and-windows-only")
#         ),
#         pytest.param("msie", id="msie", marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only")),
#     ),
# )
# def test_browser_is_installed(browser: str) -> None:
#     assert installed_browsers.do_i_have_installed(browser)
#
#
# @pytest.mark.parametrize(
#     "browser",
#     (
#         pytest.param("chrome", id="chrome"),
#         pytest.param("firefox", id="firefox"),
#         pytest.param("safari", id="safari", marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only")),
#         pytest.param(
#             "msedge", id="msedge", marks=pytest.mark.skipif(sys.platform == "linux", reason="mac-and-windows-only")
#         ),
#         pytest.param("msie", id="msie", marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only")),
#     ),
# )
# @patch("os.path.isfile")
# def test_browser_is_not_installed(mock_isfile, browser: str) -> None:
#     mock_isfile.return_value = False
#     assert not installed_browsers.do_i_have_installed(browser)


@pytest.mark.parametrize(
    "browser",
    (
        pytest.param(b'firefox_firefox.desktop', id="firefox"),
    ),
)
@patch("subprocess.check_output")
def test_default_browser_is_firefox(mock_subprocess, browser) -> None:
    mock_subprocess.return_value = browser
    assert installed_browsers.what_is_the_default_browser() == DEFAULT_BROWSER


@pytest.mark.parametrize(
    "browser",
    (
        pytest.param(b'', id="firefox"),
    ),
)
@patch("subprocess.check_output")
def test_no_default_browser(mock_subprocess, browser) -> None:
    mock_subprocess.return_value = browser
    assert installed_browsers.what_is_the_default_browser() == NO_DEFAULT_BROWSER


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
            marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only"),
            id="chrome-mac",
        ),
        pytest.param(
            "firefox",
            {
                "name": "firefox",
                "description": "Firefox",
                "version": ANY,
                "location": "/Applications/Firefox.app/Contents/MacOS/firefox"
            },
            marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only"),
            id="firefox-mac",
        ),
        pytest.param(
            "safari",
            {
                "name": "safari",
                "description": "Safari",
                "version": ANY,
                "location": "/Applications/Safari.app"
            },
            marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only"),
            id="safari-mac",
        ),
        pytest.param(
            "msedge",
            {
                "name": "msedge",
                "description": "Microsoft Edge",
                "version": ANY,
                "location": "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
            },
            marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only"),
            id="msedge-mac",
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
            "chromium",
            {
                "name": "chromium",
                "description": "Chromium Web Browser",
                "version": ANY,
                "location": ANY
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
def test_get_browser_details(browser: str, details: Dict) -> None:
    assert installed_browsers.give_me_details_of(browser) == details


@pytest.mark.parametrize(
    ("browser", "version"),
    (
        pytest.param(
            "chrome",
            {
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only"),
            id="chrome-mac",
        ),
        pytest.param(
            "firefox",
            {
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only"),
            id="firefox-mac",
        ),
        pytest.param(
            "safari",
            {
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only"),
            id="safari-mac",
        ),
        pytest.param(
            "msedge",
            {
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only"),
            id="msedge-mac",
        ),
        pytest.param(
            "chrome",
            {
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "linux", reason="linux-only"),
            id="chrome-linux",
        ),
        pytest.param(
            "chromium",
            {
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "linux", reason="linux-only"),
            id="chromium-linux",
        ),
        pytest.param(
            "firefox",
            {
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "linux", reason="linux-only"),
            id="firefox-linux",
        ),
        pytest.param(
            "chrome",
            {
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only"),
            id="chrome-win32",
        ),
        pytest.param(
            "firefox",
            {
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only"),
            id="firefox-win32",
        ),
        pytest.param(
            "msedge",
            {
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only"),
            id="msedge-win32",
        ),
        pytest.param(
            "msie",
            {
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only"),
            id="msie-win32",
        ),
    ),
)
class TestBrowserVersion:
    def test_version_of_browser(self, browser: str, version: Dict) -> None:
        assert installed_browsers.get_version_of(browser) == version

    @patch("os.path.isfile")
    def test_version_not_determined(self, mock_file, browser: str, version: Dict) -> None:
        mock_file.return_value = False
        assert installed_browsers.get_version_of(browser) == BROWSER_NOT_INSTALLED

#
# @pytest.mark.parametrize(
#     ("browser", "version"),
#     (
#         pytest.param(
#             "chrome",
#             {
#                 "version": ANY,
#             },
#             marks=pytest.mark.skipif(sys.platform != "linux", reason="linux-only"),
#             id="chrome-linux",
#         ),
#     )
# )
# def test_version_of_browser(browser: str, version: Dict) -> None:
#     assert installed_browsers.get_version_of(browser) == version
#
#
# @pytest.mark.parametrize(
#     ("browser", "version"),
#     (
#         pytest.param(
#             "chrome",
#             {
#                 "version": ANY,
#             },
#             marks=pytest.mark.skipif(sys.platform != "linux", reason="linux-only"),
#             id="chrome-linux",
#         ),
#     )
# )
# @patch("os.path.isfile")
# def test_version_not_determined(mock_file, browser: str, version: Dict) -> None:
#     mock_file.return_value = False
#     assert installed_browsers.get_version_of(browser) == BROWSER_NOT_INSTALLED

