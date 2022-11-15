#!/usr/bin/env python


import sys
import os
import uuid
import pandas as pd
## used to find genes that are in the same capture as input peaks
uid = str(uuid.uuid4()).split("-")[-1]

peaks = sys.argv[1]
cap = sys.argv[2] # /home/yli11/Data/Mouse/mm9/captureC/target.bed

# command1 = "module load bedtools;bedtools intersect -a %s -b %s -u > %s.capC.gene.bed"%(cap,peaks,peaks)
command1 = "module load bedtools;bedtools intersect -b %s -a %s -wa -wb > %s.capC.gene.bed"%(cap,peaks,peaks)
os.system(command1)

