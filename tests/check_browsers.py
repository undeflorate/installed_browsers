import builtins
import sys
from pathlib import Path
from typing import Dict
from unittest.mock import ANY, mock_open
from unittest.mock import Mock
from unittest.mock import patch

import pytest

import installed_browsers
from installed_browsers.common import OS

"""
These tests are based on the existing browsers of GitHub Actions virtual environments.
"""

# constant declaration
DEFAULT_BROWSER_LINUX = "Firefox"
DEFAULT_BROWSER_MAC = "Firefox"
DEFAULT_BROWSER_WINDOWS_FIREFOX = "Mozilla Firefox"
DEFAULT_BROWSER_WINDOWS_CHROME_CANARY = "Google Chrome Canary"
DEFAULT_BROWSER_WINDOWS_EDGE = "Microsoft Edge"
DEFAULT_BROWSER_WINDOWS_MIN = "Min"
DEFAULT_BROWSER_WINDOWS_DUCK = "DuckDuckGo"
DESKTOP_BROWSER = "DesktopBrowser"
NO_DEFAULT_BROWSER = "No browser is set to default."
BROWSER_NOT_INSTALLED = "Browser is not installed."
DEFAULT_BROWSER_NOT_SUPPORTED = "Default browser is not supported."
DUMMY_DEFAULT_BROWSER = "dummy.browser"
OPERATING_SYSTEM_NOT_SUPPORTED = "This operating system is not yet supported."

# winreg should be mocked for linux and mac
match sys.platform:
    case OS.LINUX | OS.MAC:
        MockWinreg = Mock()
        MockWinreg.QueryValueEx.return_value = dict(dummy="dummy")
        MockWin32API = Mock()
        MockWin32API.GetFileVersion.return_value = 666
    case OS.WINDOWS:
        import winreg, win32api
        MockWinreg = winreg
        MockWin32API = win32api


