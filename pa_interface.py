#!/usr/bin/env python

"""
A simplified interface to pulseaudio.
This can be used with and without a graphical frontend.

Syntax:
Set volume to 50%
pa_interface.py 50%

Turn volume up 5%
pa_interface.py up

Turn volume down 5%
pa_interface.py down

Mute/Unmute volume.
pa_interface.py mute

Get a formatted string of all pulse audio sinks and their current info.
pa_interface.py get-sinks

Set default sink to sink index 2.
pa_interface.py set-sink 2
"""

import re
import subprocess
import sys
import argparse

def parse():
  parser = argparse.ArgumentParser(description='Adjust pulseaudio settings.')
	g = parser.add_mutually_exclusive_group(required=True)
	g.add_argument('volume', nargs='?')
	g.add_argument('--up', nargs='?', const='5%')
	g.add_argument('--down', nargs='?', const='5%')
	g.add_argument('--mute-sink', nargs='?', type=int, const=True)
	g.add_argument('--get-sinks', action='store_true')
	g.add_argument('--set-sink', type=int)
	g.add_argument('--mute-source', nargs='?', type=int, const=True)
	g.add_argument('--get-sources', action='store_true')
	g.add_argument('--set-source', type=int)
	
	return vars(parser.parse_args())

def run_cmd(args):
	print(args)
	if args['up']:
		set_volume(args['up'])
	if args['down']:
		set_volume(args['down'])
	if args['mute_sink'] is not None:
		mute_s(args['mute_sink'], is_sink=True)
	if args['get_sinks']:
		print_s(get_all_s(is_sink=True))
	if args['set_sink'] is not None:
		set_sink(args['set_sink'])
	if args['mute_source'] is not None:
		mute_s(args['mute_source'], is_sink=False)
	if args['get_sources']:
		print_s(get_all_s(is_sink=False))

def __exec(cmd):
	cmdlist = cmd.split(" ")
	process = subprocess.Popen(cmdlist, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	return process.stdout

def set_volume(amount, sink=None, pid=None):
	"""
	Sets the volume.
	amount can be an integer, percent, or decibal (db).
			amount may set a specific volume, or use +/- at the
			front to adjust the current volume.
	sink is an index of the sink to be affected (uses default)
	pid is not yet implemented (will adjust volume of specific programs)
	"""
	all = get_all_s(is_sink=True)
	if sink == None:
		sink = default_s_index(all)
	cmd = "pactl set-sink-volume -- %s %s" % (sink, amount)
	__exec(cmd)

def get_s_mute(s, is_sink):
	all = get_all_s(is_sink)
	if s is True:
		s = default_s_index(all)
	
	if all[s][3] == "muted: no":
		return False
	return True

def mute_s(s, is_sink): # Toggles mute.
	all = get_all_s(is_sink)
	
	if s is True:
		s = default_s_index(all)
	if all[s][3] == "muted: no":
		if is_sink:
			__exec("pactl set-sink-mute %s 1" % s)
		else:
			__exec("pactl set-source-mute %s 1" % s)
		return True
	else:
		if is_sink:
			__exec("pactl set-sink-mute %s 0" % s)
		else:
			__exec("pactl set-source-mute %s 0" % s)
		return False

def default_s_index(all):
	for i in xrange(len(all)):
		if all[i][0] == "default":
			return i

def get_all_s(is_sink):
	if is_sink:
		output = __exec("pacmd list-sinks")
	else:
		output = __exec("pacmd list-sources")
	all = [] # A list to hold info for all sinks.
	temp = ["    alt"] # Temporary list for building info on a sink.
	for line in output:
		line = line.strip()
		if line.startswith("* index: "):
			temp[0] = "default" # Notify that the current sink is the default.
		if line.startswith("volume: 0: "):
			temp += re.compile('\d+%').findall(line) # Adds left and right channels.
		if line.startswith("muted: "):
			temp.append(line)
		if line.startswith("device.description = "):
			temp.append(line[22:-1]) # Append an identifiable device name.
			all.append(temp) # Add the sink info to list and recycle the variable.
			temp = ["    alt"]
			
	return all

def print_s(s):
	# Prints as: [index] [state] [left channel] [right channel] [description]
	for i, j in enumerate(s):
		print i, " ".join(j)

def set_sink(id):
	__exec("pacmd set-default-sink %s" % id)
	get_sinks()


def main():
	args = parse()
	run_cmd(args)

if __name__ == '__main__':
	main()

