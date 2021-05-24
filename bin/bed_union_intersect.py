#!/usr/bin/env python


import sys
import os

bed1=sys.argv[1]
bed2=sys.argv[2]


union = "module load bedtools; cat %s %s |cut -f 1,2,3| sort -k1,1 -k2,2n - | bedtools merge -i - > union.bed"%(bed1,bed2)
os.system(union)

intersect = "module load bedtools; bedtools intersect -a union.bed -b %s -u | bedtools intersect -a - -b %s -u > intersect.bed"%(bed1,bed2)
os.system(intersect)

