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
For Firefox in Mac, system can not make any difference between stable and beta version other than the application name.
Beta version is not supported officially.
For proper working, make sure that either stable or beta version is installed but not both.
"""

# constant declaration
DEFAULT_BROWSER_LINUX = "Firefox Web Browser"
DEFAULT_BROWSER_MAC = "Firefox"
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
    case OS.WINDOWS:
        import winreg
        MockWinreg = winreg


# check if given browser is installed in system
@pytest.mark.parametrize(
    "browser",
    (
        pytest.param(["chrome", "Google Chrome"], id="chrome"),
        pytest.param(["chromium", "Chromium"], id="chromium"),
        pytest.param(["firefox", "Mozilla Firefox"], id="firefox"),
        pytest.param(["safari", "Safari"], id="safari",
                     marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only")),
        pytest.param(
            ["msedge", "Microsoft Edge"], id="msedge",
            marks=pytest.mark.skipif(sys.platform == "linux", reason="mac-and-windows-only")
        ),
        pytest.param(["msie", "Internet Explorer"], id="msie",
                     marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only")),
        pytest.param(["dummy_browser", "Dummy Browser"], id="dummy_browser"),
    ),
)
class TestBrowserInstallation:
    def test_installed_browsers(self, browser: str):
        available_browsers = [individual_browser["name"] for individual_browser in installed_browsers.browsers()]
        if browser[0] in available_browsers:
            assert browser[0] in available_browsers
        else:
            assert browser[0] not in available_browsers

    @patch("winreg.QueryValue")
    def test_browser_is_installed_or_not(self, mock_winreg_qv, browser: str):
        available_browsers = [individual_browser["name"] for individual_browser in installed_browsers.browsers()]
        match sys.platform:
            case OS.WINDOWS:
                mock_winreg_qv.return_value = browser[1]
                if browser[0] in installed_browsers.windows.POSSIBLE_BROWSER_NAMES:
                    assert installed_browsers.do_i_have_installed(browser[0])
                else:
                    assert not installed_browsers.do_i_have_installed(browser[0])
            case _:
                if browser[0] in available_browsers:
                    assert installed_browsers.do_i_have_installed(browser[0])
                else:
                    assert not installed_browsers.do_i_have_installed(browser[0])
        #     available_browsers = [individual_browser["name"] for individual_browser in installed_browsers.browsers()]
        #     print(installed_browsers.do_i_have_installed("chromium"), "chromium")
        #     if browser in available_browsers:
        #         assert installed_browsers.do_i_have_installed(browser)
        #     else:
        #         assert not installed_browsers.do_i_have_installed(browser)


# only linux, mac and windows operating systems are supported
@patch("sys.platform", "BDS")
def test_os_is_not_supported():
    for browsers in installed_browsers.browsers():
        assert browsers['description'] == OPERATING_SYSTEM_NOT_SUPPORTED


# check default browser
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
@patch("os.path.isfile")
@patch("xdg.DesktopEntry.DesktopEntry.getName")
@patch("subprocess.getoutput")
@patch.dict("sys.modules", winreg=MockWinreg)
@patch('winreg.QueryValueEx')
@patch('winreg.QueryValue')
def test_default_browser(mock_winreg_qv, mock_winreg_qve, mock_subprocess_get,
                         mock_desktopentry, mock_isfile, mock_subprocess_check, mock_load, browser):
    match sys.platform:
        case OS.LINUX:
            mock_subprocess_check.return_value = browser
            mock_isfile.return_value = True
            mock_desktopentry.return_value = DEFAULT_BROWSER_LINUX
            assert installed_browsers.what_is_the_default_browser() == DEFAULT_BROWSER_LINUX
        case OS.MAC:
            mock_load.side_effect = [browser, {'CFBundleExecutable': 'firefox'}]
            mock_subprocess_get.return_value = '/Applications/Firefox.app'
            assert installed_browsers.what_is_the_default_browser() == DEFAULT_BROWSER_MAC
        case OS.WINDOWS:
            if browser == BROWSER_FIREFOX:
                mock_winreg_qve.return_value = ["FirefoxURL-308046B0AF4A39CB"]
                mock_winreg_qv.return_value = BROWSER_FIREFOX
                assert installed_browsers.what_is_the_default_browser() == BROWSER_FIREFOX
            elif browser == BROWSER_CHROME_CANARY:
                mock_winreg_qve.return_value = ["ChromeSSHTM.308046B0AF4A39CB"]
                mock_winreg_qv.return_value = BROWSER_CHROME_CANARY
                assert installed_browsers.what_is_the_default_browser() == BROWSER_CHROME_CANARY
            elif browser == BROWSER_EDGE:
                mock_winreg_qve.return_value = ["MSEdgeHTM"]
                mock_winreg_qv.return_value = BROWSER_EDGE
                assert installed_browsers.what_is_the_default_browser() == BROWSER_EDGE


# check missing default browser
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
            id="no_default_empty_mac", marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only")
        ),
        pytest.param(
            {'LSHandlers': [{'LSHandlerURLScheme': 'https', 'LSHandlerRoleAll': 'org.mozilla.firefox',
                             'LSHandlerPreferredVersions': {'LSHandlerRoleAll': '-'}}]},
            id="no_default_deleted_mac", marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only")
        ),
        pytest.param(
            [""], id="no_default_windows",
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only")
        ),
        pytest.param(
            ["ChromeSSHTM.308046B0AF4A39CB"], id="no_default_windows",
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only")
        ),
    ),
)
@patch("plistlib.load")
@patch("subprocess.check_output")
@patch.dict("sys.modules", winreg=MockWinreg)
@patch('winreg.QueryValueEx')
@patch('winreg.QueryValue')
def test_no_default_browser(mock_winreg_qv, mock_winreg_qve, mock_check_output, mock_load, browser):
    match sys.platform:
        case OS.LINUX:
            mock_check_output.return_value = browser
        case OS.MAC:
            mock_load.side_effect = [browser, {'CFBundleExecutable': ''}]
        case OS.WINDOWS:
            mock_winreg_qve.return_value = browser
            mock_winreg_qv.return_value = ""
    assert installed_browsers.what_is_the_default_browser() == NO_DEFAULT_BROWSER


# check browser details
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
                "location": ANY
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
                "name": ANY,
                "description": ANY,
                "version": ANY,
                "location": ANY,
            },
            id="dummy_browser",
        ),
    ),
)
def test_get_browser_details(browser: str, details: Dict):
    available_browsers = [individual_browser["name"] for individual_browser in installed_browsers.browsers()]
    if browser in available_browsers:
        assert installed_browsers.give_me_details_of(browser) == details
    else:
        assert installed_browsers.give_me_details_of(browser) == BROWSER_NOT_INSTALLED


# check browser version
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
            id="dummy_browser",
        ),
    ),
)
class TestBrowserVersion:
    def test_version_of_browser(self, browser: str, version: Dict):
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
        assert installed_browsers.get_version_of(browser) == BROWSER_NOT_INSTALLED
