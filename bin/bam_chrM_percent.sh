#!/bin/bash

#### Calculate percentage of reads mapped to mitochondrial genome (mtDNA) using SAMtools idxstats
#### Can be useful for ATAC-seq data. Requires an indexed BAM file:
## tested by Yichao

if [[ $# -eq 0 ]] ; then
  echo '[ERROR]: No input file given!'
  exit 1
fi

## Check if index is present. If not, create it:
if [[ ! -e ${1}.bai ]];
  then
  echo '[INFO]: File does not seem to be indexed. Indexing now:'
  samtools index $i
  fi

## Calculate %mtDNA:
mtReads=$(samtools idxstats $1 | grep 'chrM' | cut -f 3)
totalReads=$(samtools idxstats $1 | awk '{SUM += $3} END {print SUM}')

echo $1 ':' $(bc <<< "scale=2;100*$mtReads/$totalReads")'%'

## Usage: ./script.sh atacseq.bam

