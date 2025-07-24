#!/usr/bin/env python

# https://github.com/lh3/minimap2/issues/25
# ┌────┬──────┬───────────────────────────────────────────────────────┐
# │Tag │ Type │                      Description                      │
# ├────┼──────┼───────────────────────────────────────────────────────┤
# │ tp │  A   │ Type of aln: P/primary, S/secondary and I,i/inversion │
# │ cm │  i   │ Number of minimizers on the chain                     │
# │ s1 │  i   │ Chaining score                                        │
# │ s2 │  i   │ Chaining score of the best secondary chain            │
# │ NM │  i   │ Total number of mismatches and gaps in the alignment  │
# │ MD │  Z   │ To generate the ref sequence in the alignment         │
# │ AS │  i   │ DP alignment score                                    │
# │ ms │  i   │ DP score of the max scoring segment in the alignment  │
# │ nn │  i   │ Number of ambiguous bases in the alignment            │
# │ ts │  A   │ Transcript strand (splice mode only)                  │
# │ cg │  Z   │ CIGAR string (only in PAF)                            │
# │ cs │  Z   │ Difference string                                     │
# └────┴──────┴───────────────────────────────────────────────────────┘

import pysam
import pandas as pd
# from joblib import Parallel, delayed
import sys


# key differences to other cas9 library
# this is not random mutation library, so we dont need to keep the sequence, so it saved the memory
# the last 15 soft-clip bases should be the barcode, however, the actual observed length can vary

bamFile=sys.argv[1]
label=sys.argv[2]


def read_to_list(f):
	if ".bam" in f:
		f = pysam.AlignmentFile(f)
	else:
		f = pysam.AlignmentFile(f,"r")
	myList = []
	# count = 0
	for read in f.fetch():
		if read.is_supplementary:
			continue
		if not read.is_mapped:
			continue
		# count += 1
		# if count > 100:
			# return myList
		readDict={}

		readDict['read_name'] = read.query_name
		readDict['reference_name'] =  read.reference_name
		readDict['AS'] =  read.get_tag("AS")
		readDict['NM'] =  read.get_tag("NM")
		readDict['is_forward'] = read.is_forward # should all be forward mapping
		myList.append(readDict)
	return myList


myList = read_to_list(bamFile)
df = pd.DataFrame(myList)
df.to_csv(f"{label}.read_stat.csv",index=False)