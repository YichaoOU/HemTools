#!/bin/bash

label=$1
# awk -F"\t" '$4 ~ /_rev_/  && $6=="+" { print $1"\t"$2"\t"$2+1"\t1"}' $label.dedup.R2.bed |sort -k1,1 -k2,2n | bedtools groupby -g 1,2,3 -c 4 -o sum > $label.dedup.R2.rev.plus.bdg
# awk -F"\t" '$4 ~ /_fwd_/  && $6=="+" { print $1"\t"$2"\t"$2+1"\t1"}' $label.dedup.R2.bed |sort -k1,1 -k2,2n | bedtools groupby -g 1,2,3 -c 4 -o sum > $label.dedup.R2.fwd.plus.bdg
awk -F"\t" '$4 ~ /_fwd_/  && $6=="-" { print $1"\t"$3-1"\t"$3"\t1"}' $label.dedup.R2.bed |sort -k1,1 -k2,2n | bedtools groupby -g 1,2,3 -c 4 -o sum > $label.dedup.R2.fwd.minus.bdg
awk -F"\t" '$4 ~ /_rev_/  && $6=="-" { print $1"\t"$3-1"\t"$3"\t1"}' $label.dedup.R2.bed |sort -k1,1 -k2,2n | bedtools groupby -g 1,2,3 -c 4 -o sum > $label.dedup.R2.rev.minus.bdg





