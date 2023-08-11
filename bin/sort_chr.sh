#!/bin/sh

## Usage: ./sort_chr.sh input.txt

input=$1

sed -i 's/chrX/chr23/g; s/chrY/chr24/g' $input
sort -k 1.4,1n -k 2,2n -k 3,3n $input > $input.sorted
sed -i 's/chr23/chrX/g; s/chr24/chrY/g' $input.sorted
mv $input{.sorted,}

### Alternative: only sorts chrom location, doesn't sort chromosome
# sortBed -i bedfile.bed > sorted.bed

