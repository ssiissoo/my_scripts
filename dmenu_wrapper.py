#!/bin/python3
from subprocess import check_output


# hardcoded constants
DEFAULT_FONT = "sans:size=14"

def dmenu(query, options, font=DEFAULT_FONT):
	"""
	this function is a python wrapper for dmenu

	query: 	what question should be displayed in dmenu?
		for example: "choose file…"
		this is string

	optins:	what options should be displayed in dmenu?
		for example: ['file0', 'file1', …]
		this is a list

	font:	what font should dmenu be displayed in?
		for example "sans:size=14"
		this is a string
		there is a default value hardcoded in the file, where this
		function is located

	returns a string (the string returned by dmenu)
		
	"""
	try:
		return str(check_output(('echo "{}" | dmenu -i -fn ' +
			'{} -p "{}"').format('\n'.join(options), font, query),
			shell=1), 'utf-8').strip()
	except:
		return ''
