import sys
import blink
import light

for line in sys.stdin:
    blink.handle_line(line)
    light.handle_line(line)

