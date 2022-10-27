#!/usr/bin/env bash

mySam=$1
myList=$2
label=$3
module load samtools/1.15.1
samtools view -Sb -N $myList $mySam  > $label.bam
samtools index $label.bam
