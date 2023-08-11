#!/usr/bin/env python

import pandas as pd
import sys
import os

# Merged MethylDackel result
MethylDackel_input = sys.argv[1]

MethylKit_output = sys.argv[2]

df = pd.read_csv(MethylDackel_input,sep="\t",header=None)

# chr1    10468   10470   57      11      8
# chr1    10470   10472   60      14      9
# chr1    10483   10485   64      11      6
# chr1    10488   10490   84      16      3
# chr1    10492   10494   68      13      6

# The chromosome/contig/scaffold name
# The start coordinate
# The end coordinate
# The methylation percentage rounded to an integer
# The number of alignments/pairs reporting methylated bases
# The number of alignments/pairs reporting unmethylated bases

df['chr'] = df[0]
df['base'] = df[1]+1
df['chrBase'] = df['chr']+"."+df['base'].astype(str)
df['strand'] = "F"
df['coverage'] = df[4]+df[5]
df['freqC'] = df[3]
df['freqT'] = 100-df[3] # T is unmethylated bases

# chrBase	chr	base	strand	coverage	freqC	freqT
# chr21.9764539	chr21	9764539	R	12	25.00	75.00
# chr21.9764513	chr21	9764513	R	12	0.00	100.00
# chr21.9820622	chr21	9820622	F	13	0.00	100.00

df = df[["chrBase","chr","base","strand","coverage","freqC","freqT"]]
df.to_csv(MethylKit_output,sep="\t",index=False)
