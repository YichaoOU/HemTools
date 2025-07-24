#!/usr/bin/env bash

bam=$1
/home/yli11/.conda/envs/jupyterlab_2024/bin/sinto fragments -b $bam -f fragments.tsv --chunksize 200000 -p 30 -t MC -m 0 
liftover.py --bed fragments.tsv -g hg38 -o hg38.fragments
sort -k1,1V -k2,2n -k3,3n hg38.fragments.bed | awk 'BEGIN{OFS="\t"} {$4="NA"; print}' > hg38.fragments.tsv
gzip hg38.fragments.tsv
