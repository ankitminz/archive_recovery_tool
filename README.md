# Craker - Password Recovery Tool
**Craker** is a brute force password recovery tool written entirely in python. It is a console app with no fancy gui.

## How to Use
1. Either download windows executable *(craker.exe file)* or python script *(craker.py file)* from [Releases](https://github.com/ankitminz/archive_recovery_tool/releases). I recommend using python script as its little bit fast and interperater give traceback of errors if program crash but you'll need to have python *(probably latest version)* installed with required modules in your system.
2. If you are trying to recover password of rar file then put UnRAR.exe in same directory of craker.exe or craker.py. You'll need to download WinRAR from https://www.win-rar.com/start.html?&L=0. Default directory of UnRAR.exe is `C:\Program Files (x86)\WinRAR\` or `C:\Program Files\WinRAR\` depending on whether it is 32-bit or 64-bit.
3. Then run the executable by double clicking it or python script from terminal *(cmd or powershell)* and follow instructions.

## Supported file formats:
* zip
* 7z
* rar
* pdf

## Supported platform:
* Windows 10

## Tools Used
* Python 3.10.1
* Notepad++ 8.1.3
* Pyinstaller 4.7

## Python Modules Used
* pyzipper
* py7zr
* rarfile
* itertools
* time
* os
* PyPDF2

## Features:
* It provides two methods:
  * Brute force using charcter set
  * Using dictionary
* You can define your own character set or use available ones
* You have to give minimum and maximum length of password
* You can give prefix or suffix or both
* CPU and memory usage is negligible

## Cons:
* Very slow especially for 7z, rar and pdf
* Archives with encrypted file names and pdf encrypted with AES are not supported
