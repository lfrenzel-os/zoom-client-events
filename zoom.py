import subprocess
import io
import argparse
import sys

import notification
import meeting

raiseNotificationCmd = ''
dropNotificationCmd = ''
joinMeetingCmd = ''
leaveMeetingCmd = ''

parser = argparse.ArgumentParser()
parser.add_argument("--chat", help="Command to execute on first new chat message.")
parser.add_argument("--clear", help="Command to execute when there are no more unread messages.")
parser.add_argument("--join", help="Command to execute when a meeting is joined.")
parser.add_argument("--leave", help="Command to execute when a meeting is left.")

args = parser.parse_args()

if args.chat is None or args.clear is None or args.join is None or args.leave is None:
    parser.print_help()
    sys.exit(2)

dbusMonitor = subprocess.Popen("/usr/bin/dbus-monitor", shell=True, stdout=subprocess.PIPE).stdout
for line in io.TextIOWrapper(dbusMonitor):
    notification.handle_line(line, args.chat, args.clear)
    meeting.handle_line(line, args.join, args.leave)
