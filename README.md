# Archive recovery tool - Craker
**Craker** is a brute force password recovery tool written entirely in python. It is a console app with no fancy gui.

## Supported platform:
* Windows 10

*However the source code might run fine on any platform which has python installed with required modules*

## Supported file formats:
* zip
* 7z
* rar
* pdf

*rar requires UnRAR.exe to be in same directory or its path has to be provided in environment variables. It is already provided with Craker.exe executable. Use can also get it by downloading WinRAR*

## Features:
* It provides two methods:
  * Brute force using charcter set
  * Using dictionary
* You can define your own character set or use available ones
* You have to give minimum and maximum length of password
* You can give prefix or suffix or both
* It shows elapsed time
* CPU and memory usage is negligible

## Cons:
* Very slow especially for 7z, rar and pdf
* Archives with encrypted file names and pdf encrypted with AES are not supported
