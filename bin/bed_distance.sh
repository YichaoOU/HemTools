
first=$1
second=$2
out=$3
sort -k1,1 -k2,2n $first > first.sorted.bed
# sort -k1,1 -k2,2n $second | cut -f 1-3 > second.sorted.bed
sort -k1,1 -k2,2n $second  > second.sorted.bed

bedtools closest -a first.sorted.bed -b second.sorted.bed -d -D a > $out
# bedtools closest -a first.sorted.bed -b second.sorted.bed -d > $out
