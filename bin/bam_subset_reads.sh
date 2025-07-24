#!/bin/bash




module load picard/2.9.4

inBam=$1
readList=$2
outBam=$3

java -jar /hpcf/apps/picard/install/2.9.4/picard.jar FilterSamReads I=$inBam O=$outBam READ_LIST_FILE=$readList FILTER=includeReadList SORT_ORDER=coordinate;samtools index $outBam

