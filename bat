#!/bin/bash

lvl0=$(echo "$(upower -i /org/freedesktop/UPower/devices/battery_BAT0)" | awk '/percentage/ {print $2}' | grep -o '[0-9]\+')
lvl1=$(echo "$(upower -i /org/freedesktop/UPower/devices/battery_BAT1)" | awk '/percentage/ {print $2}' | grep -o '[0-9]\+')

out=""

#if [ -z "$var" ]
#then
#	if [ "$lvl1"  -gt 80 ]
#	then
#		out="  "
#	elif [ $lvl1 -gt 60 ]
#	then
#		out="  "
#	elif [ $lvl1 -gt 40 ]
#	then
#		out="  "
#	elif [ $lvl1 -gt 15 ]
#	then
#		out="  "
#	else
#	out="  "
#	fi
#else
#	out="  "
#fi
#
#if [ "$lvl0" -gt "80" ]
#then
#	out="$out  "
#elif [ "$lvl0" -gt "60" ]
#then
#	out="$out  "
#elif [ "$lvl0" -gt "40" ]
#then
#	out="$out  "
#elif [ "$lvl0" -gt "15" ]
#then
#	out="$out  "
#else
#	out="$out  "
#fi

echo "$out[$(printf '%03d' $lvl1)] [$(printf '%03d' $lvl0)]"
