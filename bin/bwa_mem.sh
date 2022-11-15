#!/usr/bin/env bash

module load bwa

module load samtools/1.7

fasta=$1
R1=$2
R2=$3
bwa index $fasta
bwa mem $fasta $R1 $R2 | samtools view -bS - > $R1.bam
samtools sort -o $R1.st.bam $R1.bam
mv $R1.st.bam $R1.bam
samtools index $R1.bam
