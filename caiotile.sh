#!/bin/bash

BAR_SIZE=50

if [ $1 == "change_workspace" ]
then
    ACTIVE_WINDOW="$(xdotool getactivewindow)"
    LAST_DESKTOP="$(xdotool get_desktop_for_window $ACTIVE_WINDOW)"
    NEW_DESKTOP=$(( $LAST_DESKTOP+1 % 2 ))
    echo $NEW_DESKTOP $LAST_DESKTOP $ACTIVE_WINDOW
    xdotool set_desktop_for_window $ACTIVE_WINDOW $NEW_DESKTOP

elif [ $1 == "tile_left" ]
then
    GEOMETRY="$(xdotool getdisplaygeometry)"
    GEO_ARRAY=($GEOMETRY)
    echo array = ${GEO_ARRAY[0]}, ${GEO_ARRAY[1]}
    X=$(( ${GEO_ARRAY[0]} / 2 ))
    Y=$(( ${GEO_ARRAY[1]} - $BAR_SIZE ))
    POS="0 0"
    SIZE="$X $Y"
    
    echo pos = $POS
    echo size = $SIZE

    xdotool windowmove `xdotool getwindowfocus` $POS
    xdotool windowsize `xdotool getwindowfocus` $SIZE
elif [ $1 == "tile_right" ]
then
    GEOMETRY="$(xdotool getdisplaygeometry)"
    GEO_ARRAY=($GEOMETRY)
    echo array = ${GEO_ARRAY[0]}, ${GEO_ARRAY[1]}
    X=$(( ${GEO_ARRAY[0]} / 2 ))
    Y=$(( ${GEO_ARRAY[1]} - $BAR_SIZE ))
    POS="$X 0"
    SIZE="$X $Y"

    echo pos = $POS
    echo size = $SIZE

    xdotool windowmove `xdotool getwindowfocus` $POS
    xdotool windowsize `xdotool getwindowfocus` $SIZE
fi


exit 0
