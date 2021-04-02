#!/bin/python3
from argparse import ArgumentParser
from os.path import isfile, isdir, dirname
from json import load
import datetime as dt
from notify_wrapper import notify


WEEKDAY = {'mon': 0, 'tue': 1, 'wed': 2, 'thu': 3, 'fri': 4, 'sat': 5,
	'sun': 6}

# template for events file
"""
{
	"event name":{ -> event name; make sure its unique and does not
				contain a semicolon

		"recurring": True, -> is this a single envent?
		"date": "yyyy-mm-dd HH:MM", -> for single events
		"occurrences": [ -> for recurring events
			"sun HH:MM",
			"mon HH:MM"
		],
		"exceptions": [ -> when to skip notification
			"yyyy-mm-dd HH:MM",
			"yyyy-mm-dd HH:MM"
		],
		"end": "yyyy-mm-dd HH:MM", -> when does the series of events
						stop?
		"notify": 10 -> how many minutes beforehand should you be
					notified?
		"description": "foo bar" -> further infos

	}
}
"""

#example for data stored in temp file
"""
1612864196.399505;event name 0
1612864197.399505;event name 1
1612864198.399505;event name 2
"""

def _read_temp(tp):
	content = ""
	try:
		with open(tp, 'r') as f:
			content = f.read()
	except Exception as e:
		print(f"could not read temp file: {e}"); exit(1)
	content = content.strip()
	if content == '': return []
	sp = lambda l: l.split(';')
	d = lambda l: dt.datetime.fromtimestamp(float(sp(l)[0]))
	n = lambda l: sp(l)[1]
	data = [(d(i), n(i)) for i in content.split('\n') if d(i) > dt.datetime.now()]
	try:
		with open(tp, 'w') as f:
			pass
	except Exception as e:
		print(f"could not clear temp file: {e}"); exit(1)
	return data

def _read_events(ev):
	data = {}
	try:
		with open(ev) as f:
			data = load(f)
	except Exception as e:
		print(f"cannot load events json file: {e}"); exit(1)
	return data

def _next_weekday(d, weekday):
	if type(weekday) == type(""):
		w = weekday.lower().strip()
		if w in WEEKDAY:
			weekday = WEEKDAY[w]
		else:
			print(f"unknown weekday: {w}")
			exit(1)
	if weekday == d.weekday():
		return d
	days_ahead = weekday - d.weekday()
	if days_ahead <= 0:
		days_ahead += 7
	return d + dt.timedelta(days_ahead)

def _ch_time(da, hour, minute):
	return dt.datetime(year=da.year, month=da.month, day=da.day,
		hour=hour, minute=minute)

def _get_next_occurrences(nam, l, da):
	sb = lambda s, i: s.split(' ')[i]
	sc = lambda s, i: s.split(':')[i]
	h = lambda s: int(sc(sb(s, 1), 0))
	m = lambda s: int(sc(sb(s, 1), 1))
	try:
		return [_ch_time(_next_weekday(da, sb(i, 0)), h(i), m(i)) for i in l]
	except:
		print(f"wrong formatting for occurrences in {nam}; format: "+
			"\"mon HH:MM\"")
		exit(1)

def _recognize_notify(nam, ev, da):
	if not 'recurring' in ev.keys():
		print(f"the 'recurring' key is mandatory in the declaraion " +
			"of events: {nam} is missng that key")
		exit(1)
	if not 'notify' in ev.keys():
		print(f"the 'notify' key is mandatory in the declaraion " +
			"of events: {nam} is missng that key")
		exit(1)
	if not type(ev['notify']) == type(2):
		print(f"value of 'notify' key must be an integer: {nam} " +
			"does not satisfy this")
	if not ev['recurring']:
		if not 'date' in ev.keys():
			print(f"the 'date' key is mandatory in the " +
				"declaraion of non-recurring events: {nam} " +
				"is missng that key")
			exit(1)
		try:
			d = dt.datetime.strptime(ev['date'], '%Y-%m-%d %H:%M')
		except:
			print(f"date of {nam} is not formatted correctly: " +
				"'yyyy-mm-dd HH:MM' is the format")
			exit(1)
		if d - dt.timedelta(minutes=ev['notify']) <= da and d >= da:
			return (d, nam), None if not 'description' in ev.keys() else ev['description']
		else:
			return None, None
	if not 'occurrences' in ev.keys():
		print(f"the 'occurrences' key is mandatory in the " +
			"declaraion of recurring events: {nam} is missng " +
			"that key")
		exit(1)
	occ = _get_next_occurrences(nam, ev['occurrences'], da)
	if 'exceptions' in ev.keys():
		try:
			ex = [dt.datetime.strptime(i, '%Y-%m-%d %H:%M') for i in ev['exceptions']]
			for i in occ:
				if i in ex:
					del occ[occ.index(i)]
		except:
			print(f"exception of {nam} is not formatted " +
				"correctly: 'yyyy-mm-dd HH:MM' is the format")
			exit(1)
	if 'end' in ev.keys():
		try:
			e = dt.datetime.strptime(ev['end'], '%Y-%m-%d %H:%M')
		except:
			print(f"end of {nam} is not formatted " +
				"correctly: 'yyyy-mm-dd HH:MM' is the format")
		if min(occ) >= e:
			return None, None
	if min(occ) - dt.timedelta(minutes=ev['notify']) <= da and min(occ) >= da:
		return (min(occ), nam), None if not 'description' in ev.keys() else ev['description']
	return None, None
		
	

if __name__ == '__main__':
	par = ArgumentParser(description="a program that should be run " +
		"by a scheduling program, cron for example. It uses system " +
		"notifications to remind the user of recurring events or " +
		"single occations. Those are managed in a JSON file")
	par.add_argument('events_file', help="path to the JSON file " +
		"containing the information on the events")
	par.add_argument('temp_file', help="path to temporary file, in " +
		"which information about already notified events is " +
		"stored. Make sure this file does not exist, is empty or " +
		"contains friendly_reminder infos only.")
	args = par.parse_args()
	ev = args.events_file
	tp = args.temp_file
	if not isfile(ev): print("events file does not exist"); exit(1)
	notified = []
	if isfile(tp): notified = _read_temp(tp)
	elif not isdir(dirname(tp)) and not dirname(tp) == '':
		print("folder for temp file does not exist"); exit(1)
	events = _read_events(ev)
	for i in events.keys():
		ev, des = _recognize_notify(i, events[i], dt.datetime.now())
		if not ev:
			continue
		if ev and not ev in notified:
			notify(ev[0].strftime('%d.%m %H:%M ') + ev[1], des, 2)
			with open(tp, 'a') as f:
				f.write(f"{ev[0].timestamp()};{ev[1]}")
	if len(notified) > 0:
		with open(tp, 'a') as f:
			f.write('\n'.join([str(i[0].timestamp()) + ';' + 
				i[1] for i in notified]) + '\n')
