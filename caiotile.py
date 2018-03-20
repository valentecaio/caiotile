#!/usr/bin/python3

import argparse
import subprocess
import re


HEIGHT_OFFSET = 60

class Display:
    def __init__(self, pos_x, pos_y, width, height):
        self.pos_x = int(pos_x)
        self.pos_y = int(pos_y)
        self.width = int(width)
        self.height = int(height)

    def __str__(self):
        return str(self.pos_x) + ',' + str(self.pos_y) + ',' \
               + str(self.width) + ',' + str(self.height)

    def __repr__(self):
        return "position: (" + str(self.pos_x) + \
               "," + str(self.pos_y) + ')'\
               ", width: " + str(self.width) + \
               ", height: " + str(self.height)


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
        displays.append(Display(x, y, width, height))

    return displays


def parse_arguments():
    parser = argparse.ArgumentParser(description='Tile tool')
    parser.add_argument('-t', '--tile', dest='tile',
                        choices=['left', 'right'], help='horizontal tile')
    parser.add_argument('-v', '--vertical-tile', dest='v_tile',
                        choices=['top', 'bottom'], help='vertical tile')
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


def get_active_window_position():
    cmd = 'xdotool getactivewindow getwindowgeometry'
    s1 = "Position: "
    s2 = " (screen:"

    r = str(execute(cmd))
    return r[r.find(s1) + len(s1): r.find(s2)].split(',')


def find_active_display(displays):
    x, y = get_active_window_position()
    for d in displays:
        if (d.pos_x <= int(x) <= d.pos_x+d.width) and\
                (d.pos_y <= int(y) <= d.pos_y+d.height):
            return d


def find_inactive_display(displays):
    x, y = get_active_window_position()
    for d in displays:
        if not ((d.pos_x <= int(x) <= d.pos_x+d.width) and\
                (d.pos_y <= int(y) <= d.pos_y+d.height)):
            return d


def set_window_size_and_position(x, y, width, height):
    cmd_header = 'wmctrl -r ":ACTIVE:" -e 0,'

    cmd = cmd_header + str(x) + ',' + str(y) + ',' + str(width) + ',' +\
          str(height - HEIGHT_OFFSET)
    execute(cmd)


def main():
    args = parse_arguments()
    displays = get_displays()

    if args.tile:
        d = find_active_display(displays)

        new_width = int(d.width/2)
        if args.tile == 'left':
            new_x = d.pos_x
        elif args.tile == 'right':
            new_x = d.pos_x + new_width

        set_window_size_and_position(new_x, d.pos_y, new_width, d.height)

    if args.v_tile:
        d = find_active_display(displays)

        new_height = int(d.height/2)
        if args.v_tile == 'top':
            new_y = d.pos_y
        elif args.v_tile == 'bottom':
            new_y = d.pos_y + new_height

        set_window_size_and_position(d.pos_x, new_y, d.width, new_height)

    if args.display is not None:
        d = displays[args.display]
        set_window_size_and_position(d.pos_x, d.pos_y, d.width, d.height)

    if args.switch_display:
        d = find_inactive_display(displays)
        set_window_size_and_position(d.pos_x, d.pos_y, d.width, d.height)

    if args.maximize:
        d = find_active_display(displays)
        set_window_size_and_position(d.pos_x, d.pos_y, d.width, d.height)


if __name__ == "__main__":
    main()
