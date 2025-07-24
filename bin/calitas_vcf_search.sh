#!/bin/bash


# make sure you have some vcf like below
##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
# chrY	25294950	.	C	CTTGTCAAGGCTATTGGTCAAGG	.	.	.

gRNA=$1
label=$2
vcf=$3

genome=/home/yli11/Data/Human/hg38/fasta/hg38.main.fa
rm input.vcf.gz*
bgzip -c $vcf > input.vcf.gz
tabix -p vcf input.vcf.gz
# calitas SearchReference -i CTTGTCAAGGCTATTGGTCAngg -I g34 -r /home/yli11/Data/Human/hg38/fasta/hg38.main.fa -o g34.hits.5.1.3.tsv --max-guide-diffs 5 --max-pam-mismatches 1 --max-gaps-between-guide-and-pam 3 -v test3.vcf.gz -c chrY
# calitas SearchReference -i CTTGTCAAGGCTATTGGTCAngg -I g34 -r /home/yli11/Data/Human/hg38/fasta/hg38.main.fa -o g34.hits.5.1.3.tsv --max-guide-diffs 5 --max-pam-mismatches 1 --max-gaps-between-guide-and-pam 3 -v test3.vcf.gz -c chrY
calitas SearchReference -i $gRNA -I $label -r $genome -o $label.calitas.5.2.2.tsv --max-guide-diffs 5 --max-total-diffs 5 --max-pam-mismatches 2 --max-gaps-between-guide-and-pam 2 -v input.vcf.gz -c chr1


