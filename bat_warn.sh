#!/bin/sh


lvl0=$(upower -i /org/freedesktop/UPower/devices/battery_BAT0 |
	 awk '/percentage/ {print $2}' |
	 grep -o '[0-9]\+')
lvl1=$(upower -i /org/freedesktop/UPower/devices/battery_BAT1 |
	 awk '/percentage/ {print $2}' |
	 grep -o '[0-9]\+')
total=$(($lvl0 + $lvl1))

charging=`upower -i /org/freedesktop/UPower/devices/battery_BAT0 | grep state: | awk '{gsub(/\s*state:\s*/,"");}1'`

if [ $charging == "charging" ]
then
	exit 0
fi

if [ $total -lt 15 ];
then
	sudo -u s DISPLAY=:0 DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus notify-send -u 'critical' "Battery Warning" "Your total battery capacity is below 15%!"
fi
