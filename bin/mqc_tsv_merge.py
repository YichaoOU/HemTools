#!/usr/bin/env python

import sys
import os
import uuid
import glob

def parse_file(file, template = True):
	out = []
	with open(file) as f:
		for line in f:
			line = line.strip()
			if len(line)<=1:
				continue
			if template:
					out.append(line)
			else:
				out = [line] # last line
	return out
files = glob.glob("*%s"%(sys.argv[1]))
if len(files) == 0:
	print ("No files found for %s"%(sys.argv[1]))
	exit()
out = parse_file(files[0], template = True)
for f in files[1:]:
	out+=parse_file(f, template = False)

outfile = sys.argv[2]
f = open(outfile,'wb')
f.write("\n".join(out).encode())
f.close()

