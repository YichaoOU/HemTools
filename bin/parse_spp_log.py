#!/usr/bin/env python

import sys
# import pandas as pd

input = sys.argv[1]
output = input+".tsv"

"""
Normalized Strand cross-correlation coefficient (NSC) 1.606347 
Relative Strand cross-correlation Coefficient (RSC) 2.32619 
Phantom Peak Quality Tag 2
"""
out = open(output,'w')
header="""
# plot_type: 'table'
# section_name: 'phantom peak quality'
sample	NSC	RSC	QTag
"""
out.write(header)

def parse_line(x):
	x = x.split()
	value = x[-1]
	return "%s\t%s"%(" ".join(x[:-1]),value)

outlines = [input.replace(".spp.log","")]
with open(input) as f:
	for line in f:
		if "(NSC)" in line:
			outlines.append(line.split()[-1])
		if "(RSC)" in line:
			outlines.append(line.split()[-1])
		if "Phantom Peak Quality Tag" in line:
			outlines.append(line.split()[-1])



out.write("\t".join(outlines))
out.close()
