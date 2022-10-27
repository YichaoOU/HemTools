#!/usr/bin/env python

import sys
import os

sra_id = sys.argv[1]

import glob
iter=0
while True:
	iter +=1
	if iter > 1000:
		exit()
	print ("%s iteration %s"%(sra_id,iter))
	files = glob.glob("%s*fastq"%(sra_id))
	print (files)
	if len(files) == 0:
		os.system("fasterq-dump -e 1 %s"%(sra_id))
	else:
		exit()

