# Alarm Clock #

A plugin for both Sublime Text 2 and 3 that allows alarms to be set X hours / X
minutes into the future or at XX:XX time.

## Details ##

Need to be able to get your head down and bury yourself in your code without
missing that important meeting? This really simple plugin allows you to quickly
set alarms either a number of hours / minutes into the future or at a particular
time. Includes that all important snooze functionality in case you're not quite
done yet.

The plugin has a few dependencies on other software to make the actual alarm sound.
On windows a tiny (4KB) executable (with source code) is provided to play wav / mp3
files. In OSX the dependency is on afplay which should be available from version
10.5+. In linux the dependency is on aplay which relies on ALSA being present
and does not play mp3 files, only wav. The commands and alarm files are
configured in the settings file so you are free to amend both the command used
and the alarm sound if you wish.

## Manual installation ##

At present the plugin is not in package control so you will need to install manually.

### Using GIT (recommended): ###
Go to the Packages directory (`Preferences` / `Browse Packages…`). Then clone this
repository:

    git clone git://github.com/CodeEffect/AlarmClock

### Manually: ###
Downoad a zip of the project (click on the zip icon further up the page) and extract
it into your packages directory (`Preferences` / `Browse Packages…`).
Go to the "Packages" directory (`Preferences` / `Browse Packages…`). Then clone this
repository:

## Default key bindings ##

`f8` - Shows all options as a quick panel list
`shift+f8` - Add new alarm

## History ##

After a considerable amount of tinkering trying to get a cross platform pc speaker
beep working a different route was decided upon. Windows and ST3 worked without
issue using winsound on ST3. I was using threading to ensure that the beep
continued while the ok / cancel diaglog was displayed but unfortunately on ST2
(at least on win) the OK cancel dialog halted execution of the other thread as
well. I managed to get a PC speaker beep on win ST2 by calling a tiny vbscript file
which itself called a tiny batch file which echo'd a bell character to the console.
the vbscript file was required to hide the console window that would otherwise
have popped up. The batch file itself was needed as echo'ing the bell character
straight into the ST console just printed [BEL] rather than making a sound. I
believe that a similar approach would have worked with Linux / OSX but after some
digging it became apparent that at least on Ubuntu the PC speaker was disabled
out of the box in some configurations. This, combined with the other issues
encountered along the way pushed me to seek a simpler, more robust method.

## Compiling the mp3 player for windows ##

I used bloodshed Dev-C++ to compile the code. Apart from main.c all that was
required was to link WinMM.Lib and libwinmm.a against the project. Once built I
used the UPX packer with the command:
> upx.exe --ultra-brute --overlay=strip mp3.exe
This brought the size down from just under 20KB or so to 4KB.

## License ##

Alarm clock is licensed under the MIT license.

  Copyright (c) 2013 Steven Perfect <steve@codeeffect.co.uk>

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.
