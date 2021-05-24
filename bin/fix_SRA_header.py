#!/usr/bin/env python

"""remove SRR ID in fastq

@SRR908270.1 FCD0VJ4ACXX:7:1101:1139:2150 length=90


"""

import sys
import os

def write_file(file_name,message):
	out = open(file_name,"wt")
	out.write(message)
	out.close()

input = sys.argv[1]
output = sys.argv[2]

out = open(output,"wt")
n = 4
with open(input, 'r') as fh:
	lines = []
	for line in fh:
		lines.append(line.rstrip())
		if len(lines) == n:
			# print (lines[0])
			lines[0] = "@"+lines[0].split()[1]
			out.write("\n".join(lines)+"\n")
			lines = []
out.close()
