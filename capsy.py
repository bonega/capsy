import subprocess
import time
import re
import sys
from ctypes import cdll
from ctypes import c_uint

X11 = cdll.LoadLibrary("libX11.so.6")

def set_caps(state):
    state = 2 if state else 0 # manpage says '1', bit?
    display = X11.XOpenDisplay(None)
    X11.XkbLockModifiers(display, c_uint(0x0100), c_uint(2), c_uint(state))
    X11.XCloseDisplay(display)

def get_focused():
    result = subprocess.run(['xdotool', 'getwindowfocus', 'getwindowname'], stdout=subprocess.PIPE)
    return result.stdout

def run_caps_setter(programs):
    while True:
        current_focus = str(get_focused(), 'utf-8')
        match = None
        for i in programs:
            if re.match(i, current_focus):
                match = True
        set_caps(match)
        time.sleep(0.1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Please provide one or more regex to match')
        sys.exit(0)
    run_caps_setter(sys.argv[1:])