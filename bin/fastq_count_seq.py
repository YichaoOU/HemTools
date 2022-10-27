#!/usr/bin/env python

import sys
import subprocess

def wccount(filename,myString):
	# out = subprocess.Popen(['zcat', filename, "|","grep",myString,"|","wc","-l"],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0]
	out = subprocess.Popen("zcat %s | grep %s | wc -l"%(filename,myString),stdout=subprocess.PIPE,stderr=subprocess.STDOUT,shell=True).communicate()[0]
	# print (out)
	return int(out.partition(b' ')[0])

filename=sys.argv[1]
myString=sys.argv[2]
# print (filename,myString)
try:
	lines = open(myString).readlines()
	for l in lines:
		a=l.strip().split()
		print ("%s\t%s\t%s"%(filename,a[0],wccount(filename,a[-1])))
except:
	print ("%s\t%s"%(filename,wccount(filename,myString)))