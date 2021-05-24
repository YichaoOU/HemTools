#!/usr/bin/env python

## This script is used to facilitate users to generate correct target bed file
import sys

import os

target = sys.argv[1] # user input bed file
ref = sys.argv[2] # reference RE bed file
output = sys.argv[3] # final output target bed file, to be used for hicpro_captureC



"""

double bait is here
chr11_paternal	33917808	33917929	v1
chr11_paternal	33918703	33918824	v2

grep 33917808 MboI_resfrag_hg19_ins7.bed 
chr11_paternal	33917808	33918820	HIC_chr11_paternal_82356	0	+

these two baits should be the RE for HIC_chr11_paternal_82356

the end site (33918824) is another RE start, we check the overlap, <70bp overlap between RE and bait, then the RE will be discarded, as it is not likely to be the actual bait

"""
# get all REs overlaped with target
# command = "module load bedtools;bedtools intersect -a %s -b %s -f 0.95 -u > Target.overlap.RE.bed"%(ref,target)
command = "module load bedtools;bedtools intersect -a %s -b %s -f 0.95 -u | sort -k1,1 -k2,2n - | bedtools merge -i - -d 1 -c 4 -o collapse -delim ';'| cut -f 1,2,3,4 > %s"%(ref,target,output)
print (command)
os.system(command)

# command = '''awk -F"\t" '$(NF) > 70 { print $1"\t"$2"\t"$3"\t"$4"\t"$5"\t"$6 }' Target.overlap.RE.bed > %s'''%(output)
# os.system(command)
















