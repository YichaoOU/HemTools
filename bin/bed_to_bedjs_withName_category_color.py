#!/home/yli11/.conda/envs/py2/bin/python

import sys
import os
import pandas as pd
from unique_color import unique_color as uc
import random
my_colors = uc.unique_color_rgb()
random.shuffle(my_colors)
bed = sys.argv[1]

df = pd.read_csv(bed,sep="\t",header=None)
df[1] = df[1].astype(int)
df[2] = df[2].astype(int)
if df.shape[1]<5:
	df[4]="."
	df[5]="+"
# lines = open(bed).readlines()
outfile = "%s.bedjs"%(bed)
out = open(outfile,"wt")

	

	
count=0
for s,d in df.groupby(3):
	color = my_colors[count]
	print (color)
	count +=1
	if count >= len(my_colors):
		count = 0
	for r in d.values:
		# print (r)
		# print (r[4])
		# name = """{"strand":"%s","name":"%s","color":"rgba(%s,%s,%s,%s)","exon":[["%s","%s"]]}"""%(r[5],s,color[0],color[1],color[2],150,r[1],r[2])
		name = """{"strand":"%s","name":"%s","color":"rgba(%s,%s,%s,%s)"}"""%(r[5],s,color[0],color[1],color[2],0.7)
		out.write("\t".join([r[0],str(r[1]),str(r[2]),name])+"\n")
		# print ("\t".join([r[0],str(r[1]),str(r[2]),name]))

out.close()
os.system("module load htslib;sort -k1,1 -k2,2n %s > %s.sorted;bgzip %s.sorted;tabix -p bed %s.sorted.gz"%(outfile,outfile,outfile,outfile))