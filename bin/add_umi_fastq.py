#!/usr/bin/env python


import re
import gzip
import sys
import os
import argparse
import gzip
# -------------------- helper functions -----------------------

'''

@M04990:161:000000000-JYH4C:1:1101:8477:1395 1:N:0:TCCGTCTT+ACTGCATACAACATTAGT
GGCCAGGGGCCGGCGGCTGGCTAGGGATGAAGAATAA
+
CCCCCGGGGGGGGGGGGGGGGGGGGGGGGGGGFFGGG

'''

def fq(file):
    if re.search('.gz$', file):
        fastq = gzip.open(file, 'rb')
    else:
        fastq = open(file, 'r')
    with fastq as f:
        while True:
            l1 = f.readline().rstrip('\n')
            if not l1:
                break
            l2 = f.readline().rstrip('\n')
            l3 = f.readline().rstrip('\n')
            l4 = f.readline().rstrip('\n')
            yield [l1, l2, l3, l4]


def my_args():
	mainParser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	mainParser.add_argument('-o',  help="output fastq file name", required=True)	
	mainParser.add_argument('-f',  help="read fastq", required=True)	

	##------- add parameters above ---------------------
	args = mainParser.parse_args()	
	return args


def main():

	args = my_args()
	read1 = fq(args.f)
	o1 = open(args.o, 'wb')

	for r1 in read1:

		tmp = r1[0].strip().split()
		read_name = tmp[0]
		umi = tmp[-1].split("+")[-1]
		
		o1.write(read_name+"_"+umi[-10:]+"\n")
		o1.write(r1[1]+"\n")
		o1.write(r1[2]+"\n")
		o1.write(r1[3]+"\n")

if __name__ == "__main__":
	main()






