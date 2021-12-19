# Caiotile

Caiotile is a tiling tool for XFCE graphical interface.
This tool is intended to be used in integration with XFCE keyboard shortcuts
and so, it aims to be fast enought so a user could fastly trigger multiple 
commands using shortcuts without blocking the graphical interface.

By now, it can work with two displays, and it has the restriction that the
taskbar may be at the bottom of the screen.

## DEPENDENCIES

You will need wmctrl and xdotool installed:

```
$ sudo apt install wmctrl xdotool
```

And some python3 libraries:

```
pip3 install argparse
```

## USAGE
```
usage: caiotile [-h] [-t {left,right,top,bottom}] [-w {left,right,top,bottom}]
                [-s] [-c DISPLAY] [-m]

XFCE Tiling tool

optional arguments:
  -h, --help            show this help message and exit
  -t {left,right,top,bottom}, --tile {left,right,top,bottom}
                        tile relatively to display
  -w {left,right,top,bottom}, --tile-window {left,right,top,bottom}
                        tile relatively to window itself
  -s, --switch-display  move window to next display
  -c DISPLAY, --change-to-display DISPLAY
                        move window to specified display
  -m, --maximize        maximize window
```

## INTEGRATION WITH KEYBOARD SHORTCUTS

This tool works on the active window, so it is intended to be triggered by
keyboard shortcuts, which can be set with the xfce4-settings-manager tool,
under the Keyboard section
