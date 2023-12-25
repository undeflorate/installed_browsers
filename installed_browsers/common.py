import sys

if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


class OS:
    LINUX = "linux"
    WINDOWS = "win32"
    MAC = "darwin"


class Browser(TypedDict):
    name: str
    description: str
    version: str
    location: str


class Version(TypedDict):
    version: str
