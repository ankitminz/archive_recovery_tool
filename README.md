# Archive recovery tool - Craker
**Craker** is a brute force archive recovery tool written entirely in python. It is a console app with no fancy gui.

## Supported platform:
* Windows

*However the source code might run fine on any platform which has python installed with required modules*

## Supported archive formats:
* zip
* 7z
* rar

*rar requires UnRAR.exe to be in same directory or its path has to be provided in environment variables. It is already provided with Craker.exe executable. Use can also get it by downloading WinRAR*

## Speed of brute forcing various archive formats:
* zip - *testing in progress*
* 7z - *testing in progress*
* rar - *testing in progress*

## Features:
* It provides two methods:
  * Brute force using charcter set
  * Using dictionary
* You can define your own character set or use available ones
* You have to give minimum and maximum length of password
* You can give prefix or suffix or both
* It shows elapsed time
* CPU and memory usage is negligible

*I have opted not to show estimated time because that would slow down the process*

## Cons:
* Very slow especially for 7z and rar archives *this is because of next point*
* Didn't use GPU

## Last thoughts
You can recover your data by using its full potential. Use it responsibly
