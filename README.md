# my_scripts

In this repository you will find short scripts, that help me through the day.
Usually they will not be complicated and you might even find a better
alternative online, but whatever.

## dmenu wrapper

This is just a python wrapper for dmenu. It is used by other scripts.

## notify wrapper

This is a wrapper for the notify-send command. It is used by other scripts.

## dmenu menu

You can create a json file containing keywords and commands as a list of keys
and values and run this program on it. I think it is a more convenient way to
call custom dmenu prompts.

## friendly reminder

Here you can create a json file containing some information about upcoming
meetings etc. which you will be reminded of when you constantly call this
script (e.g. using cron). The notify-send command is used for this. It is
basically a crappy calender.

## vol

A simple script that gets the volume of your default output device and places
a fontawesome symol in front of it. Use it with dwmblocks for example.

## mic

Same as vol with your default input device.

## audio

This script lets you mange your audio devices via dmenu. It's written in
quite a crappy style but works. I will have to rewrite this some day

## bluetoothctl

This manages your bluetooth devices via dmenu. It too is crappy and very
incomplete but enough for my usecases.

## bat

Displays battery levels for a two battery setup.

## xp-pen_driver

A script that detects when a xp-pen graphics tablet is plugged in an
automaticly opens the configuration.

## mpd_block

A script that shows some info on what mpd is up to. This is supposed to be
used with programs like dwmblocks

## mpd_skip

Like `mpc next` but with notification.

## mpd_prev

Analogous to mpd_skip

## bat_warn

A script, that warns one if the total battery level is less than 15 upon
execution.

## contactman

A contact manager, which uses dmenu and reads from card dav files in the .rolo
folder. rolo is a nice commandline program to manipulate card dav files.

## screenie

Lets you take screenshots using scrot. dmenu asks whether the entire screen
should be selected or a region and whether the screenshot should be copied
or you want to do ocr on it using tesseract. Make sure to change the path to
suit your computer.

## formman

This is a WIP project which is supposed to be able to save often used formulas
and lets you manipulate it using sympy python.
