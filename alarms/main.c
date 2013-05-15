// cmdmp3win
// A command-line MP3 player for Windows
// (window-mode version)
//
// License: MIT / X11
// Copyright (c) 2009 by James K. Lawless
// jimbo@radiks.net http://www.radiks.net/~jimbo
// http://www.mailsend-online.com
//
// Permission is hereby granted, free of charge, to any person
// obtaining a copy of this software and associated documentation
// files (the "Software"), to deal in the Software without
// restriction, including without limitation the rights to use,
// copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the
// Software is furnished to do so, subject to the following
// conditions:
//
// The above copyright notice and this permission notice shall be
// included in all copies or substantial portions of the Software.
//
// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
// EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
// OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
// NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
// HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
// WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
// FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
// OTHER DEALINGS IN THE SOFTWARE.



#include <windows.h>
#include <string.h>

#pragma comment(lib,"winmm.lib")
#pragma comment(lib,"kernel32.lib")
#pragma comment(lib, "user32.lib")

char msg[MAX_PATH + 128];

extern int __argc;
extern char ** __argv;

int sendCommand(char *);

int WINAPI WinMain( HINSTANCE hInstance,
               HINSTANCE hPrevInstance,
               LPSTR lpCmdLine,
               int nCmdShow ) {

   char cmd[MAX_PATH + 64];
   int loop = 0;

   if(__argc < 2) {
      sprintf(msg, "Syntax:\n\ttinymp3 \"c:\\path to file.mp3\"\n");
      MessageBox(NULL, msg, "tinymp3", MB_OK);
      return 1;
   }

   if (strncmp(__argv[1], "-l", 2) == 0 || strncmp(__argv[1], "-L", 2) == 0) {
       loop = 1;
   }

   if (strlen(__argv[1 + loop]) > MAX_PATH) {
      sprintf(msg, "File path greater than max length of %d\n", MAX_PATH);
      MessageBox(NULL, msg, "tinymp3", MB_OK);
      return 1;
   }

   sprintf(cmd, "Open \"%s\" Type MPEGVideo Alias MP3", __argv[1 + loop]);

   do {
      if (
         sendCommand("Close All") ||
         sendCommand(cmd) ||
         sendCommand("Play MP3 Wait")
         ) {
         return 1;
      }
   } while (loop);

   return 0;
}

int sendCommand(char *cmd) {
   int fail = mciSendString(cmd, NULL, 0, 0);

   if (fail) {
      sprintf(msg, "Error %d when sending %s\n", fail, cmd);
      MessageBox(NULL, msg, "tinymp3", MB_OK);
      return 1;
   }

   return 0;
}
