#!/usr/bin/python3

import argparse
import subprocess


class Display:
    def __init__(self, display_id, pos_x, pos_y, width, height):
        self.display_id = int(display_id)
        self.pos_x = int(pos_x)
        self.pos_y = int(pos_y)
        self.width = int(width)
        self.height = int(height)

    def __str__(self):
        return str(self.pos_x) + ',' + str(self.pos_y) + ',' \
               + str(self.width) + ',' + str(self.height)

    def __repr__(self):
        return "display_id: " + str(self.display_id) + \
               ", position: (" + str(self.pos_x) + \
               "," + str(self.pos_y) + ')'\
               ", width: " + str(self.width) + \
               ", height: " + str(self.height)


def read_monitors(filename):
    f = open(filename, "r")
    monitors = []
    for line in f:
        l = line.split(',')
        monitors.append(Display(l[0], l[1], l[2], l[3], l[4]))
    return monitors


def parse_arguments():
    parser = argparse.ArgumentParser(description='Tile tool')
    parser.add_argument('-s', '--side', dest='side',
                        choices=['left', 'right'], help='tile to side')
    parser.add_argument('-d', '--display', dest='display',
                        type=int, help='move window to specified display')
    parser.add_argument('-c', '--change-display', dest='change_display',
                        action='store_true',
                        help='move window to next display')
    parser.add_argument('-f', '--filepath', dest='filepath',
                        help='displays CSV file path')
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


def main():
    cmd_header = 'wmctrl -r ":ACTIVE:" -e 0,'
    parse_arguments()
    args = parse_arguments()

    if args.filepath:
        filepath = args.filepath
    else:
        filepath = "displays.csv"
    displays = read_monitors(filepath)

    if args.side:
        d = find_active_display(displays)

        new_width = int(d.width/2)
        if args.side == 'left':
            new_x = d.pos_x
        elif args.side == 'right':
            new_x = d.pos_x + new_width
        cmd = cmd_header + str(new_x) + ',' + str(d.pos_y) +\
              ',' + str(new_width) + ',' + str(d.height)
        execute(cmd)

    elif args.display is not None:
        d = displays[args.display]
        cmd = cmd_header + str(d)
        execute(cmd)

    elif args.change_display:
        d = find_inactive_display(displays)
        cmd = cmd_header + str(d)
        execute(cmd)

    elif args.maximize:
        d = find_active_display(displays)
        cmd = cmd_header + str(d)
        execute(cmd)

    print(args)


if __name__ == "__main__":
    main()
