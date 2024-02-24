import sys
from typing import Dict
from unittest.mock import ANY
from unittest.mock import Mock
from unittest.mock import patch

import pytest

import installed_browsers
from installed_browsers.common import OS

"""
These tests are based on which browsers exist in GitHub Actions virtual environments.
"""

DEFAULT_BROWSER_LINUX = "firefox_firefox.desktop"
DEFAULT_BROWSER_MAC = "Firefox"
DEFAULT_BROWSER_WINDOWS = "Microsoft Edge"
BROWSER_FIREFOX = "Mozilla Firefox"
BROWSER_CHROME_CANARY = "Google Chrome Canary"
BROWSER_EDGE = "Microsoft Edge"
NO_DEFAULT_BROWSER = "No browser is set to default."
BROWSER_NOT_INSTALLED = "Browser is not installed."
OPERATING_SYSTEM_NOT_SUPPORTED = "This operating system is not yet supported."

# winreg should be mocked for linux and mac
match sys.platform:
    case OS.LINUX | OS.MAC:
        MockWinreg = Mock()
        MockWinreg.QueryValueEx.return_value = dict(dummy="dummy")


@pytest.mark.parametrize(
    "browser",
    (
        pytest.param("chrome", id="chrome"),
        pytest.param("chromium", id="chromium"),
        pytest.param("firefox", id="firefox"),
        pytest.param("safari", id="safari",
                     marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only")),
        pytest.param(
            "msedge", id="msedge",
            marks=pytest.mark.skipif(sys.platform == "linux", reason="mac-and-windows-only")
        ),
        pytest.param("msie", id="msie",
                     marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only")),
        pytest.param("dummy_browser", id="dummy_browser"),
    ),
)
class TestBrowserInstallation:
    def test_installed_browsers(self, browser: str) -> None:
        available_browsers = [individual_browser["name"] for individual_browser in installed_browsers.browsers()]
        if browser in available_browsers:
            assert browser in available_browsers
        else:
            assert browser not in available_browsers

    def test_browser_is_installed_or_not(self, browser: str) -> None:
        available_browsers = [individual_browser["name"] for individual_browser in installed_browsers.browsers()]
        if browser in available_browsers:
            assert installed_browsers.do_i_have_installed(browser)
        else:
            assert not installed_browsers.do_i_have_installed(browser)


@patch("sys.platform", "BDS")
def test_os_is_not_supported() -> None:
    for browsers in installed_browsers.browsers():
        assert browsers['description'] == OPERATING_SYSTEM_NOT_SUPPORTED


@pytest.mark.parametrize(
    "browser",
    (
        pytest.param(
            b'firefox_firefox.desktop', id="default_firefox_linux",
            marks=pytest.mark.skipif(sys.platform != "linux", reason="linux-only")
        ),
        pytest.param(
            {'LSHandlers': [{'LSHandlerURLScheme': 'https', 'LSHandlerRoleAll': 'org.mozilla.firefox',
                             'LSHandlerPreferredVersions': {'LSHandlerRoleAll': '-'}}]},
            id="default_firefox_mac", marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only")
        ),
        pytest.param(
            "Microsoft Edge", id="default_edge_windows",
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only")
        ),
        pytest.param(
            "Mozilla Firefox", id="default_firefox_windows",
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only")
        ),
        pytest.param(
            "Google Chrome Canary", id="default_canary_windows",
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only")
        ),
    ),
)
@patch("plistlib.load")
@patch("subprocess.check_output")
@patch.dict("sys.modules", winreg=MockWinreg)
@patch('winreg.QueryValueEx')
def test_default_browser(mock_winreg, mock_subprocess, mock_load, browser) -> None:
    match sys.platform:
        case OS.LINUX:
            mock_subprocess.return_value = browser
            assert installed_browsers.what_is_the_default_browser() == DEFAULT_BROWSER_LINUX
        case OS.MAC:
            mock_load.return_value = browser
            assert installed_browsers.what_is_the_default_browser() == DEFAULT_BROWSER_MAC
        case OS.WINDOWS:
            if browser == BROWSER_FIREFOX:
                mock_winreg.return_value = ("FirefoxURL-308046B0AF4A39CB", 0)
                assert installed_browsers.what_is_the_default_browser() == "Mozilla Firefox"
            elif browser == BROWSER_CHROME_CANARY:
                mock_winreg.return_value = ("ChromeSSHTM.308046B0AF4A39CB", 0)
                assert installed_browsers.what_is_the_default_browser() == "Google Chrome Canary"
            elif browser == BROWSER_EDGE:
                mock_winreg.return_value = ("MSEdgeHTM", 0)
                assert installed_browsers.what_is_the_default_browser() == DEFAULT_BROWSER_WINDOWS


@pytest.mark.parametrize(
    "browser",
    (
        pytest.param(
            b'', id="no_default_linux",
            marks=pytest.mark.skipif(sys.platform != "linux", reason="linux-only")
        ),
        pytest.param(
            {'LSHandlers': [{'LSHandlerURLScheme': 'https', 'LSHandlerRoleAll': '',
                             'LSHandlerPreferredVersions': {'LSHandlerRoleAll': '-'}}]},
            id="no_default_mac", marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only")
        ),
        pytest.param(
            ("", 0), id="no_default_windows",
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only")
        ),
    ),
)
@patch("plistlib.load")
@patch("subprocess.check_output")
@patch.dict("sys.modules", winreg=MockWinreg)
@patch('winreg.QueryValueEx')
def test_no_default_browser(mock_winreg, mock_check_output, mock_load, browser) -> None:
    match sys.platform:
        case OS.LINUX:
            mock_check_output.return_value = browser
        case OS.MAC:
            mock_load.return_value = browser
        case OS.WINDOWS:
            mock_winreg.return_value = browser
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
            id="chrome_mac",
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
            id="firefox_mac",
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
            id="safari_mac",
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
            id="msedge_mac",
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
            id="chrome_linux",
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
            id="chromium_linux",
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
            id="firefox_linux",
        ),
        pytest.param(
            "chrome",
            {
                "name": "chrome",
                "description": "Google Chrome",
                "version": ANY,
                "location": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            },
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only"),
            id="chrome_windows",
        ),
        pytest.param(
            "firefox",
            {
                "name": "firefox",
                "description": "Mozilla Firefox",
                "version": ANY,
                "location": r"C:\Program Files\Mozilla Firefox\firefox.exe",
            },
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only"),
            id="firefox_windows",
        ),
        pytest.param(
            "msedge",
            {
                "name": "msedge",
                "description": "Microsoft Edge",
                "version": ANY,
                "location": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            },
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only"),
            id="msedge_windows",
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
            id="msie_windows",
        ),
        pytest.param(
            "dummy_browser",
            {
                "version": ANY,
            },
            id="dummy_browser",
        ),
    ),
)
def test_get_browser_details(browser: str, details: Dict) -> None:
    available_browsers = [individual_browser["name"] for individual_browser in installed_browsers.browsers()]
    if browser in available_browsers:
        assert installed_browsers.give_me_details_of(browser) == details
    else:
        assert installed_browsers.give_me_details_of(browser) == BROWSER_NOT_INSTALLED


