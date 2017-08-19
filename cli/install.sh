#!/bin/sh
# copy keymap
cp workman-ergo.map /usr/share/kbd/keymaps/i386
# enable layout on system start
echo KEYMAP=workman-ergo >> /etc/vconsole.conf

# set font
echo FONT=Lat2-Terminus16 >>/etc/vconsole.conf
