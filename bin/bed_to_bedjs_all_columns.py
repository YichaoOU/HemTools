#!/hpcf/apps/python/install/2.7.13/bin/python

"""

specifically used for encode footprint tracks

"""

import sys
import os

bed = sys.argv[1]
outfile = "%s.bedjs"%(bed)
out = open(outfile,"wb")
with open(bed) as f:
	for line in f:
		line = line.strip()
		if line == "":
			continue
		line = line.split("\t")

		# strand info here
		if line[5] in ["-","+"]:
			name = """{"strand":"%s","name":"{name_all}"}"""%(line[5])
		else:
			name = """{"name":"{name_all}"}"""
		columns_info = "<br>".join(line[3:])
		name = name.replace("{name_all}",columns_info)
		print >>out,"\t".join([line[0],line[1],line[2],name])

out.close()
os.system("module load htslib;sort -k1,1 -k2,2n %s > %s.sorted;bgzip %s.sorted;tabix -p bed %s.sorted.gz"%(outfile,outfile,outfile,outfile))