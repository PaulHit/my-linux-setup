#! /bin/bash 
picom -b &
nitrogen --restore &
xinput set-prop "Synaptics TM3336-001" "libinput Tapping Enabled" 1
flameshot &
blueman-manager &
qbittorrent &
copyq &
xrandr --output eDP-1 --off --output HDMI-1 --primary --mode 1920x1080 --pos 0x0 --rotate normal --output DP-1 --off --output HDMI-2 --off
