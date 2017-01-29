#!/bin/bash

# spare modifier
spare_modifier="Menu"
# map an unused modifier's keysym to spacebar's keycode
xmodmap -e "keycode 65 = $spare_modifier"
# make it AltGr modifier 
xmodmap -e "remove mod4 = $spare_modifier"
xmodmap -e "add AltGr = $spare_modifier"
xmodmap -e "keycode any = space"

xcape -e "$spare_moifier=space"
