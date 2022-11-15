

a=$1
b=$2
c=$3
d=$4
# genomeFasta=/home/yli11/Data/Human/hg38/fasta/hg38.fa
# TCsrc=/home/yli11/Programs/TranscriptClean
# all hg38 format
# SJ=/home/yli11/Programs/TranscriptClean/gencode_v40_SJs.tsv
# SNP=/home/yli11/Data/Human/hg38/SNP150_iso_seq/00-common_all.vcf.gz
# DB=/home/yli11/Data/Human/hg38/annotations/gencode_v40/talon.db

fasta=/home/yli11/Data/Human/hg38/fasta/hg38.fa
gtf=/home/yli11/Data/Human/hg38/annotations/gencode_v40/gencode.v40.annotation.annotation_utr.gtf
chromSize=/home/yli11/Data/Human/hg38/annotations/hg38.chrom.sizes

#ployA
# lapa --alignment $a,$b --fasta $fasta --annotation $gtf --chrom_sizes $chromSize --output_dir lapa_polyA_out
#tss
# lapa_tss --alignment $a,$b --fasta $fasta --annotation $gtf --chrom_sizes $chromSize --output_dir lapa_TSS_out
# link
# lapa_link_tss_to_tes --alignment $a,$b --lapa_dir lapa_polyA_out --lapa_tss_dir  lapa_TSS_out --output lapa_tss_to_tes_out
#talon
lapa_correct_talon --links lapa_tss_to_tes_out --read_annot $c --gtf_input $gtf --gtf_output lapa.gtf --abundance_input $d --abundance_output lapa.abundance.tsv




