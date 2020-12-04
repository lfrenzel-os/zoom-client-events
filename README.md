# zoom-client-events
Linux tool to perform shell commands on new zoom chat message, entering or leaving a meeting, when all messages have been read.

## Motivation
The linux zoom client does not yet feature individual audio output settings for notification sounds and for meeting audio. I wanted to have notification sounds played back on my speakers while I want to use a headset for meetings. Also I like to listen to music on the speakers and got tired of manually pausing/resuming that when joining or leaving a meeting. These things usually should be no problem using linux, adding command calls to any of the events.
In the end I even integrated smart lighting actions when those scripts get called. But that's all up to your imagingation.

I wanted a solution that worked just locally on my system, without causing further network load.

## Pre-Requisites
Tested on Ubuntu 20.04 with python3.

## Usage
`python3 zoom.py --chat=<cmd> --clear=<cmd> --join=<cmd> --leave=<cmd>`


The individual commands will be called (shell scripts) when the respective events happen.

## How it works
The tool intercepts the dbus and reacts on individual events. 
* Meeting join/leave is triggered by zoom disabling or enabling the screen saver. 
* The chat messages are triggered by zoom updating the zoom icon in the status bar (where it shows a small red dot when messages are pending). Or the icon is reset to the normal state (without any dot/number).