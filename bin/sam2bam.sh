#!/usr/bin/env bash

module load samtools/1.7

file=$1
inbam=$(basename ${file})
samtools view -bS $file > $inbam.bam
samtools sort -@ 4 -o $inbam.st.bam $inbam.bam
samtools index $inbam.st.bam
rm $inbam.bam
