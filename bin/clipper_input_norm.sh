#!/usr/bin/env bash
module load samtools/1.7
module load R/3.5.1
module load perl
t=$1
c=$2
src="/home/yli11/Programs/merge_peaks/bin/perl"

samtools view -c ${t}_results/${t}.dedup.bam > $t.readnum.txt
samtools view -c ${c}_results/${c}.dedup.bam > $c.readnum.txt
perl $src/overlap_peakfi_with_bam.pl ${t}_results/${t}.dedup.bam ${c}_results/${c}.dedup.bam ${t}_results/${t}.dedup.clipper.default.bed $t.readnum.txt $c.readnum.txt $t.vs.$c.bed

