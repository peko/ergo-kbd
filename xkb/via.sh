#!/bin/bash
cd ./lab/ergoxkb/xkb/
# ./init_as_overlay.sh
xkbcomp -I`pwd`/via/ via/via.xkb $DISPLAY
