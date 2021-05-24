bed=$1
awk -F "\t" '{print $1"\t"$3"\t"$4"\t"$5"\t"$6}' $bed.bed > $bed.vcf  