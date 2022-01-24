# Craker - Password Recovery Tool
**Craker** is a brute force password recovery tool written entirely in python. It is a console app with no fancy gui.

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
