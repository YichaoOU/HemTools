#!/hpcf/apps/python/install/2.7.13/bin/python

import sys
import os

bed = sys.argv[1]
lines = open(bed).readlines()
outfile = "%s.bedjs"%(bed)
out = open(outfile,"wb")
for line in lines:
	line = line.strip().split("\t")
	if line == [""]:
		continue
	name = """{"strand":"%s","name":"%s","color":"rgba(255,0,0,%s)"}"""%(line[5],line[3],line[4])
	print >>out,"\t".join([line[0],line[1],line[2],name])

out.close()
os.system("module load htslib;sort -k1,1 -k2,2n %s > %s.sorted;bgzip %s.sorted;tabix -p bed %s.sorted.gz"%(outfile,outfile,outfile,outfile))