#!/usr/bin/python3

import argparse
import subprocess
import re


HEIGHT_OFFSET = 60

class Rectangle:
    def __init__(self, x, y, w, h):
        self.x = int(x) # origin x
        self.y = int(y) # origin y
        self.w = int(w) # width
        self.h = int(h) # height

    def __str__(self):
        return str(self.x) + ',' + str(self.y) + ',' \
               + str(self.w) + ',' + str(self.h)

    def __repr__(self):
        return "position: (" + str(self.x) + \
               "," + str(self.y) + ')'\
               ", size: " + str(self.w) + \
               "," + str(self.h) + ')'


# example ['1366x768+1024+373', '1024x768+0+0']
def get_displays():
    out = str(execute('xrandr'))

    # remove occurrences of 'primary' substring
    out = out.replace("primary ", "")

    start_flag = " connected "
    end_flag = " ("
    resolutions = []
    for m in re.finditer(start_flag, out):
        # start substring in the end of the start_flag
        start = m.end()
        # end substring before the end_flag
        end = start + out[start:].find(end_flag)

        resolutions.append(out[start:end])

    displays = []
    for r in resolutions:
        width = r.split('x')[0]
        height, x, y = r.split('x')[1].split('+')
        displays.append(Rectangle(x, y, width, int(height)-HEIGHT_OFFSET))

    return displays


def parse_arguments():
    parser = argparse.ArgumentParser(description='Tile tool')
    parser.add_argument('-t', '--tile', dest='tile',
                        choices=['left', 'right', 'top', 'bottom'],
                        help='tile relatively to display')
    parser.add_argument('-w', '--tile-window', dest='tile_w',
                        choices=['left', 'right', 'top', 'bottom'],
                        help='tile relatively to window itself')
    parser.add_argument('-s', '--switch-display', dest='switch_display',
                        action='store_true',
                        help='move window to next display')
    parser.add_argument('-c', '--change-to-display', dest='display',
                        type=int, help='move window to specified display')
    parser.add_argument('-m', '--maximize', dest='maximize',
                        action='store_true', help='maximize window')
    return parser.parse_args()


def execute(cmd):
    print('$ ' + cmd)
    return subprocess.check_output(['bash', '-c', cmd])


def get_active_window():
    cmd = 'xdotool getactivewindow getwindowgeometry'
    flag_pos_start = "Position: "
    flag_pos_end = " (screen:"
    flag_geom_start = "Geometry: "
    flag_geom_end = "\\n"

    r = str(execute(cmd))
    
    str_pos = r[r.find(flag_pos_start) + len(flag_pos_start) \
              : r.find(flag_pos_end)]
    str_geom = r[r.find(flag_geom_start) + len(flag_geom_start) \
               : r.rfind(flag_geom_end)]

    pos = str_pos.split(',')
    geom = str_geom.split('x')

    return Rectangle(pos[0], pos[1], geom[0], geom[1])


def window_is_in_display(w, d):
   return (d.x <= w.x <= d.x+d.w) and (d.y <= w.y <= d.y+d.h)


def get_display(displays, active):
    w = get_active_window()
    for d in displays:
        if window_is_in_display(w, d):
            if active:
                return d
        else:
            if not active:
                return d


def get_active_display(displays):
    return get_display(displays, True)


def get_inactive_display(displays):
    return get_display(displays, False)


def set_window(x, y, w, h):
    cmd_header = 'wmctrl -r ":ACTIVE:" -e 0,'

    cmd = cmd_header + str(x) + ',' + str(y) + ',' + str(w) + ',' + str(h)
    execute(cmd)


def tile(direction, basis, display):
    x = basis.x
    y = basis.y
    w = basis.w
    h = basis.h

    if direction == 'left':
        w = int(display.w/2)
        x = display.x
    elif direction == 'right':
        w = int(display.w/2)
        x = display.x + w
    elif direction == 'top':
        h = int(display.h/2)
        y = display.y
    elif direction == 'bottom':
        h = int(display.h/2)
        y = display.y + h

    set_window(x, y, w, h)


def main():
    args = parse_arguments()
    displays = get_displays()

    if args.tile:
        display = get_active_display(displays)
        tile(args.tile, display, display)

    if args.tile_w:
        display = get_active_display(displays)
        window = get_active_window()
        tile(args.tile_w, window, display)

    if args.display is not None:
        d = displays[args.display]
        set_window(d.x, d.y, d.w, d.h)

    if args.switch_display:
        d = get_inactive_display(displays)
        set_window(d.x, d.y, d.w, d.h)

    if args.maximize:
        d = get_active_display(displays)
        set_window(d.x, d.y, d.w, d.h)


if __name__ == "__main__":
    main()
