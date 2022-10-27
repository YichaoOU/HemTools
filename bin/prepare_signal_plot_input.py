#!/usr/bin/env python

import sys


def parse_config(x):
	myDict = {}
	with open(x) as f:
		for line in f:
			line = line.strip()
			if len(line) < 1:
				continue
			if line[0] == "#":
				continue
			line = line.split()
			## make sure it is case-insensitive
			if len(line)==2:
				myDict[line[0].lower()] = line[1]
			if len(line)==1:
				label = ".".join(line[0].split(".")[:-1])
				myDict[label.lower()] = line[0]
			# myDict[line[0]] = line[1]
	return myDict
def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()

bed_list = parse_config(sys.argv[1])
bw_list = parse_config(sys.argv[2])


out = []
for i in bed_list:
	for j in bw_list:
		out.append("\t".join([bed_list[i],i,bw_list[j],j,i+"_"+j]))
out = "\n".join(out)
write_file("signal_plot_input.list",out)