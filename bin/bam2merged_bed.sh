#!/bin/bash

bam=$1

bedtools bamtobed -i $bam | sort -k1,1 -k2,2n | bedtools merge -i - > $bam.bed