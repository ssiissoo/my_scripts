#!/bin/python3
from argparse import ArgumentParser
from dmenu_wrapper import dmenu 
from os.path import isfile
from json import load
from os import system


if __name__ == '__main__':
	par = ArgumentParser(description="a python program which creates " +
		"a menu using dmenu to run commands associated with " +
		"keywords which are all defined in a json file")
	par.add_argument('query', help="the query printed out by dmenu")
	par.add_argument('file', help="the path to the json file " +
		"containing the keywords and commands")
	args = par.parse_args()
	f = args.file
	if not isfile(f): raise Exception("file does not exist!")
	dic = {}
	with open(f) as fi:
		dic = load(fi)
	choice = dmenu(args.query, dic.keys())
	if choice in dic.keys():
		system(dic[choice])
