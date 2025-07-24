#!/usr/bin/env bash

module load samtools/1.7
bam=$1

samtools view $1 | cut -f 1 | sort | uniq | wc -l
