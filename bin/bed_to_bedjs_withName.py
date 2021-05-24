#!/hpcf/apps/python/install/2.7.13/bin/python

import sys
import pandas as pd
import os

bed = sys.argv[1]
input_name=""
try:
	input_name = sys.argv[2]
except:
	pass
lines = open(bed).readlines()
outfile = "%s.bedjs"%(bed)
out = open(outfile,"wb")
for line in lines:
	line = line.strip().split("\t")
	if line == [""]:
		continue
	if not input_name == "":
		name = """{"strand":"+","name":"%s"}"""%(input_name)
	else:
		name = """{"strand":"+","name":"%s"}"""%(line[3])
	if len(line)==6:
		name = """{"strand":"%s","name":"%s"}"""%(line[5],line[3])
	print >>out,"\t".join([line[0],line[1],line[2],name])

out.close()
os.system("module load htslib;sort -k1,1 -k2,2n %s > %s.sorted;bgzip %s.sorted;tabix -p bed %s.sorted.gz"%(outfile,outfile,outfile,outfile))