# check if given browser is installed in system
@pytest.mark.parametrize(
    ("browser", "description"),
    (
        pytest.param("chrome", "Google Chrome", id="chrome"),
        pytest.param("chromium", "Chromium", id="chromium"),
        pytest.param("firefox", "Mozilla Firefox", id="firefox"),
        pytest.param("safari", "Safari", id="safari",
                     marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only")),
        pytest.param(
            "msedge", "Microsoft Edge", id="msedge",
            marks=pytest.mark.skipif(sys.platform == "linux", reason="mac-and-windows-only")
        ),
        pytest.param("dummy_browser", "Dummy Browser", id="dummy_browser"),
    ),
)
class TestBrowserInstallation:
    def test_installed_browsers(self, browser: str, description: str):
        available_browsers = [individual_browser["name"] for individual_browser in installed_browsers.browsers()]
        if browser in available_browsers:
            assert browser in available_browsers
        else:
            assert browser not in available_browsers

    @patch.dict("sys.modules", winreg=MockWinreg)
    @patch("winreg.QueryValue")
    def test_browser_is_installed_or_not(self, mock_winreg_qv, browser: str, description: str):
        match sys.platform:
            case OS.LINUX | OS.MAC:
                available_browsers = [individual_browser["name"] for individual_browser in
                                      installed_browsers.browsers()]
                if browser in available_browsers:
                    assert installed_browsers.do_i_have_installed(browser)
                else:
                    assert not installed_browsers.do_i_have_installed(browser)
            case OS.WINDOWS:
                mock_winreg_qv.return_value = description
                if browser in installed_browsers.windows.POSSIBLE_BROWSER_NAMES:
                    assert installed_browsers.do_i_have_installed(browser)
                else:
                    assert not installed_browsers.do_i_have_installed(browser)


# check if duckduckgo browser is installed in windows
@pytest.mark.parametrize(
    ("browser", "description"),
    (
        pytest.param(
            "duckduckgo", "AppX", id="duckduckgo",
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only")
        ),
    ),
)
class TestDuckDuckGoWindowsInstallation:
    def test_installed_browsers(self, browser: str, description: str):
        available_browsers = [individual_browser["name"] for individual_browser in installed_browsers.browsers()]
        if browser in available_browsers:
            assert browser in available_browsers
        else:
            assert browser not in available_browsers

    @patch.dict("sys.modules", winreg=MockWinreg)
    @patch("winreg.OpenKey")
    @patch("winreg.QueryValue")
    @patch("winreg.QueryValueEx")
    @patch("winreg.EnumKey")
    def test_browser_is_installed_or_not(self, mock_winreg_ek, mock_winreg_qve, mock_winreg_qv, mock_winreg_ok, browser: str, description: str):
        match sys.platform:
            case OS.WINDOWS:
                mock_winreg_ok.return_value = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Classes")
                mock_winreg_qv.return_value = description
                mock_winreg_qve.return_value = [DESKTOP_BROWSER]
                mock_winreg_ek.return_value = description
                if browser in installed_browsers.windows.POSSIBLE_BROWSER_NAMES:
                    assert installed_browsers.do_i_have_installed(browser)
                else:
                    assert not installed_browsers.do_i_have_installed(browser)


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
            {'LSHandlers': [{'LSHandlerURLScheme': 'https', 'LSHandlerRoleAll': DUMMY_DEFAULT_BROWSER,
                             'LSHandlerPreferredVersions': {'LSHandlerRoleAll': '-'}}]},
            id="default_dummy_not_supported_mac", marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only")
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
        pytest.param(
            "Min", id="default_min_windows",
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only")
        ),
        pytest.param(
            "DuckDuckGo", id="default_duckduckgo_windows",
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
            if DEFAULT_BROWSER_MAC.lower() in str(browser):
                mock_load.side_effect = [browser, {'CFBundleExecutable': 'firefox'}]
                mock_subprocess_get.return_value = '/Applications/Firefox.app'
                # with patch("builtins.open", mock_open(), create=True):
                # with patch.object(Path, "open"):
                with patch.object(Path, "open"):
                    with patch.object(builtins, "open"):
                        assert installed_browsers.what_is_the_default_browser() == DEFAULT_BROWSER_MAC
            else:
                mock_load.side_effect = [browser, {'CFBundleExecutable': DUMMY_DEFAULT_BROWSER}]
                with patch.object(Path, "open"):
                    with patch.object(builtins, "open"):
                        assert installed_browsers.what_is_the_default_browser() == DEFAULT_BROWSER_NOT_SUPPORTED
        case OS.WINDOWS:
            if browser == DEFAULT_BROWSER_WINDOWS_FIREFOX:
                mock_winreg_qve.return_value = ["FirefoxURL-308046B0AF4A39CB"]
                mock_winreg_qv.return_value = DEFAULT_BROWSER_WINDOWS_FIREFOX
                assert installed_browsers.what_is_the_default_browser() == DEFAULT_BROWSER_WINDOWS_FIREFOX
            elif browser == DEFAULT_BROWSER_WINDOWS_CHROME_CANARY:
                mock_winreg_qve.return_value = ["ChromeSSHTM.308046B0AF4A39CB"]
                mock_winreg_qv.return_value = DEFAULT_BROWSER_WINDOWS_CHROME_CANARY
                assert installed_browsers.what_is_the_default_browser() == DEFAULT_BROWSER_WINDOWS_CHROME_CANARY
            elif browser == DEFAULT_BROWSER_WINDOWS_EDGE:
                mock_winreg_qve.return_value = ["MSEdgeHTM"]
                mock_winreg_qv.return_value = DEFAULT_BROWSER_WINDOWS_EDGE
                assert installed_browsers.what_is_the_default_browser() == DEFAULT_BROWSER_WINDOWS_EDGE
            elif browser == DEFAULT_BROWSER_WINDOWS_MIN:
                mock_winreg_qve.return_value = ["Min"]
                mock_winreg_qv.return_value = DEFAULT_BROWSER_WINDOWS_MIN
                assert installed_browsers.what_is_the_default_browser() == DEFAULT_BROWSER_WINDOWS_MIN


# check default duckduckgo
@pytest.mark.parametrize(
    "browser",
    (
        pytest.param(
            "DuckDuckGo", id="default_duckduckgo_windows",
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only")
        ),
    ),
)
@patch.dict("sys.modules", winreg=MockWinreg)
@patch('winreg.QueryValueEx')
@patch('winreg.QueryValue')
@patch('winreg.OpenKey')
def test_default_duckduckgo(mock_winreg_ok, mock_winreg_qv, mock_winreg_qve, browser):
    match sys.platform:
        case OS.WINDOWS:
            if browser == DEFAULT_BROWSER_WINDOWS_DUCK:
                mock_winreg_qve.side_effect = [['AppX'], [DEFAULT_BROWSER_WINDOWS_DUCK]]
                mock_winreg_qv.return_value = DEFAULT_BROWSER_WINDOWS_DUCK
                mock_winreg_ok.return_value = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Classes")
                assert installed_browsers.what_is_the_default_browser() == DEFAULT_BROWSER_WINDOWS_DUCK


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
            with patch.object(Path, "open"):
                assert installed_browsers.what_is_the_default_browser() == NO_DEFAULT_BROWSER
                return
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
                "description": "Firefox Web Browser", # rename for only Firefox after 17th January 2025
                "version": ANY,
                "location": "firefox"                 # change to ANY after 17th January 2025
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
                "location": r"C:\Program Files\Mozilla Firefox\firefox.exe",  # ANY
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
@patch.dict("sys.modules", winreg=MockWinreg, win32api=MockWin32API)
@patch("winreg.QueryValue")
@patch('win32api.GetFileVersionInfo')
@patch('os.stat')
def test_get_browser_details(mock_os_stat, mock_win32api_fileversion, mock_winreg_qv, browser: str, details: Dict):
    match sys.platform:
        case OS.LINUX | OS.MAC:
            available_browsers = [individual_browser["name"] for individual_browser in installed_browsers.browsers()]
            if browser in available_browsers:
                assert installed_browsers.give_me_details_of(browser) == details
            else:
                assert installed_browsers.give_me_details_of(browser) == BROWSER_NOT_INSTALLED
        case OS.WINDOWS:
            mock_winreg_qv.side_effect = [details["description"], details["location"]]
            mock_win32api_fileversion.return_value = {'FileVersionMS': 65536, 'FileVersionLS': 0}
            mock_os_stat.return_value = True
            if browser in installed_browsers.windows.POSSIBLE_BROWSER_NAMES:
                assert next(installed_browsers.give_me_details_of(browser)) == details
            else:
                assert installed_browsers.give_me_details_of(browser) == BROWSER_NOT_INSTALLED


# check browser details
@pytest.mark.parametrize(
    ("browser", "details"),
    (
        pytest.param(
            "duckduckgo",
            {
                "name": "duckduckgo",
                "description": "DuckDuckGo",
                "version": ANY,
                "location": r"C:\Program Files\WindowsApps\DuckDuckGo.DesktopBrowser_0.134.4.0_x64__ya2fgkz3nks94"
                            r"\WindowsBrowser\DuckDuckGo.exe",
            },
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only"),
            id="duckduckgo_windows",

        ),
    ),
)
@patch.dict("sys.modules", winreg=MockWinreg)
@patch("winreg.QueryValueEx")
@patch("winreg.QueryValue")
@patch('winreg.OpenKey')
@patch('winreg.EnumKey')
@patch('win32api.GetFileVersionInfo')
@patch('os.stat')
def test_get_duckduckgo_details(mock_os_stat, mock_win32api_fileversion, mock_winreg_ek, mock_winreg_ok, mock_winreg_qv,
                                mock_winreg_qve, browser: str, details: Dict):
    match sys.platform:
        case OS.WINDOWS:
            mock_winreg_qve.side_effect = [[DESKTOP_BROWSER], [DEFAULT_BROWSER_WINDOWS_DUCK]]
            mock_winreg_qv.side_effect = ['AppX', details["location"], details["location"]]
            mock_winreg_ok.return_value = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Classes")
            mock_winreg_ek.side_effect = ['AppX', OSError]
            mock_win32api_fileversion.return_value = {'FileVersionMS': 65536, 'FileVersionLS': 0}
            mock_os_stat.return_value = True
            if browser in installed_browsers.windows.POSSIBLE_BROWSER_NAMES:
                assert installed_browsers.give_me_details_of(browser) == details
            else:
                assert installed_browsers.give_me_details_of(browser) == BROWSER_NOT_INSTALLED


# check browser version
@pytest.mark.parametrize(
    ("browser", "description", "version", "location"),
    (
        pytest.param(
            "chrome",
            "Google Chrome",
            {
                "version": ANY,
            },
            ANY,
            marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only"),
            id="chrome_mac",
        ),
        pytest.param(
            "firefox",
            "Firefox",
            {
                "version": ANY,
            },
            ANY,
            marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only"),
            id="firefox_mac",
        ),
        pytest.param(
            "safari",
            "Safari",
            {
                "version": ANY,
            },
            ANY,
            marks=pytest.mark.skipif(sys.platform != "darwin", reason="mac-only"),
            id="safari_mac",
        ),
        pytest.param(
            "msedge",
            "Microsoft Edge",
            {
                "version": ANY,
            },
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            marks=pytest.mark.skipif(sys.platform == "linux", reason="mac-and-windows-only"),
            id="msedge_mac_windows",
        ),
        pytest.param(
            "chrome",
            "Google Chrome",
            {
                "version": ANY,
            },
            ANY,
            marks=pytest.mark.skipif(sys.platform != "linux", reason="linux-only"),
            id="chrome_linux",
        ),
        pytest.param(
            "chromium",
            "Chromium",
            {
                "version": ANY,
            },
            ANY,
            marks=pytest.mark.skipif(sys.platform != "linux", reason="linux-only"),
            id="chromium_linux",
        ),
        pytest.param(
            "firefox",
            "Mozilla Firefox",
            {
                "version": ANY,
            },
            ANY,
            marks=pytest.mark.skipif(sys.platform != "linux", reason="linux-only"),
            id="firefox_linux",
        ),
        pytest.param(
            "chrome",
            "Google Chrome",
            {
                "version": ANY,
            },
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only"),
            id="chrome_windows",
        ),
        pytest.param(
            "firefox",
            "Mozilla Firefox",
            {
                "version": ANY,
            },
            r"C:\Program Files\Mozilla Firefox\firefox.exe",
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only"),
            id="firefox_windows",
        ),
        pytest.param(
            "msie",
            "Internet Explorer",
            {
                "version": ANY,
            },
            r"C:\Program Files\Internet Explorer\iexplore.exe",
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only"),
            id="msie_windows",
        ),
        pytest.param(
            "msedge-canary",
            "Microsoft Edge Canary",
            {
                "version": ANY,
            },
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only"),
            id="msedge_canary_windows",
        ),
        pytest.param(
            "dummy_browser",
            "Dummy Browser",
            {
                "version": ANY,
            },
            ANY,
            id="dummy_browser",
        ),
    ),
)
class TestBrowserVersion:
    @patch.dict("sys.modules", winreg=MockWinreg, win32api=MockWin32API)
    @patch("winreg.QueryValue")
    @patch('win32api.GetFileVersionInfo')
    @patch('os.stat')
    def test_version_of_browser(self, mock_os_stat, mock_win32api_fileversion, mock_winreg_qv, browser: str,
                                description: str, version: Dict, location: str):
        match sys.platform:
            case OS.LINUX | OS.MAC:
                available_browsers = [individual_browser["name"] for individual_browser
                                      in installed_browsers.browsers()]
                if browser in available_browsers:
                    assert installed_browsers.get_version_of(browser) == version
            case OS.WINDOWS:
                mock_winreg_qv.side_effect = [description, location]
                mock_win32api_fileversion.return_value = {'FileVersionMS': 65536, 'FileVersionLS': 0}
                mock_os_stat.return_value = True
                if browser in installed_browsers.windows.POSSIBLE_BROWSER_NAMES:
                    assert installed_browsers.get_version_of(browser) == version
                else:
                    assert installed_browsers.get_version_of(browser) == BROWSER_NOT_INSTALLED

    @patch("subprocess.getoutput")
    @patch("os.path.isfile")
    @patch.dict("sys.modules", winreg=MockWinreg)
    @patch("winreg.QueryValue")
    def test_version_not_determined(self, mock_winreg_qv, mock_file, mock_output, browser: str,
                                    description: str, version: Dict, location: str) -> None:
        match sys.platform:
            case OS.LINUX:
                mock_file.return_value = False
            case OS.MAC:
                mock_output.return_value = ""
            case OS.WINDOWS:
                mock_winreg_qv.return_value = "dummy"
        assert installed_browsers.get_version_of(browser) == BROWSER_NOT_INSTALLED


# check duckduckgo version in windows
@pytest.mark.parametrize(
    ("browser", "description", "version", "location"),
    (
        pytest.param(
            "duckduckgo",
            "AppX",
            {
                "version": ANY,
            },
            r"C:\Program Files\WindowsApps\DuckDuckGo.DesktopBrowser_0.134.4.0_x64__ya2fgkz3nks94"
            r"\WindowsBrowser\DuckDuckGo.exe",
            marks=pytest.mark.skipif(sys.platform != "win32", reason="windows-only"),
            id="duckduckgo_windows",
        ),
    ),
)
class TestDuckDuckGoWindowsVersion:
    @patch.dict("sys.modules", winreg=MockWinreg)
    @patch("winreg.OpenKey")
    @patch("winreg.QueryValue")
    @patch("winreg.QueryValueEx")
    @patch("winreg.EnumKey")
    @patch('win32api.GetFileVersionInfo')
    @patch('os.stat')
    def test_version_of_browser(self, mock_os_stat, mock_win32api_fileversion, mock_winreg_ek, mock_winreg_qve,
                                mock_winreg_qv, mock_winreg_ok, browser: str, description: str, version: Dict,
                                location: str):
        match sys.platform:
            case OS.WINDOWS:
                mock_winreg_qv.side_effect = [description, location]
                mock_winreg_ok.return_value = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Classes")
                mock_winreg_qve.return_value = [DESKTOP_BROWSER]
                mock_winreg_ek.side_effect = [description, OSError]
                mock_win32api_fileversion.return_value = {'FileVersionMS': 65536, 'FileVersionLS': 0}
                mock_os_stat.return_value = True
                if browser in installed_browsers.windows.POSSIBLE_BROWSER_NAMES:
                    assert installed_browsers.get_version_of(browser) == version
                else:
                    assert installed_browsers.get_version_of(browser) == BROWSER_NOT_INSTALLED