@pytest.mark.parametrize(
    ("browser", "version"),
    (
        pytest.param(
            "chrome",
            {
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only"),
            id="chrome_mac",
        ),
        pytest.param(
            "firefox",
            {
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only"),
            id="firefox_mac",
        ),
        pytest.param(
            "safari",
            {
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only"),
            id="safari_mac",
        ),
        pytest.param(
            "msedge",
            {
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform == "linux", reason="mac-and-windows-only"),
            id="msedge_mac_windows",
        ),
        pytest.param(
            "chrome",
            {
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "linux", reason="linux-only"),
            id="chrome_linux",
        ),
        pytest.param(
            "chromium",
            {
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "linux", reason="linux-only"),
            id="chromium_linux",
        ),
        pytest.param(
            "firefox",
            {
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "linux", reason="linux-only"),
            id="firefox_linux",
        ),
        pytest.param(
            "chrome",
            {
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only"),
            id="chrome_windows",
        ),
        pytest.param(
            "firefox",
            {
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only"),
            id="firefox_windows",
        ),
        pytest.param(
            "msie",
            {
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only"),
            id="msie_windows",
        ),
        pytest.param(
            "dummy_browser",
            {
                "version": ANY,
            },
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only"),
            id="dummy_windows",
        ),
    ),
)
class TestBrowserVersion:
    def test_version_of_browser(self, browser: str, version: Dict) -> None:
        available_browsers = [individual_browser["name"] for individual_browser in installed_browsers.browsers()]
        if browser in available_browsers:
            assert installed_browsers.get_version_of(browser) == version

    @patch("subprocess.getoutput")
    @patch("os.path.isfile")
    @patch.dict("sys.modules", winreg=MockWinreg)
    @patch("winreg.QueryValue")
    def test_version_not_determined(self, mock_winreg, mock_file, mock_output, browser: str, version: Dict) -> None:
        match sys.platform:
            case OS.LINUX:
                mock_file.return_value = False
            case OS.MAC:
                mock_output.return_value = ""
            case OS.WINDOWS:
                mock_winreg.return_value = "dummy"

        # mock_version = Mock()
        # mock_version.return_value = version
        assert installed_browsers.get_version_of(browser) == BROWSER_NOT_INSTALLED
