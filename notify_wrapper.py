#!/bin/python3
from os import system


URGENCY = ['low', 'normal', 'critical']

def notify(title, msg, urgency=0):
	"""
	this function is a python wrapper for the linux program notify-send

	title:		the title of the notification
			this is a string

	msg:		the content of the notification
			this is a string

	urgency:	the urgency of the notification
			this is either a string or a number ('low', 'normal',
			'critical' or 0, 1, 2)
	"""
	if type(urgency) == type(1):
		urgency = URGENCY[urgency]
	system("sudo -u s DISPLAY=:0 " +
		"DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus " +
		f'notify-send "{title}" "{msg}" --urgency={urgency}')
