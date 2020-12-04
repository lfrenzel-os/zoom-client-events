import re
import os
import sys

this = sys.modules[__name__]

serialRegEx = re.compile(' serial=[0-9]+')

active = False
mySerial = ''
returnSerial = ''
waitForReturn = False
myHandle = ''
insideReturn = False
lightsAreOn = False
lightsMayBeOn = True


def handle_line(line, joinCommand, leaveCommand):
    if line.startswith("method call"):
        this.insideReturn = False
        if line.endswith("path=/ScreenSaver; interface=org.freedesktop.ScreenSaver; member=Inhibit\n"):
            # hier noch die serial holen
            m = this.serialRegEx.search(line)
            if m:
                this.mySerial = m.group()
                this.active = True
        elif line.endswith("path=/ScreenSaver; interface=org.freedesktop.ScreenSaver; member=UnInhibit\n"):
            this.active = True
        else:
            this.active = False
    elif this.active:
        if line.startswith('   string "'):
            if line=='   string "in a meeting"\n':
                this.waitForReturn = True
                this.returnSerial = " reply_" + mySerial[1:] + "\n"
                this.active = False
                os.system(joinCommand)
                this.lightsAreOn = True
        elif line==this.myHandle:
            this.active = False
            if this.lightsAreOn or this.lightsMayBeOn:
                os.system(leaveCommand)
                this.lightsAreOn = False
                this.lightsMayBeOn = False
        else:
            this.active = False
    
    if this.waitForReturn:
        if line.startswith('method return '):
            if line.endswith(this.returnSerial):
                this.insideReturn = True
                this.waitForReturn = False
    elif this.insideReturn:
        if line.startswith('   uint32 '):
            this.myHandle = line
            this.insideReturn = False
        else:
            this.insideReturn = False
