#!/hpcf/apps/python/install/2.7.13/bin/python

import sys
import re
import glob
files = glob.glob("*.fastq.gz")

mysamples = {}
for k in files:
	lables = k.split("_")
	clean = []
	for l in lables:
		if bool(re.match("SRR[0-9]*", l)):
			continue
		
		clean.append(l.replace(".fastq.gz",""))
	label = "_".join(clean)
	if label in mysamples:
		mysamples[label].append(k)
	else:
		mysamples[label] = [k]


for k in mysamples:
	print ("cat %s > %s.fastq.gz"%(" ".join(mysamples[k]),k))
