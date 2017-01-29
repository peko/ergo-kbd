#!/bin/bash
# setxkbmap -symbols ergo -print | xkbcomp -I`pwd`/ - "${DISPLAY%%.*}"
xkbcomp -I`pwd`/ ergo.xkb $DISPLAY
