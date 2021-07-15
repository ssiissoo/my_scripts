#!/bin/sh


lvl0=$(upower -i /org/freedesktop/UPower/devices/battery_BAT0 |
	 awk '/percentage/ {print $2}' |
	 grep -o '[0-9]\+')
lvl1=$(upower -i /org/freedesktop/UPower/devices/battery_BAT1 |
	 awk '/percentage/ {print $2}' |
	 grep -o '[0-9]\+')
total=$(($lvl0 + $lvl1))

if [ $total -lt 15 ];
then
	notify-send -u 'critical' "Battery Warning" "Your total battery capacity is below 15%!"
fi
