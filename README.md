# installed browsers
A simple python library to help you identify the installed browsers in host operating system.

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
+ google chrome canary
+ chromium
+ firefox
+ firefox developer
+ firefox nightly
+ safari [^1]
+ opera
+ opera beta
+ opera developer
+ internet explorer [^2]
+ microsoft edge
+ microsoft edge beta
+ microsoft edge canary
+ microsoft edge developer
+ brave
+ brave beta
+ brave developer
[^1]: only for mac
[^2]: only for windows

!!! note

> [!IMPORTANT]
> Firefox beta is not supported in any of the operating systems as it is almost identical with the stable version.
> + Beta and stable versions use the same naming convention, although, for mac you need to add a different name for the application if you have already installed the stable version.  
> + Beta and stable versions use the installing location (except in windows because beta is installed at `Application Data`).
> 
> Technical naming is the same, so python is not able to make proper difference between these versions. It is quite likely that you get beta details for stable version and vica versa. To avoid this inconsistent behaviour, **do not install firefox stable and beta** together.

## usage
## how to install?
## 
