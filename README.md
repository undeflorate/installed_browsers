# installed browsers
A simple python library to help you identify the installed browsers in your host operating system.

## functions you can do with this library
+ identify installed browsers
+ identify default browser
+ get specific browser details
+ get specific browser version

## supported operating systems
+ linux
+ macos
+ windows

## supported browsers
+ google chrome
+ google chrome canary [^1]
+ chromium
+ firefox
+ firefox developer [^1]
+ firefox nightly [^1]
+ safari [^2]
+ opera
+ opera beta
+ opera developer
+ internet explorer [^3]
+ microsoft edge
+ microsoft edge beta
+ microsoft edge canary [^1]
+ microsoft edge developer
+ brave
+ brave beta
+ brave developer
+ vivaldi [^4]
+ vivaldi snapshot [^4]
+ min
+ arc [^2]
+ kosmik [^2]
+ pale moon [^1]  
[^1]: only for mac and windows
[^2]: only for mac
[^3]: only for windows
[^4]: windows has restrictions

> [!NOTE]
> Firefox beta, developer and nightly are portable versions in linux, these cannot be installed through package managers.  
> Identification of these versions (as kind of local installations) is not supported by this library.

> [!NOTE]
> Vivaldi stable and snapshot cannot be installed simultaneously on windows. Any of them counts as vivaldi after installation, only the application icon and version number differ between these, but only one instance can be used.   
> For identification, it does not matter which one is installed, it is detected as vivaldi.

> [!NOTE]
> Kosmik is partially supported by mac. Identification works but from its specific nature, browser cannot be set as default currently.

> [!NOTE]
> Pale moon is not supported by linux as it behaves as a kind of local installation.

> [!IMPORTANT]
> **Firefox beta is not supported** in any of the operating systems as it is almost identical with the stable version.
> + Beta and stable versions use the same naming convention. For proper working, make sure that either stable or beta version is installed but not both.
> + For mac, you need to add a different application name for beta if you have already installed the stable version previously.  
> + By default, in windows, beta is installed into a different location than stable: `Application Data`.
> 
> Technical naming is the same, so python is not able to make proper difference between these versions. It is quite likely that you get beta details for stable version and vice versa. To avoid this inconsistent behaviour, **do not install firefox stable and beta** altogether.

## how to install?
```bash
pip install installed_browsers
```

## usage
### import
```python
import installed_browsers
```
### identify installed browsers
Returns an iterator of dictionary of browser key and information.
```python
import installed_browsers

print(list(installed_browsers.browsers()))
```
#### output
```
[{'name': 'chrome', 'description': 'Google Chrome', 'version': '123.0.6312.58', 'location': '/usr/bin/google-chrome-stable'},
{'name': 'firefox', 'description': 'Firefox Web Browser', 'version': '124.0', 'location': 'firefox'}]
```
### identify default browser
Returns default browser description.
```python
import installed_browsers

print(installed_browsers.what_is_the_default_browser())
```
#### output
```
Google Chrome
```
### get specific browser details
Returns a dictionary containing browser name, description, desktop version and location.
```python
import installed_browsers

print(installed_browsers.give_me_details_of("chrome"))
```
#### output
```
{'name': 'chrome', 'description': 'Google Chrome', 'version': '123.0.6312.58', 'location': '/usr/bin/google-chrome-stable'}
```
### get specific browser version
Returns a dictionary containing browser version.
```python
import installed_browsers

print(installed_browsers.get_version_of("chrome"))
```
#### output
```
{'version': '123.0.6312.58'}
```
## references
Thanks for the inspiration to [Ronie Martinez](https://github.com/roniemartinez/browsers).
